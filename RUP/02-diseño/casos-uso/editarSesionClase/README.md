# CGU > editarSesionClase > Diseño

> | [🏠️](/README.md) | [Diseño](/RUP/02-diseño/README.md) | [Detalle](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Profesor/editarSesionClase.puml) | [Análisis](/RUP/01-analisis/casos-uso/editarSesionClase/README.md) | **Diseño** | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Caso de uso**: `editarSesionClase()`
- **Actor**: Profesor
- **Versión**: 1.0
- **Fecha**: 2026-06-02

## diagrama de secuencia

<div align=center>

|![Secuencia editarSesionClase()](/images/RUP/02-diseño/casos-uso/editarSesionClase/secuencia.svg)|
|-|
|**Disciplina**: Diseño RUP<br>**Enfoque**: Diagrama de secuencia con tecnología concreta|

</div>

[Código PlantUML](/modelosUML/RUP/02-diseño/casos-uso/editarSesionClase/secuencia.puml)

El diagrama muestra solo la fase de guardado. La carga inicial de la sesión es idéntica a la del consultar (no hay CU separado por ahora; el `GET /sesiones-clase/{id}` lo materializaremos junto al CU de visualización activa). El editar reutiliza la `SesionDeClase` ya cargada en `SesionClaseActivaPage` — el patrón "no duplicar fases" aplicado en [editarUsuario](/RUP/02-diseño/casos-uso/editarUsuario/README.md) y [editarSolicitudDispensaDirector](/RUP/02-diseño/casos-uso/editarSolicitudDispensaDirector/README.md).

## participantes

| Participante | Rol |
|---|---|
| **SesionClaseActivaPage** (React, ruta `/sesiones-clase/{id}`) | Vista de la sesión activa con cabecera editable in-situ — toggle "Editar"/"Guardar"/"Cancelar". **No es ruta separada** (decisión del análisis respetada: in-situ, no modal) |
| **sesionesClaseService** (axios) | Método `actualizar(id, cambios)` — diff cliente-side, mismo patrón que `EditarUsuarioPage` |
| **SesionesClaseRouter** (FastAPI) | Endpoint `PATCH /sesiones-clase/{id}` con `Depends(require_rol(["profesor"]))` en parámetro (necesita `current_user` para defensa de propiedad) |
| **require_rol** (dependency) | Autoriza `"profesor"` — la verificación de propiedad es responsabilidad del Service |
| **SesionClaseService** | Valida propietario (`sesion.profesor_id == current_user.id`), estado (`== ABIERTA`) y campos (descartados los no editables por el schema). Aplica los cambios con `exclude_unset=True` |
| **SesionClaseRepository** | Método `actualizar(sesion, cambios)` ya existente desde el patrón consolidado |
| **SQLite** | Tabla `sesiones_clase` (introducida en [crearSesionClase](/RUP/02-diseño/casos-uso/crearSesionClase/README.md)) |

## materialización del análisis

| Mensaje del análisis | Materialización en diseño |
|---|---|
| `:Sesion Asistencia Abierta → EditarSesionClaseView : editarSesionClase(sesion)` | Click "Editar" en la cabecera de `SesionClaseActivaPage` activa el modo edición in-situ; los campos `fecha`/`hora`/`aula`/`tema` pasan de display a inputs |
| `modificarCampos(sesionId, cambios) : boolean` | `PATCH /sesiones-clase/{id}` con body parcial (solo los campos que cambiaron — diff cliente-side, mismo patrón que `EditarUsuarioPage`) |
| `actualizar(sesion) : boolean` | `SesionClaseRepository.actualizar` aplica `setattr` por cada campo del dict y hace `flush` |
| Vuelta al mismo estado `SESION_ASISTENCIA_ABIERTA` | Tras 200, salir del modo edición — la página no navega, los campos vuelven a display con los nuevos valores |

## decisiones de diseño

