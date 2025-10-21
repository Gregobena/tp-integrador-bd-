# Este archivo contiene funciones generales o compartidas por todo el sistema.
# No depende directamente de Mongo ni de Neo4j, sino que maneja cosas como archivos, rutas, formatos o transformaciones.

import json
import os
from bson import ObjectId
from config_paths import DATA_DIR

# === Lectura de archivos ===

def cargar_json(nombre_archivo):
    """
    Lee un archivo JSON desde la carpeta /data y devuelve su contenido.
    Ejemplo: cargar_json("usuarios.json")
    """
    ruta = os.path.join(DATA_DIR, nombre_archivo)
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

# === Compatibilidad con Mongo ===

def convertir_objectid_a_str(documento):
    """
    Convierte ObjectId a string en documentos de MongoDB para compatibilidad con Neo4j.
    """
    for k, v in documento.items():
        if isinstance(v, ObjectId):
            documento[k] = str(v)
    return documento