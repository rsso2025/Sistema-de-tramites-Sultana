from app.services.vehiculo_mysql_service import VehiculoMySQLService

service = VehiculoMySQLService()

vehiculo = service.buscar_por_id(3)

if vehiculo:
    print("=" * 50)
    print("DATOS DEL VEHÍCULO")
    print("=" * 50)

    print("Placa:", vehiculo.placa)
    print("Marca:", vehiculo.marca)
    print("Modelo:", vehiculo.modelo)
    print("Clase:", vehiculo.clase)
    print("Número interno:", vehiculo.numero_interno)

    print()

    print("=" * 50)
    print("PROPIETARIO")
    print("=" * 50)

    print("Nombre:", vehiculo.nombre_propietario)
    print("Documento:", vehiculo.documento_propietario)
    print("Ciudad expedición:", vehiculo.ciudad_expedicion)   # <-- Línea agregada
    print("Teléfono:", vehiculo.telefono_propietario)
    print("Dirección:", vehiculo.direccion_propietario)

    print()

    print("=" * 50)
    print("CONDUCTOR")
    print("=" * 50)

    print("Nombre:", vehiculo.nombre_conductor)
    print("Documento:", vehiculo.documento_conductor)
    print("Celular:", vehiculo.celular_conductor)
    print("Dirección:", vehiculo.direccion_conductor)
    print("Correo:", vehiculo.correo_conductor)

else:
    print("No se encontró vehículo con ID 3.")