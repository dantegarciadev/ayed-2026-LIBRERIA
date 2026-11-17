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
    resultado = b""

    for caracter in str(texto):
        codificado = caracter.encode("utf-8")

        if len(resultado) + len(codificado) > ancho:
            break

        resultado += codificado

    return resultado.ljust(ancho, b"\x00")


def _a_texto(datos):
    return datos.rstrip(b"\x00").decode("utf-8")


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


def _validar_cabecera(archivo, ruta):
    archivo.seek(0)
    cabecera = archivo.read(HEADER.size)

    if len(cabecera) != HEADER.size:
        raise ArchivoInvalidoError(
            f"Binario truncado: encabezado incompleto en {ruta}."
        )

    try:
        magia, tema, cantidad = HEADER.unpack(cabecera)
    except struct.error as error:
        raise ArchivoInvalidoError(
            f"No se pudo interpretar el encabezado: {error}"
        ) from error

    if magia != MAGIA:
        raise ArchivoInvalidoError(
            "Magia incorrecta: este archivo no pertenece al TP."
        )

    if tema != TEMA:
        raise ArchivoInvalidoError(
            f"Tema incorrecto: se esperaba {TEMA!r}, vino {tema!r}."
        )

    archivo.seek(0, 2)
    tamanio_real = archivo.tell()
    tamanio_esperado = HEADER.size + cantidad * FORMATO.size

    if tamanio_real < tamanio_esperado:
        raise ArchivoInvalidoError(
            "Binario truncado: faltan registros respecto al encabezado."
        )

    if tamanio_real > tamanio_esperado:
        raise ArchivoInvalidoError(
            "Binario corrupto: sobran bytes al final del archivo."
        )

    archivo.seek(HEADER.size)

    return cantidad


def guardar_binario(ruta, items):
    ruta = Path(ruta)

    try:
        elementos = list(items)
        cantidad = len(elementos)

        with ruta.open("wb") as archivo:
            archivo.write(HEADER.pack(MAGIA, TEMA, cantidad))

            for item in elementos:
                datos = _item_a_tupla(item)
                archivo.write(FORMATO.pack(*datos))

    except (OSError, struct.error, ValueError, TypeError, KeyError, AttributeError) as error:
        raise ArchivoInvalidoError(
            f"No se pudo guardar el archivo binario: {error}"
        ) from error


def cargar_binario(ruta, constructor_item=None):
    ruta = Path(ruta)

    if not ruta.exists():
        raise ArchivoInvalidoError(
            f"No existe el archivo binario: {ruta}"
        )

    try:
        with ruta.open("rb") as archivo:
            cantidad = _validar_cabecera(archivo, ruta)
            catalogo = ListaEnlazada()

            for _ in range(cantidad):
                datos = archivo.read(FORMATO.size)

                if len(datos) != FORMATO.size:
                    raise ArchivoInvalidoError(
                        "Binario truncado: registro incompleto."
                    )

                try:
                    fila = _tupla_a_dict(FORMATO.unpack(datos))
                except (struct.error, UnicodeDecodeError) as error:
                    raise ArchivoInvalidoError(
                        f"Registro binario inválido: {error}"
                    ) from error

                elemento = (
                    constructor_item(**fila)
                    if constructor_item
                    else fila
                )

                catalogo.insertar_al_final(elemento)

        return catalogo

    except ArchivoInvalidoError:
        raise

    except (OSError, struct.error, UnicodeDecodeError, TypeError, ValueError) as error:
        raise ArchivoInvalidoError(
            f"No se pudo cargar el archivo binario: {error}"
        ) from error


def actualizar_registro(ruta, posicion, item):
    ruta = Path(ruta)

    if not ruta.exists():
        raise ArchivoInvalidoError(
            f"No existe el archivo binario: {ruta}"
        )

    try:
        datos = FORMATO.pack(*_item_a_tupla(item))

        with ruta.open("r+b") as archivo:
            cantidad = _validar_cabecera(archivo, ruta)

            if posicion < 0 or posicion >= cantidad:
                raise ItemNoEncontradoError(
                    f"Posición {posicion} fuera de rango "
                    f"(0 a {cantidad - 1})."
                )

            desplazamiento = HEADER.size + posicion * FORMATO.size
            archivo.seek(desplazamiento)
            archivo.write(datos)

    except (ArchivoInvalidoError, ItemNoEncontradoError):
        raise

    except (OSError, struct.error, ValueError, TypeError, KeyError, AttributeError) as error:
        raise ArchivoInvalidoError(
            f"No se pudo actualizar el registro: {error}"
        ) from error


def alta_binario(ruta, item):
    ruta = Path(ruta)

    if not ruta.exists():
        raise ArchivoInvalidoError(
            f"No existe el archivo binario: {ruta}"
        )

    try:
        datos = FORMATO.pack(*_item_a_tupla(item))

        with ruta.open("r+b") as archivo:
            cantidad = _validar_cabecera(archivo, ruta)

            archivo.seek(0, 2)
            archivo.write(datos)

            archivo.seek(0)
            archivo.write(
                HEADER.pack(MAGIA, TEMA, cantidad + 1)
            )

    except ArchivoInvalidoError:
        raise

    except (OSError, struct.error, ValueError, TypeError, KeyError, AttributeError) as error:
        raise ArchivoInvalidoError(
            f"No se pudo agregar el registro: {error}"
        ) from error


def baja_binario(ruta, posicion):
    ruta = Path(ruta)

    if not ruta.exists():
        raise ArchivoInvalidoError(
            f"No existe el archivo binario: {ruta}"
        )

    try:
        with ruta.open("r+b") as archivo:
            cantidad = _validar_cabecera(archivo, ruta)

            if posicion < 0 or posicion >= cantidad:
                raise ItemNoEncontradoError(
                    f"Posición {posicion} fuera de rango "
                    f"(0 a {cantidad - 1})."
                )

            registros = []

            for _ in range(cantidad):
                registro = archivo.read(FORMATO.size)

                if len(registro) != FORMATO.size:
                    raise ArchivoInvalidoError(
                        "Binario truncado: hay un registro incompleto."
                    )

                registros.append(registro)

            del registros[posicion]

            archivo.seek(0)
            archivo.truncate()

            archivo.write(
                HEADER.pack(MAGIA, TEMA, len(registros))
            )

            for registro in registros:
                archivo.write(registro)

    except (ArchivoInvalidoError, ItemNoEncontradoError):
        raise

    except (OSError, struct.error, ValueError, TypeError) as error:
        raise ArchivoInvalidoError(
            f"No se pudo eliminar el registro: {error}"
        ) from error
