from src.dominio.canciones import obtener_catalogo
from src.dominio.cancion import Cancion

class Biblioteca:
    """Gestiona la colección del catálogo incluyendo las relaciones de versiones."""

    def __init__(self):
        # Convertimos la lista de diccionarios de canciones.py en Objetos Cancion
        self.catalogo = [
            Cancion(
                c["id"], c["titulo"], c["artista"], 
                c["album"], c["genero"], c["anio"], c["duracion_seg"]
            )
            for c in obtener_catalogo()
        ]
        
        # Diccionario de versiones: id_cancion -> lista de ids de sus versiones derivadas
        self.versiones_map = {
            1: [62],    # De Musica Ligera -> Live 
            12: [13],   # Jijiji -> Live 
            19: [63],   # Flaca -> Live 
            31: [66],   # Blank Space -> Cover 
            32: [33],   # Bohemian Rhapsody -> Live 
            37: [67],   # Get Lucky -> Remix
            47: [48],   # Wonderwall -> Live
            51: [52],   # Billie Jean -> Remix
            54: [65],   # Yellow -> Live
            55: [64],   # Creep -> Live
            61: [16],   # Gracias a la Vida -> Cover 
        }

    def obtener_catalogo(self):
        return self.catalogo

    def buscar_por_id(self, id_cancion):
        for c in self.catalogo:
            if c.id == int(id_cancion):
                return c
        return None

    def buscar_versiones_directas(self, id_cancion):
        return self.versiones_map.get(int(id_cancion), [])

    def obtener_versiones_derivadas(self, id_cancion):
        """Función recursiva para obtener derivados."""
        directas = self.buscar_versiones_directas(id_cancion)
        
        # CASO BASE: Si no tiene derivados
        if not directas:
            return []

        resultado = list(directas)
        
        # CASO RECURSIVO
        for v in directas:
            resultado += self.obtener_versiones_derivadas(v)

        return resultado
