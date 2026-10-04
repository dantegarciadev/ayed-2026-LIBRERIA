from src.tads.lista_enlazada import ListaEnlazada
from src.excepciones import ColaVaciaError

class Cola:
    
    def __init__(self):
        self._items = ListaEnlazada()

    def encolar(self, dato):
        self._items.insertar_al_final(dato)

    def desencolar(self):
        if self.esta_vacia():
            raise ColaVaciaError("No hay canciones en la cola de reproducción.")
        frente = self.ver_frente()
        self._items.eliminar(frente)
        return frente

    def ver_frente(self):
        if self.esta_vacia():
            raise ColaVaciaError("La cola de reproducción está vacía.")
        return self._items._cabeza.dato

    def esta_vacia(self):
        return self._items.esta_vacia()
