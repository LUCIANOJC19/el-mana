from datetime import datetime
from flask import Flask, redirect, render_template, request, session, url_for
import sqlite3
import urllib.parse
import os
import csv
import io
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "el_mana_clave_secreta_muy_segura"

# Archivo donde SQLite guardará toda la base de datos
DB_NAME = "negocio_mana.db"

def obtener_conexion():
    conexion = sqlite3.connect(DB_NAME)
    # Esto permite acceder a las columnas por nombre (tipo diccionario) si hace falta
    conexion.row_factory = sqlite3.Row
    return conexion


def normalizar(texto):
    if not texto:
        return ""
    texto = texto.strip().lower()
    texto = (
        texto.replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
    )
    return texto


def obtener_etiqueta_medio(nombre_prod, unidad_db):
    """Determina si corresponde 'Medio' o 'Media' basándose en la unidad o el nombre del producto."""
    texto_evaluar = f"{unidad_db} {nombre_prod}".lower()
    if "bolsa" in texto_evaluar or "lata" in texto_evaluar or unidad_db.strip().lower().endswith('a'):
        return "Media"
    return "Medio"


@app.route("/")
def home():
    try:
        departamento_activo = request.args.get("dep", "Mercaderia")
        dep_activo_norm = normalizar(departamento_activo)
        texto_busqueda = normalizar(request.args.get("busqueda", ""))

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT monto_minimo, radio_km FROM configuracion LIMIT 1")
        config = cursor.fetchone()

        if config:
            monto_minimo, radio_km = config["monto_minimo"], config["radio_km"]
        else:
            monto_minimo = 60000
            radio_km = 10

        cursor.execute(
            "SELECT id, nombre, precio, stock, sabores, categoria, imagen, departamento, descripcion, permite_medio_pack, nombre_unidad FROM mercaderia"
        )
        productos = cursor.fetchall()

        cursor.close()
        conexion.close()

        productos_procesados = list()
        for prod in productos:
            (
                p_id,
                p_nombre,
                p_precio,
                p_stock,
                p_sabores,
                p_categoria,
                p_imagen,
                p_departamento,
                p_descripcion,
                p_permite_medio,
                p_nombre_unidad,
            ) = prod
            sabores_seguros = p_sabores if p_sabores else ""
            categoria_segura = p_categoria if p_categoria else "Otros"
            imagen_segura = p_imagen if p_imagen else "logo.npg.jpeg"
            dep_seguro = p_departamento if p_departamento else "Mercaderia"
            desc_segura = p_descripcion if p_descripcion else ""
            permite_medio_seguro = p_permite_medio if p_permite_medio is not None else 0
            unidad_segura = p_nombre_unidad if p_nombre_unidad else "Pack"

            productos_procesados.append(
                (
                    p_id,
                    p_nombre,
                    p_precio,
                    p_stock,
                    sabores_seguros,
                    categoria_segura,
                    imagen_segura,
                    dep_seguro,
                    desc_segura,
                    permite_medio_seguro,
                    unidad_segura,
                )
            )

        carrito = session.get("carrito", {})
        items_carrito = list()
        subtotal = 0

        for prod in productos_procesados:
            (
                id_prod,
                nombre_prod,
                precio_prod,
                stock_prod,
                sabores_prod,
                cat_prod,
                img_prod,
                dep_prod,
                desc_prod,
                permite_medio_prod,
                unidad_prod,
            ) = prod

            for clave, cantidad in list(carrito.items()):
                partes = clave.split("_")
                partes_iter = iter(partes)
                id_carrito = int(next(partes_iter))

                if id_carrito == id_prod:
                    sabor = next(partes_iter) if len(partes) > 1 else ""
                    
                    es_medio = "medio" in partes
                    precio_real = (precio_prod / 2) if es_medio else precio_prod
                    
                    if es_medio:
                        prefijo_medio = obtener_etiqueta_medio(nombre_prod, unidad_prod)
                        etiqueta_pack = f" ({prefijo_medio} {unidad_prod})"
                    else:
                        etiqueta_pack = ""

                    nombre_completo = f"{nombre_prod}{etiqueta_pack}"
                    if sabor:
                        nombre_completo = f"{nombre_prod} (Sabor: {sabor}){etiqueta_pack}"

                    total_item = precio_real * cantidad
                    subtotal += total_item
                    items_carrito.append(
                        {
                            "clave": clave,
                            "nombre": nombre_completo,
                            "precio": precio_real,
                            "cantidad": cantidad,
                            "total": total_item,
                        }
                    )

        productos_filtrados = list()
        for prod in productos_procesados:
            p_id, p_nombre, p_precio, p_stock, p_sabores, p_cat, p_img, p_dep, p_desc, p_pm, p_nu = prod
            if normalizar(p_dep) == dep_activo_norm:
                if not texto_busqueda or texto_busqueda in normalizar(p_nombre):
                    productos_filtrados.append(prod)

        productos_por_categoria = {}
        for prod in productos_filtrados:
            p_id, p_nombre, p_precio, p_stock, p_sabores, p_cat, p_img, p_dep, p_desc, p_pm, p_nu = prod
            if p_cat not in productos_por_categoria:
                productos_por_categoria[p_cat] = list()
            productos_por_categoria[p_cat].append(prod)

        envio_gratis = subtotal >= monto_minimo
        restante_envio = (
            monto_minimo - subtotal if subtotal < monto_minimo else 0
        )

        whatsapp_url = ""
        if items_carrito:
            mensaje = "🏪 *¡Hola El Mana! Quisiera hacer el siguiente pedido:*\n\n"
            for item in items_carrito:
                mensaje += (
                    f"• {item['nombre']} x{item['cantidad']} - (${item['total']})\n"
                )

            mensaje += f"\n💵 *Monto Total de la compra: ${subtotal}*"
            if envio_gratis:
                mensaje += f"\n🚚 *¡Envío Gratis solicitado!* (Supera los ${monto_minimo} dentro de los {radio_km} km)"
            else:
                mensaje += "\n🛵 *Envío a coordinar con el repartidor.*"

            mensaje += "\n\n✍️ *Por favor, completa tus datos antes de enviar este mensaje:*"
            mensaje += "\n👤 *Nombre y Apellido:* "
            mensaje += "\n📍 *Dirección de entrega:* "
            mensaje += "\n🏡 *Barrio / Localidad:* "
            mensaje += "\n📞 *Teléfono de contacto:* "
            mensaje += "\n💬 *Notas o indicaciones adicionales:* "

            mensaje_codificado = urllib.parse.quote(mensaje)
            mi_telefono = "5493777229583"
            whatsapp_url = (
                f"https://wa.me/{mi_telefono}?text={mensaje_codificado}"
            )

        return render_template(
            "index.html",
            productos_por_categoria=productos_por_categoria,
            items_carrito=items_carrito,
            subtotal=subtotal,
            envio_gratis=envio_gratis,
            restante_envio=restante_envio,
            whatsapp_url=whatsapp_url,
            monto_minimo=monto_minimo,
            radio_km=radio_km,
            departamento_activo=departamento_activo,
        )

    except Exception as e:
        return f"<h1>Error al conectar con la base de datos</h1><p>{e}</p>"


