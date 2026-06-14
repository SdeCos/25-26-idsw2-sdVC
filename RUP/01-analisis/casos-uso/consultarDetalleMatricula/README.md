# CGU > consultarDetalleMatricula > Análisis

> | [🏠️](/README.md) | [Análisis](/RUP/01-analisis/README.md) | [Detalle](/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Secretaria/) | **Análisis** | Diseño | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Inception
- **Disciplina**: Análisis
- **Caso de uso**: `consultarDetalleMatricula()`
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-05-28

## propósito

Análisis del caso de uso `consultarDetalleMatricula()` mediante diagrama de colaboración MVC. La Secretaria consulta la **ficha completa** de una matrícula desde el listado: datos del alumno (nombre, identidad), contexto académico (curso académico, facultad, plan de estudios) y **lista completa de asignaturas matriculadas** (con código, ECTS, curso, carácter, nº matrícula).

Es el CU read-only del bloque "Matrículas" de la Secretaria, paralelo a [[consultarDetalleAlumno]] del Profesor pero centrado en la entidad `Matricula` en lugar de `Alumno`. Confirma `Matricula` como **agregado complejo** con su colección de asignaturas matriculadas.

## diagrama de colaboración

<div align=center>

|![Análisis consultarDetalleMatricula()](/images/RUP/01-analisis/casos-uso/consultarDetalleMatricula/colaboracion.svg)|
|-|
|**Disciplina**: Análisis RUP<br>**Enfoque**: Diagramas de colaboración MVC|

</div>


[Código PlantUML](/modelosUML/RUP/01-analisis/casos-uso/consultarDetalleMatricula/colaboracion.puml)
## discrepancia en el requisitado — nombres de transición

| Fuente | Nombre |
|-|-|
| Actor `DiagramaCompletoCasoDeUso.puml` package "Matrículas" | **`consultarDetalleMatricula()`** |
| Filename del detallado | `consultarDetalleMatricula.puml` |
| Título interno del detallado | `Ver detalle de matrícula` |
| Transición de entrada en el detallado | **`verDetalleMatricula()`** |
| Transición de salida en el detallado | `cerrarDetalleMatricula()` |

Análisis adopta **`consultarDetalleMatricula()`** como nombre canónico (matches actor + filename + índice del análisis). El nombre `verDetalleMatricula()` es probable un eco del primer nombre del CU (también aparece en `importarMatricula.puml` como transición a `verDetalleMatricula()`). Mismo patrón de discrepancia que con `abrirLista()` ↔ `consultarListaAlumnos()` en [[consultarListaAlumnosSecretaria]].

**Deuda para 02-diseño**: reconciliar terminología en detallado/notas.

## clases de análisis identificadas

### clases model (naranja #F2AC4E)

| Clase | Responsabilidad | Trazabilidad |
|-|-|-|
| **Matricula** | Entidad de dominio; se confirma como **agregado complejo** con su colección de asignaturas matriculadas | Reutilizada de [[importarMatriculas]]; **gana atributos** desde el prototipo |
| **MatriculaRepository** | Recupera la matrícula por id, con su agregado de asignaturas | Reutilizado; estrena `obtenerPorId(matriculaId) : Matricula` |

### clases view (azul #629EF9)

