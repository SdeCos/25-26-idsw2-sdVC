# CGU > iniciarSesion > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/iniciarSesion/README.md) | [Diseño](/RUP/02-diseño/casos-uso/iniciarSesion/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `iniciarSesion()`
- **Actor**: Usuario (cualquier subtipo)
- **Versión**: 1.0
- **Fecha**: 2026-05-29

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| LoginPage | [src/frontend/src/pages/LoginPage.tsx](/src/frontend/src/pages/LoginPage.tsx) |
| authService | [src/frontend/src/services/authService.ts](/src/frontend/src/services/authService.ts) |
| AuthContext | [src/frontend/src/context/AuthContext.tsx](/src/frontend/src/context/AuthContext.tsx) |
| AuthRouter (`POST /auth/login`) | [src/backend/app/routers/auth.py](/src/backend/app/routers/auth.py) |
| AuthService (`autenticar`, `emitir_token`) | [src/backend/app/services/auth_service.py](/src/backend/app/services/auth_service.py) |
| UsuarioRepository (`obtener_por_username`) | [src/backend/app/repositories/usuario_repository.py](/src/backend/app/repositories/usuario_repository.py) |
| Modelo Usuario + subtipos (STI) | [src/backend/app/models/usuario.py](/src/backend/app/models/usuario.py) |
| Schemas `LoginRequest`, `TokenResponse`, `UsuarioOut` | [src/backend/app/schemas/auth.py](/src/backend/app/schemas/auth.py) |
| JWT + bcrypt | [src/backend/app/core/security.py](/src/backend/app/core/security.py) |
| SQLite | `cgu.db` (gitignored) — generado por `python -m scripts.seed` |

## sustituciones respecto al diseño

| Diseño | Implementación | Motivo |
|---|---|---|
| `python-jose` | `PyJWT` | `python-jose` sin releases activos; PyJWT mejor mantenida y API más simple |
| `passlib[bcrypt]` | `bcrypt` directo | Conflicto entre `passlib` y `bcrypt ≥ 4.x`; el wrapper aporta poco para hashear contraseñas |

Ambas sustituciones preservan la decisión de fondo (JWT firmado HS256 + bcrypt salt).

## verificación end-to-end

Validado vía `curl` contra `localhost:8000` y `localhost:5173`:

| Escenario | Resultado |
|---|---|
| Login `admin` / `admin123` | 200 con JWT + `usuario.tipo = "administrador"` |
| Login `alumno1` / `alumno123` | 200 con `usuario.tipo = "alumno"` — polimorfismo STI confirmado |
| Login con contraseña incorrecta | 401 `Credenciales no válidas` |
| Login con usuario inexistente | 401 `Credenciales no válidas` (mismo mensaje — no se filtra existencia) |
| Proxy de Vite `/api/auth/login` | 200 — frontend → backend OK |

Validación a nivel navegador (form submit → redirect a `/dashboard`) pendiente de ejecución manual.

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/iniciarSesion/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/iniciarSesion/README.md)
- [conversation-log.md](/conversation-log.md)