@app.route("/confirmar-pedido")
def confirmar_pedido():
    carrito = session.get("carrito", {})
    if not carrito:
        return redirect(url_for("home"))

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT id, nombre, precio, nombre_unidad FROM mercaderia")
        productos_db = cursor.fetchall()

        subtotal = 0
        detalle_texto = ""
        items_a_guardar = []

        for prod in productos_db:
            id_prod, nombre_prod, precio_prod, nombre_unidad_db = prod
            unidad_nombre = nombre_unidad_db if nombre_unidad_db else "Pack"
            
            for clave, cantidad in list(carrito.items()):
                partes = clave.split("_")
                if int(partes[0]) == id_prod:
                    sabor = partes[1] if len(partes) > 1 and not partes[1] == "medio" else ""
                    es_medio = "medio" in partes
                    
                    precio_real = (precio_prod / 2) if es_medio else precio_prod
                    
                    if es_medio:
                        prefijo_medio = obtener_etiqueta_medio(nombre_prod, unidad_nombre)
                        etiqueta_pack = f" ({prefijo_medio} {unidad_nombre})"
                    else:
                        etiqueta_pack = ""

                    nombre_completo = f"{nombre_prod}{etiqueta_pack}"
                    if sabor and sabor != "medio":
                        nombre_completo = f"{nombre_prod} (Sabor: {sabor}){etiqueta_pack}"

                    total_item = precio_real * cantidad
                    subtotal += total_item
                    detalle_texto += (
                        f"• {nombre_completo} x{cantidad} - (${total_item})\n"
                    )
                    items_a_guardar.append({
                        "nombre": nombre_completo,
                        "cantidad": cantidad,
                        "precio_unitario": precio_real
                    })

        cursor.execute("SELECT monto_minimo, radio_km FROM configuracion LIMIT 1")
        config = cursor.fetchone()
        monto_minimo = config["monto_minimo"] if config else 60000
        radio_km = config["radio_km"] if config else 10
        envio_gratis = subtotal >= monto_minimo

        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute(
            "INSERT INTO pedidos (fecha, productos, total, cliente_nombre, cliente_direccion) VALUES (?, ?, ?, ?, ?)",
            (fecha_actual, detalle_texto, subtotal, "Cliente Web", "A coordinar"),
        )
        pedido_id = cursor.lastrowid

        for item in items_a_guardar:
            cursor.execute(
                "INSERT INTO detalle_pedido (pedido_id, producto_nombre, cantidad, precio_unitario) VALUES (?, ?, ?, ?)",
                (pedido_id, item["nombre"], item["cantidad"], item["precio_unitario"])
            )

        conexion.commit()
        cursor.close()
        conexion.close()

        mensaje = "🏪 *¡Hola El Mana! Quisiera hacer el siguiente pedido:*\n\n"
        mensaje += detalle_texto
        mensaje += f"\n💵 *Monto Total de la compra: ${subtotal}*"
        if envio_gratis:
            mensaje += f"\n🚚 *¡Envío Gratis solicitado!* (Supera los ${monto_minimo} dentro de los {radio_km} km)"
        else:
            mensaje += "\n🛵 *Envío a coordinar con el repartidor.*"

        mensaje += "\n\n✍️ *Por favor, completa tus datos antes de enviar este mensaje:*"
        mensaje += "\n👤 *Nombre y Apellido:* "
        mensaje += "\n📍 *Dirección de entrega:* "
        mensaje += "\n🏡 *Barrio / Localidad:* "
        mensaje += "\n📞 *Teléfono de contacto:* "
        mensaje += "\n💬 *Notas o indicaciones adicionales:* "

        mensaje_codificado = urllib.parse.quote(mensaje)
        mi_telefono = "5493777229583"
        whatsapp_url = f"https://wa.me/{mi_telefono}?text={mensaje_codificado}"

        session["carrito"] = {}

        return redirect(whatsapp_url)

    except Exception as e:
        return f"<h1>Error al procesar el pedido</h1><p>{e}</p>"


