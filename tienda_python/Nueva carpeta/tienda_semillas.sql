SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

-- Crear base de datos para semillas
CREATE DATABASE IF NOT EXISTS tienda_semillas;
USE tienda_semillas;

-- Crear tabla de semillas
CREATE TABLE IF NOT EXISTS semillas (
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT DEFAULT NULL,
    precio DECIMAL(10,2) NOT NULL,
    imagen_url VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Insertar datos de ejemplo para semillas
INSERT INTO semillas (nombre, descripcion, precio, imagen_url) VALUES
('Semillas de Tomate Cherry', 'Semillas orgánicas de tomate cherry, ideales para huertos caseros', 49.99, 'img/semilla_tomate.jpg'),
('Semillas de Albahaca', 'Semillas de albahaca italiana, perfecta para cocina', 39.99, 'img/semilla_albahaca.jpg'),
('Semillas de Girasol', 'Semillas de girasol gigante para jardín decorativo', 29.99, 'img/semilla_girasol.jpg'),
('Semillas de Lavanda', 'Semillas de lavanda aromática para jardín', 44.99, 'img/semilla_lavanda.jpg'),
('Semillas de Chile', 'Semillas de chile jalapeño, picante medio', 34.99, 'img/semilla_chile.jpg'),
('Semillas de Cilantro', 'Semillas de cilantro fresco', 25.99, 'img/semilla_cilantro.jpg'),
('Semillas de Perejil', 'Semillas de perejil aromático', 22.99, 'img/semilla_perejil.jpg'),
('Semillas de Zanahoria', 'Semillas de zanahoria orgánica', 35.99, 'img/semilla_zanahoria.jpg'),
('Semillas de Lechuga', 'Semillas de lechuga romana', 28.99, 'img/semilla_lechuga.jpg'),
('Semillas de Pimiento', 'Semillas de pimiento morrón', 42.99, 'img/semilla_pimiento.jpg');

COMMIT;