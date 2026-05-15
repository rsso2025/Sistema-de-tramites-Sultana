import sqlite3
from pathlib import Path

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Ruta del archivo de base de datos
DB_PATH = BASE_DIR / "app" / "database" / "sistema_tramites.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # Tabla propietarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS propietarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            documento TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            telefono TEXT,
            direccion TEXT
        )
    """)
    # Tabla vehículos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT NOT NULL UNIQUE,
            numero_interno TEXT,
            marca TEXT,
            modelo TEXT,
            clase TEXT,
            fecha_afiliacion TEXT,
            propietario_id INTEGER NOT NULL,
            FOREIGN KEY (propietario_id) REFERENCES propietarios(id)
        )
    """)
    # Tabla historial de documentos generados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documentos_generados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_documento TEXT NOT NULL,
            placa_vehiculo TEXT NOT NULL,
            ruta_archivo TEXT NOT NULL,
            fecha_generacion TEXT NOT NULL
        )
    """)
    # Tabla trámites
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tramites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            descripcion TEXT,
            vehiculo_id INTEGER NOT NULL,
            fecha_creacion TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'Pendiente',
            FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id)
        )
    """)
    conn.commit()
    conn.close()


def insertar_propietario(documento, nombre, telefono, direccion):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO propietarios (documento, nombre, telefono, direccion)
        VALUES (?, ?, ?, ?)
    """, (documento, nombre, telefono, direccion))

    conn.commit()
    conn.close()


def obtener_propietarios():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, documento, nombre, telefono, direccion
        FROM propietarios
        ORDER BY nombre
    """)
    resultados = cursor.fetchall()
    conn.close()

    return [dict(fila) for fila in resultados]


def insertar_vehiculo(placa, numero_interno, marca, modelo, clase, fecha_afiliacion, propietario_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO vehiculos (
            placa,
            numero_interno,
            marca,
            modelo,
            clase,
            fecha_afiliacion,
            propietario_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (placa, numero_interno, marca, modelo, clase, fecha_afiliacion, propietario_id))

    conn.commit()
    conn.close()


def obtener_vehiculos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            placa,
            numero_interno,
            marca,
            modelo,
            clase,
            fecha_afiliacion,
            propietario_id
        FROM vehiculos
        ORDER BY placa
    """)
    resultados = cursor.fetchall()
    conn.close()

    return [dict(fila) for fila in resultados]


def obtener_vehiculos_con_propietario():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            v.id,
            v.placa,
            v.numero_interno,
            v.marca,
            v.modelo,
            v.clase,
            v.fecha_afiliacion,
            v.propietario_id,
            p.documento AS documento_propietario,
            p.nombre AS nombre_propietario,
            p.telefono AS telefono_propietario,
            p.direccion AS direccion_propietario
        FROM vehiculos v
        INNER JOIN propietarios p ON v.propietario_id = p.id
        ORDER BY v.placa
    """)
    resultados = cursor.fetchall()
    conn.close()

    return [dict(fila) for fila in resultados]