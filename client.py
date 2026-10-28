# Cliente para PFO 3 - Sistema Distribuido Cliente-Servidor
# Envía tareas al dispatcher y recibe resultados

import socket
import uuid
from config import DISPATCHER_HOST, DISPATCHER_PORT, BUFFER_SIZE
from protocol import encode_message, decode_messages, Task

class Client:
    def __init__(self):
        self.host = DISPATCHER_HOST
        self.port = DISPATCHER_PORT
        self.socket = None
        self.buffer = ""
    
    def connect(self):
        """Conecta al dispatcher (balanceador)"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, self.port))
            print(f"[CLIENTE] Conectado al Dispatcher/Balanceador {self.host}:{self.port}")
            print(f"[CLIENTE] Sistema Distribuido Cliente-Servidor")
            print("=" * 50)
            return True
        except Exception as e:
            print(f"[ERROR] No se pudo conectar: {e}")
            print(f"[INFO] Asegurate de que el dispatcher esté corriendo: python dispatcher.py")
            return False
    
    def send_task(self, content):
        """Envía una tarea al dispatcher"""
        task_id = str(uuid.uuid4())[:8]
        task = {
            'type': 'TASK',
            'task_id': task_id,
            'content': content
        }
        try:
            self.socket.sendall(encode_message(task))
            print(f"[CLIENTE] Tarea enviada [ID:{task_id}]: '{content}'")
            
            # Esperar respuesta
            self.buffer = ""
            while True:
                data = self.socket.recv(BUFFER_SIZE)
                if not data:
                    break
                self.buffer += data.decode('utf-8')
                messages, self.buffer = decode_messages(self.buffer)
                for msg in messages:
                    if msg.get('type') == 'RESPONSE' and msg.get('task_id') == task_id:
                        print(f"[CLIENTE] Respuesta recibida:")
                        print(f"           {msg.get('result')}")
                        print(f"           Status: {msg.get('status')}")
                        print("-" * 50)
                        return msg
            return None
        except Exception as e:
            print(f"[ERROR] {e}")
            return None
    
    def close(self):
        """Cierra la conexión"""
        if self.socket:
            try:
                self.socket.sendall(encode_message({'type': 'QUIT'}))
                self.socket.close()
            except:
                pass

if __name__ == "__main__":
    client = Client()
    if not client.connect():
        exit(1)
    
    try:
        while True:
            mensaje = input("\nEscribí tu tarea/mensaje (o 'éxito' para salir): ")
            if mensaje.lower() == "éxito":
                print("[CLIENTE] Cerrando conexión...")
                break
            if not mensaje.strip():
                continue
            client.send_task(mensaje.strip())
    except KeyboardInterrupt:
        print("\n[CLIENTE] Interrumpido por el usuario")
    finally:
        client.close()
        print("[CLIENTE] Desconectado")
