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
