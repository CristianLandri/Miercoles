-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 14-11-2025 a las 20:34:39
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tienda`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  `imagen_url` varchar(255) NOT NULL,
  `stock` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id`, `nombre`, `descripcion`, `precio`, `imagen_url`, `stock`) VALUES
(1, 'Arvejas', 'Arvejas frescas, calidad premium', 60.00, 'img/3b0118ae1692a0a6a3f2c710b0aea838.jpg', 0),
(2, 'Naranja', 'Arbol de naranja', 0.00, 'img/3b0118ae1692a0a6a3f2c710b0aea838.jpg', 0),
(3, 'Ruda', 'Ruda para infusiones', 50.00, 'img/beneficios-de-la-planta-la-ruda.jpg', 0),
(4, 'Pimiento', 'Pimiento rojo fresco', 90.00, 'img/pimiento rojo.jpeg', 0),
(5, 'Tomates', 'Tomates frescos', 50.00, 'img/mas tomates.jpeg', 0),
(6, 'Perejil', 'Perejil fresco', 90.00, 'img/Perejil.jpg', 0),
(7, 'Limonero', 'Limonero joven', 90.00, 'img/limonero.jpg', 0),
(8, 'Naranjo', 'Naranjo joven', 90.00, 'img/Naranja.jpg', 0),
(9, 'Manzanero', 'Manzano de variedad roja', 90.00, 'img/manzanero.jpeg', 0),
(10, 'Lima', 'Lima fresca', 90.00, 'img/Lima.webp', 0);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
