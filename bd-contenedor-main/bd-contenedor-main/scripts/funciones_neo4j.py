from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# === Cargar variables de entorno desde /docker/.env ===
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "docker", ".env"))

# === Datos de conexión ===
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4j123")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")

# === Conexión con Neo4j ===
try:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
except Exception as e:
    driver = None
    print("❌ Error al conectar con Neo4j:", e)


# ======================================================
# FUNCIONES PRINCIPALES
# ======================================================

def crear_nodo(tx, label, propiedades):
    """
    Crea o actualiza un nodo (MERGE) con las propiedades dadas.
    """
    if not propiedades:
        return
    props = ", ".join([f"{k}: ${k}" for k in propiedades.keys()])
    query = f"MERGE (n:{label} {{ {props} }})"
    tx.run(query, **propiedades)


def insertar_varios_nodos(label, lista_nodos):
    """
    Inserta múltiples nodos en una colección (usando MERGE).
    """
    if not lista_nodos:
        print(f"[ADVERTENCIA] No hay nodos para insertar en '{label}'.")
        return

    with driver.session() as session:
        for nodo in lista_nodos:
            session.execute_write(crear_nodo, label, nodo)
    print(f"✅ Se insertaron {len(lista_nodos)} nodos en '{label}'.")


def crear_relacion(tx, label_origen, prop_origen, valor_origen,
                   label_destino, prop_destino, valor_destino,
                   tipo_relacion):
    """
    Crea una relación dirigida entre dos nodos, si ambos existen.
    """
    query = (
        f"MATCH (a:{label_origen} {{{prop_origen}: $valor_origen}}), "
        f"(b:{label_destino} {{{prop_destino}: $valor_destino}}) "
        f"MERGE (a)-[r:{tipo_relacion}]->(b)"
    )
    tx.run(query, valor_origen=valor_origen, valor_destino=valor_destino)


def insertar_varias_relaciones(lista_relaciones):
    """
    Inserta múltiples relaciones entre nodos.
    Espera una lista de diccionarios con las claves:
    label_origen, prop_origen, valor_origen, label_destino, prop_destino, valor_destino, tipo
    """
    if not lista_relaciones:
        print("[ADVERTENCIA] Lista vacía: no se insertaron relaciones.")
        return

    with driver.session() as session:
        for rel in lista_relaciones:
            session.execute_write(
                crear_relacion,
                rel["label_origen"], rel["prop_origen"], rel["valor_origen"],
                rel["label_destino"], rel["prop_destino"], rel["valor_destino"],
                rel["tipo"]
            )
    print(f"✅ Se insertaron {len(lista_relaciones)} relaciones.")


def limpiar_base():
    """
    Elimina todos los nodos y relaciones del grafo (⚠️ cuidado con usar en producción).
    """
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    print("🧹 Base de datos Neo4j limpiada con éxito.")


def probar_conexion():
    """
    Verifica si la conexión con Neo4j es exitosa.
    """
    try:
        with driver.session() as session:
            result = session.run("RETURN 1 AS ok")
            if result.single()["ok"] == 1:
                print("✅ Conexión a Neo4j exitosa.")
                return True
    except Exception as e:
        print("❌ Error al conectar con Neo4j:", e)
        return False


def cerrar_conexion():
    """
    Cierra el driver de Neo4j.
    """
    if driver:
        driver.close()
        print("🔒 Conexión con Neo4j cerrada correctamente.")