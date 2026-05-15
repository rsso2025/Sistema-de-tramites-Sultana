"""
Repositorio de Propietarios.

Encapsula las operaciones de base de datos para la entidad Propietario.
Utiliza las funciones de conexión definidas en app.database.database.
"""

import sqlite3
from typing import List

from app.database.database import get_connection
from app.core.entities import PropietarioDTO


class PropietarioRepository:
    """Maneja la persistencia de propietarios en SQLite."""

    def insertar(self, propietario: PropietarioDTO) -> PropietarioDTO:
        """
        Inserta un nuevo propietario y devuelve el DTO con el ID asignado.

        Lanza sqlite3.IntegrityError si el documento ya existe.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO propietarios (documento, nombre, telefono, direccion)
            VALUES (?, ?, ?, ?)
            """,
            (
                propietario.documento,
                propietario.nombre,
                propietario.telefono or "",
                propietario.direccion or "",
            ),
        )
        conn.commit()
        propietario.id = cursor.lastrowid
        conn.close()
        return propietario

    def obtener_todos(self) -> List[PropietarioDTO]:
        """Devuelve todos los propietarios ordenados por nombre."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, documento, nombre, telefono, direccion
            FROM propietarios
            ORDER BY nombre
            """
        )
        filas = cursor.fetchall()
        conn.close()

        return [
            PropietarioDTO(
                id=fila[0],
                documento=fila[1],
                nombre=fila[2],
                telefono=fila[3],
                direccion=fila[4],
            )
            for fila in filas
        ]