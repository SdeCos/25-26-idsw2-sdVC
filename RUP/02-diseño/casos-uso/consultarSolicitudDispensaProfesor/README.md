# CGU > consultarSolicitudDispensa (Profesor) > Diseño

> | [🏠️](/README.md) | [Diseño](/RUP/02-diseño/README.md) | [Detalle](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Profesor/consultarSolicitudDispensa.puml) | [Análisis](/RUP/01-analisis/casos-uso/consultarSolicitudDispensaProfesor/README.md) | **Diseño** | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Caso de uso**: `consultarSolicitudDispensa()` (Profesor)
- **Actor**: Profesor
- **Versión**: 1.0
- **Fecha**: 2026-06-02

## diagrama de secuencia

<div align=center>

|![Secuencia consultarSolicitudDispensa() Profesor](/images/RUP/02-diseño/casos-uso/consultarSolicitudDispensaProfesor/secuencia.svg)|
|-|
|**Disciplina**: Diseño RUP<br>**Enfoque**: Diagrama de secuencia con tecnología concreta|

</div>

[Código PlantUML](/modelosUML/RUP/02-diseño/casos-uso/consultarSolicitudDispensaProfesor/secuencia.puml)

El diagrama muestra solo la ficha individual. El listado del Profesor (`GET /dispensas`) es estructuralmente idéntico al ya existente para Alumno/Director/Secretaria — la `PoliticaProfesor.obtener_listado` filtra y la `DispensasPage` ya ramifica por rol. Sin diagrama dedicado del listado (regla "no modelar fases triviales").

## participantes

| Participante | Rol |
|---|---|
| **ConsultarDispensaPage** (React, `/dispensas/{id}`) | Ficha enriquecida ya existente — la sección "Acciones" no muestra ningún botón para el Profesor (read-only puro, sin editar/cancelar/veredicto) |
| **dispensasService** (axios) | Reutiliza `obtener(id)` ya existente |
| **DispensasRouter** (FastAPI) | Endpoint `GET /dispensas/{id}` ya existente — se amplía `require_rol` a `["alumno", "secretaria", "director", "profesor"]` |
| **require_rol** (dependency) | Autoriza los cuatro roles |
| **SolicitudDispensaService** | `obtener(id, current_user)` ya existente — delega a la Política la verificación de visibilidad |
| **politica_acceso** | Estrena `PoliticaProfesor` (factory `politica_para(usuario)` actualizado, **cuarta política** del módulo) |
| **SolicitudDispensaRepository** | Reutiliza `obtener_por_id` ya existente (con eager-load del agregado) |
| **SQLite** | Tablas `solicitudes_dispensa`, `asignaturas_matriculadas`, `matriculas`, `asignaturas`, `usuarios`, `profesor_asignaturas` |

## materialización del análisis

| Mensaje del análisis | Materialización en diseño |
|---|---|
| `:Dispensas Abierto → ConsultarSolicitudDispensaProfesorView : consultarSolicitudDispensa(solicitudId)` | Click en fila del listado → `navigate("/dispensas/{id}")` |
| `cargarSolicitud(solicitudId) : SolicitudDispensa` | `dispensasService.obtener(id)` → `GET /dispensas/{id}` |
| `obtenerPorId(solicitudId) : SolicitudDispensa` | `SolicitudDispensaRepository.obtener_por_id` (eager-load ya existente) |
| Verificación "Profesor competente" | `PoliticaProfesor.puede_ver(solicitud, usuario)` → `True` si `solicitud.asignatura_matriculada.asignatura_id ∈ usuario.asignaturas_impartidas`. 403 si no |

## decisiones de diseño

- **`PoliticaProfesor` introducida en este CU** — **cuarta política** del módulo `app/services/politica_acceso.py`, cierre del polimorfismo del Controller sobre `SolicitudDispensa` para todos los roles del proyecto. Contrato:
  - `obtener_listado(usuario)` — filtra por `JOIN solicitudes_dispensa → asignaturas_matriculadas → asignatura JOIN profesor_asignaturas WHERE profesor_id = usuario.id`
  - `puede_ver(solicitud, usuario)` → `True` si la asignatura de la solicitud está en las impartidas; `False` si no
  - `transiciones_permitidas(usuario)` → `set()` vacío (read-only puro, sin write paths)
  - `campos_editables(estado, usuario)` → `set()` vacío
  - `side_effects` → ninguno