@app.route("/agregar-producto", methods=("GET", "POST"))
def agregar_producto():
    if not session.get("admin"):
        return redirect(url_for("login"))

    if request.method == "POST":
        nombre = request.form.get("nombre")
        try:
            precio = float(request.form.get("precio", 0))
        except ValueError:
            precio = 0.0

        try:
            stock = int(request.form.get("stock", 0))
        except ValueError:
            stock = 0

        sabores = request.form.get("sabores", "")
        categoria = request.form.get("categoria", "Otros")
        departamento = request.form.get("departamento", "Mercaderia")
        descripcion = request.form.get("descripcion", "")
        
        try:
            permite_medio_pack = int(request.form.get("permite_medio_pack", 0))
        except ValueError:
            permite_medio_pack = 0

        nombre_unidad = request.form.get("nombre_unidad", "Pack").strip()
        if not nombre_unidad:
            nombre_unidad = "Pack"

        imagen_final = "logo.npg.jpeg"  
        
        archivo_imagen = request.files.get("imagen")
        if archivo_imagen and archivo_imagen.filename != "":
            nombre_archivo = secure_filename(archivo_imagen.filename)
            ruta_carpeta_static = os.path.join(app.root_path, "static")
            os.makedirs(ruta_carpeta_static, exist_ok=True)
            
            ruta_completa = os.path.join(ruta_carpeta_static, nombre_archivo)
            archivo_imagen.save(ruta_completa)
            
            imagen_final = nombre_archivo

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO mercaderia (nombre, precio, stock, sabores, categoria, imagen, departamento, descripcion, permite_medio_pack, nombre_unidad) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    nombre,
                    precio,
                    stock,
                    sabores,
                    categoria,
                    imagen_final,
                    departamento,
                    descripcion,
                    permite_medio_pack,
                    nombre_unidad,
                ),
            )
            conexion.commit()
            cursor.close()
            conexion.close()
            return redirect(url_for("listar_productos_admin"))
        except Exception as e:
            return f"<h1>Error al guardar el nuevo producto</h1><p>{e}</p>"

    return render_template("agregar_producto.html")


