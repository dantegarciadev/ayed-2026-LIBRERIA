# Protocolo de pruebas

Pruebas **manuales**. Cada fila es un caso. Ejecutar sobre el tag que entregan.

Leyenda de resultado: `pasa` / `no pasa` / `no corrido`.

Mínimos: 8 casos escritos en E2; ejecutados en E3; 15 de regresión en E6 (pila, cola, archivos, recursión, búsquedas).

| ID | Entrega | Acción (pasos en el CLI) | Datos | Resultado esperado | Resultado | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| P01 | E1 | Arrancar el programa y listar catálogo | dataset de la cátedra | lista no vacía, sin traceback | pasa | Verificado con Opción 1 |
| P02 | E1 | Elegir un ítem inexistente | id = -1 | mensaje claro, el menú sigue | pasa | Devuelve "Canción no encontrada" |
| P03 | E2 | Operación recursiva sobre un ítem con cadena | ver consigna §3.3 | imprime la cadena completa | pasa | Muestra la lista de versiones derivadas |
| P04 | E2 | Operación recursiva sobre un ítem sin derivados | | solo el ítem (caso base) | pasa | Muestra advertencia de Caso Base |
| P05 | E1 | Ver el detalle de una canción existente | Opción 2, ID = 1 | muestra todos los datos de la canción | pasa | Muestra detalle de 'De Música Ligera' |
| P06 | E1 | Ver el detalle de una canción que NO existe | Opción 2, ID = 999 | mensaje claro, no se corta el programa | pasa | Notifica canción no encontrada |
| P07 | E1 | Elegir una opción de menú inválida | Opción = "9z" | vuelve a mostrar el menú | pasa | Advierte opción no válida |
| P08 | E1 | Pasar ENTER vacío en el menú principal | Entrada = "" | no explota; vuelve a preguntar | pasa | Solicita nuevamente la opción |
| P09 | E3 | Agregar a la colección principal hasta el tope | Opción 4 con 7 canciones | el séptimo falla con excepción propia | pasa | Lanza ColeccionLlenaError y el menú sigue |
| P10 | E3 | Desapilar historial vacío | Opción 7 sin reproducciones | excepción propia, menú sigue | pasa | Lanza PilaVaciaError sin interrupción |
| P11 | E3 | Desencolar cola vacía | Opción 9 sin canciones encoladas | excepción propia, menú sigue | pasa | Lanza ColaVaciaError sin interrupción |
| P12 | E3 | Listar colección con el iterador | Opción 5 con 2+ canciones | el orden coincide con las inserciones | pasa | Recorre mediante for usando el iterador |
| P13 | E4 | Elegir opción 10, método 1 e ingresar el título | Crimen | Encuentra y muestra la canción | pasa | Muestra la canción ID 4 mediante búsqueda lineal |
| P14 | E4 | Elegir opción 10, método 1 e ingresar un título inexistente | Cancion inexistente | Muestra "Canción no encontrada", sin traceback; el menú continúa | pasa | La búsqueda termina sin coincidencias y permite seguir usando el menú |
| P15 | E4 | Iniciar el programa sin ordenar; elegir opción 10, método 2 e ingresar el título | Crimen | Avisa que ordena por título y encuentra la canción mediante búsqueda binaria | pasa | Muestra el aviso de ordenamiento y la canción ID 4 |
| P16 | E4 | Elegir opción 11, criterio 1, algoritmo 1; listar con opción 1. Luego elegir opción 11, criterio 2, algoritmo 2 y volver a listar | Título con selección; duración con inserción | El catálogo queda ordenado ascendentemente por cada criterio y cambia el orden del listado | pasa | Se comprueba el resultado de ambos ordenamientos mediante la opción 1 |
| P17 | E5 | Guardar catálogo en TXT, salir del programa y volver a cargarlo | Catálogo de 67 canciones | El catálogo se guarda y recupera correctamente desde el archivo TXT | pasa | Se guardó el catálogo en `data/canciones.txt` y, al reiniciar el programa, se cargaron correctamente las 67 canciones |
| P18 | E5 | Guardar catálogo en binario, modificar una canción por ID y volver a cargarlo | Catálogo de 67 canciones | El catálogo se guarda, permite modificar registros por ID y conserva los cambios al volver a cargarlo | pasa | Se guardó el catálogo en `data/canciones.bin`, se modificó un registro por ID y se comprobó que los cambios persistieron al cargar nuevamente el archivo |
| P19 | E5 | Intentar cargar un archivo binario truncado y otro con magia incorrecta | Archivos BIN inválidos | El sistema detecta los archivos inválidos y muestra mensajes de error sin interrumpir inesperadamente el programa | pasa | Se verificó la detección de archivos truncados y de archivos con magia incorrecta mediante los mensajes de error correspondientes |
