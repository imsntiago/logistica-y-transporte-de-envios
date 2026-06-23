# 🚚 PROYECTO 3 — LOGÍSTICA Y TRANSPORTE DE ENVÍOS

## Contexto

Base de datos para una empresa de logística encargada de gestionar envíos de mercancía. El sistema debe permite registrar envíos, clientes, rutas y seguir del estado de los paquetes.

## Alcance

El modelo de datos contempla:

• Clientes

• Envíos

• Rutas

• Eventos de seguimiento

## Descripción de las entidades

• Clientes: Información de quienes envían o reciben paquetes.

• Envíos: Registro principal de cada paquete con origen, destino, peso y estado.

• Rutas: Definición de trayectos logísticos entre ubicaciones.

• Seguimiento: Registro de eventos en el ciclo de vida del envío (recogido, en tránsito, entregado).

## Reglas de negocio

• Un cliente puede generar múltiples envíos.

• Cada envío tiene un origen y un destino.

• Un envío puede tener múltiples eventos de seguimiento.

• Cada evento registra fecha, estado y ubicación.

## Simplificaciones

• No se optimizan rutas automáticamente.

• No se modela asignación de vehículos.

• No se incluyen costos operativos detallados.

## Objetivo analítico

El modelo permite analizar:

• Tiempos de entrega

• Estados de los envíos

• Volumen de envíos por cliente o región

• Eficiencia en entregas

# 🧱 Modelado de Datos

En la primera entrega se realizó el diseño del modelo entidad-relación (ER), identificando las siguientes entidades principales:

• Clientes

• Rutas

• Envíos

• Seguimiento

Posteriormente, se transformó al modelo relacional definiendo:

• Claves primarias

• Claves foráneas

• Tipos de datos adecuados

## Incluye:

• Diagrama Entidad-Relación (ER)
!['Diagrama ER'](assets/MER.jpeg)


• Modelo relacional
!['Modelo Relacional'](assets/MR.jpeg)

# Implementación de la Base de Datos

Se implementó la base de datos en MySQL Workbench mediante scripts SQL.

### Tablas creadas:

### 📌 Clientes
Almacena la información de personas y empresas que realizan o reciben envíos.

### 📌 Rutas
Contiene las rutas utilizadas para el transporte de mercancías dentro del territorio colombiano.

### 📌 Envíos
Registra cada envío realizado, relacionando remitente, destinatario y ruta.

### 📌 Seguimiento
Permite registrar eventos del envío (estado, ubicación, incidencias).

-----------

## 🔗 3. Relaciones

• Un cliente puede ser remitente o destinatario en múltiples envíos

• Un envío pertenece a una ruta

• Un envío puede tener múltiples eventos de seguimiento

----------

## ⚙️ 4. Implementación Técnica

Se utilizó:

• MySQL Workbench → Creación y gestión de la base de datos

• Python (VS Code) → Generación e inserción de datos

• Librería Faker → Creación de datos simulados realistas

----------

## 🧪 5. Inserción de Datos (DML con Python)

Se desarrolló un script en Python (`faker_script.py`) para poblar la base de datos automáticamente.

### 🔹 Proceso:

1. Conexión a MySQL mediante `mysql.connector`

2. Generación de datos con Faker

3. Inserción en orden lógico según dependencias: Clientes, rutas, envíos, seguimiento

## 📊 6. Generación de Datos Realistas

Se implementaron mejoras para simular un entorno real:

### 👥 Clientes
Se generarón 500 clientes ficticios

Características:

• Personas naturales y empresas

• Clientes activos e inactivos

• Información distribuida entre los 32 departamentos de Colombia

• Direcciones, correos y teléfonos simulados.

### 📍​ Rutas

Se generaron rutas nacionales utilizando las capitales de los 32 departamentos colombianos
Características:

• Destinos nacionales

• Clasificación por zona urbana y rural

• Distancias simuladas 

• Tiempos estimados de entregas

• Se generarón 100 rutas (Interdepartamental, intermunicipal y urbana)

### 🚚 Envíos

Se generarón 5.000 envíos

Características:

• Tipos: Express, estándar, carga pesada, frágil

• Costos calculados según peso y tipo

• Estados: Pendiente, recogido, en centro logístico, en tránsito, en reparto y entregado

• Período utilizado entre el 01/01/2022 al 15/06/2026

### 📍 Seguimiento

Se generarón eventos de seguimiento para cada envío al igual que incidencias 

- Eventos de seguimiento dentro del ciclo de vida del envío:

  • Admisión del paquete

  • Procesamiento logístico
  
  • Transporte
  
  • Entrega final

- Incidencias dentro del ciclo de vida del envío:

  • Cliente no encontrado
  
  • Dirección incorrecta
  
  • Problemas en la vía
  
  • Alta demanda operativa
  
  • Retraso por clima
  
  • Paquete dañado
  
  • Intento de entrega fallido
  
  • Demora logística
  
  • Reprogramación de entrega


📈 Estacionalidad Implementada

También se incorporó estacionalidad en la generación de los envíos para representar el comportamiento real del negocio.

Los períodos con mayor demanda fueron:

• Noviembre (Black friday)

• Diciembre (Temporada navideña)

• Semana santa

• Temporadas de vacaciones
 
---------

## 🧠 7. Validación de Datos

Se verificó:

• Integridad referencial (FK)

• Consistencia de datos

• Distribución de valores (consultas SQL)

• Coherencia entre las tablas

---

## ⚠️ 8. Retos y Soluciones

Durante el desarrollo de esta segunda entrega se presentaron desafíos como:

1. Configuración de la conexión entre Python y MySQL

• Desafío: Establecer correctamente la conexión entre Python y la base de datos en MySQL

• Solución: Configurar adecuadamente mysql-connector-python y validar la conexión antes de realizar las inserciones.

2. Gestión de claves primarias y foráneas 

• Desafío: Se presentaron errores relacionados con columnas que no tenían AUTO_INCREMENT y restricciones de claves foráneas

• Solución: Ajustar la estructura de las tablas y definir correctamente las relaciones entre entidades.

3. Orden correcto para cargar los datos

• Desafío:Algunas tablas dependían de información existente en otras tablas, generando errores al insertar.

• Solución: Definir el orden de inserción respetando la integridad referencial: clientes, rutas, envíos y seguimiento.

4. Generación de datos coherentes

• Desafío: Generar información ficticia que representara una operación logística real y mantuviera consistencia entre las tablas

• Solución: Utilizar Faker junto con reglas de negocio para relacionar clientes, rutas y envíos de manera lógica.

---------


## 🎯 9. Resultados

Se logró:

• Base de datos funcional (Creación tablas DDL e inserción DML en Python)

• Generación de datos realistas y coherentes con la librería Faker

-----------


## 👨‍💻 Autores equipo 7

• Lina Camila Arrieta Ceballos

• Narling Ximena Camargo Gomez

• Santiago Jaramillo Graciano

• Eduar Santiago García Serrano

## Incluye:

• Script de creación de tablas (DDL)

• Script de inserción de datos (DML o Python)

!['Python Script'](faker_script_bd.py)

!['SQL Script'](proyecto_logistica_final.sql)

# Continuará...
