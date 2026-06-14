# CGU > crearSolicitudDispensa (Secretaria) > Diseño

> | [🏠️](/README.md) | [Diseño](/RUP/02-diseño/README.md) | [Detalle](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Secretaria/crearSolicitudDispensa.puml) | [Análisis](/RUP/01-analisis/casos-uso/crearSolicitudDispensaSecretaria/README.md) | **Diseño** | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Caso de uso**: `crearSolicitudDispensa()` (Secretaria)
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-06-01

## diagrama de secuencia

<div align=center>

|![Secuencia crearSolicitudDispensa() Secretaria](/images/RUP/02-diseño/casos-uso/crearSolicitudDispensaSecretaria/secuencia.svg)|
|-|
|**Disciplina**: Diseño RUP<br>**Enfoque**: Diagrama de secuencia con tecnología concreta|

</div>

[Código PlantUML](/modelosUML/RUP/02-diseño/casos-uso/crearSolicitudDispensaSecretaria/secuencia.puml)

## participantes

| Participante | Rol |
|---|---|
| **CrearSolicitudDispensaSecretariaPage** (React, ruta `/dispensas/nuevo-en-nombre-de`) | Form con **selector de Alumno** (autocomplete contra `GET /alumnos?q=`) + selector de Asignatura Matriculada del alumno elegido (cascada, `GET /alumnos/{id}/asignaturas-matriculadas`) + motivo |
| **dispensasService** (axios) | Método `crear(datos)` extendido para aceptar `alumno_id` en el body |
| **DispensasRouter** (FastAPI) | Endpoint `POST /dispensas` ya existente — se amplía `require_rol` y el schema acepta `alumno_id` opcional |
| **require_rol** (dependency) | Autoriza `["alumno", "secretaria"]` (antes solo `"alumno"`) |
| **SolicitudDispensaService** | Resuelve `responsable_id = current_user.id`; si el rol es Secretaria, lee `alumno_id` del body; si es Alumno, lo sobrescribe con `current_user.id` (defensa contra suplantación) |
| **politica_acceso** | Estrena `PoliticaSecretaria` (factory `politica_para(usuario)` actualizado) |
| **SolicitudDispensaRepository** | Misma firma `crear(alumno_id, asignatura_matriculada_id, motivo, responsable_id)` — agnóstico al rol |
| **SQLite** | Tabla `solicitudes_dispensa` (con `asignatura_matriculada_id` FK tras migración — ver "prerrequisito") |

## materialización del análisis

| Mensaje del análisis | Materialización en diseño |
|---|---|
| `:Dispensas Abierto → CrearSolicitudDispensaSecretariaView : crearSolicitudDispensa()` | Click "+ Nueva en nombre de" en `DispensasPage` (visible solo si rol Secretaria) → `/dispensas/nuevo-en-nombre-de` |
| Validar `alumno`, `asignatura`, `periodo`, `horario` | El form valida `alumno_id` (autocomplete contra la BD) + `asignatura_matriculada_id` debe pertenecer a `alumno_id` (defensa en el Service) |
| `crearSolicitudDispensaEnNombreDe(...) : SolicitudDispensa` | `POST /dispensas` con body `{ alumno_id, asignatura_matriculada_id, motivo }`. El Service distingue por rol — no hay endpoint separado |
| Resolución implícita de `responsable = Sesion.usuario` | `responsable_id = current_user.id` en el Service — la Secretaria queda como auditor del alta |
| `<<include>> editarSolicitudDispensa(solicitudNueva)` | Tras 201, navega a `/dispensas/{id}` (ficha de consulta) — desde ahí la Secretaria puede pulsar "Editar" si quiere refinar. Misma decisión que en [crearSolicitudDispensa Alumno](/RUP/02-diseño/casos-uso/crearSolicitudDispensa/README.md) |

## decisiones de diseño

