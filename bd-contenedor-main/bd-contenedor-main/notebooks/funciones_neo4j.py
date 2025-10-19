from neo4j import GraphDatabase
import os

# Datos de conexión desde variables de entorno
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4j123")
NEO4J_USER = "neo4j"  # usuario por defecto en el contenedor
NEO4J_URI = "bolt://neo4j:7687"  # host del contenedor de Neo4j

# Crear driver de conexión
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Función para crear nodos de cualquier tipo
def crear_nodo(tx, label, propiedades):
    props = ", ".join([f"{k}: ${k}" for k in propiedades.keys()])
    query = f"MERGE (n:{label} {{ {props} }})"
    tx.run(query, **propiedades)

# Función para insertar varios nodos
def insertar_varios_nodos(label, lista_nodos):
    with driver.session() as session:
        for nodo in lista_nodos:
            session.execute_write(crear_nodo, label, nodo)  # ← actualizado

# Función para crear relaciones entre nodos
def crear_relacion(tx, label_origen, propiedad_origen, valor_origen,
                   label_destino, propiedad_destino, valor_destino,
                   tipo_relacion):
    query = (
        f"MATCH (a:{label_origen} {{{propiedad_origen}: $valor_origen}}), "
        f"(b:{label_destino} {{{propiedad_destino}: $valor_destino}}) "
        f"MERGE (a)-[r:{tipo_relacion}]->(b)"
    )
    tx.run(query, valor_origen=valor_origen, valor_destino=valor_destino)

# Función para insertar varias relaciones
def insertar_varias_relaciones(lista_relaciones):
    with driver.session() as session:
        for rel in lista_relaciones:
            session.execute_write(  # ← actualizado
                crear_relacion,
                rel["label_origen"], rel["prop_origen"], rel["valor_origen"],
                rel["label_destino"], rel["prop_destino"], rel["valor_destino"],
                rel["tipo"]
            )
