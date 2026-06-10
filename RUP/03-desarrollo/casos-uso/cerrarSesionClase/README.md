# CGU > cerrarSesionClase > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/cerrarSesionClase/README.md) | [Diseño](/RUP/02-diseño/casos-uso/cerrarSesionClase/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `cerrarSesionClase()`
- **Actor**: Profesor
- **Versión**: 1.0
- **Fecha**: 2026-06-02

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| Botón "Finalizar sesión" + modal de confirmación | [src/frontend/src/pages/SesionClaseActivaPage.tsx](/src/frontend/src/pages/SesionClaseActivaPage.tsx) función `cerrar` |
| `PATCH /sesiones-clase/{id}` con `{estado: "cerrada"}` | reutiliza endpoint de [editarSesionClase] |
| State machine en el Service (`ABIERTA → CERRADA`) | [src/backend/app/services/sesion_clase_service.py](/src/backend/app/services/sesion_clase_service.py) |

## divergencia documentada respecto al diseño

| Diseño | Implementación | Motivo |
|---|---|---|
| "El Service sella `hora_fin = now`" | **NO se sobrescribe `hora_fin`** — se mantiene la hora planeada. | Sobrescribir la hora planeada con `datetime.now().time()` perdería información útil (¿a qué hora estaba prevista la sesión?). El cierre se identifica por `estado=cerrada`; el momento exacto del cierre solo se necesitaría si hubiera reapertura, lo cual está fuera de scope. Si emerge, se añade campo `cerrada_en` separado sin tocar `hora_fin`. |

## verificación end-to-end

| Escenario | Resultado |
|---|---|
| `PATCH /sesiones-clase/{id}` con `{estado: "cerrada"}` (ABIERTA) | 200, `estado=cerrada`, `hora_fin` preservada |
| Editar tras cerrar | 422 "sesión cerrada" |
| Reabrir (`{estado: "abierta"}`) | 422 "transición cerrada → abierta no permitida" |
| Marcar asistencia en sesión CERRADA | 422 "sesión cerrada — no se puede marcar" |
| Frontend: botón "Finalizar sesión" pide `window.confirm` antes del PATCH | confirmado |

## decisiones materializadas

- **Mismo endpoint que `editarSesionClase`** — el Service detecta la transición por el body.
- **Una sola transición legal** — `(ABIERTA, CERRADA)`. Cualquier otro `estado` en el PATCH es 422.
- **`hora_fin` no se sobrescribe** — divergencia respecto al diseño (ver tabla arriba), justificada por preservación de información planeada.
- **Modal de confirmación con `window.confirm`** — fiel al wireframe.

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/cerrarSesionClase/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/cerrarSesionClase/README.md)
- [conversation-log.md](/conversation-log.md)
