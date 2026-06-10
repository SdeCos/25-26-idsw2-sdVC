# CGU > consultarSolicitudDispensa (Profesor) > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/consultarSolicitudDispensaProfesor/README.md) | [Diseño](/RUP/02-diseño/casos-uso/consultarSolicitudDispensaProfesor/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `consultarSolicitudDispensa()` (Profesor)
- **Actor**: Profesor
- **Versión**: 1.0
- **Fecha**: 2026-06-02

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| DispensasPage adaptada (texto "Dispensas de mis asignaturas", sin botones de creación/export) | [src/frontend/src/pages/DispensasPage.tsx](/src/frontend/src/pages/DispensasPage.tsx) |
| ConsultarDispensaPage — `<Acciones rol="otro">` no renderiza botones para Profesor | [src/frontend/src/pages/ConsultarDispensaPage.tsx](/src/frontend/src/pages/ConsultarDispensaPage.tsx) |
| dispensasService.listar/obtener (sin cambios) | [src/frontend/src/services/dispensasService.ts](/src/frontend/src/services/dispensasService.ts) |
| DispensasRouter — `require_rol` extendido a `["director","alumno","secretaria","profesor"]` | [src/backend/app/routers/dispensas.py](/src/backend/app/routers/dispensas.py) |
| PoliticaProfesor (factory `politica_para` actualizada) | [src/backend/app/services/politica_acceso.py](/src/backend/app/services/politica_acceso.py) |
| SolicitudDispensaRepository.obtener_por_asignaturas (JOIN explícito) | [src/backend/app/repositories/solicitud_dispensa_repository.py](/src/backend/app/repositories/solicitud_dispensa_repository.py) |

## verificación end-to-end

| Escenario | Resultado |
|---|---|
| Profesor lista dispensas (2 de IYA040/IYA041 — IYA010 NO impartida) | filtrado correcto |
| Profesor obtiene dispensa de IYA040 | 200 |
| Profesor obtiene dispensa de IYA010 | 403 `NoAutorizado` |
| Profesor PATCH dispensa (transición vacía) | 422 `TransicionNoValida` |
| Frontend: la ficha del Profesor no muestra botones de acción | comportamiento esperado (read-only puro) |

## decisiones materializadas

- **`PoliticaProfesor`** — cuarta y última política sobre `SolicitudDispensa`. Read-only puro (transiciones y campos editables vacíos).
- **Mismo Service + Repository + endpoints** que los otros roles — el dispatch vive enteramente en la Política inyectada.
- **JOIN explícito `solicitudes_dispensa JOIN asignaturas_matriculadas`** en `obtener_por_asignaturas` — `joinedload` no permite filtrar; bug detectado durante las pruebas (listado del Profesor devolvía 3 en vez de 2) y corregido.
- **404 vs 403 distinguidos** — el Service devuelve 404 si no existe; la Política rechaza con 403 si existe pero la asignatura no es impartida.
- **Cierre del polimorfismo del Controller sobre la entidad más operada** — 4 roles, 4 políticas, 1 Service.

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/consultarSolicitudDispensaProfesor/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/consultarSolicitudDispensaProfesor/README.md)
- [conversation-log.md](/conversation-log.md)
