from src.tads.lista_enlazada import ListaEnlazada
from src.excepciones import ColeccionLlenaError

class Playlist:
    """Colección principal del dominio con tope."""

    def __init__(self, nombre="Mi Playlist", tope=6):
        self.nombre = nombre
        self._canciones = ListaEnlazada()
        self._tope = tope

    def agregar(self, cancion):
        if self._canciones.tamanio() >= self._tope:
            raise ColeccionLlenaError(f"La playlist está llena (máximo {self._tope} canciones).")
        self._canciones.insertar_al_final(cancion)

    def eliminar(self, cancion):
        self._canciones.eliminar(cancion)

    def listar(self):
        if self._canciones.esta_vacia():
            print("\nLa playlist está vacía.")
            return
        print(f"\n--- PLAYLIST: {self.nombre} ---")
        for cancion in self._canciones:
            print(cancion.resumen())
