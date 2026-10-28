# PFO 3 - Rediseño como Sistema Distribuido (Cliente-Servidor)

**Alumno:** Leandro Paryszewski

## Objetivo
Transformar el sistema del PFO 1 (chat con sockets + SQLite) a una arquitectura distribuida cliente-servidor, aplicando los conceptos vistos en las clases 8-10.

## Arquitectura propuesta

El sistema se rediseña con los siguientes componentes:

- **Clientes** (móviles/web - simulados): se conectan al dispatcher y envían tareas/mensajes
- **Balanceador/Dispatcher**: recibe las conexiones de los clientes, valida y distribuye las tareas a los workers mediante una cola de mensajes
- **Cola de mensajes**: implementada con `queue.Queue()` para desacoplar el dispatcher de los workers (simulando RabbitMQ)
- **Servidores Workers**: cada worker corre en un hilo dentro de un pool de hilos (`threading.ThreadPoolExecutor`). Procesan las tareas, guardan en almacenamiento y devuelven resultado
- **Almacenamiento distribuido**: SQLite compartido (`mensajes.db`) - simula base distribuida, manteniendo compatibilidad con PFO 1

## Diagrama del sistema

Ver [DIAGRAMA.md](./DIAGRAMA.md) con la arquitectura completa (clientes, balanceador de carga, servidores workers con pool de hilos, cola de mensajes y almacenamiento distribuido).

## Estructura de archivos

```
pfo3_sistema_distribuido/
├── README.md
├── DIAGRAMA.md        # Diagrama del sistema
├── config.py          # Configuración (puertos, workers, etc.)
├── protocol.py        # Protocolo de comunicación
├── db.py              # Acceso a base de datos
├── dispatcher.py      # Balanceador/Dispatcher + cola + workers
├── worker.py          # Lógica de procesamiento de workers
└── client.py          # Cliente que envía tareas y recibe resultados
```

## Cómo ejecutar

### 1) Iniciar el Dispatcher (con workers)
```bash
python dispatcher.py
```
El dispatcher escuchará en `localhost:5001`, levantará el pool de workers y esperará conexiones de clientes.

### 2) Iniciar uno o más clientes
En otra terminal:
```bash
python client.py
```
Escribir mensajes/tareas y recibir el resultado. Escribir `éxito` para salir.

## Diferencias con PFO 1
- **Arquitectura distribuida**: separación entre recepción (dispatcher) y procesamiento (workers)
- **Concurrencia**: múltiples workers con pool de hilos procesando en paralelo
- **Cola de mensajes**: desacoplamiento entre componentes
- **Escalable**: se pueden levantar múltiples workers/instancias
- **Mismo dominio**: mantiene la funcionalidad de guardar mensajes en SQLite
