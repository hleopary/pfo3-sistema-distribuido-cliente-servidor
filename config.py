# Configuración para PFO 3 - Sistema Distribuido

# Dispatcher (Balanceador/Recepción)
DISPATCHER_HOST = "localhost"
DISPATCHER_PORT = 5001

# Workers
WORKER_COUNT = 4  # Cantidad de workers en el pool de hilos

# Base de datos (almacenamiento - simula almacenamiento distribuido)
DB_NOMBRE = "mensajes_pfo3.db"

# Tamaño del buffer para sockets
BUFFER_SIZE = 4096

# Tiempo de espera para shutdown
SHUTDOWN_TIMEOUT = 2
