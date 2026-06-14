# CGU > editarSolicitudDispensa > Análisis

> | [🏠️](/README.md) | [Análisis](/RUP/01-analisis/README.md) | [Detalle](/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Alumno/) | **Análisis** | Diseño | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Inception
- **Disciplina**: Análisis
- **Caso de uso**: `editarSolicitudDispensa()`
- **Actor**: Alumno
- **Versión**: 1.0
- **Fecha**: 2026-05-26

## propósito

Análisis del caso de uso `editarSolicitudDispensa()` mediante diagrama de colaboración MVC. Es la sub-actividad que carga una `SolicitudDispensa` existente y persiste sus modificaciones (motivos, adjuntos). Tiene **tres puntos de entrada**: desde el listado, desde el detalle de consulta y como continuación tras [[crearSolicitudDispensa]].

## diagrama de colaboración

<div align=center>

|![Análisis editarSolicitudDispensa()](/images/RUP/01-analisis/casos-uso/editarSolicitudDispensa/colaboracion.svg)|
|-|
|**Disciplina**: Análisis RUP<br>**Enfoque**: Diagramas de colaboración MVC|

</div>


[Código PlantUML](/modelosUML/RUP/01-analisis/casos-uso/editarSolicitudDispensa/colaboracion.puml)
## clases de análisis identificadas

### clases model (naranja #F2AC4E)

| Clase | Responsabilidad | Trazabilidad |
|-|-|-|
| **SolicitudDispensa** | Entidad de dominio; la instancia editada conserva su `alumno` propietario (fijado en el alta) | Reutilizada de [[crearSolicitudDispensa]] |
| **SolicitudDispensaRepository** | Recupera la solicitud por id y persiste la modificación | Reutilizado; estrena `obtenerPorId(id)` y `actualizar(solicitud)` |

### clases view (azul #629EF9)

