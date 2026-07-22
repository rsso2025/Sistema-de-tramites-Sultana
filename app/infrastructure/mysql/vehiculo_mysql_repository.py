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
                        v.f_ingreso,
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
                        cd.nombre AS ciudad_expedicion,
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

                    LEFT JOIN ciudad cd
                        ON p.lugar_docu = cd.ciudad_id

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
                    "fecha_afiliacion": resultado[9],
                    "capacidad": resultado[10],
                    "tipo": resultado[11],
                    "combustible": resultado[12],
                    "modalidad": resultado[13],
                    "marca": resultado[14],
                    "clase": resultado[15],
                    "ruta": resultado[16],
                    "color": resultado[17],
                    "carroceria": resultado[18],
                    "servicio": resultado[19],
                    "propietario": resultado[20],
                    "documento": resultado[21],
                    "ciudad_expedicion": resultado[22],
                    "direccion": resultado[23],
                    "telefono": resultado[24],
                    "celular": resultado[25],
                    "email": resultado[26],
                    "nombre_conductor": resultado[27],
                    "documento_conductor": resultado[28],
                    "celular_conductor": resultado[29],
                    "direccion_conductor": resultado[30],
                    "correo_conductor": resultado[31]
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
                        v.f_ingreso,
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
                        cd.nombre AS ciudad_expedicion,
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

                    LEFT JOIN ciudad cd
                        ON p.lugar_docu = cd.ciudad_id

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

                # ===== LÍNEAS AGREGADAS TEMPORALMENTE =====
                print("\nResultado obtenido:")
                print(resultado)
                if resultado:
                    print("Ciudad expedición SQL:", resultado[22])
                # ===========================================

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
                    "fecha_afiliacion": resultado[9],
                    "capacidad": resultado[10],
                    "tipo": resultado[11],
                    "combustible": resultado[12],
                    "modalidad": resultado[13],
                    "marca": resultado[14],
                    "clase": resultado[15],
                    "ruta": resultado[16],
                    "color": resultado[17],
                    "carroceria": resultado[18],
                    "servicio": resultado[19],
                    "propietario": resultado[20],
                    "documento": resultado[21],
                    "ciudad_expedicion": resultado[22],
                    "direccion": resultado[23],
                    "telefono": resultado[24],
                    "celular": resultado[25],
                    "email": resultado[26],
                    "nombre_conductor": resultado[27],
                    "documento_conductor": resultado[28],
                    "celular_conductor": resultado[29],
                    "direccion_conductor": resultado[30],
                    "correo_conductor": resultado[31]
                }

        finally:
            conexion.close()