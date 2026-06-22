from faker import Faker
import mysql.connector
import random
from datetime import date, timedelta

# Faker Colombia
fake = Faker('es_CO')

# ==========================
# CONEXIÓN MYSQL
# ==========================

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="logistica_transporte_final"
)

cursor = conexion.cursor()

print("✅ Conexión exitosa")

# ==========================
# DEPARTAMENTOS Y CAPITALES
# ==========================

ubicaciones_colombia = {
    "Amazonas": "Leticia",
    "Antioquia": "Medellín",
    "Arauca": "Arauca",
    "Atlántico": "Barranquilla",
    "Bolívar": "Cartagena",
    "Boyacá": "Tunja",
    "Caldas": "Manizales",
    "Caquetá": "Florencia",
    "Casanare": "Yopal",
    "Cauca": "Popayán",
    "Cesar": "Valledupar",
    "Chocó": "Quibdó",
    "Córdoba": "Montería",
    "Cundinamarca": "Bogotá",
    "Guainía": "Inírida",
    "Guaviare": "San José del Guaviare",
    "Huila": "Neiva",
    "La Guajira": "Riohacha",
    "Magdalena": "Santa Marta",
    "Meta": "Villavicencio",
    "Nariño": "Pasto",
    "Norte de Santander": "Cúcuta",
    "Putumayo": "Mocoa",
    "Quindío": "Armenia",
    "Risaralda": "Pereira",
    "San Andrés y Providencia": "San Andrés",
    "Santander": "Bucaramanga",
    "Sucre": "Sincelejo",
    "Tolima": "Ibagué",
    "Valle del Cauca": "Cali",
    "Vaupés": "Mitú",
    "Vichada": "Puerto Carreño"
}

# ==========================
# CLIENTES
# ==========================

