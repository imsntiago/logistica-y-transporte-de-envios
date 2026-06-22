-- =====================================
-- CREACIÓN DE BASE DE DATOS
-- =====================================

CREATE DATABASE logistica_transporte_final;

USE logistica_transporte_final;


-- =====================================
-- TABLA CLIENTES
-- =====================================

CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100),
    direccion VARCHAR(150),
    ciudad VARCHAR(50) NOT NULL,
    departamento VARCHAR(50) NOT NULL,
    tipo_cliente ENUM(
        'Persona Natural',
        'Empresa'
    ) NOT NULL,
    fecha_registro DATE NOT NULL,
    estado_cliente ENUM(
        'Activo',
        'Inactivo'
    ) NOT NULL
);

-- =====================================
-- TABLA RUTAS
-- =====================================

CREATE TABLE rutas (
    id_ruta INT AUTO_INCREMENT PRIMARY KEY,
    destino VARCHAR(100) NOT NULL,
    distancia DECIMAL(10,2) NOT NULL,
    tipo_ruta ENUM(
        'Urbana',
        'Intermunicipal',
        'Interdepartamental'
    ) NOT NULL,
    tiempo_estimado INT NOT NULL
);

-- =====================================
-- TABLA ENVIOS
-- =====================================

CREATE TABLE envios (

    id_envio INT AUTO_INCREMENT PRIMARY KEY,
    id_remitente INT NOT NULL,
    id_destinatario INT NOT NULL,
    id_ruta INT NOT NULL,
    tipo_envio ENUM(
        'Express',
        'Estándar',
        'Carga Pesada',
        'Frágil'
    ) NOT NULL,
    peso DECIMAL(10,2) NOT NULL,
    fecha_envio DATE NOT NULL,
    fecha_entrega DATE,
    estado ENUM(
        'Pendiente',
        'Recogido',
        'En Centro Logístico',
        'En Tránsito',
        'En Reparto',
        'Entregado'
    ) NOT NULL,
     tiempo_entrega INT,
    costo_envio DECIMAL(10,2),
    CONSTRAINT fk_envio_remitente
        FOREIGN KEY (id_remitente)
        REFERENCES clientes(id_cliente),

    CONSTRAINT fk_envio_destinatario
        FOREIGN KEY (id_destinatario)
        REFERENCES clientes(id_cliente),

    CONSTRAINT fk_envio_ruta
        FOREIGN KEY (id_ruta)
        REFERENCES rutas(id_ruta)
);

-- =====================================
-- TABLA SEGUIMIENTO
-- =====================================

CREATE TABLE seguimiento (

    id_evento INT AUTO_INCREMENT PRIMARY KEY,

    id_envio INT NOT NULL,

    fecha_evento DATE NOT NULL,

    estado VARCHAR(50),

    ubicacion VARCHAR(100),

    tipo_evento VARCHAR(100),

    CONSTRAINT fk_seguimiento_envio
        FOREIGN KEY (id_envio)
        REFERENCES envios(id_envio)
);

-- Agreación de una nueva columna a la tabla rutas

ALTER TABLE rutas
ADD COLUMN zona_destino VARCHAR(20) NOT NULL;

-- =====================================
-- CONSULTAS DE VALIDACIÓN
-- =====================================

SELECT COUNT(*) FROM clientes;
SELECT COUNT(*) FROM rutas;
SELECT COUNT(*) FROM envios;
SELECT COUNT(*) FROM seguimiento;

SELECT * FROM clientes;
SELECT * FROM rutas;
SELECT * FROM envios;
SELECT * FROM seguimiento;

SELECT
tipo_evento,
COUNT(*) cantidad
FROM seguimiento
GROUP BY tipo_evento
ORDER BY cantidad DESC;

SELECT COUNT(*) FROM envios;

SELECT estado, COUNT(*) cantidad
FROM envios
GROUP BY estado;

SELECT YEAR(fecha_envio) AS año,
COUNT(*) cantidad
FROM envios
GROUP BY YEAR(fecha_envio)
ORDER BY año;

SELECT MONTH(fecha_envio) AS mes,
COUNT(*) cantidad
FROM envios
GROUP BY MONTH(fecha_envio)
ORDER BY mes;

SELECT
zona_destino,
COUNT(*)
FROM rutas
GROUP BY zona_destino;


SELECT MIN(fecha_envio)
FROM envios;

SELECT MAX(fecha_envio)
FROM envios;

SELECT COUNT(*)
FROM envios
WHERE fecha_envio > CURDATE();

SELECT
YEAR(fecha_envio) AS año,
COUNT(*) AS cantidad
FROM envios
GROUP BY YEAR(fecha_envio)
ORDER BY año;

SELECT
MONTH(fecha_envio) AS mes,
COUNT(*) AS cantidad
FROM envios
GROUP BY MONTH(fecha_envio)
ORDER BY mes;

SELECT COUNT(*) 
FROM envios;


SELECT tipo_ruta,
COUNT(*) cantidad
FROM rutas
GROUP BY tipo_ruta
ORDER BY cantidad DESC;
