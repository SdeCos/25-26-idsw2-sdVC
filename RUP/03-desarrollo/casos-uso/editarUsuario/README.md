# CGU > editarUsuario > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/editarUsuario/README.md) | [Diseño](/RUP/02-diseño/casos-uso/editarUsuario/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `editarUsuario()`
- **Actor**: Administrador
- **Versión**: 1.0
- **Fecha**: 2026-05-30

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| EditarUsuarioPage (`/usuarios/{id}/editar`) | [src/frontend/src/pages/EditarUsuarioPage.tsx](/src/frontend/src/pages/EditarUsuarioPage.tsx) |
| usuariosService.obtener (carga) + actualizar (guardado) | [src/frontend/src/services/usuariosService.ts](/src/frontend/src/services/usuariosService.ts) |
| UsuariosRouter (`PATCH /usuarios/{id}`) | [src/backend/app/routers/usuarios.py](/src/backend/app/routers/usuarios.py) |
| UsuarioService.actualizar (hash opcional + cambios) | [src/backend/app/services/usuario_service.py](/src/backend/app/services/usuario_service.py) |
| UsuarioRepository.actualizar | [src/backend/app/repositories/usuario_repository.py](/src/backend/app/repositories/usuario_repository.py) |
| Schema `EditarUsuarioRequest` (sin `tipo`) | [src/backend/app/schemas/usuarios.py](/src/backend/app/schemas/usuarios.py) |

## materialización de las decisiones de diseño

| Decisión del diseño | Cómo se materializa |
|---|---|
| `PATCH` con body parcial; `None` = no tocar | `model_dump(exclude_unset=True)` en `UsuarioService.actualizar` |
| Password opcional en el mismo body | Si `password` viene, se hace pop + `hash_password` → renombrado a `password_hash` antes del UPDATE |
| `tipo` no editable por contrato | `EditarUsuarioRequest` no declara el campo + `extra="ignore"` → Pydantic descarta `"tipo"` si llega |
| EditarUsuarioPage siempre hace GET fresco | `useEffect` con `obtener(id)` al montar; el form se rellena del response |
| Detección de cambios cliente-side | Función `diff()` compara form vs original; si no hay cambios, navega sin PATCH |
| 409 por `UNIQUE(username)` | `IntegrityError` capturado en el service, traducido a `UsernameEnUso` → 409 en el router |

## verificación end-to-end

Validado vía `curl` contra `localhost:8000`:

| Escenario | Resultado |
|---|---|
| `PATCH /usuarios/6` cambiando `nombre` y `email` | 200 + payload actualizado |
| `PATCH` enviando `tipo: "administrador"` | 200 — el campo se descarta, `tipo` sigue siendo `"profesor"` ✅ |
| `PATCH` cambiando `password` | 200; login con la nueva → 200, login con la antigua → 401 (rehashea correcto) |
| `PATCH` cambiando `username` a uno existente | 409 |
| `PATCH /usuarios/9999` | 404 |

Validación a nivel navegador (carga → editar → guardar → consulta) pendiente de ejecución manual.

## evolución post-base — actor extendido (2026-06-14)

Detectado en pruebas manuales: tras M4, la Secretaría podía crear alumnos pero nadie podía editarlos (Admin perdió el acceso por M4; Secretaría nunca tuvo CU de edición). Resuelto extendiendo este CU en vez de añadir un `editarAlumno` espejo — `Alumno` es `Usuario` por STI, la operación de edición es idéntica.

**Backend:**
- `routers/usuarios.py`: `require_rol(["administrador"])` movido del router a los handlers que sí son admin-only (`GET /usuarios`, `POST /usuarios`). `GET /usuarios/{id}` y `PATCH /usuarios/{id}` usan ahora `_autorizar_acceso_a(target, actor)`: alumno → Secretaria, no-alumno → Administrador.
- `repositories/usuario_repository.py::obtener_todos()`: filtra `tipo != 'alumno'` para que el listado del Admin no incluya alumnos (coherencia con M4 — bug detectado el mismo día).

**Frontend:**
- `App.tsx`: ruta `/usuarios/:id/editar` accesible a `['administrador','secretaria']`. El check fino lo hace el backend per-target.
- `pages/EditarUsuarioPage.tsx`: `rutaFicha(u)` decide la URL de vuelta según `u.tipo` (`/alumnos/:id` para alumnos, `/usuarios/:id` para el resto). El form no requiere otros cambios — el `tipo` se pinta deshabilitado igual.
- `pages/DetalleAlumnoPage.tsx`: botón "Editar" en la cabecera, visible solo para Secretaria, enlaza a `/usuarios/:id/editar`.

**Verificación curl:**
- `GET /usuarios` como admin → 0 alumnos en respuesta ✓
- `GET /usuarios/{alumno_id}` como admin → 403 ✓
- `GET /usuarios/{alumno_id}` como secretaria → 200 ✓
- `GET /usuarios/{profesor_id}` como secretaria → 403 ✓
- `PATCH /usuarios/{alumno_id}` como secretaria → 200, cambio persistido ✓
- `PATCH /usuarios/{alumno_id}` como admin → 403 ✓

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/editarUsuario/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/editarUsuario/README.md)
- [conversation-log.md](/conversation-log.md)
