from app.services.vehiculo_mysql_service import VehiculoMySQLService

service = VehiculoMySQLService()

vehiculo = service.buscar_por_id(3)

if vehiculo:
    print("Placa:", vehiculo.placa)
    print("Marca:", vehiculo.marca)
    print("Clase:", vehiculo.clase)
    print("Propietario:", vehiculo.nombre_propietario)
    print("Documento:", vehiculo.documento_propietario)
else:
    print("No se encontró vehículo con ID 3.")
    