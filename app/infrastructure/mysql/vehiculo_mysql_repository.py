from app.infrastructure.mysql.mysql_connection import get_connection


class VehiculoMySQLRepository:

    def buscar_por_placa(self, placa):
        print("\n==============================")
        print("ENTRÓ A buscar_por_placa()")
        print("placa:", placa)
        print("==============================")

        conexion = get_connection()

        try:
            with conexion.cursor() as cursor:

                cursor.execute("""
                    SELECT
                        v.vehiculo_id,
                        v.placa,
                        v.interno,
                        v.modelo,
                        v.num_motor,
                        v.num_chasis,
                        v.num_serie,
                        v.vin_serie,
                        v.f_matricula,
                        v.capacidad,
                        '' AS tipo,
                        cb.nombre AS combustible,
                        '' AS modalidad,

                        m.nombre AS marca,
                        cv.nombre AS clase,
                        r.nombre AS ruta,
                        c.nombre AS color,
                        ca.nombre AS carroceria,
                        s.nombre AS servicio,

                        p.nombre,
                        p.num_documento,
                        p.direccion,
                        p.telefono,
                        p.celular,
                        p.email,

                        mt.nombre AS motorista_nombre,
                        mt.num_documento AS motorista_documento,
                        mt.celular AS motorista_celular,
                        mt.direccion AS motorista_direccion,
                        mt.email AS motorista_email

                    FROM vehiculo v

                    LEFT JOIN propietario p
                        ON v.propietario_id = p.propietario_id

                    LEFT JOIN marca m
                        ON v.marca_id = m.marca_id

                    LEFT JOIN clasevehi cv
                        ON v.clasevehi_id = cv.clasevehi_id

                    LEFT JOIN ruta r
                        ON v.ruta_id = r.ruta_id

                    LEFT JOIN color c
                        ON v.color_id = c.color_id

                    LEFT JOIN carroceria ca
                        ON v.carroceria_id = ca.carroceria_id

                    LEFT JOIN servicio s
                        ON v.servicio_id = s.servicio_id

                    LEFT JOIN combustible cb
                        ON v.combustible_id = cb.combustible_id

                    LEFT JOIN motorista mt
                        ON v.motorista_id = mt.motorista_id

                    WHERE v.placa = %s
                """, (placa,))

                resultado = cursor.fetchone()
                print("\nResultado obtenido:")
                print(resultado)

                if resultado:
                    print("Cantidad de columnas:", len(resultado))

                if not resultado:
                    return None

                return {
                    "vehiculo_id": resultado[0],
                    "placa": resultado[1],
                    "interno": resultado[2],
                    "modelo": resultado[3],
                    "motor": resultado[4],
                    "chasis": resultado[5],
                    "serie": resultado[6],
                    "vin": resultado[7],
                    "fecha_matricula": resultado[8],
                    "capacidad": resultado[9],
                    "tipo": resultado[10],
                    "combustible": resultado[11],
                    "modalidad": resultado[12],
                    "marca": resultado[13],
                    "clase": resultado[14],
                    "ruta": resultado[15],
                    "color": resultado[16],
                    "carroceria": resultado[17],
                    "servicio": resultado[18],
                    "propietario": resultado[19],
                    "documento": resultado[20],
                    "direccion": resultado[21],
                    "telefono": resultado[22],
                    "celular": resultado[23],
                    "email": resultado[24],
                    "nombre_conductor": resultado[25],
                    "documento_conductor": resultado[26],
                    "celular_conductor": resultado[27],
                    "direccion_conductor": resultado[28],
                    "correo_conductor": resultado[29]
                }

        finally:
            conexion.close()

    def listar_vehiculos(self):
        conexion = get_connection()

        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        v.vehiculo_id,
                        v.placa,
                        v.interno,
                        p.nombre AS nombre_propietario,
                        p.num_documento AS documento_propietario
                    FROM vehiculo v
                    LEFT JOIN propietario p
                        ON v.propietario_id = p.propietario_id
                    ORDER BY v.placa
                """)

                resultados = cursor.fetchall()

                return [
                    {
                        "vehiculo_id": fila[0],
                        "placa": fila[1],
                        "interno": fila[2],
                        "nombre_propietario": fila[3],
                        "documento_propietario": fila[4]
                    }
                    for fila in resultados
                ]

        finally:
            conexion.close()

    def buscar_por_id(self, vehiculo_id):
        print("\n==============================")
        print("ENTRÓ A buscar_por_id()")
        print("vehiculo_id:", vehiculo_id)
        print("==============================")

        conexion = get_connection()

        try:
            with conexion.cursor() as cursor:

                cursor.execute("""
                    SELECT
                        v.vehiculo_id,
                        v.placa,
                        v.interno,
                        v.modelo,
                        v.num_motor,
                        v.num_chasis,
                        v.num_serie,
                        v.vin_serie,
                        v.f_matricula,
                        v.capacidad,
                        '' AS tipo,
                        cb.nombre AS combustible,
                        '' AS modalidad,

                        m.nombre AS marca,
                        cv.nombre AS clase,
                        r.nombre AS ruta,
                        c.nombre AS color,
                        ca.nombre AS carroceria,
                        s.nombre AS servicio,

                        p.nombre,
                        p.num_documento,
                        p.direccion,
                        p.telefono,
                        p.celular,
                        p.email,

                        mt.nombre AS motorista_nombre,
                        mt.num_documento AS motorista_documento,
                        mt.celular AS motorista_celular,
                        mt.direccion AS motorista_direccion,
                        mt.email AS motorista_email

                    FROM vehiculo v

                    LEFT JOIN propietario p
                        ON v.propietario_id = p.propietario_id

                    LEFT JOIN marca m
                        ON v.marca_id = m.marca_id

                    LEFT JOIN clasevehi cv
                        ON v.clasevehi_id = cv.clasevehi_id

                    LEFT JOIN ruta r
                        ON v.ruta_id = r.ruta_id

                    LEFT JOIN color c
                        ON v.color_id = c.color_id

                    LEFT JOIN carroceria ca
                        ON v.carroceria_id = ca.carroceria_id

                    LEFT JOIN servicio s
                        ON v.servicio_id = s.servicio_id

                    LEFT JOIN combustible cb
                        ON v.combustible_id = cb.combustible_id

                    LEFT JOIN motorista mt
                        ON v.motorista_id = mt.motorista_id

                    WHERE v.vehiculo_id = %s
                """, (vehiculo_id,))

                resultado = cursor.fetchone()

                if not resultado:
                    return None

                return {
                    "vehiculo_id": resultado[0],
                    "placa": resultado[1],
                    "interno": resultado[2],
                    "modelo": resultado[3],
                    "motor": resultado[4],
                    "chasis": resultado[5],
                    "serie": resultado[6],
                    "vin": resultado[7],
                    "fecha_matricula": resultado[8],
                    "capacidad": resultado[9],
                    "tipo": resultado[10],
                    "combustible": resultado[11],
                    "modalidad": resultado[12],
                    "marca": resultado[13],
                    "clase": resultado[14],
                    "ruta": resultado[15],
                    "color": resultado[16],
                    "carroceria": resultado[17],
                    "servicio": resultado[18],
                    "propietario": resultado[19],
                    "documento": resultado[20],
                    "direccion": resultado[21],
                    "telefono": resultado[22],
                    "celular": resultado[23],
                    "email": resultado[24],
                    "nombre_conductor": resultado[25],
                    "documento_conductor": resultado[26],
                    "celular_conductor": resultado[27],
                    "direccion_conductor": resultado[28],
                    "correo_conductor": resultado[29]
                }

        finally:
            conexion.close()