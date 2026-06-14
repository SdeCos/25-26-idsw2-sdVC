# CGU > importarListasAlumnos > Análisis

> | [🏠️](/README.md) | [Análisis](/RUP/01-analisis/README.md) | [Detalle](/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Secretaria/) | **Análisis** | Diseño | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Inception
- **Disciplina**: Análisis
- **Caso de uso**: `importarListasAlumnos()`
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-05-28

## propósito

Análisis del caso de uso `importarListasAlumnos()` mediante diagrama de colaboración MVC. La Secretaria adjunta uno o varios archivos con listados de alumnos, el sistema los valida e importa los registros válidos en el `AlumnoRepository`, presentando un informe con errores detectados.

Es el **gemelo estructural** de [[importarMatriculas]] (mismo patrón "Controller + Servicio Validador + Repository") aplicado a la entidad `Alumno`. Refleja la categoría operativa "carga masiva" del bloque Secretaria.

## diagrama de colaboración

<div align=center>

|![Análisis importarListasAlumnos()](/images/RUP/01-analisis/casos-uso/importarListasAlumnos/colaboracion.svg)|
|-|
|**Disciplina**: Análisis RUP<br>**Enfoque**: Diagramas de colaboración MVC|

</div>


[Código PlantUML](/modelosUML/RUP/01-analisis/casos-uso/importarListasAlumnos/colaboracion.puml)
## discrepancia crítica en el requisitado — detallado equivocado

**El archivo `importarListasAlumnos.puml` del SDR tiene contenido equivocado**: su título es `"Exportar listado de alumnos"`, su transición de entrada es `exportarListaAlumnos()`, sus sub-estados son `SolicitudFiltros / ValidarFiltros / SeleccionFormato / Descarga` (estructura de **exportación**, no de importación).

Pruebas de que es error del SDR (no nombre alternativo):

1. **El nombre del archivo y del CU en el actor** son ambos `importarListasAlumnos()` (no `exportarListasAlumnos()`).
2. **El bloque "Listas de alumnos" del actor** lista `importarListasAlumnos()` + `consultarListaAlumnos()` (no hay un CU separado de exportar listas — la exportación pertenece al bloque "Asistencias" del Profesor).
3. **Existe el prototipo `exportarListadoAlumnosPorCurso.png`** en Secretaria, sugiriendo que **sí existe la operación de exportar listas** pero no está reflejada en el actor — es probablemente otro error de migración.
4. **El detallado de [[importarMatriculas]] sí está bien**: estructura `SolicitudArchivo / ValidarFormato / ImportarRegistros / MostrarInforme` — es la plantilla esperada para una importación.

**Decisión**: modelar `importarListasAlumnos()` por **analogía con [[importarMatriculas]]**, no con el contenido equivocado del detallado. El detallado de matrículas es la fuente confiable del patrón de importación; este análisis lo replica para alumnos.

**Deuda urgente para 02-diseño / requisitos**:

- Reparar `importarListasAlumnos.puml` con el contenido correcto de importación.
- Decidir si `exportarListadoAlumnosPorCurso()` debe ser un CU del bloque Secretaria (añadir al actor + crear detallado + recontar denominador a 27).

## discrepancias menores adicionales

Heredadas de [[importarMatriculas]]:

- **Actor `SecretariaAcademica` vs `Secretaria`**: análisis adopta `Secretaria` (consistencia con índice y resto del proyecto).
- **Notas de detallados con "Alumno solicita..."** en lugar de "Secretaria solicita..." (probable copia-pega).

## clases de análisis identificadas

### clases model (naranja #F2AC4E)

| Clase | Responsabilidad | Trazabilidad |
|-|-|-|
| **Alumno** | Entidad de dominio; este CU la persiste en lote | Reutilizada de [[consultarListaAlumnos]] (Profesor) y [[consultarDetalleAlumno]] |
| **AlumnoRepository** | Persiste registros de alumno en lote | Reutilizado de [[consultarListaAlumnos]]; estrena `guardarLote(registros) : List<Alumno>` |

### clases view (azul #629EF9)

| Clase | Responsabilidad | Derivación |
|-|-|-|
| **ImportarListasAlumnosView** | Modal con selector de archivos múltiples + drag-and-drop, lista de archivos cargados, botones Cancelar/Importar, presentación del informe tras procesamiento | **Sin prototipo dedicado** en el SDR (otra deuda — el prototipo más cercano es `importarMatriculas1/2/3.png`, presumiblemente la misma estructura visual aplicaría aquí) |

### clases controller / servicios (verde #b5bd68)

