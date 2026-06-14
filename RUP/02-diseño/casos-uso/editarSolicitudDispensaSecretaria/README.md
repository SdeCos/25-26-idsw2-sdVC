# CGU > editarSolicitudDispensa (Secretaria) > Diseño

> | [🏠️](/README.md) | [Diseño](/RUP/02-diseño/README.md) | [Detalle](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Secretaria/editarSolicitudDispensa.puml) | [Análisis](/RUP/01-analisis/casos-uso/editarSolicitudDispensaSecretaria/README.md) | **Diseño** | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Caso de uso**: `editarSolicitudDispensa()` (Secretaria)
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-06-01

## diagrama de secuencia

<div align=center>

|![Secuencia editarSolicitudDispensa() Secretaria](/images/RUP/02-diseño/casos-uso/editarSolicitudDispensaSecretaria/secuencia.svg)|
|-|
|**Disciplina**: Diseño RUP<br>**Enfoque**: Diagrama de secuencia con tecnología concreta|

</div>

[Código PlantUML](/modelosUML/RUP/02-diseño/casos-uso/editarSolicitudDispensaSecretaria/secuencia.puml)

> El diagrama muestra solo la fase de guardado; la carga inicial es idéntica a [consultarSolicitudDispensaSecretaria](/RUP/02-diseño/casos-uso/consultarSolicitudDispensaSecretaria/README.md) — la `EditarSolicitudDispensaSecretariaPage` reutiliza `dispensasService.obtener(id)` y la misma cadena hasta la BD. Política consolidada del ramillete: no duplicar fases idénticas a otro CU.

## participantes

| Participante | Rol |
|---|---|
| **EditarSolicitudDispensaSecretariaPage** (React, ruta `/dispensas/{id}/editar`) | Form con campos editables según `PoliticaSecretaria` + botón "Cancelar solicitud" |
| **dispensasService** (axios) | Método `actualizar(id, datos)` con diff cliente-side (mismo patrón que el Alumno) |
| **DispensasRouter** (FastAPI) | Endpoint `PATCH /dispensas/{id}` ya existente — `require_rol` se amplía con `"secretaria"` |
| **require_rol** (dependency) | Autoriza `["alumno", "secretaria", "director"]` (antes `["alumno", "director"]`) |
| **SolicitudDispensaService** | Orquesta vía `politica_para(current_user)` → `PoliticaSecretaria` (introducida en [crearSolicitudDispensaSecretaria](/RUP/02-diseño/casos-uso/crearSolicitudDispensaSecretaria/README.md)) |
| **SolicitudDispensaRepository** | `obtener_por_id` + `actualizar` ya existentes |
| **SQLite** | Tabla `solicitudes_dispensa` |

## materialización del análisis

| Mensaje del análisis | Materialización en diseño |
|---|---|
| Origen tres colaboraciones (`:Dispensas Abierto`, `:Collaboration ConsultarSolicitudDispensaSecretaria`, `:Collaboration CrearSolicitudDispensaSecretaria`) | Tres orígenes UI conceptuales → todos navegan a `/dispensas/{id}/editar` con el mismo path. El form siempre hace `GET /dispensas/{id}` fresco al montar (política "GET fresco siempre", consolidada en `editarUsuario`) |
| `modificarCampos(motivo, asignaturaMatriculada)` (misma firma que el Alumno, distinta política) | `PATCH /dispensas/{id}` body `{ motivo?, asignatura_matriculada_id?, estado? }`. Mismo schema unificado `EditarSolicitudRequest` que ya se introdujo en el ramillete Alumno |
| Verificación de propiedad **no aplica** | `PoliticaSecretaria.puede_ver` → `True` siempre; `transiciones_permitidas` y `campos_editables` no consultan propiedad |
| Auditoría del editor (deuda del análisis — 3 opciones) | Diferida — coherente con la decisión del análisis. No se persiste `ultimo_editor`; eventual log externo cubre auditoría hasta que aparezca CU explícito |

## decisiones de diseño