| Clase | Responsabilidad | Derivación |
|-|-|-|
| **EditarSolicitudDispensaView** | Formulario de edición: motivos, documentación adjunta | [Prototipo SALT `editarSolicitudDispensaAlumno.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Alumno/editarSolicitudDispensaAlumno.png) |

### clases controller (verde #b5bd68)

| Clase | Responsabilidad | Casos de uso |
|-|-|-|
| **SolicitudDispensaController** | Orquestación del CRUD individual de `SolicitudDispensa` | Compartido entre los 3 CUs del Alumno (igual que en [[crearSolicitudDispensa]]) |

### colaboraciones (verde claro #CDEBA5)

| Colaboración | Propósito | Invocación |
|-|-|-|
| **:Dispensas Abierto** | Entrada desde el listado de dispensas del alumno | `editarSolicitudDispensa(solicitudId)` |
| **:Collaboration ConsultarSolicitudDispensa** | Entrada desde el detalle de consulta | `editarSolicitudDispensa(solicitudId)` |
| **:Collaboration CrearSolicitudDispensa** | Entrada como continuación del alta | `editarSolicitudDispensa(solicitudNueva)` |

## mensajes de colaboración

### flujo principal

| # | Origen | Destino | Mensaje | Intención |
|-|-|-|-|-|
| 1 | **:Dispensas Abierto** / **:Collaboration ConsultarSolicitudDispensa** / **:Collaboration CrearSolicitudDispensa** | **EditarSolicitudDispensaView** | `editarSolicitudDispensa(solicitudId \| solicitudNueva)` | Abrir el formulario de edición |
| 2 | **EditarSolicitudDispensaView** | **SolicitudDispensaController** | `cargarSolicitudParaEdicion(solicitudId) : SolicitudDispensa` | Recuperar el estado actual (solo si se entra por id) |
| 3 | **SolicitudDispensaController** | **SolicitudDispensaRepository** | `obtenerPorId(solicitudId) : SolicitudDispensa` | Consulta al repositorio |
| 4 | **EditarSolicitudDispensaView** | **SolicitudDispensaController** | `modificarCampos(solicitudId, cambios) : boolean` | Solicitar persistencia de cambios |
| 5 | **SolicitudDispensaController** | **SolicitudDispensaRepository** | `actualizar(solicitud) : boolean` | Persistir cambios |

### flujo alternativo — entrada desde `crearSolicitudDispensa()`

Cuando la entrada es `:Collaboration CrearSolicitudDispensa` con `solicitudNueva`, los mensajes 2 y 3 **no se ejecutan**: la `SolicitudDispensa` ya está cargada desde el alta. Patrón idéntico al de [[editarUsuario]].

### flujo alternativo — cerrar sin guardar

El detallado contempla `cerrarSolicitudDispensa()` como salida sin persistir. En el análisis equivale a no invocar el mensaje 4. No requiere clase adicional.

## enlaces de dependencia

- **EditarSolicitudDispensaView** conoce a **SolicitudDispensaController** (delegación)
- **SolicitudDispensaController** conoce a **SolicitudDispensaRepository** (lectura y escritura)
- **SolicitudDispensaController** conoce a **SolicitudDispensa** (manipulación entidad)
- **SolicitudDispensaRepository** conoce a **SolicitudDispensa** (gestión)

## múltiples puntos de entrada

Misma característica diferenciadora que [[editarUsuario]]: el CU de edición es **el punto de convergencia** del CRUD.

| Origen | Parámetro | Mensajes 2-3 necesarios |
|-|-|-|
| `:Dispensas Abierto` | `solicitudId` | Sí — hay que cargar |
| `:Collaboration ConsultarSolicitudDispensa` | `solicitudId` | Sí — hay que cargar |
| `:Collaboration CrearSolicitudDispensa` | `solicitudNueva` (instancia) | No — ya viene cargado |

## invariante de propiedad

El `alumno` propietario de la `SolicitudDispensa` **no cambia en la edición** — se fijó en el alta. Es análogo al `tipo` invariante de [[editarUsuario]]:

- El Controller **no valida** la propiedad explícitamente en cada `actualizar()`; la inmutabilidad se asegura por construcción (no hay setter para `alumno`).
- Pero **sí debe validar** que el Alumno autenticado (resuelto vía Sesion) es el propietario de la solicitud que pretende editar. Esto es una **regla de seguridad** crítica: un Alumno no debería poder editar dispensas de otros.

Cómo se chequea (middleware, regla en el Controller, regla a nivel BD) es decisión de diseño. En análisis basta con declarar la invariante.

## trazabilidad con artefactos previos

### con especificación detallada

- **Transición de entrada `DISPENSAS_ABIERTO → SOLICITUD_DISPENSA_ABIERTA : crearSolicitudDispensa() / consultarSolicitudDispensa()`** → **dos** colaboraciones de origen del análisis (post-crear, post-consultar). El detallado **no** modela explícitamente la edición directa desde el listado, pero el análisis añade `:Dispensas Abierto` como tercer origen siguiendo el patrón pySigHor (la UI típicamente expone un atajo de edición en cada fila del listado). Misma decisión que en [[editarUsuario]].
- **Auto-actividad `editarSolicitudDispensa()` en `FormularioEdicion`** → **mensajes 4-5** (`modificarCampos` + `actualizar`)
- **Transición `guardarSolicitudDispensa()`** → **mensaje 5** `actualizar()`
- **Transición `cerrarSolicitudDispensa()`** → flujo alternativo

### con wireframe (prototipo SALT)

- **`editarSolicitudDispensaAlumno.png`** → **EditarSolicitudDispensaView**
- **`guardarSolicitudDispensaAlumno1/2.png`** → secuencia visual del guardado tras la edición

### con actores

- **`Alumno --> EditarSolicitudDispensa`** → invocación implícita en las tres colaboraciones origen

### con modelo del dominio

- **Sin trazabilidad directa**: deuda compartida con [[crearSolicitudDispensa]].

## principios de análisis aplicados

### patrón mvc

- **Controller compartido por entidad**: `SolicitudDispensaController` (consistente con [[crearSolicitudDispensa]])
- **Vista específica por CU**: `EditarSolicitudDispensaView` ≠ vistas de crear / consultar
- **Sin polimorfismo**: entidad concreta, sin jerarquía

### diagramas de colaboración

- **Múltiples enlaces de entrada explícitos**: tres colaboraciones origen
- **Flujos alternativos en prosa**: carga condicional y cierre sin guardar no se duplican en mensajes
- **Mensajes de intención**: `cargarSolicitudParaEdicion`, `modificarCampos`

### análisis puro

- **Sin tecnología**: cómo se serializa `cambios` (DTO, multipart con adjuntos) se deja al diseño
- **Sin gestión de adjuntos**: el almacenamiento físico se decide en diseño

## características del análisis

### responsabilidades identificadas

- **EditarSolicitudDispensaView**: cargar y presentar el formulario, coordinar guardado/cierre
- **SolicitudDispensaController**: mediar entre vista y repositorio; aplicar la regla de propiedad
- **SolicitudDispensaRepository**: recuperar y persistir
- **SolicitudDispensa**: representar la entidad editada (propietario invariante)

### relaciones conceptuales

- **Delegación**: vista delega lógica al controlador (idéntica a [[crearSolicitudDispensa]])
- **Convergencia**: múltiples CUs externos convergen en esta vista
- **Persistencia**: el guardado retorna `boolean` para señalizar éxito/fallo

## conexión con disciplinas rup

### desde requisitos

- **Detallado**: transición unificada de entrada → dos (en estricta) o tres (con atajo de listado) colaboraciones origen
- **Prototipo SALT**: wireframe → diseño conceptual de la vista
- **Actores**: Alumno propietario → invariante de propiedad

### hacia diseño

- Verificación de propiedad antes de cualquier `actualizar()` (regla de seguridad crítica)
- Política de concurrencia: ¿dos pestañas del mismo Alumno editando la misma solicitud?
- Gestión de adjuntos (subida, eliminación, versiones)
- Estado de la solicitud: ¿puede editarse cualquier campo en cualquier estado? (probablemente no — una solicitud "aprobada" o "rechazada" no debería ser editable; deuda de regla de negocio)
- Reconciliación de `SolicitudDispensa` con el modelo del dominio

**Código fuente:** [colaboracion.puml](/modelosUML/RUP/01-analisis/casos-uso/editarSolicitudDispensa/colaboracion.puml)

## referencias

- [Detallado `editarSolicitudDispensa()`](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Alumno/editarSolicitudDispensa.puml)
- [Prototipo SALT `editarSolicitudDispensaAlumno.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Alumno/editarSolicitudDispensaAlumno.png)
- [Caso de uso del Alumno](/modelosUML/RUP/00-requisitos/CasosDeUso/CasoDeUso/Alumno/Alumno.puml)
- [Análisis `crearSolicitudDispensa()`](/RUP/01-analisis/casos-uso/crearSolicitudDispensa/README.md)
- [Análisis `editarUsuario()`](/RUP/01-analisis/casos-uso/editarUsuario/README.md)
- [conversation-log.md](/conversation-log.md)
