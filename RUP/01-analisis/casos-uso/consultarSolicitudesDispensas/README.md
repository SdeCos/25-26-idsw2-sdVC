# CGU > consultarSolicitudesDispensas > Análisis

> | [🏠️](/README.md) | [Análisis](/RUP/01-analisis/README.md) | [Detalle](/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/DirectorDeGrado/) | **Análisis** | Diseño | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Inception
- **Disciplina**: Análisis
- **Caso de uso**: `consultarSolicitudesDispensas()`
- **Actor**: DirectorDeGrado
- **Versión**: 1.0
- **Fecha**: 2026-05-28

## propósito

> **Nota — scoping por grado.** Cuando se redactó este análisis el Director veía **todas** las dispensas del sistema. Una revisión posterior restauró la entidad `Grado` del SDR (`Grado → DirectorDeGrado : Dirigido por`), de modo que el Director ve solo las dispensas cuya asignatura pertenece a su grado. La mecánica MVC del CU no cambia (mismo Controller, mismo Repository, misma View) — lo que cambia es el filtro aplicado en `obtenerTodas()`: ahora es `obtenerPorGrado(grado_id)`. Las afirmaciones tipo "ve todas" del texto que sigue deben leerse como "ve todas las de su grado". Detalle en [[gestionarCatalogoGrados]].

Análisis del caso de uso `consultarSolicitudesDispensas()` mediante diagrama de colaboración MVC. Es el CU **read-only de master-detail** del DirectorDeGrado: el Director accede al listado de **todas** las solicitudes de dispensa del sistema, abre el detalle de una seleccionada, y opcionalmente transita a [[editarSolicitudDispensa]] para emitir veredicto (aprobar/rechazar/observar).

A diferencia del CU homólogo del Alumno ([[consultarSolicitudDispensa]] — singular), aquí el alcance abarca **el listado completo + el detalle en una misma colaboración**. El Director es el revisor, no el propietario.

## diagrama de colaboración

<div align=center>

|![Análisis consultarSolicitudesDispensas()](/images/RUP/01-analisis/casos-uso/consultarSolicitudesDispensas/colaboracion.svg)|
|-|
|**Disciplina**: Análisis RUP<br>**Enfoque**: Diagramas de colaboración MVC|

</div>


[Código PlantUML](/modelosUML/RUP/01-analisis/casos-uso/consultarSolicitudesDispensas/colaboracion.puml)
## discrepancia en el requisitado

Coexisten tres formas del nombre en los artefactos del requisitado:

| Fuente | Nombre usado |
|-|-|
| [`DirectorDeGrado.puml`](/modelosUML/RUP/00-requisitos/CasosDeUso/CasoDeUso/DirectorDeGrado/DirectorDeGrado.puml) (actor) | `consultarSolicitudesDispensa()` (singular `Dispensa`) |
| [`ConsultarSolicitudesDispensas.puml`](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/DirectorDeGrado/ConsultarSolicitudesDispensas.puml) (detallado, filename y estado interno) | `consultarSolicitudesDispensas` (plural `Dispensas`) |
| [Prototipos SALT](/RUP/00-requisitos/CasosDeUso/Prototipos/DirectorDeGrado/) | `consultarSolicitudesDispensasDirector1/2.png` (plural) |

El análisis adopta **`consultarSolicitudesDispensas()`** (plural) como nombre canónico — mayoría de artefactos (detallado + prototipos + estado interno) y semántica más coherente: el CU consulta una **lista** de solicitudes (plural), no una sola. Misma lógica que [[consultarSolicitudDispensa]] aplicó al adoptar el nombre del detallado frente a `Alumno.puml`.

**Deuda para 02-diseño**: reconciliar `DirectorDeGrado.puml` (renombrar `consultarSolicitudesDispensa` → `consultarSolicitudesDispensas`).

## clases de análisis identificadas

### clases model (naranja #F2AC4E)

| Clase | Responsabilidad | Trazabilidad |
|-|-|-|
| **SolicitudDispensa** | Entidad de dominio (operación read-only sobre ella) | Reutilizada de [[crearSolicitudDispensa]] |
| **SolicitudDispensaRepository** | Recupera la lista completa de solicitudes y solicitudes individuales | Reutilizado; estrena `obtenerTodas() : List<SolicitudDispensa>` |

### clases view (azul #629EF9)

