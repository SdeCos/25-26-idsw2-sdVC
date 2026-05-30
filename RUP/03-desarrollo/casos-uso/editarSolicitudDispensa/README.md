# CGU > editarSolicitudDispensa (Alumno) > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/editarSolicitudDispensa/README.md) | [Diseño](/RUP/02-diseño/casos-uso/editarSolicitudDispensa/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `editarSolicitudDispensa()` (Alumno — edita campos y/o cancela)
- **Actor**: Alumno
- **Versión**: 1.0
- **Fecha**: 2026-05-30

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| EditarSolicitudPage (`/dispensas/{id}/editar`) | [src/frontend/src/pages/EditarSolicitudPage.tsx](/src/frontend/src/pages/EditarSolicitudPage.tsx) |
| dispensasService.actualizar (reutilizado) | [src/frontend/src/services/dispensasService.ts](/src/frontend/src/services/dispensasService.ts) |
| DispensasRouter (`PATCH /dispensas/{id}`) extendido | [src/backend/app/routers/dispensas.py](/src/backend/app/routers/dispensas.py) |
| SolicitudDispensaService.actualizar refactorizado con Política | [src/backend/app/services/solicitud_dispensa_service.py](/src/backend/app/services/solicitud_dispensa_service.py) |
| PoliticaAlumno (transiciones, campos_editables) | [src/backend/app/services/politica_acceso.py](/src/backend/app/services/politica_acceso.py) |
| Schema unificado `EditarSolicitudRequest` | [src/backend/app/schemas/dispensas.py](/src/backend/app/schemas/dispensas.py) |

## materialización de las decisiones de diseño

| Decisión del diseño | Cómo se materializa |
|---|---|
| PATCH único compartido Alumno/Director | Mismo endpoint `PATCH /dispensas/{id}`, mismo `EditarSolicitudRequest`. La `PoliticaAcceso` decide qué transiciones y campos permite. |
| Cancelación como transición de estado | Botón "Cancelar solicitud" en el frontend → `PATCH { estado: "anulada" }`. Reutiliza la misma lógica del state machine. |
| Edición solo si PENDIENTE | `PoliticaAlumno.campos_editables(solicitud)` retorna `frozenset()` si no es PENDIENTE → cualquier campo intentado → 422 `CampoNoEditable` |
| GET fresco al montar | `useEffect` con `dispensasService.obtener(id)` |
| Confirmación al cancelar | `window.confirm(...)` antes del PATCH |
| Form muestra campos como `disabled` si no editable | flag `editable = estado === 'pendiente'` propaga a `<input disabled>` + mensaje informativo |

## verificación end-to-end

Validado vía `curl`:

| Escenario | Resultado |
|---|---|
| Alumno PATCH `{motivo: "x"}` en PENDIENTE | 200 + motivo actualizado |
| Alumno PATCH `{observaciones: "x"}` en PENDIENTE | 422 `Campo no editable: observaciones` (no está en sus editables) |
| Alumno PATCH `{estado: "aprobada"}` (transición ilegal para Alumno) | 422 `Transición pendiente → aprobada no permitida` |
| Alumno PATCH `{estado: "anulada"}` en PENDIENTE | 200 + estado=anulada |
| Alumno PATCH `{motivo: "x"}` en ANULADA (terminal) | 422 `Campo no editable: motivo` (campos_editables vacío en no-PENDIENTE) |
| Alumno PATCH `{estado: "anulada"}` en ANULADA | 422 transición ilegal (auto→auto no es válido) |
| Alumno PATCH `{estado: "en_revision"}` (rol incorrecto) | 422 transición no permitida para Alumno |
| Director EN_REVISION → Alumno intenta editar motivo | 422 (PENDIENTE-only edits) |
| Alumno intenta cancelar tras EN_REVISION | 422 transición ilegal |
| Cross-propiedad: Alumno PATCH una dispensa ajena | 403 `No autorizado para esta solicitud` |

### Bug encontrado y arreglado en vivo

Primera implementación del refactor saltaba `observaciones` siempre en el loop de campos editables (línea `if campo in ("estado", "observaciones"): continue`). Permitía al Alumno enviar `{observaciones: "x"}` sin error (la operación se ejecutaba como no-op). Detectado en prueba interna #6 (esperaba 422, obtuvo 200). Fix: skip de `observaciones` solo cuando `datos.estado is not None` (es decir, cuando vino acompañando a una transición). Si viene sin transición, se valida contra `campos_editables` como cualquier otro campo. Confirmado tras re-run: 422 `Campo no editable: observaciones`.

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/editarSolicitudDispensa/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/editarSolicitudDispensa/README.md)
- [Desarrollo `editarSolicitudDispensa()` (Director)](/RUP/03-desarrollo/casos-uso/editarSolicitudDispensaDirector/README.md) — comparte service + repo + router
- [conversation-log.md](/conversation-log.md)
