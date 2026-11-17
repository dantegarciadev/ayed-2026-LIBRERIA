from src.dominio.biblioteca import Biblioteca
from src.dominio.cancion import Cancion
from src.dominio.playlist import Playlist
from src.tads.pila import Pila
from src.tads.cola import Cola
from src.excepciones import (
    ColeccionLlenaError,
    PilaVaciaError,
    ColaVaciaError,
    ArchivoInvalidoError,
    ItemNoEncontradoError,
)
from src.algoritmos.busqueda import busqueda_lineal, busqueda_binaria
from src.algoritmos.ordenamiento import ordenar_seleccion, ordenar_insercion
from src.persistencia.texto import (
    RUTA_TXT,
    ENCABEZADO_ESPERADO,
    cargar_texto,
    guardar_texto,
)
from src.persistencia.binario import (
    RUTA_BIN,
    guardar_binario,
    cargar_binario,
    actualizar_registro,
    alta_binario,
    baja_binario,
)


def mostrar_menu():
    print("\n" + "=" * 35)
    print("    BIBLIOTECA MUSICAL — MENÚ CLI")
    print("=" * 35)
    print("1. Listar catálogo de canciones")
    print("2. Ver detalle de una canción")
    print("3. Ver versiones derivadas")
    print("4. Agregar canción a la playlist")
    print("5. Ver playlist")
    print("6. Reproducir canción (Apilar en historial)")
    print("7. Deshacer última reproducción")
    print("8. Encolar canción para reproducción")
    print("9. Sonar siguiente canción de la cola")
    print("10. Buscar canción por título")
    print("11. Ordenar catálogo")
    print("12. Gestionar catálogo (Alta / Baja / Modificación)")
    print("13. Guardar / Cargar archivos (.txt y .bin)")
    print("14. Salir")


def catalogo_a_filas(catalogo):
    filas = []
    for c in catalogo:
        filas.append({
            "id": c.id,
            "titulo": c.titulo,
            "artista": c.artista,
            "album": c.album,
            "genero": c.genero,
            "anio": c.anio,
            "duracion_seg": c.duracion_seg,
        })
    return filas


