import csv 
import ast 

def procesar_datos():
    with open("data.csv", "r",encoding='utf-8') as archivo: 
        lector = archivo.read()
    data = lector.split(";") 
    diccionarios = [ast.literal_eval('{' + u + '}') for u in data]
    info = {"usuarios" : [], "destinos" : [], "hoteles": [], "actividades":[], "reservas":[] } 
    for elem in diccionarios: 
        if list(elem.keys())[0] == 'usuario_id':
            info["usuarios"].append(elem) 
        elif list(elem.keys())[0] == "destino_id":
            info["destinos"].append(elem) 
        elif list(elem.keys())[0] == "hotel_id":
            info["hoteles"].append(elem) 
        elif list(elem.keys())[0] == "actividad_id":
            info["actividades"].append(elem) 
        elif list(elem.keys())[0] == "reserva_id":
            info["reservas"].append(elem) 
    return info 



from funciones_mongo import db  # importa tu conexión a MongoDB

from bson import ObjectId

def obtener_datos_mongo(coleccion, incluir_id=True):
    """
    Devuelve una lista de diccionarios de una colección de MongoDB.
    Convierte los ObjectId a str para compatibilidad con Neo4j.
    """
    datos = list(db[coleccion].find())
    
    for doc in datos:
        # Convertir ObjectId a str
        for k, v in doc.items():
            if isinstance(v, ObjectId):
                doc[k] = str(v)
        # O eliminar _id si no se desea
        if not incluir_id and "_id" in doc:
            del doc["_id"]
    
    return datos
        
