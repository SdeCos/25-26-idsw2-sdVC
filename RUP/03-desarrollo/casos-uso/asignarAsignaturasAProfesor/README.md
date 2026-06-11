# CGU > asignarAsignaturasAProfesor > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/asignarAsignaturasAProfesor/README.md) | [Diseño](/RUP/02-diseño/casos-uso/asignarAsignaturasAProfesor/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `asignarAsignaturasAProfesor()`
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-06-11

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| AsignarAsignaturasProfesorPage (`/asignaciones`) | [src/frontend/src/pages/AsignarAsignaturasProfesorPage.tsx](/src/frontend/src/pages/AsignarAsignaturasProfesorPage.tsx) |
| profesoresService extendido (`listar`, `impartidas`, `asignarImpartida`, `desasignarImpartida`) | [src/frontend/src/services/profesoresService.ts](/src/frontend/src/services/profesoresService.ts) |
| Ruta gated + link "Asignaciones" en el nav | [src/frontend/src/App.tsx](/src/frontend/src/App.tsx), [src/frontend/src/components/Layout.tsx](/src/frontend/src/components/Layout.tsx) |
| Router separado `routers/asignaciones.py` con `POST/DELETE/GET /usuarios/{pid}/asignaturas-impartidas/...` | [src/backend/app/routers/asignaciones.py](/src/backend/app/routers/asignaciones.py) |
| `GET /profesores` (selector de profesor para Secretaría) | [src/backend/app/routers/profesores.py](/src/backend/app/routers/profesores.py) |
| `UsuarioService.asignar`, `desasignar`, `obtener_impartidas` con validación de subtipo `isinstance(usuario, Profesor)` | [src/backend/app/services/usuario_service.py](/src/backend/app/services/usuario_service.py) |
| Excepciones `NoEsProfesor`, `AsignaturaNoEncontrada` | [src/backend/app/services/usuario_service.py](/src/backend/app/services/usuario_service.py) |
| `UsuarioRepository.crear_imparte` (idempotente), `eliminar_imparte` (idempotente), `obtener_impartidas` | [src/backend/app/repositories/usuario_repository.py](/src/backend/app/repositories/usuario_repository.py) |
| Modelo `AsignaturaImpartida` (Association Object) con PK compuesta + `responsable_id` | [src/backend/app/models/profesor_asignatura.py](/src/backend/app/models/profesor_asignatura.py) |
| `Usuario.asignaturas_impartidas` con `viewonly=True` + `primaryjoin/secondaryjoin` explícitos | [src/backend/app/models/usuario.py](/src/backend/app/models/usuario.py) |
| Schema `AsignaturaImpartidaOut` (POST devuelve la fila con `responsable_id`) | [src/backend/app/schemas/asignaturas.py](/src/backend/app/schemas/asignaturas.py) |
| Seed que escribe `AsignaturaImpartida` directamente (no por `relationship`, que es viewonly) atribuyendo a `secretaria1` | [src/backend/scripts/seed.py](/src/backend/scripts/seed.py) |

## divergencias respecto al diseño

| Diseño | Implementación | Motivo |
|---|---|---|
| `secondary=profesor_asignaturas` sin más en el `relationship` | Añadidos `primaryjoin="Usuario.id == profesor_asignaturas.c.profesor_id"` y `secondaryjoin="Asignatura.id == profesor_asignaturas.c.asignatura_id"` | Al añadir `responsable_id` como segunda FK a `usuarios`, SQLAlchemy detectaba dos caminos posibles entre la tabla secundaria y `Usuario` y abortaba con `AmbiguousForeignKeysError`. Los joins explícitos eliminan la ambigüedad sin tocar el resto del diseño. |
| `responsable_id` `NOT NULL` en la fila de la N:M | `Mapped[int \| None]` (nullable) | Mismo motivo que en [[gestionarCatalogoAsignaturas]]: backfill suave para asignaciones pre-existentes del seed. Los endpoints siempre escriben un `responsable_id` válido (la dependencia `require_rol` garantiza un `current_user`). |

El resto del diseño se conserva:
- **Endpoints anidados** `POST/DELETE /usuarios/{pid}/asignaturas-impartidas/{aid}` materializan la asimetría sujeto/objeto.
- **Router separado** `routers/asignaciones.py` porque el de usuarios tiene `Depends(require_rol(["administrador"]))` a nivel de router; los endpoints comparten el prefijo `/usuarios` y se merge-an al `include_router`.
- **POST idempotente con 201/200**: 201 al crear, 200 al ya existir. Implementado con `Response.status_code = …` controlado en el router según el flag `creada` del repo.
- **DELETE idempotente con 204** incluso si la fila no existía.
- **Validación de subtipo en service**: `isinstance(usuario, Profesor)` cubre Profesor y DirectorDeGrado (jerarquía). Alumno/Secretaria/Administrador → `NoEsProfesor` → 422.
- **`responsable_id` auto-poblado** desde `current_user.id`, nunca del cliente.
- **UI optimista** con revert al fallar: `setImpartidas` aplica el cambio antes del `await`; si la promesa rechaza, se revierte y se muestra el error inline.

## verificación end-to-end

Validado vía `curl` contra `localhost:8000` con `secretaria1` (`secre123`) y `admin` (`admin123`):

| Escenario | Resultado |
|---|---|
| `GET /usuarios/{profesor1}/asignaturas-impartidas` | 200 + `['IYA038','IYA040','IYA041']` (seed) |
| `POST /usuarios/{profesor1}/asignaturas-impartidas/{IYA020}` (nueva) | 201 + `{profesor_id, asignatura_id, responsable_id: 3}` |
| `POST /usuarios/{profesor1}/asignaturas-impartidas/{IYA020}` (ya existía) | 200 (idempotente) |
| `POST /usuarios/{alumno1}/asignaturas-impartidas/{IYA020}` | 422 `Ese usuario no es Profesor` |
| `POST /usuarios/{profesor1}/asignaturas-impartidas/99999` | 404 `Asignatura no encontrada` |
| `DELETE /usuarios/{profesor1}/asignaturas-impartidas/{IYA038}` | 204 |
| `DELETE /usuarios/{profesor1}/asignaturas-impartidas/{IYA038}` (repetido) | 204 (idempotente) |
| `GET /usuarios/{profesor1}/asignaturas-impartidas` (estado final) | `['IYA020','IYA040','IYA041']` |
| `POST /usuarios/{profesor1}/asignaturas-impartidas/{IYA020}` como `admin` | 403 `No autorizado para esta operación` |
| `tsc --noEmit` | sin errores |

Validación visual a nivel navegador pendiente de ejecución manual: `secretaria1` → `/asignaciones` → selector de profesor → checkboxes → toggle inmediato con UI optimista.

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/asignarAsignaturasAProfesor/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/asignarAsignaturasAProfesor/README.md)
- [Desarrollo `gestionarCatalogoAsignaturas()`](/RUP/03-desarrollo/casos-uso/gestionarCatalogoAsignaturas/README.md) — CU complementario
- [Desarrollo `crearUsuario()`](/RUP/03-desarrollo/casos-uso/crearUsuario/README.md) — patrón router/service/repository
- [conversation-log.md](/conversation-log.md)
