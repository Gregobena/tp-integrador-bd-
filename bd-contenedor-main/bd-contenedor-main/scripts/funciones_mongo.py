from pymongo import MongoClient
import os
from dotenv import load_dotenv

# === Cargar variables de entorno desde /docker/.env ===
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "docker", ".env"))

# === Conexión a MongoDB ===
MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME", "admin")
MONGO_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "admin123")
MONGO_HOST = os.getenv("MONGO_HOST", "mongo")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB = os.getenv("MONGO_INITDB_DATABASE", "viajes")

# Crear cliente y base
client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/")
db = client[MONGO_DB]

# === Crear índices únicos (para evitar duplicados) ===
def crear_indices():
    """
    Crea índices únicos en los campos clave de las colecciones principales.
    Evita que se inserten documentos repetidos (por ejemplo, usuario_id duplicados).
    """
    try:
        db.usuarios.create_index("usuario_id", unique=True)
        db.destinos.create_index("destino_id", unique=True)
        db.hoteles.create_index("hotel_id", unique=True)
        db.actividades.create_index("actividad_id", unique=True)
        db.reservas.create_index("reserva_id", unique=True)
        print("✅ Índices creados o ya existentes.")
    except Exception as e:
        print("⚠️ Error al crear índices:", e)


# Ejecutar creación de índices al importar el módulo
crear_indices()

# === Funciones de gestión de datos ===

def insertar_documento(coleccion, documento):
    """
    Inserta un documento en una colección de MongoDB.
    """
    try:
        db[coleccion].insert_one(documento)
    except Exception as e:
        print(f"⚠️ Error al insertar en '{coleccion}': {e}")


def insertar_varios_documentos(coleccion, lista_documentos):
    """
    Inserta varios documentos en una colección.
    Si hay duplicados (por clave única), los ignora y continúa.
    """
    if not lista_documentos:
        print(f"[ADVERTENCIA] Lista vacía: no se insertaron documentos en '{coleccion}'")
        return
    try:
        db[coleccion].insert_many(lista_documentos, ordered=False)  # 'ordered=False' para que no falle con duplicados
    except Exception as e:
        print(f"⚠️ Error al insertar varios en '{coleccion}': {e}")


def obtener_todos(coleccion):
    """
    Devuelve todos los documentos de una colección.
    """
    return list(db[coleccion].find())


def eliminar_todos(coleccion):
    """
    Elimina todos los documentos de una colección.
    Útil para reiniciar una base antes de una nueva carga.
    """
    resultado = db[coleccion].delete_many({})
    print(f"🗑️ Eliminados {resultado.deleted_count} documentos de '{coleccion}'.")


def probar_conexion():
    """
    Verifica si la conexión con MongoDB es exitosa.
    """
    try:
        db.list_collection_names()
        print("✅ Conexión a MongoDB exitosa.")
        return True
    except Exception as e:
        print("❌ Error al conectar con MongoDB:", e)
        return False
