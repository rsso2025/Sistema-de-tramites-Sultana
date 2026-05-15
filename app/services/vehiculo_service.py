"""
Servicio de Vehículos.

Contiene la lógica de negocio para la gestión de vehículos.
Utiliza VehiculoRepository y PropietarioRepository.
"""

import sqlite3
from typing import List, Tuple

from app.core.entities import PropietarioDTO, VehiculoDTO
from app.infrastructure.repositories.vehiculo_repository import VehiculoRepository
from app.infrastructure.repositories.propietario_repository import PropietarioRepository


class VehiculoService:
    """Coordina las operaciones del módulo de vehículos."""

    def __init__(
        self,
        vehiculo_repo: VehiculoRepository = None,
        propietario_repo: PropietarioRepository = None,
    ):
        self.vehiculo_repo = vehiculo_repo or VehiculoRepository()
        self.propietario_repo = propietario_repo or PropietarioRepository()

    def crear_vehiculo(
        self,
        placa: str,
        numero_interno: str,
        marca: str,
        modelo: str,
        clase: str,
        fecha_afiliacion: str,
        propietario_id: int,
    ) -> Tuple[bool, str]:
        """
        Crea un nuevo vehículo con validaciones.

        Returns:
            Tupla (éxito, mensaje).
        """
        placa = placa.strip().upper()
        if not placa:
            return False, "La placa es obligatoria."
        if not propietario_id:
            return False, "Debe seleccionar un propietario."

        dto = VehiculoDTO(
            placa=placa,
            numero_interno=numero_interno.strip(),
            marca=marca.strip(),
            modelo=modelo.strip(),
            clase=clase.strip(),
            fecha_afiliacion=fecha_afiliacion.strip(),
            propietario_id=propietario_id,
        )

        try:
            self.vehiculo_repo.insertar(dto)
            return True, f"Vehículo '{placa}' guardado correctamente."
        except sqlite3.IntegrityError:
            return False, "Ya existe un vehículo con esa placa."
        except Exception as e:
            return False, f"Error inesperado al guardar: {str(e)}"

    def listar_vehiculos_con_propietario(self) -> List[VehiculoDTO]:
        """Obtiene todos los vehículos con los datos de su propietario."""
        return self.vehiculo_repo.obtener_todos_con_propietario()

    def obtener_propietarios_para_combo(self) -> Tuple[List[str], dict]:
        """
        Devuelve la lista de etiquetas para el combo de propietarios
        y un mapa etiqueta -> id.
        """
        propietarios = self.propietario_repo.obtener_todos()
        if not propietarios:
            return ["No hay propietarios"], {}

        etiquetas = []
        mapa = {}
        for p in propietarios:
            etiqueta = f"{p.nombre} - {p.documento}"
            etiquetas.append(etiqueta)
            mapa[etiqueta] = p.id
        return etiquetas, mapa

    def obtener_datos_vehiculo_por_id(self, vehiculo_id: int) -> VehiculoDTO:
        """Carga los datos completos de un vehículo por ID (para la generación de documentos)."""
        return self.vehiculo_repo.obtener_por_id(vehiculo_id)

    def obtener_datos_para_lista(self) -> Tuple[str, str, List[str]]:
        """Devuelve encabezado, separador y filas formateadas para la UI."""
        vehiculos = self.listar_vehiculos_con_propietario()

        encabezado = (
            f"{'PLACA':<12} {'INTERNO':<12} {'MARCA':<15} "
            f"{'MODELO':<12} {'CLASE':<12} {'AFILIACIÓN':<15} {'PROPIETARIO':<20}\n"
        )
        separador = "-" * 105 + "\n"

        if not vehiculos:
            return encabezado, separador, ["No hay vehículos registrados.\n"]

        filas = []
        for v in vehiculos:
            fila = (
                f"{(v.placa or ''):<12} {(v.numero_interno or ''):<12} "
                f"{(v.marca or ''):<15} {(v.modelo or ''):<12} "
                f"{(v.clase or ''):<12} {(v.fecha_afiliacion or ''):<15} "
                f"{(v.nombre_propietario or ''):<20}\n"
            )
            filas.append(fila)

        return encabezado, separador, filas