# CGU > consultarSolicitudDispensa [Profesor] > Análisis

> | [🏠️](/README.md) | [Análisis](/RUP/01-analisis/README.md) | [Detalle](/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Profesor/) | **Análisis** | Diseño | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Inception
- **Disciplina**: Análisis
- **Caso de uso**: `consultarSolicitudDispensa()` [actor: Profesor]
- **Actor**: Profesor
- **Versión**: 1.0
- **Fecha**: 2026-05-28

## propósito

Análisis del caso de uso `consultarSolicitudDispensa()` **invocado por el Profesor** mediante diagrama de colaboración MVC. Es la operación mediante la cual el Profesor revisa el detalle de una solicitud de dispensa de un alumno de **sus asignaturas**, para conocer el motivo de su ausencia y la documentación adjunta.

Aunque comparte nombre canónico con [[consultarSolicitudDispensa]] del Alumno, las dos operaciones son **semánticamente distintas**: el Alumno consulta una dispensa **propia** (verificación de propiedad); el Profesor consulta una dispensa **ajena** (filtrada por las asignaturas que imparte). Se modelan como **análisis separados** porque sus vistas, alcance y reglas de acceso son diferentes.

Es la **tercera variante** del CU `consultarSolicitudDispensa` en el proyecto, completando el patrón polimórfico del Controller por subtipo de `Sesion.usuario`:

| Rol | Alcance del listado / filtro | Operaciones permitidas | Vista |
|-|-|-|-|
| Alumno | Solo las propias (propiedad) | Read + saltar a editar | Ficha simple |
| **Profesor** | **Solo las de sus asignaturas** | **Read-only puro** (sin editar) | **Vista enriquecida con datos del solicitante** |
| DirectorDeGrado | Todas | Read + master-detail + saltar a editar (veredicto) | Vista master-detail con listado + ficha |

## diagrama de colaboración

<div align=center>

|![Análisis consultarSolicitudDispensa() Profesor](/images/RUP/01-analisis/casos-uso/consultarSolicitudDispensaProfesor/colaboracion.svg)|
|-|
|**Disciplina**: Análisis RUP<br>**Enfoque**: Diagramas de colaboración MVC|

</div>


[Código PlantUML](/modelosUML/RUP/01-analisis/casos-uso/consultarSolicitudDispensaProfesor/colaboracion.puml)
## clases de análisis identificadas

### clases model (naranja #F2AC4E)

| Clase | Responsabilidad | Trazabilidad |
|-|-|-|
| **SolicitudDispensa** | Entidad de dominio (operación read-only sobre ella) | Reutilizada de [[crearSolicitudDispensa]] |
| **SolicitudDispensaRepository** | Recupera la solicitud por id | Reutilizado; mismo `obtenerPorId(id)` que en los otros consultar |

### clases view (azul #629EF9)

| Clase | Responsabilidad | Derivación |
|-|-|-|
| **ConsultarSolicitudDispensaProfesorView** | Ficha de visualización enriquecida: datos del **alumno solicitante** (nombre, grado, curso), **lista de asignaturas afectadas**, motivo, fechas (solicitud, edición, aprobación), comentarios | [Prototipos SALT `consultarSolicitudDispensaProfesor1.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Profesor/consultarSolicitudDispensaProfesor1.png) (listado pre-existente) y [`consultarSolicitudDispensaProfesor2.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Profesor/consultarSolicitudDispensaProfesor2.png) (ficha) |

Distinta de [[consultarSolicitudDispensa]] del Alumno: el Alumno **ya sabe** quién es él y a qué asignaturas tiene dispensa; el Profesor **necesita ese contexto** para situar la solicitud. La asimetría es de información presentada, no de operación.

### clases controller (verde #b5bd68)

| Clase | Responsabilidad | Casos de uso |
|-|-|-|
| **SolicitudDispensaController** | Orquestación del acceso a `SolicitudDispensa`; **estrena la verificación "Profesor puede ver esta dispensa"** | Compartido con todos los CUs de la entidad |

### colaboraciones (verde claro #CDEBA5)

