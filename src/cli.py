from src.dominio.biblioteca import Biblioteca
from src.dominio.playlist import Playlist
from src.tads.pila import Pila
from src.tads.cola import Cola
from src.excepciones import ColeccionLlenaError, PilaVaciaError, ColaVaciaError

def mostrar_menu():
    print("\n" + "="*35)
    print("    BIBLIOTECA MUSICAL — MENÚ CLI")
    print("="*35)
    print("1. Listar catálogo de canciones")
    print("2. Ver detalle de una canción")
    print("3. Ver versiones derivadas")
    print("4. Agregar canción a la playlist")
    print("5. Ver playlist")
    print("6. Reproducir canción (Apilar en historial)")
    print("7. Deshacer última reproducción")
    print("8. Encolar canción para reproducción")
    print("9. Sonar siguiente canción de la cola")
    print("10. Salir")
    
def listar_catalogo(biblioteca):
    catalogo = biblioteca.obtener_catalogo()
    if not catalogo:
        print("\nEl catálogo de canciones está vacío.")
        return

    print("\n--- CATÁLOGO DE CANCIONES ---")
    for cancion in catalogo:
        print(cancion.resumen())
        
    print(f"\nTotal de canciones cargadas: {len(catalogo)}")

def iniciar_cli():
    biblioteca = Biblioteca()
    playlist = Playlist(tope=6)
    historial = Pila()
    cola_repro = Cola()
    
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            listar_catalogo(biblioteca)

        elif opcion == "2":
            id_ingresado = input("Ingrese el ID de la canción: ").strip()
            cancion = biblioteca.buscar_por_id(id_ingresado)
            if not cancion and id_ingresado.isdigit():
                cancion = biblioteca.buscar_por_id(int(id_ingresado))

            if cancion:
                print(f"\n[DETALLE] ID: {cancion.id} | Título: {cancion.titulo} | Artista: {cancion.artista} | Álbum: {cancion.album} | Año: {cancion.anio} | Género: {cancion.genero} | Duración: {cancion.duracion_seg}s")
            else:
                print("\n Canción no encontrada.")

        elif opcion == "3":
            id_ingresado = input("Ingrese el ID de la canción base: ").strip()
            cancion = biblioteca.buscar_por_id(id_ingresado)
            if not cancion and id_ingresado.isdigit():
                cancion = biblioteca.buscar_por_id(int(id_ingresado))

            if cancion:
                ids_derivados = biblioteca.obtener_versiones_derivadas(cancion.id)
                print(f"\n--- Versiones derivadas de '{cancion.titulo}' (ID {cancion.id}) ---")
                if ids_derivados:
                    for v_id in ids_derivados:
                        v_obj = biblioteca.buscar_por_id(v_id)
                        if not v_obj and str(v_id).isdigit():
                            v_obj = biblioteca.buscar_por_id(int(v_id))
                        nombre = v_obj.titulo if v_obj else f"Versión ID {v_id}"
                        print(f" -> ID {v_id}: {nombre}")
                else:
                    print(" (Esta canción no posee versiones ni derivados registrados - Caso Base)")
            else:
                print("\n Canción no encontrada.")

        elif opcion == "4":
            id_ingresado = input("ID de canción a agregar a la playlist: ").strip()
            cancion = biblioteca.buscar_por_id(id_ingresado)
            if not cancion and id_ingresado.isdigit():
                cancion = biblioteca.buscar_por_id(int(id_ingresado))

            if cancion:
                try:
                    playlist.agregar(cancion)
                    print(f" Agregada a playlist: {cancion.titulo}")
                except ColeccionLlenaError as e:
                    print(f" Error: {e}")
            else:
                print("\n Canción no encontrada.")

        elif opcion == "5":
            playlist.listar()

        elif opcion == "6":
            id_ingresado = input("ID de canción a reproducir: ").strip()
            cancion = biblioteca.buscar_por_id(id_ingresado)
            if not cancion and id_ingresado.isdigit():
                cancion = biblioteca.buscar_por_id(int(id_ingresado))

            if cancion:
                historial.apilar(cancion)
                print(f" Reproduciendo: {cancion.titulo}")
            else:
                print("\n Canción no encontrada.")

        elif opcion == "7":
            try:
                deshecha = historial.desapilar()
                print(f" Deshecho: Se eliminó '{deshecha.titulo}' del historial.")
            except PilaVaciaError as e:
                print(f" Error: {e}")

        elif opcion == "8":
            id_ingresado = input("ID de canción a encolar: ").strip()
            cancion = biblioteca.buscar_por_id(id_ingresado)
            if not cancion and id_ingresado.isdigit():
                cancion = biblioteca.buscar_por_id(int(id_ingresado))

            if cancion:
                cola_repro.encolar(cancion)
                print(f" ➕ Encolada: {cancion.titulo}")
            else:
                print("\n Canción no encontrada.")

        elif opcion == "9":
            try:
                siguiente = cola_repro.desencolar()
                print(f" Sonando desde la cola: {siguiente.titulo}")
            except ColaVaciaError as e:
                print(f" Error: {e}")

        elif opcion == "10":
            print("\n¡Gracias por usar la Biblioteca Musical!")
            break

        else:
            print("\n Opción no válida. Ingrese un número de la lista.")
