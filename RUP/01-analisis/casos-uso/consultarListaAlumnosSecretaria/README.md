# CGU > consultarListaAlumnos [Secretaria] > Análisis

> | [🏠️](/README.md) | [Análisis](/RUP/01-analisis/README.md) | [Detalle](/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Secretaria/) | **Análisis** | Diseño | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Inception
- **Disciplina**: Análisis
- **Caso de uso**: `consultarListaAlumnos()` [actor: Secretaria]
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-05-28

## propósito

> **Nota — scoping por grado.** Originalmente "completo" significaba "todos los alumnos del sistema". Una revisión posterior restauró la entidad `Grado` del SDR (`Grado → SecretariaAcademica : Gestionado por`), de modo que la Secretaria ve solo los alumnos cuyas matrículas pertenecen a su grado. La cascada del scoping aplica también a matrículas y dispensas en sus respectivos CUs. La estructura MVC no cambia; cambia el filtro: `obtenerTodos()` → `obtenerPorGrado(grado_id)`. Detalle en [[gestionarCatalogoGrados]].

Análisis del caso de uso `consultarListaAlumnos()` **invocado por la Secretaria** mediante diagrama de colaboración MVC. La Secretaria consulta el listado **completo** de alumnos del sistema, sin filtro por asignatura — a diferencia del CU homólogo del Profesor ([[consultarListaAlumnos]]), que filtra por asignaturas impartidas.

Es la **cuarta política del Controller polimórfico**, ahora aplicada sobre `AlumnoController` (las tres primeras estaban sobre `SolicitudDispensaController`). Refuerza el patrón "métodos específicos por rol" como dirección consolidada hacia 02-diseño.

## diagrama de colaboración

<div align=center>

|![Análisis consultarListaAlumnos() Secretaria](/images/RUP/01-analisis/casos-uso/consultarListaAlumnosSecretaria/colaboracion.svg)|
|-|
|**Disciplina**: Análisis RUP<br>**Enfoque**: Diagramas de colaboración MVC|

</div>


[Código PlantUML](/modelosUML/RUP/01-analisis/casos-uso/consultarListaAlumnosSecretaria/colaboracion.puml)
## discrepancia en el requisitado — nombres de transición

| Fuente | Nombre |
|-|-|
| Actor `DiagramaCompletoCasoDeUso.puml` package "Listas de alumnos" | **`consultarListaAlumnos()`** |
| Filename del detallado | `consultarListaAlumnos.puml` |
| Transición de entrada en el detallado | **`abrirLista()`** |
| Prototipo SALT | `abrirListaAlumnosSecretaria.png` |

El detallado y el prototipo usan **`abrirLista()`** para la transición; el actor y el filename usan **`consultarListaAlumnos()`** para el CU. Análisis adopta **`consultarListaAlumnos()`** como nombre canónico (matches actor + filename + índice del análisis).

**Deuda para 02-diseño**: reconciliar `abrirLista()` ↔ `consultarListaAlumnos()` en el detallado y los prototipos.

## clases de análisis identificadas

### clases model (naranja #F2AC4E)

| Clase | Responsabilidad | Trazabilidad |
|-|-|-|
| **Alumno** | Entidad de dominio (read-only en este CU) | Reutilizada de [[consultarListaAlumnos]] (Profesor) e [[importarListasAlumnos]] |
| **AlumnoRepository** | Recupera el listado completo de alumnos | Reutilizado; estrena `obtenerTodos() : List<Alumno>` (paralelo a `obtenerPorAsignatura` del Profesor) |

### clases view (azul #629EF9)