| Colaboración | Propósito | Invocación |
|-|-|-|
| **:Dispensas Abierto** | Estado de origen — el Profesor en el listado de dispensas que le competen | Punto de entrada del CU |

## mensajes de colaboración

### flujo principal

| # | Origen | Destino | Mensaje | Intención |
|-|-|-|-|-|
| 1 | **:Dispensas Abierto** | **ConsultarSolicitudDispensaProfesorView** | `consultarSolicitudDispensa(solicitudId)` | Abrir la ficha de la solicitud seleccionada |
| 2 | **ConsultarSolicitudDispensaProfesorView** | **SolicitudDispensaController** | `cargarSolicitud(solicitudId) : SolicitudDispensa` | Recuperar la instancia |
| 3 | **SolicitudDispensaController** | **SolicitudDispensaRepository** | `obtenerPorId(solicitudId) : SolicitudDispensa` | Consulta al repositorio |

### flujo alternativo — cerrar la ficha

El detallado contempla `cerrarSolicitud()` (transición roja) como salida. En el análisis equivale a que la `ConsultarSolicitudDispensaProfesorView` se cierre y el sistema vuelva a `:Dispensas Abierto`. Sin clase adicional.

## sin `<<include>>` saliente — read-only puro

Asimetría destacada con los otros dos consultar:

| CU | Operaciones del actor sobre dispensas | `<<include>>` saliente a editar |
|-|-|-|
| [[consultarSolicitudDispensa]] (Alumno) | crear, editar, consultar | Sí, opcional |
| [[consultarSolicitudesDispensas]] (Director) | consultar, editar (veredicto) | Sí, opcional |
| `consultarSolicitudDispensa` (Profesor) | **solo consultar** | **No** |

El `Profesor.puml` solo lista `consultarSolicitudDispensa()` en el package "Dispensas". No tiene `editarSolicitudDispensa()` ni `crearSolicitudDispensa()`. Por tanto, el `<<include>>` saliente no aplica — el Profesor no puede transitar a editar desde la ficha.

Es el primer CU `consultar` del proyecto sin salida a un CU de modificación. Refleja la **separación de responsabilidades** entre roles: el Profesor es **observador** del flujo de dispensas (necesita la información para gestionar asistencias), no participante.

## verificación de acceso "Profesor competente"

El Profesor **no** ve todas las dispensas (no es Director) ni solo las propias (no es Alumno). Ve las **de las asignaturas que imparte** — porque una dispensa concedida afecta a la asistencia que él gestiona.

El detallado no enuncia la regla explícitamente, pero el actor (`Profesor --> consultarSolicitudDispensa`) y el contexto del bloque (un profesor en su flujo de asistencias) la implican.

**Decisión de modelado**: la verificación vive en el `SolicitudDispensaController` (tras el mensaje 3) o en una capa de autorización superior. Cómo se materializa es decisión de diseño.

**Regla implícita en análisis**: `solicitud.asignaturas ∩ sesion.usuario.asignaturasImpartidas ≠ ∅`.

Esto introduce una **nueva relación de dominio**: `Profesor` tiene asignaturas que imparte. No estaba modelada en `iniciarSesion` (allí `Profesor` era solo subtipo de `Usuario` sin atributos). **Deuda para 02-diseño**: añadir `Profesor.asignaturasImpartidas` al modelo del dominio.

## tercer caso del polimorfismo del Controller — refuerza la opción "métodos por rol"

Con este CU se completa la tríada de roles operando sobre `SolicitudDispensa` con políticas distintas:

| Rol | Método del Controller (carga) | Filtro aplicado |
|-|-|-|
| Alumno | `cargarSolicitud(solicitudId)` + verificación `solicitud.alumno == sesion.usuario` | Por propiedad |
| Profesor | `cargarSolicitud(solicitudId)` + verificación `solicitud.asignaturas ∩ usuario.asignaturasImpartidas ≠ ∅` | Por relación docente |
| Director | `cargarSolicitud(solicitudId)` (sin verificación) | Sin filtro |

