def mostrar_menu():
    print("\n" + "="*35)
    print("   BIBLIOTECA MUSICAL — MENÚ CLI")
    print("="*35)
    print("1. Listar catálogo de canciones")
    print("2. Salir")

def listar_catalogo(canciones):
    if not canciones:
        print("\nEl catálogo de canciones está vacío.")
        return

    print("\n--- CATÁLOGO DE CANCIONES ---")
    for cancion in canciones:
        cid = cancion.get("id", "-")
        titulo = cancion.get("titulo", "Sin título")
        artista = cancion.get("artista", "Artista desconocido")
        album = cancion.get("album", "Álbum desconocido")
        genero = cancion.get("genero", "Género desconocido")
        anio = cancion.get("anio", "Desconocido")
        duracion = cancion.get("duracion_seg", "Desconocida")

        print(f"[{cid}] {titulo} - {artista} ({album}, {anio}) | {genero} - {duracion}s")
        
    print(f"\nTotal de canciones cargadas: {len(canciones)}")

def iniciar_cli(canciones):
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            listar_catalogo(canciones)
        elif opcion == "2":
            print("\n¡Gracias por usar la Biblioteca Musical!")
            break
        else:
            print("\nOpción no válida. Ingrese un número de la lista.")
