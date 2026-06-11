from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.database import Base, engine
from app.routers import alumnos as alumnos_router
from app.routers import asignaciones as asignaciones_router
from app.routers import asignaturas as asignaturas_router
from app.routers import asistencias as asistencias_router
from app.routers import auth as auth_router
from app.routers import dispensas as dispensas_router
from app.routers import grados as grados_router
from app.routers import matriculas as matriculas_router
from app.routers import profesores as profesores_router
from app.routers import sesiones_clase as sesiones_clase_router
from app.routers import usuarios as usuarios_router

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # Importar modelos para que Base.metadata los registre antes de create_all.
    import app.models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(usuarios_router.router)
app.include_router(asignaciones_router.router)
app.include_router(alumnos_router.router)
app.include_router(asignaturas_router.router)
app.include_router(matriculas_router.router)
app.include_router(grados_router.router)
app.include_router(profesores_router.router)
app.include_router(dispensas_router.router)
app.include_router(sesiones_clase_router.router)
app.include_router(asistencias_router.router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"name": settings.APP_NAME, "docs": "/docs"}
