from app.infrastructure.mysql.vehiculo_mysql_repository import VehiculoMySQLRepository
from app.core.entities import VehiculoDTO


class VehiculoMySQLService:

    def __init__(self):
        self.repo = VehiculoMySQLRepository()

    def buscar_por_placa(self, placa):

        placa = placa.strip().upper()

        if not placa:
            return None

        datos = self.repo.buscar_por_placa(placa)

        if not datos:
            return None

        return VehiculoDTO(
            id=datos["vehiculo_id"],
            placa=datos["placa"],
            propietario_id=0,
            numero_interno=str(datos["interno"]) if datos["interno"] else "",
            marca=datos["marca"] or "",
            modelo=str(datos["modelo"]) if datos["modelo"] else "",
            clase=datos["clase"] or "",
            fecha_afiliacion="",

            documento_propietario=str(datos["documento"]) if datos["documento"] else "",
            nombre_propietario=datos["propietario"] or "",
            telefono_propietario=datos["telefono"] or "",
            direccion_propietario=datos["direccion"] or ""
        )

    def obtener_vehiculo_prueba(self):
        return self.buscar_por_placa("CBD745")