# Informe del TP

## 1. Grupo y tema

- **Tema:** Biblioteca Musical
- **Por qué lo eligieron:** Elegimos este tema porque, a diferencia de opciones más comunes como Pokédex, nos pareció un dominio con mayor flexibilidad. Una colección de música nos permite experimentar con diversas funciones y atributos variados (artistas, géneros, duraciones). Además, resulta muy práctico para modelar de forma natural las estructuras que pide la materia, como listas de reproducción, historial (pilas) y colas de reproducción.


## 2. Modelo

Un ítem del catálogo representa una canción individual del archivo `canciones.txt`, que es almacenada temporalmente como un diccionario de Python con los campos `id`, `titulo`, `artista`, `album`, `genero`, `anio` y `duracion_seg`.

### Mutabilidad

- **Inmutables:**
 - `id` (cadena/entero): Identificador único del registro que no debe cambiar.
 - `titulo`, `artista`, `album`, `genero` (str): Las cadenas de texto son inmutables en Python; cualquier modificación genera un nuevo objeto.
 - `anio`, `duracion_seg` (int): Los tipos de datos numéricos básicos son inmutables por definición.
- **Mutables:**
  - `cancion` (dict): Contenedor de datos por tema que admite cambios en sus valores.
  - `catalogo` (list): Lista lineal completa de canciones cargadas desde el archivo, permite operaciones de inserción, eliminación y reordenamiento.

### Relación entre componentes del sistema

```text
[ Archivo data/canciones.txt ]
               │
               ▼  (Carga secuencial)
       [ Catálogo General ]
               │
   ┌───────────┼───────────┐
   ▼           ▼           ▼
[Colección]  [ Pila ]   [ Cola ]
Principal  Historial  Reproducción
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
