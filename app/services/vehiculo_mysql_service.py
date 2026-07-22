from app.infrastructure.mysql.vehiculo_mysql_repository import VehiculoMySQLRepository
from app.core.entities import VehiculoDTO


class VehiculoMySQLService:

    def __init__(self):
        self.repo = VehiculoMySQLRepository()

    def _mapear_dto(self, datos):
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
            fecha_afiliacion=datos["fecha_afiliacion"] or "",
            motor=datos["motor"] or "",
            chasis=datos["chasis"] or "",
            serie=datos["serie"] or "",
            vin=datos["vin"] or "",
            fecha_matricula=datos["fecha_matricula"] or "",
            capacidad=datos["capacidad"] or "",
            tipo=datos["tipo"] or "",
            combustible=datos["combustible"] or "",
            modalidad=datos["modalidad"] or "",
            ruta=datos["ruta"] or "",
            color=datos["color"] or "",
            carroceria=datos["carroceria"] or "",
            servicio=datos["servicio"] or "",

            documento_propietario=str(datos["documento"]) if datos["documento"] else "",
            nombre_propietario=datos["propietario"] or "",
            ciudad_expedicion=datos["ciudad_expedicion"] or "",
            telefono_propietario=datos["telefono"] or "",
            direccion_propietario=datos["direccion"] or "",

            nombre_conductor=datos["nombre_conductor"] or "",
            documento_conductor=str(datos["documento_conductor"]) if datos["documento_conductor"] else "",
            celular_conductor=datos["celular_conductor"] or "",
            direccion_conductor=datos["direccion_conductor"] or "",
            correo_conductor=datos["correo_conductor"] or ""
        )

    def buscar_por_placa(self, placa):

        placa = placa.strip().upper()

        if not placa:
            return None

        datos = self.repo.buscar_por_placa(placa)
        return self._mapear_dto(datos)

    def listar_vehiculos(self):
        return self.repo.listar_vehiculos()

    def buscar_por_id(self, vehiculo_id):

        datos = self.repo.buscar_por_id(vehiculo_id)
        return self._mapear_dto(datos)

    def obtener_vehiculo_prueba(self):
        return self.buscar_por_placa("CBD745")