- **Mismo endpoint `PATCH /dispensas/{id}` para los tres roles** — el shape de la mutación es uniforme; la política decide qué se admite. Coherente con la decisión del ramillete Alumno (Strategy `PoliticaAcceso`).
- **`PoliticaSecretaria`** (introducida en `crearSolicitudDispensaSecretaria`) define para el editar:
  - `transiciones_permitidas` → `{(PENDIENTE, ANULADA)}` — la Secretaria puede cancelar como el Alumno, pero **no** puede emitir veredicto (eso es del Director).
  - `campos_editables(PENDIENTE)` → `{motivo, asignatura_matriculada_id}` — mismos que el Alumno.
  - `campos_editables(estado != PENDIENTE)` → `{}` — no se edita una vez en revisión o terminal.
  - Sin `side_effects` (no toca `responsable_id` — ese es del alta o del Director al emitir veredicto).
- **Reglas emergentes del análisis materializadas en código**:
  > "El patrón 'métodos específicos por rol' se aplica solo cuando la signatura difiere. Cuando solo la política varía con la misma signatura, un único método con dispatch interno por subtipo de `Sesion.usuario` es más limpio."
  
  La Secretaria edita los **mismos campos** que el Alumno (`modificarCampos`) — un solo método del Service, política inyectada. Si en el futuro la Secretaria gana operaciones con signatura distinta (ej. `reasignarSolicitudDispensa` a otro alumno), entonces sí se separa.
- **Diff cliente-side antes del PATCH** — mismo patrón que el ramillete Alumno y `editarUsuario`: la página envía solo los campos que el usuario tocó. Evita PATCHes redundantes.
- **Invariante `alumno_id` ratificado** — `alumno_id` **no está en `EditarSolicitudRequest`**. Si la Secretaria necesitara transferir una solicitud a otro alumno, sería CU separado (`reasignarSolicitudDispensa`), no edición. Coherente con la decisión equivalente del Alumno (no autoediciable el propietario).
- **Sin defensa explícita "no es la propietaria"** — `PoliticaSecretaria.puede_ver = True` siempre; el flujo no necesita el check. Coherente con la posición de "operadora global" del rol Secretaria.
- **Errores diferenciados con 422** (mismos códigos que el Alumno): `CampoNoEditable` si intenta tocar un campo no permitido por su política/estado (ej. `observaciones`, que es del Director), `TransicionNoValida` si pide un cambio de estado prohibido (ej. `APROBADA` directo).
- **Sin botón "Editar" en estado terminal o EN_REVISION** — UI defensiva: la página `EditarSolicitudDispensaSecretariaPage` muestra los campos `disabled` con mensaje "no editable en este estado" si `campos_editables(estado)` retorna vacío. El backend lo enforça igual (defensa en profundidad).

## prerrequisito de implementación

Mismo prerrequisito que [crearSolicitudDispensaSecretaria](/RUP/02-diseño/casos-uso/crearSolicitudDispensaSecretaria/README.md): migración del modelo `SolicitudDispensa` a `asignatura_matriculada_id`. La política `PoliticaAlumno.campos_editables` también cambia tras la migración (`{motivo, asignatura, periodo, horario}` → `{motivo, asignatura_matriculada_id}`).

## referencias

- [Análisis `editarSolicitudDispensa()` (Secretaria)](/RUP/01-analisis/casos-uso/editarSolicitudDispensaSecretaria/README.md)
- [Diseño `editarSolicitudDispensa()` (Alumno) — política gemela con propiedad](/RUP/02-diseño/casos-uso/editarSolicitudDispensa/README.md)
- [Diseño `editarSolicitudDispensa()` (Director) — política con veredicto](/RUP/02-diseño/casos-uso/editarSolicitudDispensaDirector/README.md)
- [Diseño `crearSolicitudDispensaSecretaria()` — debut de `PoliticaSecretaria`](/RUP/02-diseño/casos-uso/crearSolicitudDispensaSecretaria/README.md)
- [conversation-log.md](/conversation-log.md)
