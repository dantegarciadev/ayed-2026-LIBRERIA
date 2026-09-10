from src.persistencia.texto import cargar_texto
from src.cli import iniciar_cli

def main():
    catalogo = cargar_texto("data/canciones.txt")
    iniciar_cli(catalogo)

if __name__ == "__main__":
    main()