- **Edición in-situ, no ruta separada** — el análisis lo exige explícitamente. La página `/sesiones-clase/{id}` es **una sola** con dos modos (ver / editar). Coherente con la decisión del prototipo del SDR: el Profesor no abandona la pantalla de asistencias para tocar metadatos.
- **`EditarSesionClaseRequest` sin `asignatura_id`/`grupo`/`profesor_id`** — las invariantes del análisis se materializan **por contrato** (Pydantic descarta esos campos con `extra="ignore"`), no por check explícito en el Service. Mismo patrón que `tipo` en `EditarUsuarioRequest` y `responsable_id`/`estado` no permitidos al Alumno por la `PoliticaAlumno`. Si el cliente los manda, se ignoran silenciosamente.
- **`PATCH` con body parcial** — `cambios` del análisis se materializa como dict de Pydantic con `exclude_unset=True`. Solo los campos enviados se actualizan; el resto queda intacto. Sin necesidad de `PUT` (que exigiría enviar el objeto completo).
- **Defensa de propiedad en el Service** — `if sesion.profesor_id != current_user.id: raise SesionClaseNoEditable` → 403. `require_rol(["profesor"])` autoriza el rol, pero **no** verifica que sea **su** sesión (un Profesor no puede editar la sesión de otro). Esta es la decisión paralela a la regla de propiedad que en `SolicitudDispensa` vive en la `PoliticaAlumno`; aquí, al no haber Strategy, vive directamente en el Service.
- **Defensa de estado en el Service** — `if sesion.estado != ABIERTA: raise SesionClaseNoEditable` → 422. No se puede editar una sesión `CERRADA`. La state machine de `SesionDeClase` (introducida en `crearSesionClase`) constriñe la edición igual que la de `SolicitudDispensa` constriñe los `modificarCampos` del Alumno (solo si `PENDIENTE`).
- **Botón "Volver" / "Cancelar" con `window.confirm`** si hay cambios sin guardar — resuelve la deuda del análisis. Mismo patrón que el botón "Cancelar solicitud" de `EditarSolicitudPage`. Sin estado de "borrador local" — YAGNI; el Profesor edita rápido o descarta.
- **Diff cliente-side** — `sesionesClaseService.actualizar(id, diff(original, modificado))` solo manda los campos cambiados. Mismo helper que ya se usa en `EditarUsuarioPage` y `EditarSolicitudPage` — el patrón es consistente en todo el frontend.
- **Sin invalidación de asistencias por edición** — el análisis lo registra como regla de negocio abierta (cambiar `aula` no invalida, cambiar `fecha` quizás sí). **Diferido**: hoy no hay `Asistencia` persistida en BD (entra con `registrarTomaAsistencia`). La regla se decidirá entonces.
- **Sin control de concurrencia** (deuda del análisis: dos pestañas del mismo Profesor) — diferido. Hoy "último-en-escribir-gana". YAGNI mientras no haya evidencia de conflicto real.

## campos editables vs invariantes

| Campo | Editable | Materialización |
|---|---|---|
| `asignatura_id` | No | Ausente del schema `EditarSesionClaseRequest`; `extra="ignore"` lo descarta si llega |
| `grupo` | No | Mismo mecanismo |
| `profesor_id` | No | Mismo mecanismo + defensa de propiedad |
| `estado` | No (aquí) | Solo cambia vía `cerrarSesionClase` (CU separado con su propia transición) |
| `fecha` | Sí | Campo del schema |
| `hora_inicio` | Sí | Campo del schema |
| `hora_fin` | Sí | Campo del schema; validación `hora_fin > hora_inicio` en el Service |
| `aula` | Sí | Campo del schema |
| `tema` | Sí | Campo del schema |

## referencias

- [Análisis `editarSesionClase()`](/RUP/01-analisis/casos-uso/editarSesionClase/README.md)
- [Diseño `crearSesionClase()` — entidad nueva, esquema y catálogo](/RUP/02-diseño/casos-uso/crearSesionClase/README.md)
- [Diseño `editarUsuario()` — patrón PATCH con diff cliente-side y `extra="ignore"`](/RUP/02-diseño/casos-uso/editarUsuario/README.md)
- [Diseño `editarSolicitudDispensa()` (Director) — patrón de validación en el Service](/RUP/02-diseño/casos-uso/editarSolicitudDispensaDirector/README.md)
- [conversation-log.md](/conversation-log.md)
