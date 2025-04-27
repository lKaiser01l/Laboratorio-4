import grpc
import saludo_pb2
import saludo_pb2_grpc

def run():
    canal = grpc.insecure_channel('localhost:50051')
    stub = saludo_pb2_grpc.SaludoServiceStub(canal)

    nombre = input("Ingresa tu nombre: ")

    request = saludo_pb2.SaludoRequest(nombre=nombre)
    response = stub.Saludar(request)

    print(response.mensaje)

if __name__ == "__main__":
    run()
    