| Clase | Responsabilidad | Derivación |
|-|-|-|
| **ConsultarSolicitudesDispensasView** | Listado de solicitudes + ficha de detalle (master-detail) | [Prototipos SALT `consultarSolicitudesDispensasDirector1/2.png`](/RUP/00-requisitos/CasosDeUso/Prototipos/DirectorDeGrado/) |

### clases controller (verde #b5bd68)

| Clase | Responsabilidad | Casos de uso |
|-|-|-|
| **SolicitudDispensaController** | Orquestación del acceso a `SolicitudDispensa` | Compartido con el bloque Alumno y con [[editarSolicitudDispensa]] del Director |

### colaboraciones (verde claro #CDEBA5)

| Colaboración | Propósito | Invocación |
|-|-|-|
| **:Sistema Disponible** | Estado de origen (Director autenticado en el menú principal) | Punto de entrada del CU |
| **:Collaboration EditarSolicitudDispensa** | Sub-colaboración a la que se delega la edición/veredicto si el Director lo solicita desde el detalle | Vía `<<include>>` opcional |

## mensajes de colaboración

### flujo principal

| # | Origen | Destino | Mensaje | Intención |
|-|-|-|-|-|
| 1 | **:Sistema Disponible** | **ConsultarSolicitudesDispensasView** | `consultarSolicitudesDispensas()` | Abrir el listado completo de dispensas |
| 2 | **ConsultarSolicitudesDispensasView** | **SolicitudDispensaController** | `cargarSolicitudes() : List<SolicitudDispensa>` | Recuperar todas las solicitudes |
| 3 | **SolicitudDispensaController** | **SolicitudDispensaRepository** | `obtenerTodas() : List<SolicitudDispensa>` | Consulta sin filtro de propiedad |
| 4 | **ConsultarSolicitudesDispensasView** | **SolicitudDispensaController** | `abrirDetalle(solicitudId) : SolicitudDispensa` | Drill-down al seleccionar una fila |
| 5 | **SolicitudDispensaController** | **SolicitudDispensaRepository** | `obtenerPorId(solicitudId) : SolicitudDispensa` | Recuperar la instancia seleccionada |
| 6 | **ConsultarSolicitudesDispensasView** | **:Collaboration EditarSolicitudDispensa** | `<<include>> editarSolicitudDispensa(solicitudId)` | Saltar a edición (opcional) |

### flujo alternativo — cerrar sin editar

El mensaje 6 es **opcional**: el Director puede cerrar el detalle sin invocar la edición (transición `cerrarSolicitudDispensa()` del detallado). En ese caso solo se ejecutan los mensajes 1-5 y la vista vuelve al listado. Mismo patrón que [[consultarSolicitudDispensa]] del Alumno.

### flujo alternativo — listado sin abrir detalle

El Director puede consultar el listado y salir sin abrir ninguna solicitud individual. En ese caso solo se ejecutan los mensajes 1-3.

## enlaces de dependencia

- **ConsultarSolicitudesDispensasView** conoce a **SolicitudDispensaController** (delegación)
- **ConsultarSolicitudesDispensasView** conoce a **:Collaboration EditarSolicitudDispensa** (inclusión opcional)
- **SolicitudDispensaController** conoce a **SolicitudDispensaRepository** (lectura)
- **SolicitudDispensaController** conoce a **SolicitudDispensa** (manipulación entidad)
- **SolicitudDispensaRepository** conoce a **SolicitudDispensa** (gestión)

## sin verificación de propiedad — asimetría clave con el Alumno

Es **el punto más característico** del bloque DirectorDeGrado y la asimetría principal con el bloque Alumno: el Director **ve todas** las solicitudes sin restricción de propiedad. El método `obtenerTodas()` no recibe parámetro `alumno` — devuelve la colección completa.

| Operación | Alumno (en [[consultarSolicitudDispensa]]) | DirectorDeGrado (este CU) |
|-|-|-|
| Lectura individual | `obtenerPorId(id)` con verificación posterior en el Controller (`solicitud.alumno == sesion.usuario`) | `obtenerPorId(id)` sin verificación |
| Lectura múltiple | (no aplica — el Alumno sólo consulta una a una) | `obtenerTodas()` sin filtro |

Esto **confirma una decisión de análisis ya intuida en el bloque Alumno** (ver [[consultarSolicitudDispensa]] sección "verificación de propiedad"): la verificación de propiedad **no vive en el `SolicitudDispensaRepository`**, sino en el `SolicitudDispensaController` (o una capa de autorización superior). Si viviera en el Repository, este CU del Director no podría reutilizarlo.

