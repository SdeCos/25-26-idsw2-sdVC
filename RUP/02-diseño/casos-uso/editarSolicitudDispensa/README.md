# CGU > editarSolicitudDispensa (Alumno) > Diseño

> | [🏠️](/README.md) | [Diseño](/RUP/02-diseño/README.md) | [Detalle](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Alumno/editarSolicitudDispensa.puml) | [Análisis](/RUP/01-analisis/casos-uso/editarSolicitudDispensa/README.md) | **Diseño** | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Caso de uso**: `editarSolicitudDispensa()` (Alumno — edita campos y/o cancela)
- **Actor**: Alumno
- **Versión**: 1.0
- **Fecha**: 2026-05-30

## diagrama de secuencia

<div align=center>

|![Secuencia editarSolicitudDispensa() Alumno](/images/RUP/02-diseño/casos-uso/editarSolicitudDispensa/secuencia.svg)|
|-|
|**Disciplina**: Diseño RUP<br>**Enfoque**: Diagrama de secuencia con tecnología concreta|

</div>

[Código PlantUML](/modelosUML/RUP/02-diseño/casos-uso/editarSolicitudDispensa/secuencia.puml)

> El diagrama muestra **solo la fase de PATCH**. La carga inicial (`GET /dispensas/{id}` al montar) es idéntica al detalle de [`consultarSolicitudDispensa`](/RUP/02-diseño/casos-uso/consultarSolicitudDispensa/README.md).

## state machine — transiciones del Alumno

Extiende la state machine introducida en el ramillete Director:

| Transición | Quién | Side effects |
|---|---|---|
| `PENDIENTE → ANULADA` | **Alumno propietario** (nueva en este ramillete) | — |
| `PENDIENTE → EN_REVISION` | Director | ya documentada |
| `EN_REVISION → APROBADA/RECHAZADA` | Director | ya documentadas |

El Alumno **solo** puede cancelar mientras esté PENDIENTE — una vez tomada para revisión, ya no. La política rechaza con 422 cualquier otra transición.

## campos editables por el Alumno

| Estado actual | Campos editables (por `PoliticaAlumno.campos_editables`) |
|---|---|
| `PENDIENTE` | `motivo`, `horario`, `asignatura`, `periodo` |
| Cualquier otro | ninguno (frozen) |

Si el Alumno envía un campo no permitido, el Service responde 422 `CampoNoEditable`. `observaciones` nunca está en sus editables (es del Director).

## participantes

| Participante | Rol |
|---|---|
| **EditarSolicitudPage** (React, ruta `/dispensas/{id}/editar`) | Form de campos editables + botón "Guardar" + botón "Cancelar solicitud" con confirmación |
| **dispensasService** (axios) | Cliente HTTP, método `actualizar(id, datos)` |
| **DispensasRouter** (FastAPI) | Endpoint `PATCH /dispensas/{id}` — extendido con `require_rol(["director", "alumno"])` |
| **require_rol** (dependency) | Acepta los dos roles |
| **SolicitudDispensaService** | Delega a `PoliticaAlumno` para validar transición + campos editables; aplica `cambios` |
| **SolicitudDispensaRepository** | `obtener_por_id` + `actualizar` (reutilizado) |
| **SQLite** | Tabla `solicitudes_dispensa` |

## materialización del análisis

| Mensaje del análisis | Materialización en diseño |
|---|---|
| Tres entradas (`:Dispensas Abierto` / consulta / post-crear) | El Alumno puede llegar desde el listado, desde la ficha de consulta o desde la pantalla de creación. Misma ruta `/dispensas/{id}/editar`. |
| `EditarSolicitudDispensaView → SolicitudDispensaController : cargarSolicitudParaEdicion(id)` | No representada — reutiliza `GET /dispensas/{id}` (mismo flujo que el detalle de [`consultarSolicitudDispensa`](/RUP/02-diseño/casos-uso/consultarSolicitudDispensa/README.md)) |
| `EditarSolicitudDispensaView → SolicitudDispensaController : modificarCampos(id, cambios)` | `PATCH /dispensas/{id}` con body `{ motivo?, horario?, asignatura?, periodo? }` |
| Cancelar (transición `PENDIENTE → ANULADA`, ramillete Alumno) | Mismo `PATCH /dispensas/{id}` con body `{ estado: "anulada" }` — un único endpoint para cualquier operación de modificación |
| Verificación de propiedad | `PoliticaAlumno.puede_ver(solicitud, alumno)` antes de cualquier mutación. 403 si no. |

## decisiones de diseño

- **PATCH único compartido entre Alumno y Director** — el mismo endpoint sirve "editar campos", "cancelar" (Alumno) y "emitir veredicto" (Director). La `PoliticaAcceso` ramifica internamente. Schema único `EditarSolicitudRequest` con todos los campos opcionales; el rol decide qué se permite tocar.
- **Cancelación = transición de estado, no acción separada** — `PATCH { estado: "anulada" }` reutiliza la misma lógica del state machine. Coherente con el patrón del Director (las tres acciones del veredicto también son transiciones).
- **Edición sólo si PENDIENTE** — encoded en `PoliticaAlumno.campos_editables(solicitud)`: si el estado no es PENDIENTE, retorna `frozenset()`. Cualquier intento de tocar un campo retorna 422 `CampoNoEditable`.
- **Form también permite combinar edición + cancelación en un solo PATCH** — si el Alumno envía `{ motivo: "x", estado: "anulada" }`, el Service valida ambas operaciones contra la política y aplica las dos. UX poco probable pero soportado por construcción.
- **EditarSolicitudPage hace GET fresco al montar** — mismo patrón que `EditarUsuarioPage` y `EmitirVeredictoPage`. Un único code path, sin propagación de estado entre rutas.
- **Botón "Cancelar solicitud" con confirmación** — operación irreversible; UX exige doble confirmación.

## referencias

- [Análisis `editarSolicitudDispensa()` (Alumno)](/RUP/01-analisis/casos-uso/editarSolicitudDispensa/README.md)
- [Diseño `editarSolicitudDispensa()` (Director)](/RUP/02-diseño/casos-uso/editarSolicitudDispensaDirector/README.md) — comparte endpoint y `SolicitudDispensaService`
- [Diseño `consultarSolicitudDispensa()` (Alumno)](/RUP/02-diseño/casos-uso/consultarSolicitudDispensa/README.md)
- [conversation-log.md](/conversation-log.md)
