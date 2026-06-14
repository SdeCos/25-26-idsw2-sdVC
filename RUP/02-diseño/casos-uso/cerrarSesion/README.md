# CGU > cerrarSesion > Diseño

> | [🏠️](/README.md) | [Diseño](/RUP/02-diseño/README.md) | [Detalle](/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Usuario/) | [Análisis](/RUP/01-analisis/casos-uso/cerrarSesion/README.md) | **Diseño** | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Caso de uso**: `cerrarSesion()`
- **Actor**: Usuario (cualquier subtipo autenticado)
- **Versión**: 1.0
- **Fecha**: 2026-05-29

## diagrama de secuencia

<div align=center>

|![Secuencia cerrarSesion()](/images/RUP/02-diseño/casos-uso/cerrarSesion/secuencia.svg)|
|-|
|**Disciplina**: Diseño RUP<br>**Enfoque**: Diagrama de secuencia con tecnología concreta|

</div>

[Código PlantUML](/modelosUML/RUP/02-diseño/casos-uso/cerrarSesion/secuencia.puml)

## participantes

| Participante | Rol |
|---|---|
| **Layout** (React) | Componente envoltorio del área autenticada; expone el botón "Cerrar sesión" |
| **AuthContext** (React Context) | Borra el token de `localStorage` y desautentica |
| **authService** (axios) | Llama a `POST /auth/logout` |
| **AuthRouter** (FastAPI) | Endpoint expuesto, no-op en esta iteración |

No participan `AuthService` ni `UsuarioRepository`: el cierre es estrictamente de sesión, no toca `Usuario`.

## materialización del análisis

| Mensaje del análisis | Materialización en diseño |
|---|---|
| `:Sistema Disponible → CerrarSesionView : cerrarSesion()` | Click del botón del `Layout` |
| `CerrarSesionView → CerrarSesionController : cerrarSesion(sesion)` | `AuthContext.logout()` orquesta el cierre |
| `CerrarSesionController → Sesion : cerrar()` | `localStorage.removeItem("access_token")` en cliente + `POST /auth/logout` en servidor (no-op futuro-proof) |
| `CerrarSesionView → :Sesión Cerrada` | `navigate("/login")` |

## decisiones de diseño

- **Cerrar sesión = borrar el token del cliente**, derivado del JWT stateless decidido en [iniciarSesion](../iniciarSesion/README.md). Consecuencia honesta: un token ya copiado sigue vivo hasta expirar; se mitiga con expiración corta.
- **Endpoint `POST /auth/logout` aunque sea no-op**: punto de extensión para blacklist o auditoría sin romper el contrato cliente-servidor.
- **Sin modal de confirmación**, consistente con la decisión explícita del análisis (divergencia consciente con pySigHor).
- **Orden de llamada**: primero `POST /auth/logout` (cliente aún tiene el `Bearer`), después borrar el token. Si la red falla, se borra igualmente — el logout nunca debe quedar a medias.

## referencias

- [Análisis `cerrarSesion()`](/RUP/01-analisis/casos-uso/cerrarSesion/README.md)
- [Diseño `iniciarSesion()`](../iniciarSesion/README.md) — donde se decide JWT stateless
- [Detallado `cerrarSesion()`](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Usuario/cerrarSesion.puml)
- [conversation-log.md](/conversation-log.md)
