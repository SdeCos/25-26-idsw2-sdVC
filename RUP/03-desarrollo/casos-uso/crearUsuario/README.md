# CGU > crearUsuario > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/crearUsuario/README.md) | [Diseño](/RUP/02-diseño/casos-uso/crearUsuario/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `crearUsuario()`
- **Actor**: Administrador
- **Versión**: 1.0
- **Fecha**: 2026-05-30

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| CrearUsuarioPage (`/usuarios/nuevo`) | [src/frontend/src/pages/CrearUsuarioPage.tsx](/src/frontend/src/pages/CrearUsuarioPage.tsx) |
| usuariosService.crear | [src/frontend/src/services/usuariosService.ts](/src/frontend/src/services/usuariosService.ts) |
| Tipos DTO (`CrearUsuarioRequest`) | [src/frontend/src/types/usuarios.ts](/src/frontend/src/types/usuarios.ts) |
| Gate `RequireAuth roles={['administrador']}` | [src/frontend/src/components/RequireAuth.tsx](/src/frontend/src/components/RequireAuth.tsx) |
| UsuariosRouter (`POST /usuarios`) | [src/backend/app/routers/usuarios.py](/src/backend/app/routers/usuarios.py) |
| require_rol (dependency) | [src/backend/app/dependencies.py](/src/backend/app/dependencies.py) |
| UsuarioService.crear (hash + delega) | [src/backend/app/services/usuario_service.py](/src/backend/app/services/usuario_service.py) |
| UsuarioRepository.crear + TIPO_A_CLASE | [src/backend/app/repositories/usuario_repository.py](/src/backend/app/repositories/usuario_repository.py) |
| Schemas `CrearUsuarioRequest`, `UsuarioDetalleOut` | [src/backend/app/schemas/usuarios.py](/src/backend/app/schemas/usuarios.py) |
| hash_password (bcrypt) | [src/backend/app/core/security.py](/src/backend/app/core/security.py) (ya existía) |

## divergencias respecto al diseño

| Diseño | Implementación | Motivo |
|---|---|---|
| Form mínimo: tipo + username + password | Form con tipo + username + password + nombre + apellidos + email | Las columnas `nombre/apellidos/email` son `NOT NULL` en el modelo; pedirlas en el alta evita un estado "usuario creado pero incompleto". El `<<include>> editarUsuario` del análisis sigue activo (redirige a `/usuarios/{id}/editar` tras crear) pero ahora ya hay datos válidos desde el alta. |

Todas las decisiones de fondo del diseño se conservan (mapa polimórfico explícito, `require_rol` paramétrico, 409 por `UNIQUE` con captura de `IntegrityError`).

## verificación end-to-end

Validado vía `curl` contra `localhost:8000`:

| Escenario | Resultado |
|---|---|
| `POST /usuarios` sin token | 401 `Token ausente` |
| `POST /usuarios` con token de `alumno1` | 403 `No autorizado para esta operación` |
| `POST /usuarios` con token de `admin` + datos válidos | 201 + `UsuarioDetalleOut` con `id`, `tipo`, etc. |
| `POST /usuarios` con `username` duplicado | 409 `El username ya está en uso` |

Validación a nivel navegador (form → submit → redirect a `/usuarios/{id}/editar`) pendiente de ejecución manual.

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/crearUsuario/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/crearUsuario/README.md)
- [conversation-log.md](/conversation-log.md)
