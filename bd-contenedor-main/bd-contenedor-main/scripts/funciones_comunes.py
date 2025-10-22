# Este archivo contiene funciones generales o compartidas por todo el sistema.
# No depende directamente de Mongo ni de Neo4j, sino que maneja cosas como archivos, rutas, formatos o transformaciones.

import json
import os
import csv
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

def cargar_csv(nombre_archivo):
    """
    Carga un archivo CSV desde la carpeta /data y devuelve una lista de diccionarios.
    Cada fila del CSV se convierte en un diccionario con los nombres de las columnas como claves.
    """
    ruta = os.path.join(DATA_DIR, nombre_archivo)
    with open(ruta, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)