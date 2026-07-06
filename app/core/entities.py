"""
Entidades del dominio del sistema de trámites.

Define objetos de transferencia de datos (DTOs) usando dataclasses.
Estas clases son independientes de la interfaz de usuario y de la base de datos.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class PropietarioDTO:
    """Representa un propietario con sus datos básicos."""
    documento: str
    nombre: str
    telefono: Optional[str] = ""
    direccion: Optional[str] = ""
    id: Optional[int] = None  # Se asigna después de insertar en BD

    def nombre_completo(self) -> str:
        """Devuelve el nombre completo para mostrar en listas."""
        return f"{self.nombre} ({self.documento})"


@dataclass
class PropietarioFiltro:
    """Filtros para búsqueda de propietarios (para uso futuro)."""
    texto: Optional[str] = None  # Busca en nombre o documentopython

@dataclass
class VehiculoDTO:
    """Representa un vehículo con sus datos y la referencia a su propietario."""
    placa: str
    propietario_id: int
    numero_interno: Optional[str] = ""
    marca: Optional[str] = ""
    modelo: Optional[str] = ""
    clase: Optional[str] = ""
    fecha_afiliacion: Optional[str] = ""
    motor: Optional[str] = None
    chasis: Optional[str] = None
    serie: Optional[str] = None
    vin: Optional[str] = None
    fecha_matricula: Optional[str] = None
    capacidad: Optional[str] = None
    tipo: Optional[str] = None
    combustible: Optional[str] = None
    modalidad: Optional[str] = None
    ruta: Optional[str] = None
    color: Optional[str] = None
    carroceria: Optional[str] = None
    servicio: Optional[str] = None
    id: Optional[int] = None

    # Datos del propietario (se llenan en consultas JOIN)
    documento_propietario: Optional[str] = None
    nombre_propietario: Optional[str] = None
    telefono_propietario: Optional[str] = None
    direccion_propietario: Optional[str] = None

    nombre_conductor: Optional[str] = None
    documento_conductor: Optional[str] = None
    celular_conductor: Optional[str] = None
    direccion_conductor: Optional[str] = None
    correo_conductor: Optional[str] = None


@dataclass
class DocumentoGeneradoDTO:
    """Representa un registro de documento generado para historial."""
    tipo_documento: str
    placa_vehiculo: str
    ruta_archivo: str
    fecha_generacion: str = field(default_factory=lambda: datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    id: Optional[int] = None 


@dataclass
class TramiteDTO:
    """Representa un trámite asociado a un vehículo."""
    tipo: str  # e.g., 'Certificación', 'Formato de Accidente'
    descripcion: str
    vehiculo_id: int
    fecha_creacion: str = field(default_factory=lambda: datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    estado: str = "Pendiente"  # Pendiente, En proceso, Finalizado
    id: Optional[int] = None
