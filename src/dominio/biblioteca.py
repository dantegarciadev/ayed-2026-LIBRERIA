from src.dominio.cancion import Cancion

class Biblioteca:
    """Gestiona la colección del catálogo incluyendo las relaciones de versiones."""

    def __init__(self):
        self.catalogo = [
            Cancion(1, "De Musica Ligera", "Soda Stereo", "Cancion Animal", "Rock", 1990, 213),
            Cancion(2, "De Musica Ligera (Live El Ultimo Concierto)", "Soda Stereo", "El Ultimo Concierto", "Rock", 1997, 240),
            Cancion(3, "De Musica Ligera (Remix 2020)", "Soda Stereo", "Remixes", "Rock", 2020, 210),
            Cancion(4, "Persiana Americana", "Soda Stereo", "Signos", "Rock", 1986, 263),
            Cancion(5, "Crimen", "Gustavo Cerati", "Ahi vamos", "Rock", 2006, 239),
        ]
        
        # Diccionario de versiones: id_cancion -> lista de ids de sus versiones derivadas
        self.versiones_map = {
            1: [2],
            2: [3],
            3: [],
            4: [],
            5: []
        }

    def obtener_catalogo(self):
        return self.catalogo

    def buscar_por_id(self, id_cancion):
        for c in self.catalogo:
            if c.id == id_cancion:
                return c
        return None

    def buscar_versiones_directas(self, id_cancion):
        """Devuelve los IDs de los derivados (covers/remixes) de una canción."""
        return self.versiones_map.get(id_cancion, [])

    def obtener_versiones_derivadas(self, id_cancion):
        """Función recursiva: Busca todas las versiones derivadas de una canción y las versiones de las versiones."""
        directas = self.buscar_versiones_directas(id_cancion)
        
        # CASO BASE: Si la canción no tiene versiones derivadas, retorna lista vacía.
        if not directas:
            return []

        resultado = list(directas)
        
        # CASO RECURSIVO: Se llama a sí misma para cada versión encontrada
        for v in directas:
            resultado += self.obtener_versiones_derivadas(v)

        return resultado
