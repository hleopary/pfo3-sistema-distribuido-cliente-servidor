# Dispatcher / Balanceador de Carga
# Recibe conexiones de clientes, distribuye tareas a workers mediante cola

import socket
import threading
import queue
import uuid
import time
from concurrent.futures import ThreadPoolExecutor
from config import DISPATCHER_HOST, DISPATCHER_PORT, WORKER_COUNT, BUFFER_SIZE
from protocol import encode_message, decode_messages, Task
from worker import Worker
from db import Database

class Dispatcher:
    def __init__(self):
        self.host = DISPATCHER_HOST
        self.port = DISPATCHER_PORT
        self.task_queue = queue.Queue()
        self.result_dict = {}
        self.db = Database()
        self.workers = []
        self.running = False
        self.server_socket = None
        
    def start_workers(self):
        """Inicia pool de workers con hilos"""
        print(f"[DISPATCHER] Iniciando {WORKER_COUNT} workers...")
        for i in range(WORKER_COUNT):
            worker = Worker(i+1, self.task_queue, self.result_dict, self.db)
            worker.start()
            self.workers.append(worker)
        print(f"[DISPATCHER] {WORKER_COUNT} workers activos con pool de hilos")
    
    def start(self):
        """Inicia el dispatcher (balanceador)"""
        self.running = True
        self.start_workers()
        
        # Crear socket del dispatcher
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(10)  # Permite múltiples clientes
            print(f"[DISPATCHER] Balanceador escuchando en {self.host}:{self.port}")
            print(f"[DISPATCHER] Arquitectura distribuida activa")
            print("=" * 60)
            
            while self.running:
                try:
                    client_socket, client_addr = self.server_socket.accept()
                    print(f"[DISPATCHER] Cliente conectado desde {client_addr}")
                    # Atender cliente en un hilo
                    thread = threading.Thread(target=self.handle_client, args=(client_socket, client_addr), daemon=True)
                    thread.start()
                except OSError:
                    if self.running:
                        print("[DISPATCHER] Error al aceptar conexión")
                    break
                    
        except Exception as e:
            print(f"[DISPATCHER ERROR] {e}")
        finally:
            self.shutdown()
    
    def handle_client(self, client_socket, client_addr):
        """Maneja la conexión con un cliente"""
        buffer = ""
        try:
            while True:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                buffer += data.decode('utf-8')
                
                messages, buffer = decode_messages(buffer)
                for msg in messages:
                    if msg.get('type') == 'TASK':
                        task_id = msg.get('task_id') or str(uuid.uuid4())
                        content = msg.get('content', '')
                        
                        print(f"[DISPATCHER] Recibida tarea {task_id} de {client_addr}: '{content}'")
                        
                        # Enviar tarea a la cola de mensajes para distribuir a workers
                        task = Task.create_task(task_id, content, client_addr)
                        self.task_queue.put(task)
                        print(f"[DISPATCHER] Tarea {task_id} en cola, distribuyendo a workers...")
                        
                        # Esperar resultado del worker
                        timeout = 10
                        start_wait = time.time()
                        while task_id not in self.result_dict and (time.time() - start_wait) < timeout:
                            time.sleep(0.01)
                        
                        if task_id in self.result_dict:
                            res = self.result_dict.pop(task_id)
                            response = Task.create_response(task_id, res['result'], res['status'])
                            client_socket.sendall(encode_message(response))
                            print(f"[DISPATCHER] Resultado enviado a {client_addr}")
                        else:
                            response = Task.create_response(task_id, "ERROR: Timeout", "ERROR")
                            client_socket.sendall(encode_message(response))
                    elif msg.get('type') == 'QUIT':
                        break
                        
        except Exception as e:
            print(f"[DISPATCHER] Error con cliente {client_addr}: {e}")
        finally:
            try:
                client_socket.close()
                print(f"[DISPATCHER] Conexión cerrada con {client_addr}")
            except:
                pass
    
    def shutdown(self):
        """Apaga el dispatcher y workers"""
        print("\n[DISPATCHER] Cerrando sistema distribuido...")
        self.running = False
        # Enviar señal de parada a workers
        for _ in self.workers:
            self.task_queue.put(None)
        if self.server_socket:
            self.server_socket.close()
        print("[DISPATCHER] Sistema detenido")

if __name__ == "__main__":
    dispatcher = Dispatcher()
    try:
        dispatcher.start()
    except KeyboardInterrupt:
        print("\n[DISPATCHER] Detenido por el usuario")
        dispatcher.shutdown()
