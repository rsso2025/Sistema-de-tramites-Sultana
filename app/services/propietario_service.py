"""
Servicio de Propietarios.

Contiene la lógica de negocio para la gestión de propietarios.
La UI utilizará este servicio en lugar de acceder directamente a la base de datos.
"""

import sqlite3
from typing import List, Tuple

from app.core.entities import PropietarioDTO
from app.infrastructure.repositories.propietario_repository import PropietarioRepository


class PropietarioService:
    """Coordina las operaciones del módulo de propietarios."""

    def __init__(self, repositorio: PropietarioRepository = None):
        """
        Inicializa el servicio.

        Args:
            repositorio: Instancia de PropietarioRepository.
                         Si no se provee, se crea una por defecto.
        """
        self.repositorio = repositorio or PropietarioRepository()

    def crear_propietario(
        self, documento: str, nombre: str, telefono: str, direccion: str
    ) -> Tuple[bool, str]:
        """
        Crea un nuevo propietario con validaciones de negocio.

        Args:
            documento: Documento de identidad (obligatorio).
            nombre: Nombre completo (obligatorio).
            telefono: Teléfono (opcional).
            direccion: Dirección (opcional).

        Returns:
            Tupla (éxito, mensaje). Si éxito es True, el mensaje es
            un texto de confirmación. Si es False, describe el error.
        """
        # Validaciones de negocio (antes estaban en la UI)
        documento = documento.strip()
        nombre = nombre.strip()
        telefono = telefono.strip()
        direccion = direccion.strip()

        if not documento:
            return False, "El documento es obligatorio."
        if not nombre:
            return False, "El nombre es obligatorio."

        # Validación adicional: longitud mínima
        if len(documento) < 3:
            return False, "El documento debe tener al menos 3 caracteres."

        # Crear DTO
        dto = PropietarioDTO(
            documento=documento,
            nombre=nombre,
            telefono=telefono,
            direccion=direccion,
        )

        try:
            self.repositorio.insertar(dto)
            return True, f"Propietario '{nombre}' guardado correctamente."
        except sqlite3.IntegrityError:
            return False, "Ya existe un propietario con ese documento."
        except Exception as e:
            return False, f"Error inesperado al guardar: {str(e)}"

    def listar_propietarios(self) -> List[PropietarioDTO]:
        """
        Obtiene todos los propietarios registrados.

        Returns:
            Lista de PropietarioDTO.
        """
        return self.repositorio.obtener_todos()

    def obtener_datos_para_lista(self) -> Tuple[str, str, List[str]]:
        """
        Devuelve datos formateados para mostrar en la interfaz.

        Returns:
            Tupla con:
                - encabezado (str)
                - separador (str)
                - lista de filas formateadas (List[str])
        """
        propietarios = self.listar_propietarios()

        encabezado = (
            f"{'DOCUMENTO':<15} {'NOMBRE':<25} "
            f"{'TELÉFONO':<15} {'DIRECCIÓN':<25}\n"
        )
        separador = "-" * 85 + "\n"

        if not propietarios:
            return encabezado, separador, ["No hay propietarios registrados.\n"]

        filas = []
        for p in propietarios:
            fila = (
                f"{p.documento:<15} {p.nombre:<25} "
                f"{(p.telefono or ''):<15} {(p.direccion or ''):<25}\n"
            )
            filas.append(fila)

        return encabezado, separador, filas
    