# Informe del TP

## 1. Grupo y tema
- **Integrantes:** Eber Garcia y Kain Samaniego.
- **Tema:** Biblioteca Musical
- **Por qué lo eligieron:** Elegimos este tema porque, a diferencia de opciones más comunes como Pokédex, nos pareció un dominio con mayor flexibilidad. Una colección de música nos permite experimentar con diversas funciones y atributos variados (artistas, géneros, duraciones). Además, resulta muy práctico para modelar  las estructuras como, listas de reproducción, historial (pilas) y colas de reproducción.


## 2. Modelo

Un ítem del catálogo es un objeto de la clase `Cancion`, con los atributos
`id`, `titulo`, `artista`, `album`, `genero`, `anio` y `duracion_seg`.

### Mutabilidad

Los valores de tipo `str` e `int` son inmutables: una modificación implica
asignar otro valor al atributo correspondiente.

Los objetos `Cancion` son mutables porque sus atributos pueden reasignarse.
El ABM mantiene el ID al modificar una canción y reemplaza el objeto del
catálogo por uno nuevo con los datos actualizados. La clase no impide
reasignar el ID directamente.

El catálogo es una lista mutable de objetos `Cancion`. Permite agregar,
eliminar, reemplazar y ordenar sus elementos.

### Relación entre componentes del sistema

- `Biblioteca` administra el catálogo y las relaciones entre canciones
  utilizadas por la operación recursiva.
- `Playlist` almacena canciones seleccionadas en una `ListaEnlazada`,
  con un máximo de seis elementos.
- `Pila` mantiene el historial de reproducción con comportamiento LIFO.
- `Cola` mantiene las canciones pendientes con comportamiento FIFO.
- La persistencia guarda y recupera el catálogo en texto y binario.

## 3. Recursión (E2)

**Función:** `obtener_versiones_derivadas(id_cancion)`

**Caso base:** Si la canción no tiene versiones ni derivados directos (`directas == []`) $\rightarrow$ devolver `[]`.

**Caso recursivo:** `list(directas) + obtener_versiones_derivadas(v)`

---

**Traza para "De Música Ligera" (ID 1):** Según el catálogo y mapa de versiones, la canción ID 1 deriva en la canción ID 62 ("De Música Ligera - Unplugged").

* **Llamada 1:** `obtener_versiones_derivadas(1)` $\rightarrow$ tiene versión directa (ID 62)
  $\rightarrow$ devuelve `[62] + obtener_versiones_derivadas(62)`

* **Llamada 2:** `obtener_versiones_derivadas(62)` $\rightarrow$ NO tiene versiones derivadas (caso base)
  $\rightarrow$ devuelve `[]`

**Resultado final:** `[62] + [] = [62]`

## 4. TADs (E3)

| TAD | Operaciones | Invariante |
| --- | --- | --- |
| **ListaEnlazada** | `insertar_al_inicio`, `insertar_al_final`, `eliminar`, `buscar`, `tamanio`, `esta_vacia`, `__iter__` | Cadena de objetos `Nodo` enlazados secuencialmente mediante la referencia `siguiente`. El último nodo apunta a `None`. `_tamanio` refleja en todo momento la cantidad exacta de elementos presentes. |
| **Pila** | `apilar`, `desapilar`, `ver_tope`, `esta_vacia` | Estructura LIFO. Tanto el apilado como el desapilado ocurren exclusivamente por la cabeza de la `ListaEnlazada` interna, garantizando un acceso $O(1)$. |
| **Cola** | `encolar`, `desencolar`, `ver_frente`, `esta_vacia` | Estructura FIFO. La inserción de elementos se realiza al final de la `ListaEnlazada` interna y la extracción se hace siempre desde la cabeza. |

### Dónde se utiliza cada estructura en el dominio

* **`ListaEnlazada`:** Es la estructura principal que se utiliza como base para implementar la `Pila` y la `Cola`. También se utiliza para almacenar las canciones de la `Playlist`, con una capacidad máxima de 6 canciones (`_tope = 6`). Además, permite recorrer sus elementos mediante su propio iterador (`__iter__`).
* **`Pila`:** Se utiliza para mantener el historial de reproducción. Cada canción que se reproduce se agrega mediante `apilar`, quedando en la parte superior. Si el usuario selecciona *"Deshacer última reproducción"*, se utiliza `desapilar` para quitar la canción reproducida más recientemente, siguiendo el principio LIFO.
* **`Cola`:** Se utiliza para administrar las canciones pendientes de reproducción. Las canciones se agregan mediante `encolar` según el orden en que se solicitan y se reproducen mediante `desencolar`, respetando el principio FIFO.
## 5. Complejidad (E4)