| Clase | Responsabilidad | Casos de uso |
|-|-|-|
| **AlumnoController** | Orquestación: validar archivos + delegar persistencia + componer informe | Compartido con [[consultarListaAlumnos]] y [[consultarDetalleAlumno]] — "Controller por entidad" mantenido |
| **ValidadorArchivoListasAlumnos** | **Servicio de aplicación**: valida formato y estructura; produce `ResultadoValidacion` | **Nuevo**; tercer servicio del análisis. Estructura gemela de `ValidadorArchivoMatriculas` (deuda: en diseño se considerará si extraer una abstracción común `ValidadorArchivo<T>`) |

### colaboraciones (verde claro #CDEBA5)

| Colaboración | Propósito | Invocación |
|-|-|-|
| **:Listas Abierto** | Estado de origen — la Secretaria en el módulo de listas | Punto de entrada |

## mensajes de colaboración

### flujo principal

| # | Origen | Destino | Mensaje | Intención |
|-|-|-|-|-|
| 1 | **:Listas Abierto** | **ImportarListasAlumnosView** | `importarListasAlumnos()` | Abrir modal de importación |
| 2 | **ImportarListasAlumnosView** | **AlumnoController** | `importar(archivos) : InformeImportacion` | Solicitar procesamiento |
| 3 | **AlumnoController** | **ValidadorArchivoListasAlumnos** | `validar(archivos) : ResultadoValidacion` | Validar formato y estructura |
| 4 | **AlumnoController** | **AlumnoRepository** | `guardarLote(registros) : List<Alumno>` | Persistir los registros válidos |

### flujos alternativos

Idénticos a [[importarMatriculas]]: error de formato total, error parcial (best-effort), cancelar. No se repiten aquí — patrón consolidado.

## relación con `importarMatriculas` — plantilla del patrón de importación

| Característica | [[importarMatriculas]] | `importarListasAlumnos` |
|-|-|-|
| Mensajes | 4 | 4 |
| Origen | `:Matriculas Abierto` | `:Listas Abierto` |
| Servicio validador | `ValidadorArchivoMatriculas` | `ValidadorArchivoListasAlumnos` |
| Repository | `MatriculaRepository` (nuevo) | `AlumnoRepository` (reutilizado) |
| Entidad creada | `Matricula` (nueva) | `Alumno` (reutilizada) |
| Vista | `ImportarMatriculasView` | `ImportarListasAlumnosView` |
| Auditoría | `fechaImportacion` + `responsable` | Análogo |

Estructura **exactamente idéntica**, lo que sugiere un patrón de diseño OO claro a aplicar en 02-diseño: una clase abstracta o template method **`ImportadorMasivo<T>`** que delegue en `ValidadorArchivo<T>` + `Repository<T>`.

**Hipótesis de diseño**: cuando lleguen otros CUs de importación (improbable en este proyecto pero conceptualmente relevante), bastará con instanciar la plantilla con el tipo concreto.

## tipos de retorno opacos — reutilización del patrón

`InformeImportacion` y `ResultadoValidacion` son los **mismos tipos** que en [[importarMatriculas]]:

- `InformeImportacion`: `{registrosImportados: List<T>, errores: List<ErrorImportacion>}` — genérico
- `ResultadoValidacion`: `{registrosValidos: List<RegistroCrudo>, errores: List<ErrorImportacion>}` — genérico

Esto refuerza la hipótesis del genérico `<T>` en diseño. Los tipos se mantienen opacos en el análisis (sin clases formales).

## auto-resolución de campos por el Controller

Igual que en [[importarMatriculas]]:

- `fechaImportacion = ahora`
- `responsable = Sesion.usuario` (la Secretaria que ejecutó el import) — auditoría

Patrón "auto-poblado por Controller" reaplicado.

## ¿qué exactamente importa este CU?

Ambigüedad heredada del actor `Profesor.puml` que también tiene `consultarListaAlumnos()` (en el bloque del Profesor son listas de matriculados por asignatura, no entidades `Lista` propias).

**Decisión de análisis**: este CU **importa entidades `Alumno`** (datos personales y académicos). El sistema asume que los alumnos van asociados a un curso/grado en el archivo importado; la asociación a asignaturas se materializa vía [[importarMatriculas]] (que persiste `Matricula` referenciando a `Alumno`).

Es decir:

```
importarListasAlumnos → crea/actualiza Alumno
importarMatriculas    → crea Matricula (que referencia a Alumno)
```

**Implicación funcional**: el orden importa — debe ejecutarse `importarListasAlumnos` **antes** que `importarMatriculas` (o el sistema debe permitir alumnos referenciados en matrículas que no existen aún, escenario menos limpio).

