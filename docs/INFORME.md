# Informe del TP

## 1. Grupo y tema

- **Tema:** Biblioteca Musical
- **Por qué lo eligieron:** Elegimos este tema porque, a diferencia de opciones más comunes como Pokédex, nos pareció un dominio con mayor flexibilidad. Una colección de música nos permite experimentar con diversas funciones y atributos variados (artistas, géneros, duraciones). Además, resulta muy práctico para modelar  las estructuras como, listas de reproducción, historial (pilas) y colas de reproducción.


## 2. Modelo

Un ítem del catálogo representa una canción individual definida dentro del módulo de dominio, la cual es representada como un diccionario de Python con los campos `id`, `titulo`, `artista`, `album`, `genero`, `anio` y `duracion_seg`.

### Mutabilidad

- **Inmutables:**
 - `id` (str/int): Identificador único de la canción. Se define inmutable para garantizar la integridad referencial y evitar que la clave primaria del ítem cambie accidentalmente, lo que rompería las búsquedas.
 - `titulo`, `artista`, `album`, `genero` (str): Las cadenas de texto son inmutables en Python. Elegirlas así asegura la integridad de los metadatos base, evitando efectos secundarios o modificaciones colaterales no deseadas en memoria durante la ejecución.
 - `anio`, `duracion_seg` (int): Tipos numéricos básicos e inmutables por definición del lenguaje, ideales para proteger los valores cuantitativos de la canción.
- **Mutables:**
  - `cancion` (dict): Diccionario dinámico que representa la entidad. Permite modificar atributos o corregir datos sin necesidad de recrear toda la estructura del tema en memoria.
  - `catalogo` (list): Colección lineal mutable. Se elige una lista para permitir la inserción, eliminación y reordenamiento dinámico de los temas dentro del sistema.
### Relación entre componentes del sistema

```text
+-------------------------------------------------------------+
|                      BIBLIOTECA MUSICAL                     |
+-------------------------------------------------------------+
                               |
                               v
               +-------------------------------+
               |      Catálogo (list/dict)     |
               +-------------------------------+
                               |
        +----------------------+----------------------+
        |                      |                      |
        v                      v                      v
+---------------+      +---------------+      +---------------+
| Colección     |      | Historial     |      | Cola de       |
| Principal     |      | (Pila - TADS) |      | Reproducción  |
| (Listas)      |      +---------------+      | (Cola - TADS) |
+---------------+                             +---------------+
```
## 3. Recursión (E2)

- Función:
- Caso base:
- Caso recursivo:
- Traza de un ejemplo real del dataset:

## 4. TADs (E3)

| TAD | Operaciones | Invariante |
| --- | --- | --- |
| ListaEnlazada |  |  |
| Pila |  |  |
| Cola |  |  |

Dónde se usa cada uno en el dominio.

## 5. Complejidad (E4)

| Operación | Tiempo | Espacio | Por qué |
| --- | --- | --- | --- |
|  |  |  |  |

Mediciones (`time.perf_counter`):

| Operación | n | segundos |
| --- | --- | --- |
|  |  |  |

## 6. Persistencia (E5)

- Layout del registro binario (campos, `struct`, anchos):
- Header:
- Cómo se actualiza un registro por posición:

## 7. Reparto de trabajo (E6)

| Integrante | Qué hizo | Qué puede defender |
| --- | --- | --- |
|  |  |  |
