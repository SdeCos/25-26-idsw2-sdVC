# CGU > cerrarSesion > Desarrollo

> | [🏠️](/README.md) | [Desarrollo](/RUP/03-desarrollo/README.md) | [Análisis](/RUP/01-analisis/casos-uso/cerrarSesion/README.md) | [Diseño](/RUP/02-diseño/casos-uso/cerrarSesion/README.md) | **Desarrollo** |
> |-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Construcción
- **Disciplina**: Desarrollo
- **Caso de uso**: `cerrarSesion()`
- **Actor**: Usuario (cualquier subtipo autenticado)
- **Versión**: 1.0
- **Fecha**: 2026-05-29

## trazabilidad código ↔ diseño

| Participante del diseño | Implementación |
|---|---|
| Layout (botón "Cerrar sesión") | [src/frontend/src/components/Layout.tsx](/src/frontend/src/components/Layout.tsx) |
| AuthContext (`logout()` + limpieza de `localStorage`) | [src/frontend/src/context/AuthContext.tsx](/src/frontend/src/context/AuthContext.tsx) |
| authService (`logout()`) | [src/frontend/src/services/authService.ts](/src/frontend/src/services/authService.ts) |
| AuthRouter (`POST /auth/logout`) | [src/backend/app/routers/auth.py](/src/backend/app/routers/auth.py) |
| `get_current_user` (valida el `Bearer` recibido) | [src/backend/app/dependencies.py](/src/backend/app/dependencies.py) |

El endpoint en backend es deliberadamente un no-op (`return None` con `204`) — punto de extensión futuro-proof para blacklist o auditoría sin romper el contrato.

## degradación elegante en cliente

`AuthContext.logout()` envuelve la llamada al backend en `try/except`: si la red falla o el token está expirado, **igualmente** se limpia `localStorage` y se desautentica al usuario en cliente. El logout nunca queda a medias.

## verificación end-to-end

Validado vía `curl`:

| Escenario | Resultado |
|---|---|
| `POST /auth/logout` con token válido | 204 No Content |
| `POST /auth/logout` sin token | 401 `Token ausente` |
| `POST /auth/logout` con token falseado | 401 `Token inválido` |

En ningún caso la UI debe quedarse colgada — el `try/except` del `AuthContext` garantiza el cierre en cliente aunque el backend rechace.

Validación a nivel navegador (click → redirect a `/login` → no se puede volver a `/dashboard` sin reauth) pendiente de ejecución manual.

## referencias

- [Análisis](/RUP/01-analisis/casos-uso/cerrarSesion/README.md)
- [Diseño](/RUP/02-diseño/casos-uso/cerrarSesion/README.md)
- [Desarrollo `iniciarSesion`](../iniciarSesion/README.md)
- [conversation-log.md](/conversation-log.md)