Hipótesis de diseño que en [[editarSolicitudDispensaDirector]] ya se planteaba: **"métodos específicos por rol"** (camino (c) entre los tres abiertos en [[consultarSolicitudesDispensas]]). Posibles firmas concretas:

```
cargarMiSolicitud(solicitudId)         // Alumno
cargarSolicitudDeAsignatura(solicitudId) // Profesor
cargarCualquierSolicitud(solicitudId)  // Director
```

O alternativa con un único `cargarSolicitud` que recibe la `Sesion` y ramifica internamente por subtipo. Decisión abierta — pero el patrón emerge cada vez más nítido con cada rol nuevo.

## discrepancia menor en la trazabilidad — listado pre-existente

El detallado arranca de `DISPENSAS_ABIERTO_INICIAL` (sugiere que el listado ya existe), igual que en [[consultarSolicitudDispensa]] del Alumno. Pero **el prototipo `consultarSolicitudDispensaProfesor1.png` muestra ese listado** ("Lista de Solicitudes Dispensa" con filtros, columnas, paginación).

Adoptamos la misma decisión que en el Alumno: el listado se asume como estado pre-existente del actor, no como CU separado. **Deuda blanda para 02-diseño**: si se quiere consistencia con el master-detail del Director ([[consultarSolicitudesDispensas]]), el listado del Profesor podría modelarse como CU "consultarSolicitudesDispensas (Profesor)" siguiendo el mismo patrón. Por ahora se mantiene el modelo de un único CU read-only.

## enlaces de dependencia

- **ConsultarSolicitudDispensaProfesorView** conoce a **SolicitudDispensaController** (delegación)
- **SolicitudDispensaController** conoce a **SolicitudDispensaRepository** (lectura)
- **SolicitudDispensaController** conoce a **SolicitudDispensa** (manipulación entidad)
- **SolicitudDispensaController** conoce a **Sesion** (verificación de acceso vía `Sesion.usuario.asignaturasImpartidas`; no dibujada)
- **SolicitudDispensaRepository** conoce a **SolicitudDispensa** (gestión)

## trazabilidad con artefactos previos

### con especificación detallada

- **`DISPENSAS_ABIERTO_INICIAL`** → colaboración `:Dispensas Abierto` (origen)
- **Transición `consultarSolicitudDispensa()`** → mensaje 1
- **Estado `SOLICITUD_DISPENSA_ABIERTA_COMP` con sub-estado `VisualizacionDetalle`** → `ConsultarSolicitudDispensaProfesorView` + mensajes 2-3
- **Nota "Sistema muestra todos los datos de la solicitud: Alumno solicitante y Motivo, Estado actual y Documentación adjunta"** → contenido de la vista
- **Transición `cerrarSolicitud()`** → flujo alternativo (la vista se cierra)

### con wireframe (prototipo SALT)

- **`consultarSolicitudDispensaProfesor1.png`** → listado pre-existente (estado `:Dispensas Abierto`)
- **`consultarSolicitudDispensaProfesor2.png`** → ficha enriquecida → `ConsultarSolicitudDispensaProfesorView`. Datos visibles: Nombre del solicitante, Grado, Curso, Asignaturas afectadas (cada una con docente, semestre, día y hora de sesión), Motivo (texto largo), Fechas (Solicitud, Última Edición, Aprobación), Comentarios. Notable: el campo "Fecha de Aprobación" aparece como `--/--/--` en el ejemplo (solicitud pendiente) — confirma que el Profesor también ve dispensas en cualquier estado (no solo aprobadas)

### con actores

- **`Profesor --> consultarSolicitudDispensa`** en `Profesor.puml` package "Dispensas" → invocación del CU

### con modelo del dominio

- **Sin trazabilidad directa**: deuda compartida con todo el bloque dispensas
- **Nueva relación detectada**: `Profesor` ↔ asignaturas impartidas (no modelada en el SDR original)

## principios de análisis aplicados

### patrón mvc

