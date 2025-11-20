-- Crear base de datos para macetas
CREATE DATABASE IF NOT EXISTS tienda_macetas;
USE tienda_macetas;

-- Crear tabla de macetas
CREATE TABLE IF NOT EXISTS macetas (
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT DEFAULT NULL,
    precio DECIMAL(10,2) NOT NULL,
    imagen_url VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Insertar datos de ejemplo para macetas
INSERT INTO macetas (nombre, descripcion, precio, imagen_url) VALUES
('Maceta Terracota Grande', 'Maceta clásica de barro cocido, ideal para plantas grandes', 199.99, 'img/maceta_terracota.jpg'),
('Maceta Decorativa Moderna', 'Maceta de cerámica con diseños geométricos', 299.99, 'img/maceta_decorativa.jpg'),
('Maceta Colgante', 'Perfecta para plantas trepadoras y decoración exterior', 159.99, 'img/maceta_colgante.jpg'),
('Maceta Plástico Biodegradable', 'Maceta ecológica para plantas pequeñas', 89.99, 'img/maceta_eco.jpg'),
('Maceta Bonsái', 'Maceta especial para bonsái con plato', 249.99, 'img/maceta_bonsai.jpg');

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
('Semillas de Tomate Cherry', 'Semillas orgánicas de tomate cherry, fácil de cultivar', 49.99, 'img/semilla_tomate.jpg'),
('Semillas de Albahaca', 'Semillas de albahaca italiana, aromática', 39.99, 'img/semilla_albahaca.jpg'),
('Semillas de Girasol', 'Semillas de girasol gigante para jardín', 29.99, 'img/semilla_girasol.jpg'),
('Semillas de Lavanda', 'Semillas de lavanda aromática', 44.99, 'img/semilla_lavanda.jpg'),
('Semillas de Chile', 'Semillas de chile jalapeño', 34.99, 'img/semilla_chile.jpg');