@app.route("/admin/productos")
def listar_productos_admin():
    if not session.get("admin"):
        return redirect(url_for("login"))

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id, nombre, precio, stock, sabores, categoria, imagen, departamento, descripcion, permite_medio_pack, nombre_unidad FROM mercaderia"
        )
        productos = cursor.fetchall()
        cursor.close()
        conexion.close()

        texto_busqueda = normalizar(request.args.get("busqueda", ""))

        def clasificar_departamento(depto_bd, categoria):
            if depto_bd and depto_bd.strip():
                return depto_bd.strip()
            cat_lower = categoria.strip().lower() if categoria else ""
            forraperia_claves = ["perro", "gato", "mascota", "alimento", "fardo", "maiz", "trigo", "forraqueria", "forrajería"]
            for clave in forraperia_claves:
                if clave in cat_lower:
                    return "Forrajeria"
            return "Mercaderia"

        productos_agrupados = {
            "Mercaderia": {},
            "Forrajeria": {}
        }

        for prod in productos:
            p_id, p_nombre, p_precio, p_stock, p_sabores, p_categoria, p_imagen, p_departamento, p_descripcion, p_pm, p_nu = prod
            cat_nombre = p_categoria if p_categoria else "Otros"
            depto = clasificar_departamento(p_departamento, cat_nombre)

            if texto_busqueda:
                if texto_busqueda not in normalizar(p_nombre) and texto_busqueda not in normalizar(cat_nombre):
                    continue

            if depto not in productos_agrupados:
                productos_agrupados[depto] = {}

            if cat_nombre not in productos_agrupados[depto]:
                productos_agrupados[depto][cat_nombre] = []
            
            productos_agrupados[depto][cat_nombre].append(prod)

        return render_template("listar_productos.html", productos_agrupados=productos_agrupados)
    except Exception as e:
        return f"<h1>Error al cargar los productos</h1><p>{e}</p>"


@app.route("/admin/editar/<int:id_prod>", methods=("GET", "POST"))
def editar_producto(id_prod):
    if not session.get("admin"):
        return redirect(url_for("login"))

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        if request.method == "POST":
            nombre = request.form.get("nombre")
            precio = float(request.form.get("precio", 0))
            stock = int(request.form.get("stock", 0))
            sabores = request.form.get("sabores", "")
            categoria = request.form.get("categoria", "Otros")
            departamento = request.form.get("departamento", "Mercaderia")
            descripcion = request.form.get("descripcion", "")
            
            try:
                permite_medio_pack = int(request.form.get("permite_medio_pack", 0))
            except ValueError:
                permite_medio_pack = 0

            nombre_unidad = request.form.get("nombre_unidad", "Pack").strip()
            if not nombre_unidad:
                nombre_unidad = "Pack"

            cursor.execute("SELECT imagen FROM mercaderia WHERE id = ?", (id_prod,))
            prod_actual = cursor.fetchone()
            imagen_final = prod_actual[0] if prod_actual else "logo.npg.jpeg"

            archivo_imagen = request.files.get("imagen")
            if archivo_imagen and archivo_imagen.filename != "":
                nombre_archivo = secure_filename(archivo_imagen.filename)
                ruta_carpeta_static = os.path.join(app.root_path, "static")
                os.makedirs(ruta_carpeta_static, exist_ok=True)
                ruta_completa = os.path.join(ruta_carpeta_static, nombre_archivo)
                archivo_imagen.save(ruta_completa)
                imagen_final = nombre_archivo

            cursor.execute(
                """UPDATE mercaderia 
                   SET nombre = ?, precio = ?, stock = ?, sabores = ?, categoria = ?, imagen = ?, departamento = ?, descripcion = ?, permite_medio_pack = ?, nombre_unidad = ? 
                   WHERE id = ?""",
                (
                    nombre,
                    precio,
                    stock,
                    sabores,
                    categoria,
                    imagen_final,
                    departamento,
                    descripcion,
                    permite_medio_pack,
                    nombre_unidad,
                    id_prod,
                ),
            )
            conexion.commit()
            cursor.close()
            conexion.close()
            return redirect(url_for("listar_productos_admin"))

        cursor.execute(
            "SELECT id, nombre, precio, stock, sabores, categoria, imagen, departamento, descripcion, permite_medio_pack, nombre_unidad FROM mercaderia WHERE id = ?",
            (id_prod,),
        )
        producto = cursor.fetchone()
        cursor.close()
        conexion.close()

        if not producto:
            return "<h1>Producto no encontrado</h1>"

        return render_template("editar_producto.html", producto=producto)

    except Exception as e:
        return f"<h1>Error al editar el producto</h1><p>{e}</p>"