**Implicación para 02-diseño**: el Controller debe diferenciar comportamiento según el tipo polimórfico de `Sesion.usuario`. Posibles caminos: (a) ramificación explícita por subtipo, (b) un objeto `PoliticaAcceso` inyectado por rol, (c) dos métodos Controller distintos (`cargarMisSolicitudes()` vs `cargarTodasLasSolicitudes()`). Decisión abierta.

## sin polimorfismo en la entidad — pero polimorfismo implícito en el actor

`SolicitudDispensa` sigue siendo entidad concreta sin jerarquía (igual que en el bloque Alumno). Sin embargo, el subtipo de `Sesion.usuario` (Alumno vs DirectorDeGrado) **sí condiciona qué se carga**:

- Si `Sesion.usuario` es `Alumno` → debería ver solo las suyas (resuelto en su CU)
- Si `Sesion.usuario` es `DirectorDeGrado` → ve todas (este CU)

Es la **primera materialización concreta del polimorfismo de Usuario** introducido en [[iniciarSesion]] que afecta a comportamiento más allá del login. Hasta ahora el subtipo solo se usaba para construir la `Sesion`; aquí condiciona la operación de negocio.

## comparación con el CU homólogo del Alumno

| Característica | [[consultarSolicitudDispensa]] (Alumno) | `consultarSolicitudesDispensas` (Director) |
|-|-|-|
| Alcance | Una sola dispensa (ficha) | Lista completa + ficha (master-detail) |
| Mensajes | 4 | 6 |
| Punto de entrada | `:Dispensas Abierto` (listado ya cargado) | `:Sistema Disponible` (carga la lista) |
| Filtro de propiedad | Sí (en Controller) | No |
| Método del Repository | `obtenerPorId` | `obtenerTodas` + `obtenerPorId` |
| `<<include>>` saliente | `editar` (opcional) | `editar` (opcional) |
| Vista | Solo detalle | Listado + detalle |

La diferencia de **alcance** (master-detail vs solo detalle) refleja una diferencia de uso real: el Alumno entra al sistema "ya filtrado a lo suyo" (en pantallas anteriores se le muestra su listado propio), mientras que el Director arranca el flujo desde cero. El detallado lo refleja con orígenes diferentes (`DISPENSAS_ABIERTO_INICIAL` para el Director vs `DISPENSAS_ABIERTO` ya activo para el Alumno).

## trazabilidad con artefactos previos

### con especificación detallada

- **`DISPENSAS_ABIERTO_INICIAL`** → punto de entrada del CU (representado por la colaboración `:Sistema Disponible`)
- **Estado `DISPENSAS_ABIERTO` (startState, "Director selecciona una solicitud")** → **mensajes 1-3** (carga del listado) + **mensaje 4** (selección)
- **Transición `consultarSolicitudDispensa()` del detallado** → mensajes 4-5 internos al CU (no es un `<<include>>` a otro CU porque el Director no tiene un CU separado `consultarSolicitudDispensa()`; el detalle vive dentro de este mismo CU)
- **Estado `SOLICITUD_DISPENSA_ABIERTA` con `VisualizacionYEdicion` invocando `editarSolicitudDispensa()`** → **mensaje 6** (`<<include>>` opcional)
- **Transición `guardarSolicitudDispensa()`** → vive dentro de [[editarSolicitudDispensa]]; no aplica a la consulta pura
- **Transición `cerrarSolicitudDispensa()`** → flujo alternativo "cerrar sin editar"
- **Estado `DISPENSAS_ABIERTO` (endState)** → retorno tras cerrar o guardar

### con wireframe (prototipo SALT)

- **`consultarSolicitudesDispensasDirector1.png`** → vista de listado de `ConsultarSolicitudesDispensasView` (mensajes 1-3)
- **`consultarSolicitudesDispensasDirector2.png`** → vista de detalle dentro de la misma `ConsultarSolicitudesDispensasView` (mensajes 4-5)
- **`editarSolicitudDispensaDirector.png`** → transición al CU `editarSolicitudDispensa` (mensaje 6 `<<include>>`)

### con actores

- **`DirectorDeGrado --> ConsultarSolicitudesDispensa`** en `DirectorDeGrado.puml` → invocación del CU (discrepancia de nombre documentada arriba)
- **`Profesor <|-- DirectorDeGrado`** → el Director es subtipo de Profesor; en próximos análisis del bloque Profesor habrá un CU `consultarSolicitudDispensa` heredable, pero el alcance master-detail aquí es **específico** del Director (no heredado)

