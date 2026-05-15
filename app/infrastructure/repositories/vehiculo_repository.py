"""
Repositorio de Vehículos.

Encapsula las operaciones de base de datos para la entidad Vehículo.
"""

import sqlite3
from typing import List

from app.database.database import get_connection
from app.core.entities import VehiculoDTO


class VehiculoRepository:
    """Maneja la persistencia de vehículos en SQLite."""

    def insertar(self, vehiculo: VehiculoDTO) -> VehiculoDTO:
        """
        Inserta un nuevo vehículo y devuelve el DTO con el ID asignado.

        Lanza sqlite3.IntegrityError si la placa ya existe.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO vehiculos (
                placa, numero_interno, marca, modelo, clase,
                fecha_afiliacion, propietario_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                vehiculo.placa,
                vehiculo.numero_interno or "",
                vehiculo.marca or "",
                vehiculo.modelo or "",
                vehiculo.clase or "",
                vehiculo.fecha_afiliacion or "",
                vehiculo.propietario_id,
            ),
        )
        conn.commit()
        vehiculo.id = cursor.lastrowid
        conn.close()
        return vehiculo

    def obtener_todos_con_propietario(self) -> List[VehiculoDTO]:
        """Devuelve todos los vehículos con datos de su propietario, ordenados por placa."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
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
            """
        )
        filas = cursor.fetchall()
        conn.close()

        return [
            VehiculoDTO(
                id=fila[0],
                placa=fila[1],
                numero_interno=fila[2],
                marca=fila[3],
                modelo=fila[4],
                clase=fila[5],
                fecha_afiliacion=fila[6],
                propietario_id=fila[7],
                documento_propietario=fila[8],
                nombre_propietario=fila[9],
                telefono_propietario=fila[10],
                direccion_propietario=fila[11],
            )
            for fila in filas
        ]

    def obtener_por_id(self, vehiculo_id: int) -> VehiculoDTO:
        """Obtiene un vehículo con datos de su propietario por su ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
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
            WHERE v.id = ?
            """,
            (vehiculo_id,),
        )
        fila = cursor.fetchone()
        conn.close()
        if not fila:
            return None
        return VehiculoDTO(
            id=fila[0],
            placa=fila[1],
            numero_interno=fila[2],
            marca=fila[3],
            modelo=fila[4],
            clase=fila[5],
            fecha_afiliacion=fila[6],
            propietario_id=fila[7],
            documento_propietario=fila[8],
            nombre_propietario=fila[9],
            telefono_propietario=fila[10],
            direccion_propietario=fila[11],
        )

    def buscar_por_termino(self, termino: str) -> List[VehiculoDTO]:
        """
        Busca vehículos cuyo placa, interno, marca, modelo o nombre de propietario
        contengan el término (case-insensitive gracias a SQLite LIKE).
        """
        conn = get_connection()
        cursor = conn.cursor()
        term = f"%{termino}%"
        cursor.execute(
            """
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
            WHERE v.placa LIKE ?
               OR v.numero_interno LIKE ?
               OR v.marca LIKE ?
               OR v.modelo LIKE ?
               OR p.nombre LIKE ?
            ORDER BY v.placa
            """,
            (term, term, term, term, term),
        )
        filas = cursor.fetchall()
        conn.close()

        return [
            VehiculoDTO(
                id=fila[0],
                placa=fila[1],
                numero_interno=fila[2],
                marca=fila[3],
                modelo=fila[4],
                clase=fila[5],
                fecha_afiliacion=fila[6],
                propietario_id=fila[7],
                documento_propietario=fila[8],
                nombre_propietario=fila[9],
                telefono_propietario=fila[10],
                direccion_propietario=fila[11],
            )
            for fila in filas
        ]