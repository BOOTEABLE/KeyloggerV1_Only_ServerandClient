import socket
import sys
import threading

class Servidor:
    def __init__(self, ipserver, puertoserver):
        self.ipserver = ipserver
        self.puertoserver = puertoserver

    def conectar(self):
        socketAbierto = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketAbierto.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            socketAbierto.bind((self.ipserver, self.puertoserver))
        except socket.error as message:
            print(f"Error: {message}")
            sys.exit()
        socketAbierto.listen(5)
        print(f"Escuchando en puerto {self.puertoserver}...")
        connection, address = socketAbierto.accept()
        print(f"Conectado con: {address}")
        return connection

def recibir_datos(conexion):
    while True:
        try:
            recibido = conexion.recv(1024).decode()
            if not recibido or recibido.lower() == "exit":
                print("\nEl cliente cerró la conexión.")
                break
            print(f"\n[Cliente]: {recibido}\nSVR >> ", end="")
        except:
            break

if __name__ == "__main__":
    servidor = Servidor("localhost", 9999)
    conexion = servidor.conectar()

    # Hilo para recibir mensajes del cliente (mensajes o teclas)
    threading.Thread(target=recibir_datos, args=(conexion,), daemon=True).start()

    # Bucle para que el servidor le escriba al cliente
    while True:
        try:
            msg = input("SVR >> ")
            conexion.send(msg.encode())
        except KeyboardInterrupt:
            break
    conexion.close()