@app.route("/admin/eliminar/<int:id_prod>", methods=("POST", "GET"))
def eliminar_producto(id_prod):
    if not session.get("admin"):
        return redirect(url_for("login"))

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM mercaderia WHERE id = ?", (id_prod,))
        conexion.commit()
        cursor.close()
        conexion.close()
        return redirect(url_for("listar_productos_admin"))
    except Exception as e:
        return f"<h1>Error al eliminar el producto</h1><p>{e}</p>"


@app.route("/agregar/<int:id_prod>")
def agregar(id_prod):
    carrito = session.get("carrito", {})
    sabor_elegido = request.args.get("sabor", "")
    tipo_pack = request.args.get("tipo_pack", "entero")
    cantidad_elegida = request.args.get("cantidad", 1, type=int)
    dep_actual = request.args.get("dep", "Mercaderia")

    sufijo = "_medio" if tipo_pack == "medio" else ""
    base_clave = f"{id_prod}_{sabor_elegido}" if sabor_elegido else str(id_prod)
    clave_producto = f"{base_clave}{sufijo}"

    if clave_producto in carrito:
        carrito[clave_producto] += cantidad_elegida
    else:
        carrito[clave_producto] = cantidad_elegida

    session["carrito"] = carrito
    return redirect(url_for("home", dep=dep_actual, _anchor=f"prod_{id_prod}"))


@app.route("/vaciar")
def vaciar():
    dep_actual = request.args.get("dep", "Mercaderia")
    session["carrito"] = {}
    return redirect(url_for("home", dep=dep_actual))


@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        contrasena = request.form.get("contrasena")

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT usuario, contrasena FROM usuarios WHERE usuario = ?",
                (usuario,),
            )
            user = cursor.fetchone()
            cursor.close()
            conexion.close()

            if user and user["contrasena"] == contrasena:
                session["admin"] = usuario
                return redirect(url_for("admin"))
            else:
                return render_template(
                    "login.html", error="Usuario o contraseña incorrectos"
                )
        except Exception as e:
            return f"<h1>Error en el inicio de sesión</h1><p>{e}</p>"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("home"))


@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect(url_for("login"))

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT monto_minimo, radio_km FROM configuracion LIMIT 1")
        config = cursor.fetchone()

        if config:
            monto_minimo, radio_km = config["monto_minimo"], config["radio_km"]
        else:
            monto_minimo = 60000
            radio_km = 10

        cursor.execute(
            "SELECT id, fecha, productos, total, cliente_nombre, cliente_direccion FROM pedidos ORDER BY fecha DESC"
        )
        pedidos = cursor.fetchall()

        cursor.execute("SELECT SUM(total) FROM pedidos")
        ganancias_tupla = cursor.fetchone()

        if ganancias_tupla and ganancias_tupla[0]:
            total_ganancias = ganancias_tupla[0]
        else:
            total_ganancias = 0

        total_pedidos = len(pedidos)

        cursor.execute("SELECT COUNT(*) FROM mercaderia WHERE stock <= 5")
        stock_bajo_tupla = cursor.fetchone()
        stock_bajo = stock_bajo_tupla[0] if stock_bajo_tupla else 0

        cursor.close()
        conexion.close()

        return render_template(
            "admin.html",
            pedidos=pedidos,
            total_ganancias=total_ganancias,
            total_pedidos=total_pedidos,
            stock_bajo=stock_bajo,
            monto_minimo=monto_minimo,
            radio_km=radio_km,
        )
    except Exception as e:
        return f"<h1>Error al cargar el panel administrativo</h1><p>{e}</p>"