- **Mismo endpoint `POST /dispensas`, no `POST /dispensas/en-nombre-de`** — el shape de la operación es idéntico (crea una solicitud); la única diferencia es la procedencia de `alumno_id` (sesión vs body). Dos endpoints duplicarían lógica y router; uno solo con dispatch interno por rol es más limpio. El campo `alumno_id` en el body es ignorado si el rol es Alumno (Service lo sobrescribe desde `current_user`).
- **Defensa contra suplantación**: si rol Alumno y `alumno_id` en body ≠ `current_user.id`, el Service lo **descarta silenciosamente** (no 4xx) y persiste el de la sesión. Coherente con `crearUsuario` que también descarta campos invasivos en lugar de fallar. Documentado en el schema.
- **`asignatura_matriculada_id` debe pertenecer al `alumno_id`** — el Service valida que `AsignaturaMatriculada.matricula.alumno_id == alumno_id` antes de persistir. Si no, 422 `AsignaturaMatriculadaIncoherente`. Evita que la Secretaria solicite dispensa de una asignatura que el alumno no cursa.
- **`PoliticaSecretaria` introducida en este CU** y reutilizada en los 3 restantes del ramillete. Contrato del módulo `app/services/politica_acceso.py`:
  - `obtener_listado(usuario, alumno_id_filtro?)` — sin filtro de propiedad; respeta `alumno_id_filtro` si viene
  - `puede_ver(solicitud, usuario)` → `True` siempre
  - `transiciones_permitidas(usuario)` → `{(PENDIENTE, ANULADA)}` (misma capacidad que el Alumno propietario, sin restricción de propiedad)
  - `campos_editables(estado, usuario)` → `{motivo, asignatura_matriculada_id}` si `estado == PENDIENTE`, vacío si terminal
  - `side_effects` → ninguno (la Secretaria no emite veredicto)
- **Cliente envía `alumno_id` explícito** — no se infiere desde la URL ni desde un selector pre-cargado. Razón: la Secretaria opera sobre cualquier alumno; el contexto no es persistente. Coherente con el patrón de "Secretaria es operadora global" ya consolidado en [[consultarListaAlumnosSecretaria]].
- **Sin notificación al alumno** — coherente con la decisión deferida en el ramillete Director (deuda blanda registrada). El alumno verá la solicitud aparecer al consultar su listado.

## prerrequisito de implementación: migración `SolicitudDispensa → AsignaturaMatriculada`

Este diseño asume **forward-looking** que ya se ha migrado el modelo de `SolicitudDispensa`:
- **Antes** (estado actual del código): `asignatura: str, periodo: str, horario: str` libres.
- **Después** (estado asumido aquí): `asignatura_matriculada_id: int FK` → `asignaturas_matriculadas.id`. `periodo` y `horario` se derivan (curso académico de la `Matricula`; horario de `Asignatura.curso_plan` o se descarta como atributo no usado).

La migración (paso 4 del orden interno del ramillete) debe ejecutarse antes de implementar este CU. Cambios:
- `app/models/solicitud_dispensa.py`: añadir `asignatura_matriculada_id` FK, marcar columnas viejas para borrar tras migrar datos seed.
- `app/schemas/dispensas.py`: cambiar inputs y outputs.
- `app/services/politica_acceso.py`: `PoliticaAlumno.campos_editables` cambia `{motivo, asignatura, periodo, horario}` → `{motivo, asignatura_matriculada_id}`.
- `app/services/solicitud_dispensa_service.py`: ajustar `crear` y `actualizar`.
- Frontend `CrearSolicitudPage` (Alumno) y `EditarSolicitudPage` (Alumno): selector de asignatura matriculada en lugar de inputs libres.
- `scripts/seed.py`: regenerar 3 dispensas seed con FK a asignaturas matriculadas reales.

## referencias

- [Análisis `crearSolicitudDispensa()` (Secretaria)](/RUP/01-analisis/casos-uso/crearSolicitudDispensaSecretaria/README.md)
- [Diseño `crearSolicitudDispensa()` (Alumno) — CU gemelo con `alumno_id` implícito](/RUP/02-diseño/casos-uso/crearSolicitudDispensa/README.md)
- [Diseño `importarMatriculas()` — debut de `AsignaturaMatriculada`](/RUP/02-diseño/casos-uso/importarMatriculas/README.md)
- [conversation-log.md](/conversation-log.md)
