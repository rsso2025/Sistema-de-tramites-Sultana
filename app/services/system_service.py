"""
Servicio de Estado del Sistema.

Centraliza las comprobaciones del estado general de la aplicación.
Actualmente verifica la conexión con la base de datos MySQL.
"""

from app.infrastructure.mysql.mysql_connection import get_connection


class SystemService:
    """Servicio encargado de verificar el estado del sistema."""

    @staticmethod
    def verificar_mysql() -> bool:
        """
        Verifica si existe conexión con MySQL.

        Returns:
            True si la conexión fue exitosa.
            False si ocurrió cualquier error.
        """
        try:
            conexion = get_connection()
            conexion.close()
            return True

        except Exception:
            return False