- **Mismo endpoint `GET /dispensas/{id}` que los otros roles** — el dispatch por rol vive enteramente en la Política. La firma del endpoint y del Service son idénticas para los cuatro roles. Aplica la regla emergente consolidada: cuando solo la política varía, Strategy `PoliticaAcceso`; cuando la signatura difiere, métodos del Service por rol (`crearSolicitudDispensaEnNombreDe` de Secretaria).
- **Read-only puro en el frontend** — la `ConsultarDispensaPage` ya ramifica acciones por rol (componente `<Acciones rol={...}>`). Para el Profesor, ese componente **no renderiza ningún botón**. La asimetría con los otros tres roles (Alumno: Editar si PENDIENTE; Director: Iniciar revisión / Veredicto; Secretaria: Editar si PENDIENTE) es honesta — el Profesor es observador, no participante en el flujo de dispensas.
- **`require_rol` extendido** a los 4 roles en `GET /dispensas` y `GET /dispensas/{id}`. El `PATCH`, `POST` y `GET /dispensas/exportar` quedan sin cambios (siguen en sus subconjuntos previos).
- **Cierre del polimorfismo del Controller sobre `SolicitudDispensa`** — esta es la **cuarta y última política** sobre la entidad. Con cuatro roles caracterizados:
  - Alumno: propietario, edita motivo y puede cancelar (`PENDIENTE → ANULADA`)
  - Director: ve todas, edita veredicto (3 transiciones)
  - Secretaria: ve todas, edita campos como Alumno + puede cancelar
  - **Profesor: ve las de asignaturas que imparte, read-only puro**
  
  La entidad más operada del proyecto queda completamente diseñada con un único Service + un único Repository + cuatro Políticas. Sin proliferación de Controllers.
- **Filtro del listado vía join con `profesor_asignaturas`** — la Política inyecta el `JOIN profesor_asignaturas ON asignatura_id` cuando el rol es Profesor. Una sola query con filtro en `WHERE`. Reutiliza la tabla N:M introducida en [consultarListaAlumnos](/RUP/02-diseño/casos-uso/consultarListaAlumnos/README.md).
- **404 vs 403** — el Service distingue: si la dispensa **no existe** → 404. Si existe pero la Política no autoriza → 403. Coherente con la decisión paralela del Profesor sobre `consultarDetalleAlumno` (sin enmascaramiento por privacidad).
- **Sin auditoría de accesos** (deuda RGPD del análisis) — diferida. Hoy no se registra quién consultó qué dispensa. Si emerge la necesidad, se introduce un log de eventos separado.
- **Sin CU de listado separado** (deuda blanda del análisis: "consultarSolicitudesDispensas Profesor" master-detail) — fuera de scope del denominador 26. El listado existe (es el `GET /dispensas` extendido) pero no como CU formal del actor.

## cuarta política y cierre de la entidad más operada

| Rol | Política | obtener_listado | puede_ver | transiciones | campos editables |
|---|---|---|---|---|---|
| Alumno | `PoliticaAlumno` | `WHERE alumno_id = sesion.usuario.id` | propietario | `{(PENDIENTE, ANULADA)}` | motivo, asignatura_matriculada_id (si PENDIENTE) |
| Director | `PoliticaDirector` | sin filtro | siempre | 3 (veredicto) | observaciones (si EN_REVISION) |
| Secretaria | `PoliticaSecretaria` | sin filtro | siempre | `{(PENDIENTE, ANULADA)}` | motivo, asignatura_matriculada_id (si PENDIENTE) |
| **Profesor** | **`PoliticaProfesor`** | **JOIN con `profesor_asignaturas`** | **asignatura impartida** | **vacío** | **vacío** |

La tabla refleja el éxito del patrón: la entidad con más roles operando (4) se mantiene con **un único Service** + **un único Repository** + **cuatro políticas** inyectables. Sin if-else por rol en el código de aplicación.

## referencias

- [Análisis `consultarSolicitudDispensa()` (Profesor)](/RUP/01-analisis/casos-uso/consultarSolicitudDispensaProfesor/README.md)
- [Diseño `consultarSolicitudDispensa()` (Alumno) — primera política del módulo](/RUP/02-diseño/casos-uso/consultarSolicitudDispensa/README.md)
- [Diseño `consultarSolicitudesDispensas()` (Director) — `PoliticaDirector`](/RUP/02-diseño/casos-uso/consultarSolicitudesDispensas/README.md)
- [Diseño `consultarSolicitudDispensa()` (Secretaria) — `PoliticaSecretaria`](/RUP/02-diseño/casos-uso/consultarSolicitudDispensaSecretaria/README.md)
- [Diseño `consultarListaAlumnos()` (Profesor) — origen de `profesor_asignaturas`](/RUP/02-diseño/casos-uso/consultarListaAlumnos/README.md)
- [conversation-log.md](/conversation-log.md)
