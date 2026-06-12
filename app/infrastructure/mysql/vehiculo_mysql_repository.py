from app.infrastructure.mysql.mysql_connection import get_connection


class VehiculoMySQLRepository:

    def buscar_por_placa(self, placa):
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
                        p.email

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

                    WHERE v.placa = %s
                """, (placa,))

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
                    "marca": resultado[9],
                    "clase": resultado[10],
                    "ruta": resultado[11],
                    "color": resultado[12],
                    "carroceria": resultado[13],
                    "servicio": resultado[14],
                    "propietario": resultado[15],
                    "documento": resultado[16],
                    "direccion": resultado[17],
                    "telefono": resultado[18],
                    "celular": resultado[19],
                    "email": resultado[20]
                }

        finally:
            conexion.close()