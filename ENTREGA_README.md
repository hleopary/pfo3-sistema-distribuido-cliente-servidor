# Entrega PFO 3 - Rediseño como Sistema Distribuido (Cliente-Servidor)

**Materia:** Programación sobre Redes  
**Alumno:** Leandro Paryszewski  
**Fecha:** 27/10/2026

## Objetivo
Transformar el sistema del PFO 1 (chat con sockets + SQLite) a una arquitectura distribuida cliente-servidor.

## Contenido de la entrega

- **Código fuente:** Carpeta [`pfo3_sistema_distribuido/`](./pfo3_sistema_distribuido/)
- **Diagrama del sistema:** [PFO3_DIAGRAMA.md](./PFO3_DIAGRAMA.md) (incluye todos los componentes solicitados: clientes, balanceador de carga, servidores workers, cola de mensajes, almacenamiento distribuido)
- **Diagrama dentro del proyecto:** [`pfo3_sistema_distribuido/DIAGRAMA.md`](./pfo3_sistema_distribuido/DIAGRAMA.md)
- **Documentación:** [`pfo3_sistema_distribuido/README.md`](./pfo3_sistema_distribuido/README.md)

## Arquitectura implementada

La solución rediseña el sistema con:
- **Clientes** - Se conectan al dispatcher vía sockets TCP
- **Dispatcher/Balanceador** - Punto de entrada, distribuye tareas mediante cola
- **Cola de mensajes** - `queue.Queue()` desacoplando componentes (simula RabbitMQ)
- **Workers con pool de hilos** - Múltiples workers procesando concurrentemente (`threading`)
- **Almacenamiento** - SQLite compartido (simula PostgreSQL/S3)

## Cómo ejecutar

```bash
# Terminal 1 - Iniciar dispatcher con workers
cd pfo3_sistema_distribuido
python dispatcher.py

# Terminal 2 - Iniciar cliente
cd pfo3_sistema_distribuido
python client.py
```

## Repositorio GitHub
https://github.com/hleopary/pfo3-sistema-distribuido-cliente-servidor
