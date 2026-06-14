# CGU > consultarSolicitudDispensa (Secretaria) > Diseño

> | [🏠️](/README.md) | [Diseño](/RUP/02-diseño/README.md) | [Detalle](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Secretaria/consultarSolicitudDispensa.puml) | [Análisis](/RUP/01-analisis/casos-uso/consultarSolicitudDispensaSecretaria/README.md) | **Diseño** | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Caso de uso**: `consultarSolicitudDispensa()` (Secretaria)
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-06-01

## diagrama de secuencia

<div align=center>

|![Secuencia consultarSolicitudDispensa() Secretaria](/images/RUP/02-diseño/casos-uso/consultarSolicitudDispensaSecretaria/secuencia.svg)|
|-|
|**Disciplina**: Diseño RUP<br>**Enfoque**: Diagrama de secuencia con tecnología concreta|

</div>

[Código PlantUML](/modelosUML/RUP/02-diseño/casos-uso/consultarSolicitudDispensaSecretaria/secuencia.puml)

> El diagrama modela solo la ficha individual (`GET /dispensas/{id}`). El listado `GET /dispensas` con la Secretaria como nuevo rol autorizado es endpoint complementario (mismo método del Repository que ya usan Alumno y Director vía sus políticas). Regla "no modelar fases estructuralmente triviales" — list endpoints genéricos viven en prosa.

## participantes

| Participante | Rol |
|---|---|
| **ConsultarDispensaPage** (React, ruta `/dispensas/{id}`) | Vista enriquecida con datos del Alumno titular + metadatos de auditoría (responsable, fechas, observaciones); botón "Editar" si `PoliticaSecretaria.campos_editables(estado)` ≠ vacío |
| **dispensasService** (axios) | Método `obtener(id)` ya existente |
| **DispensasRouter** (FastAPI) | Endpoint `GET /dispensas/{id}` ya existente — `require_rol` se amplía con `"secretaria"` |
| **require_rol** (dependency) | Autoriza `["alumno", "secretaria", "director"]` |
| **SolicitudDispensaService** | Consulta `PoliticaSecretaria.puede_ver(...)` → siempre `True`; sin filtro ni excepción |
| **SolicitudDispensaRepository** | `obtener_por_id` con eager-load del agregado (alumno, responsable, asignatura matriculada → asignatura) |
| **SQLite** | Tabla `solicitudes_dispensa` con joins a `usuarios`, `asignaturas_matriculadas`, `asignaturas` |

## materialización del análisis

| Mensaje del análisis | Materialización en diseño |
|---|---|
| `:Dispensas Abierto → ConsultarSolicitudDispensaSecretariaView : consultarSolicitudDispensa(id)` | Click en fila de `DispensasPage` (la Secretaria ve la lista global desde el ramillete anterior — extendida aquí) → navegación a `/dispensas/{id}` |
| `cargarSolicitud(id) : SolicitudDispensa` | `GET /dispensas/{id}` |
| `obtenerPorId(id) : SolicitudDispensa` | `SolicitudDispensaRepository.obtener_por_id(id)` — ya existente, sin cambios |
| Vista enriquecida con datos del Alumno y metadatos de auditoría | Schema `SolicitudDispensaDetalleOut` incluye `alumno` embedded, `responsable` embedded, `fecha_solicitud`, `fecha_resolucion`, `observaciones` (visible aunque sea Director quien las pone). La Secretaria ve todo lo mismo que el Director — separación por rol UI, no por schema |
| `<<include>>` opcional a editar | Botón "Editar" condicional en el frontend según `PoliticaSecretaria.campos_editables(estado)` ≠ vacío. No es transición saliente del diagrama |

## decisiones de diseño

- **Mismo endpoint `GET /dispensas/{id}`** que Alumno y Director — un solo handler, política inyectada. Coherente con la regla emergente del análisis ("misma signatura → un método").
- **`PoliticaSecretaria.puede_ver = True` siempre** — no hay ramificación `else propiedad ajena` en el `alt`. Solo `else no existe` (404).
- **Listado `GET /dispensas?alumno_id=?` extendido con Secretaria** — el endpoint ya existía para Alumno y Director. La Secretaria entra con:
  - `PoliticaSecretaria.obtener_listado(usuario, alumno_id_filtro=None)` → sin filtro de propiedad; respeta `alumno_id_filtro` si viene en la query.
  - Filtros opcionales por estado, alumno_id (no la fuerza la política — son query params del cliente). Sin Parameter Object hoy; si crecen filtros se introducirá `FiltrosDispensa` (deuda blanda registrada en [análisis exportarDispensas](/RUP/01-analisis/casos-uso/exportarDispensas/README.md)).
- **Schema único `SolicitudDispensaDetalleOut`** para los cuatro roles. La UI ramifica qué muestra (Alumno no ve `responsable_id`; Secretaria sí), pero el backend serializa el detalle completo y delega la presentación al cliente. Más simple que cuatro schemas-por-rol — el riesgo de filtración es mitigado porque el listado ya filtró por permisos.
- **Vista enriquecida con datos del Alumno titular** — incluye `nombre, apellidos, email, grado` (derivado de la matrícula). Misma decisión que la del Director: la Secretaria necesita contexto del Alumno para auditar.
- **404 honesto al id inexistente** — `obtener_por_id` retorna `None`, traducido a HTTP 404 por el Router. Mismo patrón que el resto del proyecto.
- **Sin política de auditoría de accesos** (deuda sensible RGPD del análisis) — diferido. Cuando entre el proyecto en producción esto requerirá log de accesos por la Secretaria a fichas de terceros. Hoy fuera de scope.

## prerrequisito de implementación

Mismo que los otros 3 CUs del bloque dispensa Secretaria: migración del modelo `SolicitudDispensa` para incluir FK `asignatura_matriculada_id`. La ficha de detalle muestra el agregado completo (alumno + matrícula + asignatura) — necesita el FK para hacer el `JOIN`.

## referencias

- [Análisis `consultarSolicitudDispensa()` (Secretaria)](/RUP/01-analisis/casos-uso/consultarSolicitudDispensaSecretaria/README.md)
- [Diseño `consultarSolicitudDispensa()` (Alumno) — política con propiedad](/RUP/02-diseño/casos-uso/consultarSolicitudDispensa/README.md)
- [Diseño `consultarSolicitudesDispensas()` (Director) — política sin restricción](/RUP/02-diseño/casos-uso/consultarSolicitudesDispensas/README.md)
- [Diseño `crearSolicitudDispensaSecretaria()` — debut de `PoliticaSecretaria`](/RUP/02-diseño/casos-uso/crearSolicitudDispensaSecretaria/README.md)
- [conversation-log.md](/conversation-log.md)