| Clase | Responsabilidad | Derivación |
|-|-|-|
| **ConsultarListaAlumnosSecretariaView** | Listado tabular sin selector de asignatura: columnas Alumno, Nº Carnet, Grado, Curso, Estado | [Prototipo SALT `abrirListaAlumnosSecretaria.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Secretaria/abrirListaAlumnosSecretaria.png) |

**Diferencia visual con la vista del Profesor**: idéntica estructura tabular pero **sin pestañas** en la cabecera. El Profesor veía una pestaña por asignatura impartida; la Secretaria ve la lista global directamente.

### clases controller (verde #b5bd68)

| Clase | Responsabilidad | Casos de uso |
|-|-|-|
| **AlumnoController** | Orquestación del acceso a `Alumno`; **estrena el método sin filtro de asignatura** | Compartido con [[consultarListaAlumnos]] (Profesor), [[consultarDetalleAlumno]] e [[importarListasAlumnos]] |

### colaboraciones (verde claro #CDEBA5)

| Colaboración | Propósito | Invocación |
|-|-|-|
| **:Listas Abierto** | Estado de origen — la Secretaria en el módulo de listas | Punto de entrada |

## mensajes de colaboración

### flujo principal

| # | Origen | Destino | Mensaje | Intención |
|-|-|-|-|-|
| 1 | **:Listas Abierto** | **ConsultarListaAlumnosSecretariaView** | `consultarListaAlumnos()` | Abrir el listado completo |
| 2 | **ConsultarListaAlumnosSecretariaView** | **AlumnoController** | `cargarTodos() : List<Alumno>` | Recuperar todos los alumnos del sistema |
| 3 | **AlumnoController** | **AlumnoRepository** | `obtenerTodos() : List<Alumno>` | Consulta sin filtro |

### flujo alternativo — cerrar la lista

El detallado contempla `cerrarLista()` (transición roja) para volver a `:Listas Abierto`. En el análisis equivale a que la vista se cierre. Sin clase adicional.

### flujo alternativo — mantener la lista abierta para operaciones detalladas

El detallado menciona una **salida 1** explícita: "Sistema permite mantener la lista abierta para operaciones detalladas". Esto sugiere que el estado posterior (`LISTA_ABIERTA`) habilita acciones derivadas — probablemente el menú contextual de cada fila (`verDetalleAlumno()` del bloque "Alumnos", no migrado al análisis, o un eventual `verDetalleMatricula()` del bloque "Matrículas").

Análisis: este CU es **read-only puro**, las acciones derivadas son invocación de **otros CUs** desde `:Lista Abierta` (no `<<include>>`). Igual que la lista del Profesor habilita `consultarDetalleAlumno()`.

## cuarta política del Controller polimórfico — ahora sobre `AlumnoController`

Hasta ahora el polimorfismo del Controller se había manifestado solo sobre `SolicitudDispensaController` (Alumno/Profesor/Director). Este CU lo aplica también a `AlumnoController`, generalizando el patrón:

| Controller | Rol | Filtro/política |
|-|-|-|
| **`AlumnoController`** | Profesor (en [[consultarListaAlumnos]]) | Por asignatura impartida |
| **`AlumnoController`** | **Secretaria (este CU)** | **Sin filtro — visión global** |
| `SolicitudDispensaController` | Alumno | Por propiedad |
| `SolicitudDispensaController` | Profesor | Por asignaturas impartidas |
| `SolicitudDispensaController` | Director | Sin filtro |

**Implicación para 02-diseño**: el patrón "métodos específicos por rol" (camino (c) consolidado en [[editarSolicitudDispensaDirector]] y [[consultarSolicitudDispensaProfesor]]) se aplica también a `AlumnoController`:

```
AlumnoController.cargarListaParaProfesor(asignatura)   // con filtro
AlumnoController.cargarListaParaSecretaria()           // sin filtro
```

Alternativa más uniforme: un método `cargarLista(filtro)` con un objeto `Filtro` que vive en la Sesion. Decisión final pertenece a 02-diseño.

## sin verificación de acceso — la Secretaria es operadora global

La Secretaria no tiene restricción de visibilidad sobre alumnos. No hay regla "Secretaria competente" como sí había "Profesor competente". La política emerge del rol:

- Profesor: opera sobre **su** docencia → filtro por asignaturas impartidas.
- **Secretaria**: opera sobre **el sistema completo** → sin filtro.
- Director: opera sobre **flujo administrativo de dispensas** → sin filtro (en su scope).

Este CU **no necesita validación adicional en el Controller** más allá de "el `Sesion.usuario` es una `Secretaria`" — que viene resuelto desde [[iniciarSesion]] como decisión de autorización a nivel router/middleware. **Deuda para 02-diseño**: confirmar política de autorización (defensa en profundidad en el Controller, o solo en el router).

## comparación con el CU homólogo del Profesor

| Característica | [[consultarListaAlumnos]] (Profesor) | `consultarListaAlumnos` (Secretaria) |
|-|-|-|
| Mensajes | 3 | 3 |
| Origen | `:Listas Abierto` | `:Listas Abierto` |
| Parámetro del CU | `asignatura` | (ninguno) |
| Filtro | Por asignatura impartida | **Sin filtro** |
| Selector de pestañas | Sí (asignaturas) | **No** |
| Verificación | "Profesor competente" | (ninguna) |
| Método del Repository | `obtenerPorAsignatura(asignatura)` | `obtenerTodos()` |
| Vista | `ConsultarListaAlumnosView` | `ConsultarListaAlumnosSecretariaView` |

Las 6 diferencias justifican el análisis separado (mismo patrón que [[editarSolicitudDispensaDirector]] vs [[editarSolicitudDispensa]]).

## sin destino — read-only puro

Igual que [[consultarListaAlumnos]] del Profesor: el destino a "detalle" no se modela como `<<include>>` — es invocación de otro CU desde `:Lista Abierta`. Consistencia mantenida.

## enlaces de dependencia

- **ConsultarListaAlumnosSecretariaView** conoce a **AlumnoController** (delegación)
- **AlumnoController** conoce a **AlumnoRepository** (lectura)
- **AlumnoController** conoce a **Alumno** (manipulación entidad)
- **AlumnoRepository** conoce a **Alumno** (gestión)

(Notar la ausencia: el Controller **no** necesita conocer a `Sesion` en este CU — no hay filtro contextual, solo el `obtenerTodos()`.)

## trazabilidad con artefactos previos

### con especificación detallada

- **`LISTAS_ABIERTO_INICIAL`** → colaboración `:Listas Abierto` (origen)
- **Transición `abrirLista()`** → mensaje 1 (renombrado `consultarListaAlumnos()` por discrepancia documentada)
- **Estado `CONSULTAR_LISTA_COMP` con sub-estado `MostrarLista`** → `ConsultarListaAlumnosSecretariaView` + mensajes 2-3
- **Nota "Sistema muestra la lista solicitada por el usuario"** → contenido de la vista
- **Salida 1 (`LISTA_ABIERTA_FINAL`)** → estado posterior que habilita CUs de detalle (no modelado como mensaje)
- **Salida 2 (`cerrarLista()`)** → flujo alternativo

### con wireframe (prototipo SALT)

- **`abrirListaAlumnosSecretaria.png`** → tabla de alumnos sin pestañas → `ConsultarListaAlumnosSecretariaView`. Idéntica estructura visual a la del Profesor (`consultarListaAlumnos.png`) **excepto la ausencia del selector de pestañas**. Confirma la decisión: la Secretaria ve global, el Profesor ve filtrado

### con actores

- **`SecretariaAcademica --> ListasConsultarLista`** en package "Listas de alumnos" → invocación del CU (discrepancia de nombre de actor documentada en [[importarMatriculas]])

### con modelo del dominio

- **Sin trazabilidad directa**: deuda heredada de [[consultarListaAlumnos]] del Profesor.

## principios de análisis aplicados

### patrón mvc

- **Controller por entidad**: `AlumnoController` reutilizado (cuarto CU que lo usa)
- **Vista específica por rol**: sin selector de pestañas
- **Sin polimorfismo en la entidad**: `Alumno` concreta

### diagramas de colaboración

- **3 mensajes**: CU mínimo, idéntico al homólogo del Profesor en estructura
- **Sin destino**: read-only puro
- **Sin verificación contextual**: la Secretaria no aplica filtro de propiedad

### análisis puro

- **Sin paginación / filtros**: el prototipo los muestra (paginación 1-14 de 332 elementos, 24 páginas) pero pertenecen a presentación
- **Sin búsqueda interna**: el campo "Filtrar alumnos" del prototipo es UI, no parámetro del CU

## características del análisis

### responsabilidades identificadas

- **ConsultarListaAlumnosSecretariaView**: presentar listado tabular global
- **AlumnoController**: cargar todos los alumnos sin filtro
- **AlumnoRepository**: recuperar el conjunto completo
- **Alumno**: representar las entidades listadas

### relaciones conceptuales

- **Delegación**: vista → controlador
- **Sin filtrado**: política de "operador global" propia del rol Secretaria

## conexión con disciplinas rup

### desde requisitos

- **Detallado**: `LISTA_ABIERTA` → vista; `cerrarLista()` → flujo alternativo
- **Prototipo SALT**: tabla sin pestañas → vista con visión global
- **Actores**: `Secretaria --> consultarListaAlumnos()` en package "Listas de alumnos"

### hacia diseño

- **Reconciliar `abrirLista()` ↔ `consultarListaAlumnos()`** en el detallado del SDR
- **Materialización del polimorfismo de `AlumnoController`**: métodos específicos por rol vs filtro genérico parametrizado por `Sesion`
- **Política de autorización**: ¿defensa en profundidad en Controller (revalidación de que `Sesion.usuario` es `Secretaria`) o solo router/middleware?
- **Paginación / filtros / búsqueda** en el listado (332 elementos según prototipo → relevante)
- **Ordenación** del listado (por carnet, por curso, por grado, alfabético)

**Código fuente:** [colaboracion.puml](/modelosUML/RUP/01-analisis/casos-uso/consultarListaAlumnosSecretaria/colaboracion.puml)

## referencias

- [Detallado `consultarListaAlumnos()` (Secretaria)](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Secretaria/consultarListaAlumnos.puml)
- [Prototipo SALT `abrirListaAlumnosSecretaria.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Secretaria/abrirListaAlumnosSecretaria.png)
- [Caso de uso de Secretaria](/modelosUML/RUP/00-requisitos/CasosDeUso/CasoDeUso/Secretaria/DiagramaCompletoCasoDeUso.puml)
- [Análisis `consultarListaAlumnos()` (Profesor)](/RUP/01-analisis/casos-uso/consultarListaAlumnos/README.md)
- [Análisis `consultarSolicitudesDispensas()` (Director)](/RUP/01-analisis/casos-uso/consultarSolicitudesDispensas/README.md) — paralelo "sin filtro" sobre otra entidad
- [conversation-log.md](/conversation-log.md)
