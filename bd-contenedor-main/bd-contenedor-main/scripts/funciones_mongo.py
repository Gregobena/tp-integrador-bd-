# scripts/funciones_mongo.py
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

# Crear cliente
client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/")
db = client[MONGO_DB]

# === Funciones ===

def insertar_documento(coleccion, documento):
    """
    Inserta un documento en una colección de MongoDB.
    """
    db[coleccion].insert_one(documento)


def insertar_varios_documentos(coleccion, lista_documentos):
    """
    Inserta varios documentos en una colección.
    """
    if not lista_documentos:
        print(f"[ADVERTENCIA] Lista vacía: no se insertaron documentos en '{coleccion}'")
        return
    db[coleccion].insert_many(lista_documentos)


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
    print(f"Eliminados {resultado.deleted_count} documentos de '{coleccion}'.")


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