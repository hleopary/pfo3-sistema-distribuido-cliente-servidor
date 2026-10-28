# Worker - Procesador de tareas con hilos

import threading
import time
from datetime import datetime
from db import Database

class Worker:
    def __init__(self, worker_id: int, task_queue, result_dict, db: Database):
        self.worker_id = worker_id
        self.task_queue = task_queue
        self.result_dict = result_dict
        self.db = db
        self.running = True
        self.thread = threading.Thread(target=self.run, daemon=True, name=f"Worker-{worker_id}")
    
    def start(self):
        self.thread.start()
        print(f"[WORKER-{self.worker_id}] Iniciado")
    
    def stop(self):
        self.running = False
    
    def run(self):
        """Procesa tareas de la cola"""
        while self.running:
            try:
                # Obtener tarea de la cola (bloqueante con timeout)
                task = self.task_queue.get(timeout=1)
                if task is None:  # Señal de parada
                    break
                
                task_id = task['task_id']
                content = task['content']
                client_addr = task['client_addr']
                
                print(f"[WORKER-{self.worker_id}] Procesando tarea {task_id} desde {client_addr}")
                
                # Simular procesamiento
                time.sleep(0.1)
                
                # Guardar en base de datos (almacenamiento)
                ip_cliente = client_addr[0] if isinstance(client_addr, tuple) else str(client_addr)
                self.db.save_message(task_id, content, ip_cliente, f"Worker-{self.worker_id}")
                
                # Generar respuesta
                result = f"Procesado por Worker-{self.worker_id} | Mensaje: '{content}' | Timestamp: {datetime.now().isoformat(timespec='seconds')}"
                
                # Almacenar resultado
                self.result_dict[task_id] = {
                    'status': 'OK',
                    'result': result,
                    'worker_id': self.worker_id
                }
                
                self.task_queue.task_done()
                print(f"[WORKER-{self.worker_id}] Tarea {task_id} completada")
                
            except Exception as e:
                if self.running:
                    print(f"[WORKER-{self.worker_id}] Error: {e}")
                continue
