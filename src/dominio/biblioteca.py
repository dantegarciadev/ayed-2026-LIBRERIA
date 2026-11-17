from src.dominio.cancion import Cancion
from src.persistencia.texto import cargar_texto, RUTA_TXT


class Biblioteca:
    def __init__(self, ruta_txt=RUTA_TXT):
        self.catalogo = []
        self.cargar_desde_filas(cargar_texto(ruta_txt))

        self.versiones_map = {
            1: [62],
            12: [13],
            19: [63],
            31: [66],
            32: [33],
            37: [67],
            47: [48],
            51: [52],
            54: [65],
            55: [64],
            61: [16],
        }

    def cargar_desde_filas(self, filas):
        self.catalogo = [
            Cancion(
                int(c["id"]),
                c["titulo"],
                c["artista"],
                c["album"],
                c["genero"],
                int(c["anio"]),
                int(c["duracion_seg"]),
            )
            for c in filas
        ]

    def establecer_catalogo(self, nueva_coleccion):
        self.catalogo = list(nueva_coleccion)

    def obtener_catalogo(self):
        return self.catalogo

    def agregar_cancion(self, cancion):
        self.catalogo.append(cancion)

    def eliminar_cancion(self, id_cancion):
        for i, c in enumerate(self.catalogo):
            if str(c.id) == str(id_cancion):
                del self.catalogo[i]
                return True
        return False

    def buscar_por_id(self, id_cancion):
        for c in self.catalogo:
            if str(c.id) == str(id_cancion):
                return c
        return None

    def buscar_versiones_directas(self, id_cancion):
        try:
            clave_int = int(id_cancion)
            if clave_int in self.versiones_map:
                return self.versiones_map[clave_int]
        except (ValueError, TypeError):
            pass

        return self.versiones_map.get(str(id_cancion), [])

    def obtener_versiones_derivadas(self, id_cancion):
        directas = self.buscar_versiones_directas(id_cancion)

        if not directas:
            return []

        resultado = list(directas)

        for v in directas:
            resultado += self.obtener_versiones_derivadas(v)

        return resultado
