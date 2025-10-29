✈️ Sistema de Gestión y Recomendación de Viajes

Bases de Datos: Neo4j + MongoDB + Redis (Docker + Python + JupyterLab)

Este proyecto implementa un sistema distribuido que integra bases de datos relacionales y no relacionales para modelar un Sistema de Gestión y Recomendación de Viajes.
Permite almacenar información de usuarios, destinos, hoteles, actividades y reservas, además de generar recomendaciones personalizadas y estadísticas utilizando Neo4j, MongoDB y Redis.

🚀 Requisitos

Docker Desktop
 (Windows/Mac) o Docker Engine (Linux)

docker compose (v2+)

Navegador web para acceder a JupyterLab y Neo4j Browser

💡 En Windows, si usás WSL2, asegurate de que Docker Desktop tenga activado el backend WSL.

🧩 Servicios
Servicio	Descripción	Acceso
python	Contenedor con JupyterLab y librerías (neo4j, pymongo, redis, matplotlib, pandas, etc.)	http://localhost:8888
neo4j	Base de datos de grafos para modelar relaciones sociales y de viajes	http://localhost:7474 (Browser) / bolt://localhost:7687
mongo	Base documental para almacenar usuarios, destinos, hoteles, actividades y reservas	mongodb://<user>:<pass>@localhost:27017/
redis	Base en memoria para manejar búsquedas recientes, sesiones activas y reservas temporales	redis://:<password>@localhost:6379
🔒 Variables de entorno

Editables en docker/.env (o copiando .env.example):

NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j123
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=admin123
MONGO_INITDB_DATABASE=viajes
REDIS_PASSWORD=redis123


Para empezar rápido:

cp docker/.env.example docker/.env

▶️ Levantar el entorno

Desde la raíz del proyecto:

docker compose -f docker/docker-compose.yml up -d --build


La primera ejecución descargará las imágenes necesarias y construirá el entorno completo.

⏹️ Apagar y limpiar contenedores
docker compose down


Para eliminar también los volúmenes (datos persistentes):

docker compose down -v

🧠 Estructura del proyecto
📦 sistema-viajes/
│
├── 🧠 notebooks/
│   └── Notebook_Principal.ipynb       # Ejecución principal del TP
│   └── data/
│       ├── usuarios.json
│       ├── destinos.json
│       ├── hoteles.json
│       ├── actividades.json
│       ├── reservas.json
│       ├── relaciones_sociales.csv
│       └── visitas.csv
│
├── 🐳 docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── .env
│
├── 📜 scripts/
│   ├── config_paths.py
│   ├── funciones_comunes.py
│   ├── funciones_mongo.py
│   ├── funciones_neo4j.py
│   ├── funciones_redis.py
│
├── 📊 Otros/
│   └── consigna TP.pdf
│
├── 📘 README.md
└── .gitignore

🧩 Interacción entre archivos y servicios
                        ┌─────────────────────────┐
                        │Notebook_Principal.ipynb │
                        │   (orquestador general) │
                        └──────────┬──────────────┘
                                   │
                 ┌─────────────────┼────────────────────┐
                 │                 │                    │
      ┌──────────▼────────┐ ┌──────▼──────────┐ ┌───────▼─────────┐
      │ funciones_mongo.py│ │ funciones_neo4j │ │ funciones_redis │
      │ (CRUD + consultas)│ │ (nodos y rel.)  │ │(cache, sesiones)│
      └──────────┬────────┘ └────────┬────────┘ └────────┬────────┘
                 │                   │                   │
        ┌────────▼────────┐   ┌──────▼──────────┐ ┌──────▼────────┐
        │   MongoDB       │   │     Neo4j       │ │     Redis     │
        │ (colecciones)   │   │ (nodos y rel.)  │ │   (memoria)   │
        └─────────────────┘   └─────────────────┘ └───────────────┘
                 ▲                   ▲
                 │                   │
      ┌──────────┴──────────┐  ┌─────┴────────────┐
      │ funciones_comunes.py│  │ funciones_comunes│
      │ (lectura JSON/CSV)  │  │ (lectura CSV)    │
      │   JSON → MongoDB    │  │  CSV → Neo4j     │
      └─────────────────────┘  └──────────────────┘

🧪 Carga y consultas principales

El sistema implementa consultas integradas entre las tres bases, por ejemplo:

Usuarios que visitaron Bariloche (Neo4j)

Amigos de un usuario que compartieron destinos (Neo4j + MongoDB)

Recomendaciones basadas en amigos y destinos no visitados (Neo4j + Redis)

Hoteles y actividades en destinos sugeridos (MongoDB)

Usuarios conectados actualmente (Redis)

Estadísticas gráficas:

Destino más visitado

Hotel más económico

Actividad más popular