- **Controller compartido por entidad**: `SolicitudDispensaController` ya usado en todos los CUs de dispensa anteriores
- **Vista específica por rol**: enriquecida con contexto del solicitante (Alumno, sus asignaturas)
- **Sin polimorfismo en la entidad**: `SolicitudDispensa` concreta, polimorfismo de comportamiento en el Controller por subtipo de `Sesion.usuario`

### diagramas de colaboración

- **3 mensajes**: CU mínimo, igual que [[consultarSolicitudDispensa]] del Alumno
- **Sin destino**: read-only puro, sin transiciones a otros CUs
- **Verificación de acceso en prosa**: la regla "Profesor competente" se documenta, no se modela como mensaje

### análisis puro

- **Sin paginación / búsqueda**: el prototipo muestra ambas (filtros "2º Curso", "Aprobada", paginación 1-8 de 8 elementos) pero pertenecen al listado pre-existente, no a la ficha
- **Sin política de redacción de comentarios**: el campo aparece pero el Profesor no puede escribir en él (read-only)

## características del análisis

### responsabilidades identificadas

- **ConsultarSolicitudDispensaProfesorView**: presentar la ficha enriquecida con contexto del solicitante
- **SolicitudDispensaController**: cargar la solicitud, **aplicar verificación de acceso "Profesor competente"**
- **SolicitudDispensaRepository**: recuperar la instancia
- **SolicitudDispensa**: representar la entidad consultada

### relaciones conceptuales

- **Delegación**: vista → controlador
- **Lectura**: sin escritura
- **Verificación específica del rol**: tercera política distinta sobre el mismo Repository

## conexión con disciplinas rup

### desde requisitos

- **Detallado**: `SOLICITUD_DISPENSA_ABIERTA_COMP` con `VisualizacionDetalle` → vista enriquecida read-only
- **Prototipos SALT**: dos pantallas (listado + ficha enriquecida)
- **Actores**: `Profesor --> consultarSolicitudDispensa()` único en package "Dispensas" — sin `editar` ni `crear`

### hacia diseño

- **Añadir `Profesor.asignaturasImpartidas` al modelo del dominio** (relación necesaria para la verificación de acceso)
- **Materialización del polimorfismo del Controller** — con tres roles operando con políticas distintas, la opción "métodos por rol" se vuelve la más limpia
- **Política de "Profesor competente"**: ¿exigir intersección no vacía de asignaturas? ¿permitir a profesores del mismo grado aunque no impartan la asignatura concreta? Regla de negocio abierta
- **Listado del Profesor como CU separado**: deuda blanda si se quiere consistencia con el master-detail del Director
- **Campos del prototipo no presentes en el detallado**: "Comentarios", "Fecha de Aprobación", lista de asignaturas con docente/día/hora — emergen como atributos del modelo del dominio
- **Visibilidad de dispensas pendientes vs aprobadas**: el prototipo confirma que el Profesor ve cualquier estado; ¿debería diferenciar el comportamiento por estado? (p.ej. notificar al pasar lista que existe una dispensa pendiente)

**Código fuente:** [colaboracion.puml](/modelosUML/RUP/01-analisis/casos-uso/consultarSolicitudDispensaProfesor/colaboracion.puml)

## referencias

- [Detallado `consultarSolicitudDispensa()` (Profesor)](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Profesor/consultarSolicitudDispensa.puml)
- [Prototipo SALT `consultarSolicitudDispensaProfesor1.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Profesor/consultarSolicitudDispensaProfesor1.png)
- [Prototipo SALT `consultarSolicitudDispensaProfesor2.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Profesor/consultarSolicitudDispensaProfesor2.png)
- [Caso de uso del Profesor](/modelosUML/RUP/00-requisitos/CasosDeUso/CasoDeUso/Profesor/Profesor.puml)
- [Análisis `consultarSolicitudDispensa()` (Alumno)](/RUP/01-analisis/casos-uso/consultarSolicitudDispensa/README.md)
- [Análisis `consultarSolicitudesDispensas()` (Director)](/RUP/01-analisis/casos-uso/consultarSolicitudesDispensas/README.md)
- [conversation-log.md](/conversation-log.md)