def posicion_del_id(catalogo, id_buscado):
    for pos, c in enumerate(catalogo):
        if int(c.id) == int(id_buscado):
            return pos
    raise ItemNoEncontradoError(f"No hay canción con ID {id_buscado}.")


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
                print(
                    f"\n[DETALLE] ID: {cancion.id} | Título: {cancion.titulo} | "
                    f"Artista: {cancion.artista} | Álbum: {cancion.album} | "
                    f"Año: {cancion.anio} | Género: {cancion.genero} | "
                    f"Duración: {cancion.duracion_seg}s"
                )
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
                print(f" Encolada: {cancion.titulo}")
            else:
                print("\n Canción no encontrada.")

        elif opcion == "9":
            try:
                siguiente = cola_repro.desencolar()
                print(f" Sonando desde la cola: {siguiente.titulo}")
            except ColaVaciaError as e:
                print(f" Error: {e}")

        elif opcion == "10":
            print("\nBuscar por título:")
            print("1. Búsqueda lineal")
            print("2. Búsqueda binaria")

            metodo = input("Seleccione el método: ").strip()

            if metodo not in ("1", "2"):
                print("\nOpción no válida.")
                continue

            titulo = input("Ingrese el título: ").strip()
            catalogo = biblioteca.obtener_catalogo()

            if metodo == "1":
                cancion = busqueda_lineal(catalogo, titulo, lambda c: c.titulo)

            elif metodo == "2":
                ordenar_insercion(catalogo, lambda c: c.titulo)
                print("\nCatálogo ordenado por título; usando búsqueda binaria.")
                cancion = busqueda_binaria(catalogo, titulo, lambda c: c.titulo)

            if cancion:
                print(cancion.resumen())
            else:
                print("\nCanción no encontrada.")

        elif opcion == "11":
            print("\nOrdenar por:")
            print("1. Título")
            print("2. Duración")

            criterio = input("Seleccione el criterio: ").strip()

            if criterio == "1":
                obtener_clave = lambda c: c.titulo
            elif criterio == "2":
                obtener_clave = lambda c: c.duracion_seg
            else:
                print("\nOpción no válida.")
                continue

            print("\nAlgoritmo:")
            print("1. Selección")
            print("2. Inserción")

            algoritmo = input("Seleccione el algoritmo: ").strip()
            catalogo = biblioteca.obtener_catalogo()

            if algoritmo == "1":
                ordenar_seleccion(catalogo, obtener_clave)
            elif algoritmo == "2":
                ordenar_insercion(catalogo, obtener_clave)
            else:
                print("\nOpción no válida.")
                continue

            guardar_texto(RUTA_TXT, catalogo_a_filas(catalogo), ENCABEZADO_ESPERADO)
            if RUTA_BIN.exists():
                guardar_binario(RUTA_BIN, catalogo)

            print("\nCatálogo ordenado y guardado.")

       
        elif opcion == "12":
            print("\n--- GESTIÓN DE CATÁLOGO (ABM PERSISTENTE) ---")
            print("1. Alta de canción")
            print("2. Modificar canción por ID")
            print("3. Baja de canción por ID")
            sub_abm = input("Seleccione una opción: ").strip()

            try:
                catalogo = biblioteca.obtener_catalogo()

                if sub_abm not in ("1", "2", "3"):
                    print("\nSubopción no válida.")
                    continue

                if not RUTA_BIN.exists():
                    guardar_binario(RUTA_BIN, catalogo)

                if sub_abm == "1":
                    nuevo_id = int(input("ID: ").strip())

                    if biblioteca.buscar_por_id(nuevo_id):
                        print("\nError: Ya existe una canción con ese ID.")
                        continue

                    titulo = input("Título: ").strip()
                    artista = input("Artista: ").strip()
                    album = input("Álbum: ").strip()
                    genero = input("Género: ").strip()
                    anio = int(input("Año: ").strip())
                    duracion = int(input("Duración (seg): ").strip())

                    nueva = Cancion(
                        nuevo_id, titulo, artista, album, genero, anio, duracion
                    )

                    alta_binario(RUTA_BIN, nueva)
                    biblioteca.agregar_cancion(nueva)

                    guardar_texto(
                        RUTA_TXT,
                        catalogo_a_filas(biblioteca.obtener_catalogo()),
                        ENCABEZADO_ESPERADO
                    )

                    print("\nCanción agregada y persistida en .txt y .bin.")

                elif sub_abm == "2":
                    id_mod = int(input("ID de canción a modificar: ").strip())
                    pos = posicion_del_id(catalogo, id_mod)
                    cancion = catalogo[pos]

                    nuevo_titulo = input(
                        f"Nuevo título [{cancion.titulo}]: "
                    ).strip()

                    nuevo_artista = input(
                        f"Nuevo artista [{cancion.artista}]: "
                    ).strip()

                    titulo = nuevo_titulo if nuevo_titulo else cancion.titulo
                    artista = nuevo_artista if nuevo_artista else cancion.artista

                    modificada = Cancion(
                        cancion.id,
                        titulo,
                        artista,
                        cancion.album,
                        cancion.genero,
                        cancion.anio,
                        cancion.duracion_seg
                    )

                    actualizar_registro(RUTA_BIN, pos, modificada)
                    catalogo[pos] = modificada

                    guardar_texto(
                        RUTA_TXT,
                        catalogo_a_filas(catalogo),
                        ENCABEZADO_ESPERADO
                    )

                    print(f"\nRegistro en posición {pos} actualizado.")

                elif sub_abm == "3":
                    id_baja = int(input("ID de canción a eliminar: ").strip())
                    pos = posicion_del_id(catalogo, id_baja)

                    baja_binario(RUTA_BIN, pos)
                    biblioteca.eliminar_cancion(id_baja)

                    guardar_texto(
                        RUTA_TXT,
                        catalogo_a_filas(biblioteca.obtener_catalogo()),
                        ENCABEZADO_ESPERADO
                    )

                    print("\nCanción eliminada y archivos actualizados.")

            except (ValueError, ItemNoEncontradoError, ArchivoInvalidoError, OSError) as e:
                print(f"\nError: {e}")

        elif opcion == "13":
            print("\n--- PERSISTENCIA (.TXT Y .BIN) ---")
            print("a) Cargar catálogo desde .txt")
            print("b) Guardar catálogo en .txt")
            print("c) Guardar catálogo en binario (.bin)")
            print("d) Cargar catálogo desde binario (.bin)")
            sub_arch = input("Seleccione una subopción: ").strip().lower()

            try:
                if sub_arch == "a":
                    filas = cargar_texto(RUTA_TXT)
                    biblioteca.cargar_desde_filas(filas)
                    print(f"\nCatálogo cargado desde .txt: {len(filas)} canciones.")

                elif sub_arch == "b":
                    guardar_texto(RUTA_TXT, catalogo_a_filas(biblioteca.obtener_catalogo()), ENCABEZADO_ESPERADO)
                    print("\nCatálogo guardado en data/canciones.txt.")

                elif sub_arch == "c":
                    guardar_binario(RUTA_BIN, biblioteca.obtener_catalogo())
                    print("\nCatálogo guardado en data/canciones.bin.")

                elif sub_arch == "d":
                    ruta_custom = input("Ruta .bin (Enter para data/canciones.bin): ").strip()
                    ruta_objetivo = ruta_custom if ruta_custom else RUTA_BIN
                    lista_enlazada = cargar_binario(ruta_objetivo, Cancion)
                    biblioteca.establecer_catalogo(lista_enlazada)
                    print(f"\nCatálogo cargado desde binario: {lista_enlazada.tamanio()} canciones.")

                else:
                    print("\nSubopción no válida.")

            except ArchivoInvalidoError as e:
                print(f"\nArchivo inválido: {e}")

        elif opcion == "14":
            print("\n¡Gracias por usar la Biblioteca Musical!")
            break

        else:
            print("\n Opción no válida. Ingrese un número de la lista.")