| Operación | Tiempo (Peor) | Tiempo (Mejor)| Espacio | Por qué |
| :--- | :--- | :--- | :--- | :--- |
| **Listar catálogo** | $O(n)$ | $O(n)$ | $O(1)$ | Recorre todos los elementos del catálogo uno por uno con el iterador de la lista. |
| **Búsqueda lineal** | $O(n)$ | $O(1)$ | $O(1)$ | Va mirando elemento por elemento en un bucle `for` hasta encontrar la canción o llegar al final. |
| **Búsqueda binaria** | $O(\log n)$ | $O(1)$ | $O(1)$ | Necesita que la lista esté ordenada. En cada paso calcula el punto medio y descarta la mitad que no sirve. |
| **Ordenar por selección** | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Para cada posición, recorre los elementos restantes buscando el mínimo. Realiza una cantidad cuadrática de comparaciones, incluso si el catálogo ya está ordenado, y como máximo un intercambio por posición. |
| **Ordenar por inserción** | $O(n^2)$ | $O(n)$ | $O(1)$ | Si ya está ordenada hace 1 sola comparación por elemento ($O(n)$); si está al revés, tiene que desplazar todo hacia atrás ($O(n^2)$). |
| **Ver detalle de un ítem** | $O(n)$ | $O(1)$ | $O(1)$ | Recorre la colección hasta encontrar la coincidencia por ID. |

Las cotas de búsqueda y ordenamiento corresponden a los algoritmos sobre
el catálogo en memoria. La opción de búsqueda binaria del CLI también
ordena previamente y guarda los archivos, por lo que su costo total
incluye esas operaciones.

Mediciones (`time.perf_counter`):

| Operación | n | segundos |
| --- | --- | --- |
| Busqueda lineal | 26 | 0.000002900 | 
| Busqueda lineal | 260 | 0.000003000 | 
| Búsqueda binaria | 26 | 0.000003200 |
| Búsqueda binaria | 260 | 0.000002200 |

## 6. Persistencia (E5)

### Persistencia en texto

Se utiliza un archivo CSV (`canciones.txt`) para almacenar el catálogo. La lectura se realiza mediante `csv.DictReader` y la escritura mediante `csv.DictWriter`. Se verifica que el encabezado coincida con los campos esperados y que cada fila tenga la cantidad correcta de datos.

### Persistencia binaria

Se utiliza el módulo `struct` para guardar registros de longitud fija.

**Header:**

- Formato: `struct.Struct("<4s 1s I")`
- Magia: `AYED` (4 bytes).
- Tema: `M` (1 byte).
- Cantidad de registros: entero sin signo (4 bytes).
- Tamaño total: 9 bytes.

**Registro de canción:**

Formato: `struct.Struct("<I 30s 25s 30s 12s 2H")`

| Campo | Tipo | Tamaño |
|---|---|---:|
| ID | `I` | 4 bytes |
| Título | `30s` | 30 bytes |
| Artista | `25s` | 25 bytes |
| Álbum | `30s` | 30 bytes |
| Género | `12s` | 12 bytes |
| Año | `H` | 2 bytes |
| Duración en segundos | `H` | 2 bytes |
| **Total** | | **105 bytes** |

El prefijo `<` indica que los datos se almacenan en little-endian, sin alineación automática.

### Actualización de un registro por posición

Para modificar un registro se utiliza el método `seek()` del archivo binario. La posición se calcula mediante:

`HEADER.size + posicion * FORMATO.size`

De esta manera, se accede directamente al registro correspondiente sin necesidad de reescribir todo el archivo. Luego se utiliza `write()` para sobrescribir sus datos.

### Alta y baja persistentes

El alta agrega un registro al final del archivo binario y actualiza la
cantidad de registros del header.

La baja elimina el registro indicado por su posición y reescribe el
archivo con los registros restantes, actualizando también el header.

El archivo de texto se reescribe con el catálogo completo después
de cada alta, baja o modificación.

### Sincronización

Después de ordenar el catálogo, incluso para realizar una búsqueda
binaria, o de cargarlo desde texto o binario, se guardan ambos formatos.
Así, el orden de los registros del binario coincide con el catálogo
en memoria y permite actualizar o eliminar por posición.

### Cadenas de longitud fija

Las cadenas se codifican en UTF-8. Si superan el ancho del campo,
se recortan sin cortar un carácter multibyte. Si son más cortas,
se completan con bytes nulos.

Esta representación puede perder parte de los textos largos.
Por ejemplo, el campo artista admite hasta 25 bytes.

## 7. Reparto de trabajo (E6)

| Integrante | Qué hizo | Qué puede defender |
| --- | --- | --- |
| Eber Garcia | Organización inicial del repositorio e integración de entregas. Integración de búsquedas y ordenamientos en el CLI, corrección de la búsqueda binaria y de parámetros de los ordenamientos. Incorporación de mediciones de rendimiento y actualización de los casos de prueba de E4. Revisión y actualización del informe para E6. | Búsqueda lineal y binaria, requisito de orden previo, ordenamiento por selección e inserción, integración de los algoritmos con el menú, complejidad temporal y mediciones con time.perf_counter. |
| Kain Samaniego | Desarrollo del menú inicial y de las clases del dominio. Implementación de la operación recursiva de versiones, ListaEnlazada, Pila, Cola y Playlist con tope. Implementación inicial de búsquedas y ordenamientos. Desarrollo de persistencia en texto y binario, actualización por posición e integración del ABM persistente. Documentación y actualización del protocolo de pruebas de esas funcionalidades. | Modelo de Cancion y Biblioteca, caso base y caso recursivo, invariantes de los TADs, iterador, comportamiento LIFO y FIFO, control del tope, lectura y escritura de archivos, layout binario con struct, cálculo del seek y ABM persistente. |
