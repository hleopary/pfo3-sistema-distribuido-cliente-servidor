# Protocolo de comunicación para PFO 3

import json
from datetime import datetime

# Delimitador para mensajes
DELIMITER = '\n'

def encode_message(data: dict) -> bytes:
    """Codifica un mensaje dict a bytes con delimitador"""
    msg = json.dumps(data) + DELIMITER
    return msg.encode('utf-8')

def decode_messages(buffer: str) -> list:
    """Decodifica mensajes del buffer separados por delimitador"""
    messages = []
    while DELIMITER in buffer:
        idx = buffer.index(DELIMITER)
        msg_str = buffer[:idx]
        buffer = buffer[idx + len(DELIMITER):]
        if msg_str.strip():
            try:
                messages.append(json.loads(msg_str))
            except json.JSONDecodeError:
                pass
    return messages, buffer

class Task:
    """Representa una tarea a procesar"""
    @staticmethod
    def create_task(task_id: str, content: str, client_addr: tuple) -> dict:
        return {
            'type': 'TASK',
            'task_id': task_id,
            'content': content,
            'client_addr': client_addr,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def create_response(task_id: str, result: str, status: str = 'OK') -> dict:
        return {
            'type': 'RESPONSE',
            'task_id': task_id,
            'result': result,
            'status': status,
            'timestamp': datetime.now().isoformat()
        }
    
    @staticmethod
    def create_ack(message: str) -> dict:
        return {
            'type': 'ACK',
            'message': message
        }
