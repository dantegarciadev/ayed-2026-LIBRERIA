class Cancion:
    """Representa una entidad Canción del catálogo de la Biblioteca."""

    def __init__(self, id_cancion, titulo, artista, album, genero, anio, duracion_seg):
        self.id = id_cancion
        self.titulo = titulo
        self.artista = artista
        self.album = album
        self.genero = genero
        self.anio = anio
        self.duracion_seg = duracion_seg

    def resumen(self):
        """Retorna una cadena formateada para el listado del catálogo."""
        return f"[{self.id}] {self.titulo} - {self.artista} ({self.album}, {self.anio}) | {self.genero} - {self.duracion_seg}s"

    def __str__(self):
        return f"Cancion('{self.titulo}' de {self.artista})"
