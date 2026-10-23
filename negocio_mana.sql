-- Servidor: 127.0.0.1
-- Tiempo de generación: 23-10-2026 a las 01:11:52
-- Versión del servidor: 10.3.16-MariaDB
-- Versión de PHP: 7.3.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `negocio_mana`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `configuracion`
--

CREATE TABLE `configuracion` (
  `id` int(11) NOT NULL,
  `monto_minimo` int(11) NOT NULL,
  `radio_km` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `configuracion`
--

INSERT INTO `configuracion` (`id`, `monto_minimo`, `radio_km`) VALUES
(1, 8000, 8);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_pedido`
--

CREATE TABLE `detalle_pedido` (
  `id` int(11) NOT NULL,
  `pedido_id` int(11) NOT NULL,
  `producto_nombre` varchar(255) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mercaderia`
--

CREATE TABLE `mercaderia` (
  `ID` int(11) NOT NULL,
  `NOMBRE` varchar(100) NOT NULL,
  `descripcion` text NOT NULL,
  `SABORES` varchar(150) NOT NULL,
  `CATEGORIA` varchar(50) NOT NULL,
  `imagen` varchar(100) NOT NULL,
  `departamento` varchar(50) NOT NULL,
  `PRECIO` int(11) NOT NULL,
  `STOCK` int(11) NOT NULL,
  `permite_medio_pack` tinyint(4) DEFAULT 0,
  `nombre_unidad` varchar(50) DEFAULT 'Pack'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `mercaderia`
--

INSERT INTO `mercaderia` (`ID`, `NOMBRE`, `descripcion`, `SABORES`, `CATEGORIA`, `imagen`, `departamento`, `PRECIO`, `STOCK`, `permite_medio_pack`, `nombre_unidad`) VALUES
(2, 'packc manaos 3L', 'pack manaos de 3 litros contiene 6 unidades ', 'naranja, cola, lima, pomelo, citrus', 'Bebidas', 'manaos_3l.jpeg', 'Mercaderia', 12000, 14, 1, 'pack'),
(3, 'pack manaos de 1,5L', 'pack gaseosa manaos de 1,5 litros, contiene 6 unidades ', 'naranja, cola, lima, pomelo', 'Bebidas', 'manaos_1.5l.jpg', 'Mercaderia', 9000, 5, 1, 'Pack'),
(4, 'pack fresh ', '', 'pomelo, naranja, manzana', 'Bebidas', 'fresh_pack.png', 'Mercaderia', 8500, 6, 0, 'Pack'),
(5, 'pack soda manaos ', '', '', 'Bebidas', 'soda_manaos.jpeg', 'Mercaderia', 10800, 8, 0, 'Pack'),
(6, 'pack yerba mañanita', 'contiene 10 yerba de 1/2 kg ', '', 'Yerbas', 'yerba_mañanita.jpeg', 'Mercaderia', 22500, 5, 0, 'Pack'),
(7, 'pack fideos tallarin', 'pack fideo sol pampeano tallarin, contiene 20 unidades de 500g', '', 'Pastas', 'fideo_tallarin.jpg', 'Mercaderia', 19200, 3, 0, 'Pack'),
(9, 'pack fideos codito', 'pack fideo sol pampeano codito, contiene 15 unidades de 500g', '', 'Pastas', 'fideo_codito.jpg', 'Mercaderia', 14500, 3, 0, 'Pack'),
(10, 'pure tomate 530g', '12 unidades de 530g', '', 'Almacen', 'pure_tomate.jpeg', 'Mercaderia', 12800, 5, 0, 'Pack'),
(11, 'vino encepado ', '', 'dulce, clasico', 'Bebidas', 'encepado_vino.jpeg', 'Mercaderia', 15500, 5, 1, 'Pack'),
(14, 'harina ramirez 25kg 000', 'harina marca ramirez de 25kg tipo 000 ', '', 'Harinas', 'harina25.jpeg', 'Mercaderia', 24800, 5, 0, 'Pack'),
(15, 'papel higienico vual bolson ', '24 papelhigénicos de 50 metros cada uno', '', 'Almacen', 'papel_vual.jpeg', 'Mercaderia', 15800, 5, 0, 'Pack'),
(16, 'pack vino canciller', '', 'dulce, tinto ', 'Bebidas', 'vinos_canciller.png', 'Mercaderia', 18000, 5, 0, 'Pack'),
(17, 'pack harina ramirez 1kg 0000', '', '', 'Harinas', 'pack_ramirez.jpg', 'Mercaderia', 12800, 5, 0, 'Pack'),
(18, ' pack harina ramirez 1kg 000', 'pack harina ramirez tipo 000, contiene 10 unidades de 1kg', '', 'Harinas', 'harina000.jpeg', 'Mercaderia', 10500, 5, 0, 'Pack'),
(19, 'pack arroz Ñambe', 'contiene 10 arroz de 1kg tipo 0000', '', 'Almacen', 'arroz_ñambe.jpeg', 'Mercaderia', 8500, 5, 0, 'Pack'),
(20, 'pack vino toro botella ', 'vino toro tinto 6 unidades', '', 'Bebidas', 'vino_toro.jpeg', 'Mercaderia', 18500, 5, 0, 'Pack'),
(21, 'pack vino chanchullo 3/4', 'vino tinto 3/4 6 unidades', '', 'Bebidas', 'vino_chanchullo.jpg', 'Mercaderia', 24000, 5, 0, 'Pack'),
(22, 'pack arroz cope doce', 'contiene 10 paquetes de 1 kg, arroz de buena calidad de 00000', '', 'Almacen', 'cope12.jpeg', 'Mercaderia', 13500, 5, 0, 'Pack'),
(24, 'harina premezcla para pizza ', 'harina ramirez premezcla para pizza base de trigo, contiene 10 paquetes de 1kg ', '', 'Harinas', 'pizza.jpeg ', 'Mercaderia', 15500, 5, 0, 'Pack'),
(25, ' fideo spaghetti por bolsa 5kg', 'fideo spaghetti marca estrella del Paraná, contiene 5kg ', '', 'Pastas', 'spa5kg.jpeg', 'Mercaderia', 14500, 2, 0, 'Pack'),
(26, 'pack fideo spaghetti ', 'pack fideo sol pampeano spaghetti, contiene 20 unidades de 500g ', '', 'Pastas', 'spaghetti500.jpeg', 'Mercaderia', 14500, 5, 0, 'Pack'),
(27, 'pack fideo Ave Maria ', 'pack fideo sol pampeano Ave Maria, contiene 20 unidades de 500g', '', 'Pastas', 'avemaria.jpeg', 'Mercaderia', 14500, 5, 0, 'Pack'),
(28, 'pack fideo tirabuzón ', 'pack fideo sol pampeano tirabuzón, contiene 15 unidades  ', '', 'Pastas', 'tirabuzon.jpeg', 'Mercaderia', 14500, 5, 0, 'Pack'),
(29, 'pack fideo dedal ', 'pack sol pampeano fideo dedal, contiene 15 unidades de 500g ', '', 'Pastas', 'dedal.jpeg', 'Mercaderia', 14500, 5, 0, 'Pack'),
(30, 'fideo cinta por bolsa de 5kg ', 'fideo cinta marca estrella del Paraná, contiene 5kg', '', 'Pastas', 'cinta.jpeg', 'Mercaderia', 14500, 3, 0, 'Pack'),
(31, 'pack yerba playadito 1kg ', 'pack de yerba marca playadito de 1kg, contiene 5 unidades ', '', 'Yerbas', 'playadito.jpg', 'Mercaderia', 23500, 5, 0, 'Pack'),
(32, 'pack yerba amanda de 1/2 kg', 'pack de yerba amanda, contiene 10 unidades de 1/2 kg ', '', 'Yerbas', 'amanda.jpg', 'Mercaderia', 21000, 5, 0, 'Pack'),
(33, 'pack de yerba yemaype de 1 kg', 'pack de yerbas yemaype, contiene 5 unidades de 1kg ', '', 'Yerbas', 'playaditoo.jpg', 'Mercaderia', 21500, 5, 0, 'Pack'),
(34, 'pack yerba CBSE de 1/2 kg', 'pack de yerba CBSE, contiene 12 unidades de 1/2 kg', '', 'Yerbas', 'cbse.jpg', 'Mercaderia', 24000, 5, 0, 'Pack'),
(35, 'pack aceite Ricoleo de 900ml', 'pack aceite Ricoleo, contiene 15 unidades de 900ml', '', 'Aceites', 'ricoleo.jpg', 'Mercaderia', 43200, 4, 0, 'Pack'),
(36, 'Aceite Prados del Sol de 5 Litros', 'aceite de girasol prados del sol en bidón de 5litro ', '', 'Aceites', 'prados.jpg', 'Mercaderia', 14000, 5, 0, 'Pack'),
(37, 'Aceite Leira de 4,5 litros ', 'Aceite leira en bidón de 4,5 litros ', '', 'Aceites', 'leira.jpg', 'Mercaderia', 13600, 5, 0, 'Pack'),
(38, 'pack vino manojo de uvas rosado ', 'pack vino de uvas rosado, contiene 12 unidades de 1 litro', '', 'Bebidas', 'rosita.jpeg', 'Mercaderia', 19500, 5, 0, 'Pack'),
(39, 'pack vino manojo de uvas tinto', 'pack de vino manojo de uvas tinto, contiene 12 unidades de 1 litro', '', 'Bebidas', 'tintilloo.jpeg', 'Mercaderia', 21000, 5, 0, 'Pack'),
(40, 'Mayonesa Hellmann\'s por caja ', 'mayonesa hellmann\'s por caja de 24 unidades de 250 g', '', 'Almacen', 'hellmans.png', 'Mercaderia', 35000, 7, 0, 'Pack'),
(41, 'Pack sal fina Tresal', 'pack de sal fina Tresal contiene 24 unidades', '', 'Almacen', 'salfina.png', 'Mercaderia', 9500, 5, 0, 'Pack'),
(42, 'Galletitas Lia surtidas por caja ', 'contiene 12 unidades de 300g cada una ', '', 'Almacen', 'watermarked_img_8712906412297762075.jpg', 'Mercaderia', 16000, 5, 0, 'Pack'),
(43, 'Galletita Pepa por caja ', 'contiene 12 unidades de 150g', '', 'Almacen', 'watermarked_img_12821628035745650703.jpg', 'Mercaderia', 11500, 3, 0, 'Pack'),
(46, 'maiz entero bolsa de 40kg', 'maiz entero en bolsa de 40 kg ', '', 'almacen', '1e1cf1e4-c98f-489c-a2b4-79742f1b5d3a.jpeg', 'Forrajeria', 17000, 5, 1, 'bolsa'),
(47, 'maiz molido por bolsa de 40 kg ', 'maiz molido en bolsa de 40 kg ', '', 'almacen', 'a640c912-18ac-448e-abf6-c55551589c5c.jpeg', 'Forrajeria', 17000, 5, 1, 'bolsa'),
(48, 'Comida de perro cachorro marca Atos', 'comida para perro cachorro de 15 kg marca Atos ', '', 'almacen', '30d92f61-6eef-429c-a448-11745c336d05.jpeg', 'Forrajeria', 23200, 4, 1, 'bolsa'),
(49, 'Comida de perro adulto marca Darwin', 'Comida de perro adulto marca Darwin, contiene 15 kg', '', 'almacen', '4c159375-e37e-4099-a200-d6ab7f140ead.jpeg', 'Forrajeria', 17500, 5, 1, 'bolsa'),
(50, 'Alimento para Ponedoras ', 'bolsa de alimento para ponedora de 25 kg ', '', 'almacen', '04207295-0f28-4557-b266-b2c3a4965d8f.jpeg', 'Forrajeria', 22500, 5, 1, 'bolsa'),
(51, 'Comida de perro adulto suelto Darwin', 'comida de perro suelto por kilo ($1600)', '', 'almacen', 'logo.npg.jpeg', 'Forrajeria', 1600, 7, 0, 'Pack'),
(54, 'Alimento Balanceado Aves Ponedoras', 'Alimento balanceado para aves ponedoras x 25 kg ', '', 'alimentos', 'logo.npg.jpeg', 'Forrajeria', 14500, 25, 1, 'Bolsa'),
(55, 'Alimento Balanceado Conejos Crecimiento', 'Alimento balanceado para conejos en etapa de crecimiento', '', 'Alimentos', 'logo.npg.jpeg', 'Forrajeria', 15200, 20, 1, 'Bolsa');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

CREATE TABLE `pedidos` (
  `id` int(11) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  `productos` text NOT NULL,
  `total` int(11) NOT NULL,
  `cliente_nombre` varchar(100) DEFAULT NULL,
  `cliente_direccion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `usuario` varchar(50) NOT NULL,
  `contrasena` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `usuario`, `contrasena`) VALUES
(1, 'Luciano Javier Carrera', 'luciano8622');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `configuracion`
--
ALTER TABLE `configuracion`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pedido_id` (`pedido_id`);

--
-- Indices de la tabla `mercaderia`
--
ALTER TABLE `mercaderia`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario` (`usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `configuracion`
--
ALTER TABLE `configuracion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `mercaderia`
--
ALTER TABLE `mercaderia`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;

--
-- AUTO_INCREMENT de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `detalle_pedido`
--
ALTER TABLE `detalle_pedido`
  ADD CONSTRAINT `detalle_pedido_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
