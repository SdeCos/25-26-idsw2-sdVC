# Backend — CGU

API REST del Centro de Gestión Universitaria. FastAPI + SQLAlchemy async + SQLite + JWT.

## Arranque

```bash
cd src/backend
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env

# Crear usuarios de prueba (idempotente):
python -m scripts.seed

# Levantar el servidor:
uvicorn app.main:app --reload --port 8000
```

Swagger UI: <http://localhost:8000/docs>

## Usuarios sembrados

| Username | Contraseña | Tipo |
|---|---|---|
| `admin` | `admin123` | administrador |
| `profesor1` | `profe123` | profesor |
| `alumno1` | `alumno123` | alumno |
| `director1` | `director123` | director |
| `secretaria1` | `secre123` | secretaria |

Emails de los seeds: `<username>@cgu.es`.

## Estructura

```
app/
├── core/           # config, database, security (bcrypt + JWT)
├── models/         # SQLAlchemy: Usuario + subtipos (STI)
├── schemas/        # Pydantic: LoginRequest, TokenResponse, UsuarioOut
├── repositories/   # UsuarioRepository
├── services/       # AuthService
├── routers/        # /auth/{login,logout,me}
├── dependencies.py # get_current_user
└── main.py         # FastAPI app + CORS + create_all en lifespan
```

Flujo de petición: `Router → Service → Repository → Model → SQLite`.

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/auth/login` | Devuelve JWT + UsuarioOut |
| POST | `/auth/logout` | No-op (futuro-proof) |
| GET | `/auth/me` | Usuario autenticado |