for _ in range(500):

    departamento = random.choice(list(ubicaciones_colombia.keys()))
    ciudad = ubicaciones_colombia[departamento]

    # 70% Persona Natural / 30% Empresa
    tipo_cliente = random.choices(
        ["Persona Natural", "Empresa"],
        weights=[70, 30],
        k=1
    )[0]

    # Nombre según tipo
    nombre = fake.company() if tipo_cliente == "Empresa" else fake.name()

    # Correo según tipo
    correo = (
        fake.company_email()
        if tipo_cliente == "Empresa"
        else fake.email()
    )

    # 85% Activo / 15% Inactivo
    estado_cliente = random.choices(
        ["Activo", "Inactivo"],
        weights=[85, 15],
        k=1
    )[0]

    fecha_registro = fake.date_between(
        start_date=date(2022, 1, 1),
        end_date=date.today()
    )

    cursor.execute("""
        INSERT INTO clientes(
            nombre,
            telefono,
            correo,
            direccion,
            ciudad,
            departamento,
            tipo_cliente,
            fecha_registro,
            estado_cliente
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        nombre,
        fake.phone_number(),
        correo,
        fake.street_address(),
        ciudad,
        departamento,
        tipo_cliente,
        fecha_registro,
        estado_cliente
    ))

conexion.commit()

print("✅ 500 clientes insertados correctamente")

# ==========================
# RUTAS
# ==========================

capitales = list(ubicaciones_colombia.values())

for _ in range(100):

    destino = random.choice(capitales)

    # Tipo de ruta
    tipo_ruta = random.choices(
        [
            "Urbana",
            "Intermunicipal",
            "Interdepartamental"
        ],
        weights=[15, 35, 50],
        k=1
    )[0]

    # Zona destino
    zona_destino = random.choices(
        ["Urbana", "Rural"],
        weights=[80, 20],
        k=1
    )[0]

    # Distancias y tiempos según el tipo de ruta
    if tipo_ruta == "Urbana":

        distancia = round(
            random.uniform(5, 40),
            2
        )

        tiempo_estimado = random.randint(1, 3)

    elif tipo_ruta == "Intermunicipal":

        distancia = round(
            random.uniform(40, 250),
            2
        )

        tiempo_estimado = random.randint(2, 8)

    else:  # Interdepartamental

        distancia = round(
            random.uniform(250, 1200),
            2
        )

        tiempo_estimado = random.randint(8, 24)

    cursor.execute("""
        INSERT INTO rutas(
            destino,
            distancia,
            tipo_ruta,
            zona_destino,
            tiempo_estimado
        )
        VALUES (%s,%s,%s,%s,%s)
    """,
    (
        destino,
        distancia,
        tipo_ruta,
        zona_destino,
        tiempo_estimado
    ))

conexion.commit()

print("✅ 100 rutas insertadas correctamente")

# ==========================
# FUNCIÓN FECHA ENVIO
# ==========================

# A través de la variable fecha envío establecemos el rango que vamos a tomar
# para nuestra base de datos

from datetime import date, timedelta

def generar_fecha_envio():

    fecha_actual = date.today()

    while True:

        mes = random.choices(
            [1,2,3,4,5,6,7,8,9,10,11,12],
            weights=[6,4,5,8,6,8,8,6,5,8,10,16],
            k=1
        )[0]

        año = random.randint(2022, fecha_actual.year)

        dia = random.randint(1, 28)

        fecha_generada = date(año, mes, dia)

        if fecha_generada <= fecha_actual:
            return fecha_generada

# ==========================
# ENVIOS
# ==========================

cursor.execute("SELECT MAX(id_cliente) FROM clientes")
max_cliente = cursor.fetchone()[0]

cursor.execute("SELECT MAX(id_ruta) FROM rutas")
max_ruta = cursor.fetchone()[0]

for _ in range(5000):

    # Remitente y destinatario diferentes
    id_remitente = random.randint(1, max_cliente)

    id_destinatario = random.randint(1, max_cliente)

    while id_destinatario == id_remitente:
        id_destinatario = random.randint(1, max_cliente)

    # Ruta
    id_ruta = random.randint(1, max_ruta)

    # Obtener zona destino
    cursor.execute("""
        SELECT zona_destino
        FROM rutas
        WHERE id_ruta = %s
    """, (id_ruta,))

    zona_destino = cursor.fetchone()[0]

    # Tipo de envío
    tipo_envio = random.choices(
        [
            "Express",
            "Estándar",
            "Carga Pesada",
            "Frágil"
        ],
        weights=[25,50,10,15],
        k=1
    )[0]

    # Peso según tipo
    if tipo_envio == "Express":
        peso = round(random.uniform(0.5, 10), 2)

    elif tipo_envio == "Estándar":
        peso = round(random.uniform(1, 20), 2)

    elif tipo_envio == "Frágil":
        peso = round(random.uniform(0.5, 15), 2)

    else:
        peso = round(random.uniform(20, 100), 2)

    # Fecha de envío
    fecha_envio = generar_fecha_envio()

    # Estado
    estado = random.choices(
        [
            "Pendiente",
            "Recogido",
            "En Centro Logístico",
            "En Tránsito",
            "En Reparto",
            "Entregado"
        ],
        weights=[2,3,5,10,10,70],
        k=1
    )[0]

    # Tiempo y fecha entrega
    if estado == "Entregado":

        if zona_destino == "Rural":
            dias_entrega = random.randint(4,12)
        else:
            dias_entrega = random.randint(1,5)

        fecha_entrega = fecha_envio + timedelta(days=dias_entrega)
        tiempo_entrega = dias_entrega

    else:

        fecha_entrega = None
        tiempo_entrega = None

    # Tarifas por tipo
    tarifas = {
        "Express": 5000,
        "Estándar": 3000,
        "Carga Pesada": 2500,
        "Frágil": 4500
    }

    costo_envio = peso * tarifas[tipo_envio]

    # Recargo rural
    if zona_destino == "Rural":
        costo_envio *= 1.15

    costo_envio = round(costo_envio, 2)

    cursor.execute("""
        INSERT INTO envios(
            id_remitente,
            id_destinatario,
            id_ruta,
            tipo_envio,
            peso,
            fecha_envio,
            fecha_entrega,
            estado,
            tiempo_entrega,
            costo_envio
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """,
    (
        id_remitente,
        id_destinatario,
        id_ruta,
        tipo_envio,
        peso,
        fecha_envio,
        fecha_entrega,
        estado,
        tiempo_entrega,
        costo_envio
    ))

conexion.commit()

print("✅ 5000 envíos insertados correctamente")

# ==========================
# SEGUIMIENTO
# ==========================

cursor.execute("""
SELECT
    e.id_envio,
    e.fecha_envio,
    e.fecha_entrega,
    e.estado,
    r.zona_destino
FROM envios e
JOIN rutas r
    ON e.id_ruta = r.id_ruta
""")

envios = cursor.fetchall()

for envio in envios:

    id_envio = envio[0]
    fecha_envio = envio[1]
    fecha_entrega = envio[2]
    estado_final = envio[3]
    zona_destino = envio[4]

    mes_envio = fecha_envio.month

    # ----------------------------------
    # TEMPORADAS DEL AÑO
    # ----------------------------------

    if mes_envio in [11, 12]:

        incidencias = [
            "Demora logística",
            "Reprogramación de entrega",
            "Alta demanda operativa"
        ]

        probabilidad_incidencia = 35

    elif mes_envio == 4:

        incidencias = [
            "Problemas en la vía",
            "Retraso por clima"
        ]

        probabilidad_incidencia = 25

    else:

        incidencias = [
            "Cliente no encontrado",
            "Dirección incorrecta",
            "Intento de entrega fallido",
            "Paquete dañado"
        ]

        probabilidad_incidencia = 20

    # ----------------------------------
    # AUMENTAR INCIDENCIAS EN ZONA RURAL
    # ----------------------------------

    if zona_destino == "Rural":
        probabilidad_incidencia += 10

    tiene_incidencia = random.choices(
        [True, False],
        weights=[
            probabilidad_incidencia,
            100 - probabilidad_incidencia
        ],
        k=1
    )[0]

    # ==================================
    # EVENTO 1
    # ==================================

    cursor.execute("""
    INSERT INTO seguimiento
    (
        id_envio,
        fecha_evento,
        estado,
        ubicacion,
        tipo_evento
    )
    VALUES (%s,%s,%s,%s,%s)
    """,
    (
        id_envio,
        fecha_envio,
        "Recogido",
        "Centro de Recolección",
        "Admisión de Paquete"
    ))

    # ==================================
    # EVENTO 2
    # ==================================

    fecha_evento_2 = fecha_envio + timedelta(days=1)

    if tiene_incidencia:

        incidencia = random.choice(incidencias)

        cursor.execute("""
        INSERT INTO seguimiento
        (
            id_envio,
            fecha_evento,
            estado,
            ubicacion,
            tipo_evento
        )
        VALUES (%s,%s,%s,%s,%s)
        """,
        (
            id_envio,
            fecha_evento_2,
            "En Tránsito",
            "Ruta Nacional",
            incidencia
        ))

    else:

        cursor.execute("""
        INSERT INTO seguimiento
        (
            id_envio,
            fecha_evento,
            estado,
            ubicacion,
            tipo_evento
        )
        VALUES (%s,%s,%s,%s,%s)
        """,
        (
            id_envio,
            fecha_evento_2,
            "En Tránsito",
            "Ruta Nacional",
            "Despacho Intermunicipal"
        ))

    # ==================================
    # EVENTO 3
    # ==================================

    if fecha_entrega is not None:

        cursor.execute("""
        INSERT INTO seguimiento
        (
            id_envio,
            fecha_evento,
            estado,
            ubicacion,
            tipo_evento
        )
        VALUES (%s,%s,%s,%s,%s)
        """,
        (
            id_envio,
            fecha_entrega,
            "Entregado",
            "Destino Final",
            "Entrega Exitosa"
        ))

    else:

        cursor.execute("""
        INSERT INTO seguimiento
        (
            id_envio,
            fecha_evento,
            estado,
            ubicacion,
            tipo_evento
        )
        VALUES (%s,%s,%s,%s,%s)
        """,
        (
            id_envio,
            fecha_evento_2 + timedelta(days=1),
            estado_final,
            "Centro Logístico Regional",
            "Seguimiento en proceso"
        ))

conexion.commit()

print("✅ Seguimiento generado correctamente")