"""
Servicio de Documentos.

Orquesta la generación de documentos desde plantillas .docx y
registra cada generación en el historial.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from docx import Document

from app.core.entities import DocumentoGeneradoDTO, VehiculoDTO
from app.infrastructure.repositories.documento_repository import DocumentoRepository
from app.infrastructure.repositories.vehiculo_repository import VehiculoRepository


def _reemplazar_texto_en_parrafo(parrafo, datos: Dict[str, str]) -> None:
    texto = parrafo.text
    nuevo_texto = texto
    for clave, valor in datos.items():
        placeholder1 = f"{{{{{clave}}}}}"
        placeholder2 = f"{{{clave}}}"
        nuevo_texto = nuevo_texto.replace(placeholder1, valor)
        nuevo_texto = nuevo_texto.replace(placeholder2, valor)

    if nuevo_texto != texto:
        for run in parrafo.runs[::-1]:
            run._element.getparent().remove(run._element)
        parrafo.add_run(nuevo_texto)


def _reemplazar_texto_en_tabla(tabla, datos: Dict[str, str]) -> None:
    for fila in tabla.rows:
        for celda in fila.cells:
            for parrafo in celda.paragraphs:
                _reemplazar_texto_en_parrafo(parrafo, datos)


def _reemplazar_texto_en_documento(documento: Document, datos: Dict[str, str]) -> None:
    for parrafo in documento.paragraphs:
        _reemplazar_texto_en_parrafo(parrafo, datos)
    for tabla in documento.tables:
        _reemplazar_texto_en_tabla(tabla, datos)


def generar_documento(ruta_plantilla: Path, ruta_salida: Path, datos: Dict[str, str]) -> Path:
    if not ruta_plantilla.exists():
        raise FileNotFoundError(f"Plantilla no encontrada: {ruta_plantilla}")

    documento = Document(ruta_plantilla)
    _reemplazar_texto_en_documento(documento, datos)
    documento.save(ruta_salida)
    return ruta_salida


class DocumentoService:
    """Coordina la generación de documentos y el historial."""

    def __init__(
        self,
        vehiculo_repo: VehiculoRepository = None,
        documento_repo: DocumentoRepository = None,
    ):
        self.vehiculo_repo = vehiculo_repo or VehiculoRepository()
        self.documento_repo = documento_repo or DocumentoRepository()
        self.config = self._cargar_configuracion()

    def _cargar_configuracion(self) -> dict:
        """Carga la configuración de tipos de documentos desde el JSON."""
        ruta_config = Path(__file__).resolve().parent.parent / "config" / "documentos_config.json"
        with open(ruta_config, "r", encoding="utf-8") as f:
            return json.load(f)

    def obtener_tipos_documento(self) -> List[str]:
        """Devuelve la lista de tipos de documento disponibles."""
        return list(self.config.keys())

    def obtener_configuracion_documento(self, tipo: str) -> Optional[dict]:
        """Devuelve la configuración para un tipo de documento específico."""
        return self.config.get(tipo)

    def cargar_datos_vehiculo(self, vehiculo_id: int) -> Optional[VehiculoDTO]:
        """Obtiene los datos completos de un vehículo por su ID."""
        return self.vehiculo_repo.obtener_por_id(vehiculo_id)

    def preparar_datos_plantilla(
        self, vehiculo: VehiculoDTO, datos_editables: Dict[str, str], tipo: str
    ) -> Dict[str, str]:
        """
        Combina los datos automáticos del vehículo con los campos editables
        y prepara el diccionario final para la plantilla.
        """
        datos = {
            "nombre_propietario": vehiculo.nombre_propietario or "",
            "documento": vehiculo.documento_propietario or "",
            "placa": vehiculo.placa or "",
            "marca": vehiculo.marca or "",
            "modelo": vehiculo.modelo or "",
            "clase": vehiculo.clase or "",
            "fecha_afiliacion": vehiculo.fecha_afiliacion or "",
            "numero_motor": vehiculo.numero_interno or "N/A",
        }

        # Agregar campos editables; si hay fecha vacía, usar fecha actual
        hoy = datetime.now().strftime("%d/%m/%Y")
        for campo, valor in datos_editables.items():
            if "fecha" in campo.lower() and not valor.strip():
                datos[campo] = hoy
            else:
                datos[campo] = valor.strip() if valor else ""

        # Rellenar campos de fecha vacíos que vienen de la configuración
        config = self.config.get(tipo, {})
        for label, clave, valor_defecto in config.get("campos_editables", []):
            if clave not in datos:
                if "fecha" in clave.lower() and not valor_defecto:
                    datos[clave] = hoy
                else:
                    datos[clave] = valor_defecto if valor_defecto else ""

        return datos

    def generar_documento(
        self,
        tipo: str,
        vehiculo: VehiculoDTO,
        datos_editables: Dict[str, str],
        ruta_salida: str,
    ) -> Tuple[bool, str]:
        """
        Genera el documento Word y registra en el historial.

        Returns:
            Tupla (éxito, mensaje). Si éxito, el mensaje es la ruta del archivo generado.
        """
        config = self.config.get(tipo)
        if not config:
            return False, "Tipo de documento no válido."

        # Preparar datos combinados
        datos = self.preparar_datos_plantilla(vehiculo, datos_editables, tipo)

        # Ruta de la plantilla
        base_dir = Path(__file__).resolve().parent.parent
        ruta_plantilla = base_dir / "assets" / "templates" / config["plantilla"]

        try:
            # Generar documento físico
            salida_path = Path(ruta_salida)
            ruta_generada = generar_documento(ruta_plantilla, salida_path, datos)

            # Registrar en historial
            registro = DocumentoGeneradoDTO(
                tipo_documento=tipo,
                placa_vehiculo=vehiculo.placa,
                ruta_archivo=str(ruta_generada),
            )
            self.documento_repo.insertar(registro)

            return True, str(ruta_generada)
        except FileNotFoundError as e:
            return False, f"No se encontró la plantilla: {e}"
        except Exception as e:
            return False, f"Error al generar el documento: {str(e)}"

    def obtener_historial(self) -> List[DocumentoGeneradoDTO]:
        """Devuelve el historial de documentos generados."""
        return self.documento_repo.obtener_todos()