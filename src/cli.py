from src.dominio.biblioteca import Biblioteca

def mostrar_menu():
    print("\n" + "="*35)
    print("   BIBLIOTECA MUSICAL — MENÚ CLI")
    print("="*35)
    print("1. Listar catálogo de canciones")
    print("2. Ver detalle de una canción")
    print("3. Ver versiones derivadas")
    print("4. Salir")

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
                # Se envía el ID tal cual lo tiene el objeto
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
            print("\n¡Gracias por usar la Biblioteca Musical!")
            break

        else:
            print("\n Opción no válida. Ingrese un número de la lista.")
