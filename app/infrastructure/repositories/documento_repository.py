"""
Repositorio de Documentos Generados.

Encapsula el acceso a la tabla documentos_generados.
"""

from typing import List

from app.database.database import get_connection
from app.core.entities import DocumentoGeneradoDTO


class DocumentoRepository:
    """Maneja la persistencia del historial de documentos generados."""

    def insertar(self, doc: DocumentoGeneradoDTO) -> DocumentoGeneradoDTO:
        """Inserta un registro de documento generado y devuelve el DTO con ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO documentos_generados (tipo_documento, placa_vehiculo, ruta_archivo, fecha_generacion)
            VALUES (?, ?, ?, ?)
            """,
            (doc.tipo_documento, doc.placa_vehiculo, doc.ruta_archivo, doc.fecha_generacion),
        )
        conn.commit()
        doc.id = cursor.lastrowid
        conn.close()
        return doc

    def obtener_todos(self) -> List[DocumentoGeneradoDTO]:
        """Devuelve todos los registros de documentos generados, ordenados por fecha descendente."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, tipo_documento, placa_vehiculo, ruta_archivo, fecha_generacion
            FROM documentos_generados
            ORDER BY fecha_generacion DESC
            """
        )
        filas = cursor.fetchall()
        conn.close()
        return [
            DocumentoGeneradoDTO(
                id=fila[0],
                tipo_documento=fila[1],
                placa_vehiculo=fila[2],
                ruta_archivo=fila[3],
                fecha_generacion=fila[4],
            )
            for fila in filas
        ]