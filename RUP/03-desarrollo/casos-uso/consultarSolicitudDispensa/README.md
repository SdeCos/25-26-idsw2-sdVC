# CGU > consultarSolicitudDispensa (Alumno) > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/consultarSolicitudDispensa/README.md) | [Diseño](/RUP/02-diseño/casos-uso/consultarSolicitudDispensa/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `consultarSolicitudDispensa()` (Alumno)
- **Actor**: Alumno
- **Versión**: 1.0
- **Fecha**: 2026-05-30

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| DispensasPage (`/dispensas`) ramificada por rol | [src/frontend/src/pages/DispensasPage.tsx](/src/frontend/src/pages/DispensasPage.tsx) — título y "+ Nueva solicitud" condicionales por `usuario.tipo` |
| ConsultarDispensaPage (`/dispensas/{id}`) reutilizada | [src/frontend/src/pages/ConsultarDispensaPage.tsx](/src/frontend/src/pages/ConsultarDispensaPage.tsx) — acciones por rol+estado vía componente `Acciones` |
| Layout link "Mis dispensas" para Alumno | [src/frontend/src/components/Layout.tsx](/src/frontend/src/components/Layout.tsx) |
| DispensasRouter extendido con `require_rol(["director", "alumno"])` | [src/backend/app/routers/dispensas.py](/src/backend/app/routers/dispensas.py) |
| PoliticaAlumno (Strategy) | [src/backend/app/services/politica_acceso.py](/src/backend/app/services/politica_acceso.py) |
| SolicitudDispensaService.obtener + listar usando Política | [src/backend/app/services/solicitud_dispensa_service.py](/src/backend/app/services/solicitud_dispensa_service.py) |
| Repository.obtener_por_alumno | [src/backend/app/repositories/solicitud_dispensa_repository.py](/src/backend/app/repositories/solicitud_dispensa_repository.py) |

## materialización de las decisiones de diseño

| Decisión del diseño | Cómo se materializa |
|---|---|
| Strategy `PoliticaAcceso` con dos casos concretos | `PoliticaAcceso` (ABC) + `PoliticaAlumno` + `PoliticaDirector` + factory `politica_para(usuario)` |
| Alumno solo ve sus propias | `PoliticaAlumno.obtener_listado` → `repo.obtener_por_alumno(usuario.id)` |
| Verificación de propiedad fina | `PoliticaAlumno.puede_ver` → `solicitud.alumno_id == usuario.id` |
| 403 (existe pero no propia) vs 404 (no existe) | Service lanza `NoAutorizado` vs `SolicitudNoEncontrada`; Router los traduce a 403/404 |
| Render condicional de acciones por rol + estado | Componente `<Acciones rol={...} solicitud={...} />` dentro de `ConsultarDispensaPage` |

## verificación end-to-end

Validado vía `curl`:

| Escenario | Resultado |
|---|---|
| `GET /dispensas` con Alumno | 200 + solo sus propias (`alumno_id == sesion.usuario.id`) |
| `GET /dispensas/{id}` propia | 200 + `SolicitudDispensaDetalleOut` |
| `GET /dispensas/{id}` ajena (creada manualmente con `alumno_id = admin.id`) | 403 `No autorizado para esta solicitud` |
| Listado del Alumno no incluye dispensas ajenas | confirmado (5 propias visibles, ajena id=6 excluida) |
| Director sigue viendo todas (sin filtro) | 200 |

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/consultarSolicitudDispensa/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/consultarSolicitudDispensa/README.md)
- [conversation-log.md](/conversation-log.md)
