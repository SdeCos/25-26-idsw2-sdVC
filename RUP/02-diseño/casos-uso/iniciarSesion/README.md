# CGU > iniciarSesion > Diseño

> | [🏠️](/README.md) | [Diseño](/RUP/02-diseño/README.md) | [Detalle](/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Usuario/) | [Análisis](/RUP/01-analisis/casos-uso/iniciarSesion/README.md) | **Diseño** | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Caso de uso**: `iniciarSesion()`
- **Actor**: Usuario (cualquier subtipo)
- **Versión**: 1.0
- **Fecha**: 2026-05-29

## diagrama de secuencia

<div align=center>

|![Secuencia iniciarSesion()](/images/RUP/02-diseño/casos-uso/iniciarSesion/secuencia.svg)|
|-|
|**Disciplina**: Diseño RUP<br>**Enfoque**: Diagrama de secuencia con tecnología concreta|

</div>

[Código PlantUML](/modelosUML/RUP/02-diseño/casos-uso/iniciarSesion/secuencia.puml)

## participantes

| Participante | Rol |
|---|---|
| **LoginPage** (React) | Captura `username` / `password` |
| **authService** (axios) | Cliente HTTP para `/auth/login` |
| **AuthContext** (React Context) | Persiste el token y expone `useAuth()` |
| **AuthRouter** (FastAPI) | Endpoint `POST /auth/login` |
| **AuthService** | Verifica contraseña y firma JWT |
| **UsuarioRepository** (SQLAlchemy) | `obtener_por_username` con resolución polimórfica del subtipo |
| **SQLite** | Tabla `usuarios` (single-table inheritance) |

## materialización del análisis

| Mensaje del análisis | Materialización en diseño |
|---|---|
| `LoginView → IniciarSesionController : autenticar(...)` | `authService.login()` → `POST /auth/login` |
| `IniciarSesionController → UsuarioRepository : validarCredenciales(...)` | Partido en dos pasos: `UsuarioRepository.obtener_por_username()` + `verify_password()` dentro del servicio |
| `IniciarSesionController → Sesion : crearSesion(usuario)` | `AuthService.create_access_token(usuario)` → JWT firmado (sin persistencia) |
| `LoginView → :Sistema Disponible` | `navigate("/dashboard")` + rutas protegidas por rol |
| Choice point | Excepción `CredencialesInvalidas` → 401 → mensaje en `LoginPage` |

## decisiones de diseño

- **JWT stateless**: la `Sesion` del análisis no se persiste; vive como token firmado en `localStorage`. Cierra la pregunta abierta del análisis ("¿promover `Sesion` al dominio?") con un no.
- **`validarCredenciales` partido por SRP**: el repositorio solo hace I/O; la verificación bcrypt vive en `AuthService`. El nombre del mensaje desaparece, la semántica se preserva en `autenticar()`.
- **Polimorfismo de Usuario** materializado como single-table inheritance en SQLAlchemy con discriminator `tipo`. El JWT lleva `tipo` en el payload → el frontend renderiza la vista por rol sin un `/auth/me` extra al cargar.
- **bcrypt** para hashes (resistente a fuerza bruta y rainbow tables); el `password_hash` nunca sale por la API.

## referencias

- [Análisis `iniciarSesion()`](/RUP/01-analisis/casos-uso/iniciarSesion/README.md)
- [Detallado `iniciarSesion()`](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Usuario/iniciarSesion.puml)
- [conversation-log.md](/conversation-log.md)
