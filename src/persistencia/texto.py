import csv
import pathlib

def cargar_texto(ruta="data/canciones.txt"):
    canciones = []
    path = pathlib.Path(ruta)

    if not path.exists():
        print(f"Error: No se encontró el archivo en {path.resolve()}")
        return canciones

    with open(path, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            canciones.append(fila)

    return canciones

def guardar_texto(ruta, filas, encabezado):
    raise NotImplementedError
    
    
