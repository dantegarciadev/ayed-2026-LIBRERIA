import struct
from pathlib import Path
from src.excepciones import ArchivoInvalidoError, ItemNoEncontradoError
from src.tads.lista_enlazada import ListaEnlazada

RAIZ = Path(__file__).resolve().parents[2]
DATA = RAIZ / "data"
RUTA_BIN = DATA / "canciones.bin"

HEADER = struct.Struct("<4s 1s I")
FORMATO = struct.Struct("<I 30s 25s 30s 12s 2H")

MAGIA = b"AYED"
TEMA = b"M"


def _a_bytes(texto, ancho):
    return str(texto).encode("utf-8")[:ancho].ljust(ancho, b"\x00")


def _a_texto(datos):
    return datos.rstrip(b"\x00").decode("utf-8", errors="ignore")


def _obtener_valor(item, campo):
    if isinstance(item, dict):
        return item[campo]
    return getattr(item, campo)


def _item_a_tupla(item):
    return (
        int(_obtener_valor(item, "id")),
        _a_bytes(_obtener_valor(item, "titulo"), 30),
        _a_bytes(_obtener_valor(item, "artista"), 25),
        _a_bytes(_obtener_valor(item, "album"), 30),
        _a_bytes(_obtener_valor(item, "genero"), 12),
        int(_obtener_valor(item, "anio")),
        int(_obtener_valor(item, "duracion_seg")),
    )


def _tupla_a_dict(t):
    return {
        "id": t[0],
        "titulo": _a_texto(t[1]),
        "artista": _a_texto(t[2]),
        "album": _a_texto(t[3]),
        "genero": _a_texto(t[4]),
        "anio": t[5],
        "duracion_seg": t[6],
    }


def guardar_binario(ruta, items):
    ruta = Path(ruta)
    cantidad = items.tamanio() if hasattr(items, "tamanio") else len(items)

    with ruta.open("wb") as archivo:
        archivo.write(HEADER.pack(MAGIA, TEMA, cantidad))
        for item in items:
            archivo.write(FORMATO.pack(*_item_a_tupla(item)))


def cargar_binario(ruta, constructor_item=None):
    ruta = Path(ruta)
    if not ruta.exists():
        raise ArchivoInvalidoError(f"No existe el archivo binario: {ruta}")

    with ruta.open("rb") as archivo:
        cabecera = archivo.read(HEADER.size)
        if len(cabecera) < HEADER.size:
            raise ArchivoInvalidoError("Binario truncado: no tiene el header completo.")

        magia, tema, cantidad = HEADER.unpack(cabecera)
        if magia != MAGIA:
            raise ArchivoInvalidoError("Magia incorrecta: este archivo no pertenece al TP.")
        if tema != TEMA:
            raise ArchivoInvalidoError(f"Tema incorrecto: se esperaba {TEMA!r}, vino {tema!r}.")

        catalogo = ListaEnlazada()
        for _ in range(cantidad):
            datos = archivo.read(FORMATO.size)
            if len(datos) < FORMATO.size:
                raise ArchivoInvalidoError("Binario truncado: faltan registros respecto al header.")
            fila = _tupla_a_dict(FORMATO.unpack(datos))
            elemento = constructor_item(**fila) if constructor_item else fila
            catalogo.insertar_al_final(elemento)

        if archivo.read(1):
            raise ArchivoInvalidoError("Binario corrupto: sobran bytes al final del archivo.")

    return catalogo


def actualizar_registro(ruta, posicion, item):
    ruta = Path(ruta)
    if not ruta.exists():
        raise ArchivoInvalidoError(f"No existe el archivo binario: {ruta}")

    with ruta.open("r+b") as archivo:
        cabecera = archivo.read(HEADER.size)
        if len(cabecera) < HEADER.size:
            raise ArchivoInvalidoError("Binario truncado: header incompleto.")

        magia, tema, cantidad = HEADER.unpack(cabecera)
        if magia != MAGIA or tema != TEMA:
            raise ArchivoInvalidoError("Header inválido en el archivo binario.")

        if posicion < 0 or posicion >= cantidad:
            raise ItemNoEncontradoError(f"Posición {posicion} fuera de rango (0 a {cantidad - 1}).")

        archivo.seek(HEADER.size + posicion * FORMATO.size)
        archivo.write(FORMATO.pack(*_item_a_tupla(item)))


def alta_binario(ruta, item):
    ruta = Path(ruta)
    with ruta.open("r+b") as archivo:
        cabecera = archivo.read(HEADER.size)
        if len(cabecera) < HEADER.size:
            raise ArchivoInvalidoError("Binario truncado.")
        magia, tema, cantidad = HEADER.unpack(cabecera)

        archivo.seek(0, 2)
        archivo.write(FORMATO.pack(*_item_a_tupla(item)))

        archivo.seek(0)
        archivo.write(HEADER.pack(magia, tema, cantidad + 1))


def baja_binario(ruta, posicion):
    ruta = Path(ruta)
    with ruta.open("r+b") as archivo:
        cabecera = archivo.read(HEADER.size)
        if len(cabecera) < HEADER.size:
            raise ArchivoInvalidoError("Binario truncado.")
        magia, tema, cantidad = HEADER.unpack(cabecera)
        if posicion < 0 or posicion >= cantidad:
            raise ItemNoEncontradoError(f"Posición {posicion} fuera de rango.")

        registros = [archivo.read(FORMATO.size) for _ in range(cantidad)]
        del registros[posicion]

        archivo.seek(0)
        archivo.truncate()
        archivo.write(HEADER.pack(magia, tema, len(registros)))
        for reg in registros:
            archivo.write(reg)
