"""Endpoints anidados bajo `/usuarios/{profesor_id}/asignaturas-impartidas/...`.

Viven en su propio router (no en `routers/usuarios.py`) porque el de usuarios
tiene `dependencies=[Depends(require_rol(["administrador"]))]` a nivel de router,
y estos endpoints los opera la Secretaría. Comparten prefijo y se merge-an al
incluir ambos en `main.py`.
"""

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies import require_rol
from app.models.usuario import Usuario
from app.repositories.asignatura_repository import AsignaturaRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.asignaturas import AsignaturaImpartidaOut, AsignaturaOut
from app.services.usuario_service import (
    AsignaturaNoEncontrada,
    NoEsProfesor,
    UsuarioNoEncontrado,
    UsuarioService,
)

router = APIRouter(prefix="/usuarios", tags=["asignaciones"])

_require_secretaria = require_rol(["secretaria"])


@router.get(
    "/{profesor_id}/asignaturas-impartidas",
    response_model=list[AsignaturaOut],
)
async def listar_impartidas(
    profesor_id: int,
    _: Usuario = Depends(_require_secretaria),
    db: AsyncSession = Depends(get_db),
) -> list[AsignaturaOut]:
    service = UsuarioService(UsuarioRepository(db))
    try:
        impartidas = await service.obtener_impartidas(profesor_id)
    except UsuarioNoEncontrado as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Profesor no encontrado") from exc
    except NoEsProfesor as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Ese usuario no es Profesor",
        ) from exc
    return [AsignaturaOut.model_validate(a) for a in impartidas]


@router.post(
    "/{profesor_id}/asignaturas-impartidas/{asignatura_id}",
    response_model=AsignaturaImpartidaOut,
)
async def asignar_impartida(
    profesor_id: int,
    asignatura_id: int,
    response: Response,
    usuario: Usuario = Depends(_require_secretaria),
    db: AsyncSession = Depends(get_db),
) -> AsignaturaImpartidaOut:
    """POST idempotente: 201 si la asignación es nueva, 200 si ya existía."""
    service = UsuarioService(UsuarioRepository(db))
    asignatura_repo = AsignaturaRepository(db)
    try:
        ai, creada = await service.asignar(
            profesor_id,
            asignatura_id,
            responsable_id=usuario.id,
            asignatura_repo=asignatura_repo,
        )
    except UsuarioNoEncontrado as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Profesor no encontrado") from exc
    except NoEsProfesor as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Ese usuario no es Profesor",
        ) from exc
    except AsignaturaNoEncontrada as exc:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "Asignatura no encontrada"
        ) from exc
    response.status_code = (
        status.HTTP_201_CREATED if creada else status.HTTP_200_OK
    )
    return AsignaturaImpartidaOut.model_validate(ai)


@router.delete(
    "/{profesor_id}/asignaturas-impartidas/{asignatura_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def desasignar_impartida(
    profesor_id: int,
    asignatura_id: int,
    _: Usuario = Depends(_require_secretaria),
    db: AsyncSession = Depends(get_db),
) -> None:
    """DELETE idempotente: 204 incluso si no existía."""
    service = UsuarioService(UsuarioRepository(db))
    try:
        await service.desasignar(profesor_id, asignatura_id)
    except UsuarioNoEncontrado as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Profesor no encontrado") from exc
    except NoEsProfesor as exc:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Ese usuario no es Profesor",
        ) from exc