@app.route("/admin/guardar-config", methods=("GET", "POST"))
def guardar_config():
    if not session.get("admin"):
        return redirect(url_for("login"))

    if request.method == "POST":
        nuevo_monto = int(request.form.get("monto_minimo", 60000))
        nuevo_radio = int(request.form.get("radio_km", 10))

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE configuracion SET monto_minimo = ?, radio_km = ? WHERE id = 1",
                (nuevo_monto, nuevo_radio),
            )
            conexion.commit()
            cursor.close()
            conexion.close()
            return redirect(url_for("admin"))
        except Exception as e:
            return (
                f"<h1>Error al actualizar la configuración de envíos</h1><p>{e}</p>"
            )


@app.route('/admin/pedidos')
def listar_pedidos():
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM pedidos ORDER BY fecha DESC")
    pedidos = cursor.fetchall()
    conexion.close()
    
    return render_template('admin_pedidos.html', pedidos=pedidos)


@app.route('/admin/pedido/<int:id_pedido>/boleta')
def ver_boleta(id_pedido):
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM pedidos WHERE id = ?", (id_pedido,))
    pedido = cursor.fetchone()
    
    cursor.execute("SELECT producto_nombre, cantidad, precio_unitario FROM detalle_pedido WHERE pedido_id = ?", (id_pedido,))
    detalles = cursor.fetchall()
    
    conexion.close()
    
    return render_template('boleta.html', pedido=pedido, detalles=detalles)


@app.route('/admin/pedidos/limpiar-anteriores', methods=['POST'])
def limpiar_pedidos_anteriores():
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # En SQLite usamos date('now') en lugar de CURDATE()
    cursor.execute("DELETE FROM detalle_pedido WHERE pedido_id IN (SELECT id FROM pedidos WHERE date(fecha) < date('now'))")
    cursor.execute("DELETE FROM pedidos WHERE date(fecha) < date('now')")
    
    conexion.commit()
    conexion.close()
    
    return redirect(url_for('listar_pedidos'))


@app.route('/admin/crear-boleta-manual', methods=('GET', 'POST'))
def crear_boleta_manual():
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    if request.method == 'POST':
        cliente_nombre = request.form.get('cliente_nombre', 'Cliente Mostrador')
        cliente_direccion = request.form.get('cliente_direccion', 'Tienda Física')
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("SELECT id, nombre, precio, stock, nombre_unidad FROM mercaderia")
        todos_productos = cursor.fetchall()

        subtotal = 0
        detalle_texto = ""
        items_a_procesar = []

        for prod in todos_productos:
            p_id, p_nombre, p_precio, p_stock, nombre_unidad_db = prod
            unidad_nombre = nombre_unidad_db if nombre_unidad_db else "Pack"
            
            cant_str = request.form.get(f'cantidad_{p_id}', '0')
            es_medio_pack = request.form.get(f'medio_pack_{p_id}')
            
            try:
                cantidad = int(cant_str)
            except ValueError:
                cantidad = 0

            if cantidad > 0:
                if cantidad > p_stock:
                    cantidad = p_stock

                precio_aplicado = (p_precio / 2) if es_medio_pack else p_precio
                total_item = precio_aplicado * cantidad
                subtotal += total_item
                
                prefijo_medio = obtener_etiqueta_medio(p_nombre, unidad_nombre)
                etiqueta_tipo = f" ({prefijo_medio} {unidad_nombre})" if es_medio_pack else ""
                
                detalle_texto += f"• {p_nombre}{etiqueta_tipo} x{cantidad} - (${total_item})\n"
                
                items_a_procesar.append({
                    "id": p_id,
                    "nombre": f"{p_nombre}{etiqueta_tipo}",
                    "cantidad": cantidad,
                    "precio_unitario": precio_aplicado,
                    "nuevo_stock": p_stock - cantidad
                })

        if not items_a_procesar:
            cursor.close()
            conexion.close()
            return redirect(url_for('crear_boleta_manual'))

        cursor.execute(
            "INSERT INTO pedidos (fecha, productos, total, cliente_nombre, cliente_direccion) VALUES (?, ?, ?, ?, ?)",
            (fecha_actual, detalle_texto, subtotal, cliente_nombre, cliente_direccion),
        )
        pedido_id = cursor.lastrowid

        for item in items_a_procesar:
            cursor.execute(
                "INSERT INTO detalle_pedido (pedido_id, producto_nombre, cantidad, precio_unitario) VALUES (?, ?, ?, ?)",
                (pedido_id, item["nombre"], item["cantidad"], item["precio_unitario"])
            )
            cursor.execute(
                "UPDATE mercaderia SET stock = ? WHERE id = ?",
                (item["nuevo_stock"], item["id"])
            )

        conexion.commit()
        cursor.close()
        conexion.close()

        return redirect(url_for('ver_boleta', id_pedido=pedido_id))

    texto_busqueda = normalizar(request.args.get('busqueda', ''))
    
    cursor.execute("SELECT id, nombre, precio, stock, sabores, categoria, imagen, departamento, descripcion FROM mercaderia")
    todos_productos = cursor.fetchall()
    
    productos = []
    for prod in todos_productos:
        p_id, p_nombre, p_precio, p_stock, p_sabores, p_categoria, p_img, p_dep, p_desc = prod
        if not texto_busqueda or texto_busqueda in normalizar(p_nombre) or texto_busqueda in normalizar(p_categoria):
            productos.append(prod)

    cursor.close()
    conexion.close()

    return render_template('crear_boleta_manual.html', productos=productos, busqueda_actual=request.args.get('busqueda', ''))