**Deuda para 02-diseño**: confirmar con el cliente el orden de operaciones esperado y la política de dependencias entre los dos imports.

## enlaces de dependencia

- **ImportarListasAlumnosView** conoce a **AlumnoController** (delegación)
- **AlumnoController** conoce a **ValidadorArchivoListasAlumnos** (servicio)
- **AlumnoController** conoce a **AlumnoRepository** (escritura)
- **AlumnoController** conoce a **Alumno** (construye instancias desde registros validados)
- **AlumnoController** conoce a **Sesion** (auditoría `responsable`; no dibujada)
- **AlumnoRepository** conoce a **Alumno** (gestión)

## trazabilidad con artefactos previos

### con especificación detallada

**No se puede mapear directamente** porque el detallado está equivocado (es de exportar). Mapeo por **analogía** con [[importarMatriculas]]:

- `LISTAS_ABIERTO_INICIAL` → colaboración `:Listas Abierto` (origen)
- Sub-estados esperados (paralelos a `IMPORTAR_MATRICULAS_COMP`):
  - `SolicitudArchivo` → vista modal (mensaje 1)
  - `ValidarFormato` → mensaje 3 (validador)
  - `ImportarRegistros` → mensaje 4 (repository)
  - `MostrarInforme` → retorno del mensaje 2

### con wireframe (prototipo SALT)

**Sin prototipo dedicado** — se asume estructura visual paralela a `importarMatriculas1/2/3.png`.

### con actores

- **`SecretariaAcademica --> ListasImportarListas`** en `DiagramaCompletoCasoDeUso.puml` package "Listas de alumnos" → invocación del CU

### con modelo del dominio

- **Sin trazabilidad directa**: deuda heredada de `Alumno` (atributos académicos no estaban en el SDR).

## principios de análisis aplicados

Idénticos a [[importarMatriculas]] — el patrón se reutiliza:

- **Controller por entidad**: `AlumnoController`
- **Servicio de aplicación**: `ValidadorArchivoListasAlumnos` separado (SRP)
- **Vista modal**: `ImportarListasAlumnosView`
- **4 mensajes** con patrón "Controller + Servicio + Repository"
- **Tipos de retorno opacos**: `InformeImportacion`, `ResultadoValidacion`

## conexión con disciplinas rup

### desde requisitos

- **Detallado**: **inutilizable directamente** (contenido equivocado). Reparación necesaria.
- **Sin prototipo dedicado**: usar el de `importarMatriculas` como referencia visual.
- **Actores**: `Secretaria --> importarListasAlumnos()` confirmada en el bloque "Listas de alumnos".

### hacia diseño

- **Reparar el detallado `importarListasAlumnos.puml`** del SDR (crítico)
- **Crear prototipo SALT dedicado** o confirmar que se reusará el modal de `importarMatriculas`
- **Extraer abstracción común `ImportadorMasivo<T>` / `ValidadorArchivo<T>`** (Template Method o composición genérica)
- **Resolver dependencia funcional** entre `importarListasAlumnos` e `importarMatriculas` (orden + integridad referencial)
- **Política "alumno duplicado"**: ¿qué pasa si el archivo trae un alumno que ya existe? (sobreescribir, ignorar, error, actualizar campos cambiados)
- **Resto de deudas heredadas** de [[importarMatriculas]] (formatos, tamaño máximo, atomicidad, auditoría)

**Código fuente:** [colaboracion.puml](/modelosUML/RUP/01-analisis/casos-uso/importarListasAlumnos/colaboracion.puml)

## referencias

- [Detallado `importarListasAlumnos.puml` — contenido equivocado, ver discrepancia](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Secretaria/importarListasAlumnos.puml)
- [Caso de uso de Secretaria](/modelosUML/RUP/00-requisitos/CasosDeUso/CasoDeUso/Secretaria/DiagramaCompletoCasoDeUso.puml)
- [Análisis `importarMatriculas()` — patrón gemelo (fuente de la analogía)](/RUP/01-analisis/casos-uso/importarMatriculas/README.md)
- [Análisis `consultarListaAlumnos()` (Profesor) — reutiliza `AlumnoController`/`AlumnoRepository`](/RUP/01-analisis/casos-uso/consultarListaAlumnos/README.md)
- [Análisis `exportarHistorialAsistencias()` (Profesor) — patrón "Controller+Servicio"](/RUP/01-analisis/casos-uso/exportarHistorialAsistencias/README.md)
- [conversation-log.md](/conversation-log.md)
