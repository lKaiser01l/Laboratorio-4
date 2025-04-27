import grpc
from concurrent import futures
import time
import saludo_pb2
import saludo_pb2_grpc
import psycopg2

# Datos de conexión
DB_HOST = "crossover.proxy.rlwy.net"
DB_NAME = "railway"
DB_USER = "postgres"
DB_PASS = "dYdXhVKkvBckpCaALFKYDenlFIprqfyC"
DB_PORT = "32985"

class SaludoServiceServicer(saludo_pb2_grpc.SaludoServiceServicer):
    def Saludar(self, request, context):
        nombre_buscar = request.nombre

        # Conectarse a PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        cur = conn.cursor()

        # Buscar el nombre en la tabla usuarios
        cur.execute("SELECT nombre, apellido FROM usuarios WHERE nombre = %s", (nombre_buscar,))
        resultado = cur.fetchone()

        mensaje = ""
        if resultado:
            nombre, apellido = resultado
            mensaje = f"¡Buen día, {nombre} {apellido}!"
        else:
            mensaje = "Nombre no encontrado."

        cur.close()
        conn.close()

        return saludo_pb2.SaludoResponse(mensaje=mensaje)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    saludo_pb2_grpc.add_SaludoServiceServicer_to_server(SaludoServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC escuchando en el puerto 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()