# --- RUTAS PARA GESTIÓN DE USUARIOS ---

@app.route('/admin/usuarios', methods=('GET', 'POST'))
def gestionar_usuarios():
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    if request.method == 'POST':
        nuevo_usuario = request.form.get('usuario', '').strip()
        nueva_contrasena = request.form.get('contrasena', '').strip()
        
        if nuevo_usuario and nueva_contrasena:
            try:
                cursor.execute(
                    "INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)",
                    (nuevo_usuario, nueva_contrasena)
                )
                conexion.commit()
            except Exception as e:
                pass 
                
        cursor.close()
        conexion.close()
        return redirect(url_for('gestionar_usuarios'))
        
    cursor.execute("SELECT id, usuario FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    return render_template('usuarios.html', usuarios=usuarios)


@app.route('/admin/usuarios/eliminar/<int:id_user>', methods=('POST', 'GET'))
def eliminar_usuario(id_user):
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_user,))
        conexion.commit()
        cursor.close()
        conexion.close()
    except Exception as e:
        pass
        
    return redirect(url_for('gestionar_usuarios'))


# --- NUEVA RUTA PARA CARGA MASIVA DE PRODUCTOS POR CSV ---

@app.route("/admin/importar-csv", methods=("GET", "POST"))
def importar_csv():
    if not session.get("admin"):
        return redirect(url_for("login"))

    if request.method == "POST":
        archivo = request.files.get("archivo_csv")
        if archivo and archivo.filename.endswith(".csv"):
            try:
                stream = io.TextIOWrapper(archivo.stream, encoding="utf-8")
                lector = csv.DictReader(stream)

                conexion = obtener_conexion()
                cursor = conexion.cursor()

                for fila in lector:
                    nombre = fila.get("nombre", "").strip()
                    if not nombre:
                        continue
                    
                    try:
                        precio = float(fila.get("precio", 0))
                    except ValueError:
                        precio = 0.0

                    try:
                        stock = int(fila.get("stock", 0))
                    except ValueError:
                        stock = 0

                    sabores = fila.get("sabores", "").strip()
                    categoria = fila.get("categoria", "Otros").strip()
                    departamento = fila.get("departamento", "Mercaderia").strip()
                    descripcion = fila.get("descripcion", "").strip()
                    
                    try:
                        permite_medio_pack = int(fila.get("permite_medio_pack", 0))
                    except ValueError:
                        permite_medio_pack = 0

                    nombre_unidad = fila.get("nombre_unidad", "Pack").strip()
                    if not nombre_unidad:
                        nombre_unidad = "Pack"

                    imagen_final = "logo.npg.jpeg"

                    cursor.execute(
                        """INSERT INTO mercaderia 
                           (nombre, precio, stock, sabores, categoria, imagen, departamento, descripcion, permite_medio_pack, nombre_unidad) 
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            nombre,
                            precio,
                            stock,
                            sabores,
                            categoria,
                            imagen_final,
                            departamento,
                            descripcion,
                            permite_medio_pack,
                            nombre_unidad,
                        ),
                    )

                conexion.commit()
                cursor.close()
                conexion.close()
                return redirect(url_for("listar_productos_admin"))
            except Exception as e:
                return f"<h1>Error al procesar el archivo CSV</h1><p>{e}</p>"

    return render_template("importar_csv.html")


if __name__ == "__main__":
    app.run(debug=True)