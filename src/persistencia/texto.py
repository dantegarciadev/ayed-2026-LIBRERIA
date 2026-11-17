import csv
from pathlib import Path
from src.excepciones import ArchivoInvalidoError

RAIZ = Path(__file__).resolve().parents[2]
DATA = RAIZ / "data"
RUTA_TXT = DATA / "canciones.txt"

ENCABEZADO_ESPERADO = ["id", "titulo", "artista", "album", "genero", "anio", "duracion_seg"]


def cargar_texto(ruta=RUTA_TXT):
    """Lee un .txt secuencial y devuelve una lista de dicts. Lanza ArchivoInvalidoError si falla."""
    path = Path(ruta)

    if not path.exists():
        raise ArchivoInvalidoError(f"No se encontró el archivo: {path}")

    canciones = []
    with open(path, mode="r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)

        
        if not lector.fieldnames or list(lector.fieldnames) != ENCABEZADO_ESPERADO:
            raise ArchivoInvalidoError(
                f"Encabezado inválido. Se esperaba {ENCABEZADO_ESPERADO}, se recibió {lector.fieldnames}"
            )

        for num_linea, fila in enumerate(lector, start=2):
           
            if None in fila or None in fila.values():
                raise ArchivoInvalidoError(
                    f"Línea {num_linea} rota: cantidad de campos incorrecta."
                )
            canciones.append(dict(fila))

    return canciones


def guardar_texto(ruta, filas, encabezado=ENCABEZADO_ESPERADO):
    """Guarda el catálogo completo en texto simple (.txt) con encabezado."""
    path = Path(ruta)

    with open(path, mode="w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=encabezado)
        escritor.writeheader()
        for fila in filas:
            escritor.writerow(fila)
