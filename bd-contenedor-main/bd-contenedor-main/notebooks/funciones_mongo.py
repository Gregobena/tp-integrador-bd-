from pymongo import MongoClient
import os 

MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME", "admin")
MONGO_PASS = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "admin123")

client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASS}@mongo:27017/")
db = client["viajes"]

def insertar_documento(coleccion, documento):
    db[coleccion].insert_one(documento)
    
def insertar_varios_documentos(coleccion, lista_documentos):
    for elem in lista_documentos:
        db[coleccion].insert_one(elem)

        
        

