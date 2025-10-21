import os #libreria para manipulacion de archivos

# Carpeta raíz del proyecto (una carpeta por encima de 'scripts')
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Subcarpetas principales
DATA_DIR = os.path.join(BASE_DIR, "data")
NOTEBOOKS_DIR = os.path.join(BASE_DIR, "notebooks")
#REPORTS_DIR = os.path.join(BASE_DIR, "reportes")
DOCKER_DIR = os.path.join(BASE_DIR, "docker")

# Archivos de datos individuales
USUARIOS_JSON = os.path.join(DATA_DIR, "usuarios.json")
DESTINOS_JSON = os.path.join(DATA_DIR, "destinos.json")
RESERVAS_JSON = os.path.join(DATA_DIR, "reservas.json")
VISITAS_CSV = os.path.join(DATA_DIR, "visitas.csv")
REL_SOCIALES_CSV = os.path.join(DATA_DIR, "relaciones_sociales.csv")

# Ejemplo de salida de reportes
#GRAFICOS_DIR = os.path.join(REPORTS_DIR, "graficos")
#CAPTURAS_DIR = os.path.join(REPORTS_DIR, "capturas")
