# Base de datos para PFO 3 - Almacenamiento (simula almacenamiento distribuido)

import sqlite3
from datetime import datetime
from config import DB_NOMBRE

class Database:
    def __init__(self, db_name=DB_NOMBRE):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        """Inicializa la base de datos"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mensajes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT,
                    contenido TEXT NOT NULL,
                    fecha_envio TEXT NOT NULL,
                    ip_cliente TEXT NOT NULL,
                    procesado_por TEXT,
                    fecha_procesado TEXT
                )
            """)
            conn.commit()
            conn.close()
            print(f"[DB] Base de datos inicializada: {self.db_name}")
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            raise
    
    def save_message(self, task_id: str, contenido: str, ip_cliente: str, worker_id: str = None):
        """Guarda un mensaje/tarea procesada"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO mensajes 
                   (task_id, contenido, fecha_envio, ip_cliente, procesado_por, fecha_procesado) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (task_id, contenido, datetime.now().isoformat(), ip_cliente, worker_id, datetime.now().isoformat())
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"[DB ERROR] No se pudo guardar: {e}")
            return False
    
    def get_all_messages(self):
        """Obtiene todos los mensajes"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mensajes ORDER BY id DESC")
            rows = cursor.fetchall()
            conn.close()
            return rows
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            return []
