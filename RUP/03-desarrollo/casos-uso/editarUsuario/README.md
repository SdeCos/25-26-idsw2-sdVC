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

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/editarUsuario/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/editarUsuario/README.md)
- [conversation-log.md](/conversation-log.md)