| Clase | Responsabilidad | Derivación |
|-|-|-|
| **ConsultarDetalleMatriculaView** | "Ficha Matrícula": datos del alumno (Nombre, Nº Identidad), contexto académico (Curso Académico, Facultad, Plan de Estudios) y tabla de asignaturas (Código, Asignatura, ECTS, Curso, Carácter, Nº Matrícula) | [Prototipo SALT `consultarDetalleMatricula.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Secretaria/consultarDetalleMatricula.png) |

### clases controller (verde #b5bd68)

| Clase | Responsabilidad | Casos de uso |
|-|-|-|
| **MatriculaController** | Orquestación del acceso a `Matricula` | Compartido con [[importarMatriculas]] |

### colaboraciones (verde claro #CDEBA5)

| Colaboración | Propósito | Invocación |
|-|-|-|
| **:Matriculas Abierto** | Estado de origen — la Secretaria en el listado de matrículas | Punto de entrada |

## mensajes de colaboración

### flujo principal

| # | Origen | Destino | Mensaje | Intención |
|-|-|-|-|-|
| 1 | **:Matriculas Abierto** | **ConsultarDetalleMatriculaView** | `consultarDetalleMatricula(matriculaId)` | Abrir la ficha de la matrícula seleccionada |
| 2 | **ConsultarDetalleMatriculaView** | **MatriculaController** | `cargarDetalle(matriculaId) : Matricula` | Recuperar el agregado completo |
| 3 | **MatriculaController** | **MatriculaRepository** | `obtenerPorId(matriculaId) : Matricula` | Consulta |

### flujo alternativo — cerrar la ficha

El detallado contempla `cerrarDetalleMatricula()` para volver a `:Matriculas Abierto`. El prototipo lo refleja con el botón "Volver". Sin clase adicional.

## `Matricula` como agregado complejo — atributos enriquecidos del prototipo

`Matricula` debutó en [[importarMatriculas]] con atributos básicos del listado: `numIdentidad`, `alumno`, `curso`, `grado`, `fechaImportacion`. El prototipo de detalle revela **muchos más atributos**:

| Atributo | Origen | Notas |
|-|-|-|
| `numIdentidad` | "Nº Identidad: Z1234567G" | Ya identificado |
| `alumno` (nombre + DNI) | "Nombre del Alumno/a" | Ya identificado, ahora con detalle |
| `cursoAcademico` | "Curso Académico: 2025-2026" | Refinamiento de `curso` (años académicos) |
| `facultad` | "Facultad: Escuela Politécnica Superior" | **Nuevo** |
| `planEstudios` | "Plan de Estudios: Ingeniería Informática" | **Nuevo** (probablemente sinónimo o atributo del grado/programa) |
| `asignaturasMatriculadas` | Tabla con `codigo, asignatura, ects, curso, caracter, nMatricula` | **Nueva colección — `Matricula` es agregado** |

Cada fila de la tabla es una **`AsignaturaMatriculada`** (entidad o value object dentro del agregado):

| Atributo | Ejemplo | Notas |
|-|-|-|
| `codigo` | IYA038 | Identificador único institucional |
| `asignatura` | Ingeniería de Software I | Nombre |
| `ects` | 6.00 | Créditos |
| `curso` | 3 | Curso del plan en que se imparte |
| `caracter` | OB | "Obligatoria" / "Optativa" / "Formación Básica"... (enum) |
| `nMatricula` | 1 | **Veces que el alumno se ha matriculado** en esta asignatura (1ª/2ª/3ª convocatoria) |

**Implicaciones para el modelo del dominio**:

1. **`Matricula` es un agregado** con `Alumno` como raíz contextual y colección de `AsignaturaMatriculada`.
2. **`Asignatura`** emerge como entidad propia (no atributo plano) — tiene código institucional único, ECTS, carácter.
3. **`AsignaturaMatriculada`** es la **tabla intermedia** entre `Matricula` y `Asignatura`, con su propio atributo `nMatricula` (semántica de convocatoria).
4. **`Facultad`** y **`PlanDeEstudios`** son catálogos institucionales (entidades de dominio académico).

Es **el primer agregado complejo** del análisis. Deuda crítica para 02-diseño: promover toda esta estructura al modelo del dominio.

## ¿modelar todas las entidades emergentes ahora?

**Decisión de análisis**: no se modelan formalmente como rectángulos del diagrama. Razones:

1. **Análisis puro**: el CU es read-only sobre el agregado completo; no se manipulan las sub-entidades.
2. **YAGNI**: `Asignatura`, `Facultad`, `PlanDeEstudios`, `AsignaturaMatriculada` no son operadas por ningún CU del análisis directamente — emergen solo como datos de la ficha.
3. **Consistencia**: igual decisión que con `Asistencia` (referenciada en [[consultarDetalleAlumno]] pero modelada formalmente solo en [[registrarTomaAsistencia]]).

`Matricula` se carga como agregado completo — el Repository entrega un grafo. Cómo se materializa (lazy loading, eager fetch, paginación de asignaturas) es decisión de diseño.

**Deuda para 02-diseño**: modelar el aggregate completo con sus sub-entidades.

## sin verificación de acceso — paralelo a `consultarListaAlumnosSecretaria`

Misma política que en [[consultarListaAlumnosSecretaria]]: la Secretaria es operadora global, sin filtro de propiedad. El `MatriculaController` no aplica verificación contextual.

## comparación con `consultarDetalleAlumno` (Profesor)

| Característica | [[consultarDetalleAlumno]] (Profesor) | `consultarDetalleMatricula` (Secretaria) |
|-|-|-|
| Mensajes | 3 | 3 |
| Entidad central | `Alumno` (con asistencias agregadas) | `Matricula` (con asignaturas agregadas) |
| Filtro de subdatos | Asistencias por asignaturas del Profesor | Sin filtro (agregado completo) |
| Verificación | "Profesor competente" | (ninguna) |
| Vista | Ficha enriquecida con secciones colapsables | Ficha plana (sin colapsables aparentes) |
| Controller | `AlumnoController` | `MatriculaController` |

Ambos son CUs read-only de ficha enriquecida, pero la diferencia entre **agregado del Alumno (con asistencias filtradas)** vs **agregado de la Matricula (con asignaturas completas)** refleja la diferencia de rol:

- Profesor: necesita ver el alumno en **su contexto docente** (asistencias propias).
- Secretaria: necesita ver el alumno en **su contexto administrativo** (matrícula académica completa).

## sin destino — read-only puro

Igual que los otros consultar de ficha del proyecto. La acción posterior (cerrar ficha) es estado.

## enlaces de dependencia

- **ConsultarDetalleMatriculaView** conoce a **MatriculaController** (delegación)
- **MatriculaController** conoce a **MatriculaRepository** (lectura)
- **MatriculaController** conoce a **Matricula** (manipulación entidad)
- **MatriculaRepository** conoce a **Matricula** (gestión)

(Sin dependencias a `Sesion` — sin filtro contextual.)

## trazabilidad con artefactos previos

### con especificación detallada

- **`MATRICULAS_ABIERTO_INICIAL`** → colaboración `:Matriculas Abierto` (origen)
- **Transición `verDetalleMatricula()`** → mensaje 1 (renombrado `consultarDetalleMatricula()` por discrepancia documentada)
- **Estado `MATRICULA_ABIERTA_COMP` con sub-estado `VisualizacionDetalle`** → `ConsultarDetalleMatriculaView` + mensajes 2-3
- **Nota "Sistema presenta todos los datos asociados a la matrícula seleccionada para su consulta"** → contenido enriquecido de la vista
- **Transición `cerrarDetalleMatricula()`** → flujo alternativo

### con wireframe (prototipo SALT)

- **`consultarDetalleMatricula.png`** → "Ficha Matrícula" con datos del alumno + contexto académico + tabla de asignaturas matriculadas → `ConsultarDetalleMatriculaView`

### con actores

- **`SecretariaAcademica --> MatriculasVerDetalle`** en package "Matrículas" → invocación del CU

### con modelo del dominio

- **Sin trazabilidad directa**: deuda crítica. `Matricula` no está en el modelo del SDR, ni las entidades derivadas (`Asignatura`, `Facultad`, `PlanDeEstudios`, `AsignaturaMatriculada`).

## principios de análisis aplicados

### patrón mvc

- **Controller por entidad**: `MatriculaController` reutilizado
- **Vista de ficha enriquecida**: tabla embebida sin operaciones de modificación
- **Sin polimorfismo en la entidad**: `Matricula` concreta

### diagramas de colaboración

- **3 mensajes**: CU mínimo
- **Sin destino**: read-only puro
- **Sin verificación contextual**: política Secretaria global

### análisis puro

- **Sin modelado formal de sub-entidades del agregado**: `Asignatura`, `Facultad`, etc. emergen como datos, no como clases del diagrama
- **Sin política de paginación de asignaturas**: el prototipo muestra 7 filas, pero un plan completo de Ingeniería tiene ~40 asignaturas — deuda

## características del análisis

### responsabilidades identificadas

- **ConsultarDetalleMatriculaView**: presentar ficha de matrícula con datos del alumno + asignaturas
- **MatriculaController**: cargar el agregado
- **MatriculaRepository**: recuperar la matrícula con su grafo
- **Matricula**: representar la entidad agregada

### relaciones conceptuales

- **Delegación**: vista → controlador
- **Agregado complejo**: `Matricula` contiene asignaturas matriculadas (1:N) con su propio atributo `nMatricula`
- **Vista plana**: sin colapsables aparentes (a diferencia de [[consultarDetalleAlumno]])

## conexión con disciplinas rup

### desde requisitos

- **Detallado**: `MATRICULA_ABIERTA_COMP` → ficha
- **Prototipo SALT**: ficha completa con tabla embebida → estructura del agregado
- **Actores**: `Secretaria --> consultarDetalleMatricula()` en package "Matrículas"

### hacia diseño

- **Reconciliar `verDetalleMatricula()` ↔ `consultarDetalleMatricula()`** en el detallado
- **Promover `Matricula` al modelo del dominio como agregado** con `Alumno` (referencia), `cursoAcademico`, `facultad`, `planEstudios` y colección de `AsignaturaMatriculada`
- **Modelar `Asignatura` como entidad** (código institucional único, ECTS, carácter, curso del plan)
- **Modelar `AsignaturaMatriculada` como tabla intermedia** con `nMatricula` (semántica de convocatoria)
- **Modelar `Facultad` y `PlanDeEstudios`** como catálogos institucionales (entidades de dominio académico)
- **Política de carga del agregado**: lazy loading vs eager fetch
- **Paginación de asignaturas** si los planes son largos
- **Definir enum del `caracter`**: OB / OP / FB (Obligatoria / Optativa / Formación Básica) — confirmar con cliente
- **Reconciliar `Asignatura` ↔ `SesionDeClase.asignatura`** del bloque Profesor (probablemente la misma entidad)

**Código fuente:** [colaboracion.puml](/modelosUML/RUP/01-analisis/casos-uso/consultarDetalleMatricula/colaboracion.puml)

## referencias

- [Detallado `consultarDetalleMatricula()`](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Secretaria/consultarDetalleMatricula.puml)
- [Prototipo SALT `consultarDetalleMatricula.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Secretaria/consultarDetalleMatricula.png)
- [Caso de uso de Secretaria](/modelosUML/RUP/00-requisitos/CasosDeUso/CasoDeUso/Secretaria/DiagramaCompletoCasoDeUso.puml)
- [Análisis `importarMatriculas()` — debut de la entidad `Matricula`](/RUP/01-analisis/casos-uso/importarMatriculas/README.md)
- [Análisis `consultarDetalleAlumno()` (Profesor) — paralelo conceptual](/RUP/01-analisis/casos-uso/consultarDetalleAlumno/README.md)
- [conversation-log.md](/conversation-log.md)
