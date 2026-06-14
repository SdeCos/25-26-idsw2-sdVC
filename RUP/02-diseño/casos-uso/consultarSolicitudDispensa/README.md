# CGU > consultarSolicitudDispensa (Alumno) > Diseño

> | [🏠️](/README.md) | [Diseño](/RUP/02-diseño/README.md) | [Detalle](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Alumno/consultarSolicitudDispensa.puml) | [Análisis](/RUP/01-analisis/casos-uso/consultarSolicitudDispensa/README.md) | **Diseño** | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Caso de uso**: `consultarSolicitudDispensa()` (Alumno)
- **Actor**: Alumno
- **Versión**: 1.0
- **Fecha**: 2026-05-30

## diagrama de secuencia

<div align=center>

|![Secuencia consultarSolicitudDispensa() Alumno](/images/RUP/02-diseño/casos-uso/consultarSolicitudDispensa/secuencia.svg)|
|-|
|**Disciplina**: Diseño RUP<br>**Enfoque**: Diagrama de secuencia con tecnología concreta|

</div>

[Código PlantUML](/modelosUML/RUP/02-diseño/casos-uso/consultarSolicitudDispensa/secuencia.puml)

> El diagrama muestra **solo la fase de detalle**. La fase de **listado** (`GET /dispensas` filtrado por `PoliticaAlumno`) es estructuralmente idéntica al patrón de cualquier list endpoint, igual que en [`consultarSolicitudesDispensas`](/RUP/02-diseño/casos-uso/consultarSolicitudesDispensas/README.md) del Director. No se duplica.

## participantes

| Participante | Rol |
|---|---|
| **ConsultarDispensaPage** (React, ruta `/dispensas/{id}`) | Reutilizada del ramillete Director; render condicional por rol + estado |
| **dispensasService** (axios) | Cliente HTTP, método `obtener(id)` |
| **DispensasRouter** (FastAPI) | Endpoint `GET /dispensas/{id}` — extendido con `require_rol(["director", "alumno"])` |
| **require_rol** (dependency) | Acepta los dos roles; el Service hace la verificación fina de propiedad |
| **SolicitudDispensaService** | Delega a `PoliticaAlumno.puede_ver(solicitud, alumno)` — solo retorna si `solicitud.alumno_id == alumno.id` |
| **SolicitudDispensaRepository** | `obtener_por_id(id)` con eager-load del alumno + responsable (reutilizado) |
| **SQLite** | Tabla `solicitudes_dispensa` |

## materialización del análisis

| Mensaje del análisis | Materialización en diseño |
|---|---|
| `:Dispensas Abierto → ConsultarSolicitudDispensaView : consultarSolicitudDispensa(id)` | Click en una fila del listado del Alumno → navegación SPA a `/dispensas/{id}` (fuera del diagrama, transición UI) |
| `ConsultarSolicitudDispensaView → SolicitudDispensaController : cargar(id)` | `dispensasService.obtener(id)` → `GET /dispensas/{id}` |
| Verificación de propiedad ("el Alumno autenticado debe coincidir con el `alumno` propietario") | `PoliticaAlumno.puede_ver(solicitud, alumno)` — `solicitud.alumno_id == alumno.id`. Si no, 403. |
| `<<include>> editarSolicitudDispensa(id)` (opcional) | Botón "Editar" en la ficha (solo visible si Alumno + estado PENDIENTE) → `navigate("/dispensas/{id}/editar")` |
| Listado complementario `:Dispensas Abierto` | `GET /dispensas` con `PoliticaAlumno` filtrando por `alumno_id == current_user.id`. Mismo endpoint que usa el Director (la política decide el filtro); fuera del diagrama. |

## decisiones de diseño

- **Endpoints reutilizados del ramillete Director, no duplicados** — `GET /dispensas` y `GET /dispensas/{id}` aceptan ahora `["director", "alumno"]` y la `PoliticaAcceso` decide el comportamiento. Una sola URL pública para "ver dispensas"; el rol determina qué se ve.
- **`PoliticaAlumno` como Strategy** — introducida en este ramillete por tener ya dos casos concretos (Alumno + Director). Hace ortogonal la lógica de qué puede ver/hacer cada rol respecto del flujo orquestador del Service. Cuando llegue Secretaria solo añade `PoliticaSecretaria`, sin tocar nada más.
- **Verificación de propiedad en el Service vía Política**, no en el Router — el Router solo distingue grueso (`require_rol`); la propiedad fina es regla de dominio, vive con las demás (transiciones, campos editables).
- **403 cuando la solicitud existe pero no es del Alumno** — distingue de 404 (no existe) para devolver mensaje correcto. Trade-off de seguridad: revela existencia. Aceptable porque los IDs son enumerables y el riesgo informativo es bajo en un contexto universitario.
- **Render condicional de acciones en la ficha por rol + estado** (Alumno: Editar/Cancelar si PENDIENTE; Director: Iniciar revisión / Emitir veredicto según estado). La misma página sirve a ambos.

## referencias

- [Análisis `consultarSolicitudDispensa()` (Alumno)](/RUP/01-analisis/casos-uso/consultarSolicitudDispensa/README.md)
- [Diseño `consultarSolicitudesDispensas()` (Director)](/RUP/02-diseño/casos-uso/consultarSolicitudesDispensas/README.md) — patrón master-detail compartido
- [conversation-log.md](/conversation-log.md)