### con modelo del dominio

- **Sin trazabilidad directa**: deuda compartida con todo el bloque de dispensas.

## principios de análisis aplicados

### patrón mvc

- **Controller compartido por entidad**: `SolicitudDispensaController` ya usado en todos los CUs de dispensa anteriores
- **Vista única por CU con dos modos**: `ConsultarSolicitudesDispensasView` integra listado y detalle (igual que el wireframe del prototipo lo presenta como dos pantallas conectadas)
- **Sin polimorfismo en la entidad**: pero polimorfismo implícito en el actor (vía `Sesion.usuario`)

### diagramas de colaboración

- **6 mensajes**: la coherencia interna del CU (master-detail) justifica el tamaño mayor frente a los 4 mensajes del homólogo del Alumno
- **Dos fases del flujo principal**: mensajes 1-3 (cargar listado) y 4-5 (drill-down), con 6 como transición opcional a editar
- **Sin nuevo `<<include>>` a `consultarSolicitudDispensa()`**: el detalle vive dentro del CU, no se reutiliza el CU del Alumno (que tiene verificación de propiedad incompatible)

### análisis puro

- **Sin paginación, búsqueda ni filtrado**: el detallado no los menciona; emergerán en diseño si el volumen lo justifica
- **Sin orden explícito**: el detallado no especifica criterio (por fecha, por estado pendiente, etc.); deuda para diseño

## características del análisis

### responsabilidades identificadas

- **ConsultarSolicitudesDispensasView**: presentar el listado y la ficha de detalle; ofrecer salto a edición
- **SolicitudDispensaController**: mediar entre vista y repositorio; **no** aplicar regla de propiedad cuando el actor es Director (sí cuando es Alumno)
- **SolicitudDispensaRepository**: recuperar el listado completo y solicitudes individuales
- **SolicitudDispensa**: representar las entidades consultadas

### relaciones conceptuales

- **Master-detail en una vista**: el listado y el detalle son del mismo CU
- **Acceso sin restricción**: la entidad se devuelve íntegra sin filtros de seguridad

## conexión con disciplinas rup

### desde requisitos

- **Detallado**: estructura master-detail (`DISPENSAS_ABIERTO` → `SOLICITUD_DISPENSA_ABIERTA`) → vista única con dos fases en mensajes 1-3 + 4-5
- **Prototipos SALT**: dos pantallas (`Director1/2.png`) → mismo CU, dos modos de la vista
- **Actores**: `DirectorDeGrado` hereda de `Profesor`, asimetría con `Alumno` en filtro de propiedad

### hacia diseño

- Reconciliar nombre del CU en `DirectorDeGrado.puml` (`consultarSolicitudesDispensa` → `consultarSolicitudesDispensas`)
- Decisión de implementación de la diferencia de comportamiento del Controller según subtipo de `Sesion.usuario` (Alumno filtra, Director no): rama explícita por subtipo vs estrategia `PoliticaAcceso` vs métodos Controller distintos
- Paginación / búsqueda / orden del listado (¿por fecha? ¿pendientes primero?)
- Diseño de la `ConsultarSolicitudesDispensasView` como single-page con panel master + panel detail vs dos vistas separadas
- Reconciliar `SolicitudDispensa` con el modelo del dominio

**Código fuente:** [colaboracion.puml](/modelosUML/RUP/01-analisis/casos-uso/consultarSolicitudesDispensas/colaboracion.puml)

## referencias

- [Detallado `ConsultarSolicitudesDispensas.puml`](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/DirectorDeGrado/ConsultarSolicitudesDispensas.puml)
- [Prototipo SALT `consultarSolicitudesDispensasDirector1.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/DirectorDeGrado/consultarSolicitudesDispensasDirector1.png)
- [Prototipo SALT `consultarSolicitudesDispensasDirector2.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/DirectorDeGrado/consultarSolicitudesDispensasDirector2.png)
- [Caso de uso del DirectorDeGrado](/modelosUML/RUP/00-requisitos/CasosDeUso/CasoDeUso/DirectorDeGrado/DirectorDeGrado.puml)
- [Análisis `consultarSolicitudDispensa()` (Alumno)](/RUP/01-analisis/casos-uso/consultarSolicitudDispensa/README.md)
- [Análisis `editarSolicitudDispensa()` (Alumno)](/RUP/01-analisis/casos-uso/editarSolicitudDispensa/README.md)
- [conversation-log.md](/conversation-log.md)
