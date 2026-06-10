from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.models.asignatura import Asignatura
from app.models.matricula import AsignaturaMatriculada, Matricula
from app.models.usuario import Usuario


class MatriculaRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def obtener_por_id(self, id: int) -> Matricula | None:
        stmt = (
            select(Matricula)
            .where(Matricula.id == id)
            .options(
                joinedload(Matricula.alumno),
                joinedload(Matricula.responsable),
                selectinload(Matricula.asignaturas_matriculadas).joinedload(
                    AsignaturaMatriculada.asignatura
                ),
            )
        )
        result = await self.session.execute(stmt)
        return result.unique().scalars().first()

    async def listar(self, grado_id: int | None = None) -> list[Matricula]:
        """Lista matrículas. Si `grado_id` viene, restringe por grado de la matrícula
        (scoping de Secretaria por grado)."""
        stmt = (
            select(Matricula)
            .options(
                joinedload(Matricula.alumno),
                selectinload(Matricula.asignaturas_matriculadas).joinedload(
                    AsignaturaMatriculada.asignatura
                ),
            )
            .order_by(Matricula.fecha_importacion.desc())
        )
        if grado_id is not None:
            stmt = stmt.where(Matricula.grado_id == grado_id)
        result = await self.session.execute(stmt)
        return list(result.unique().scalars().all())

    async def get_or_create_header(
        self,
        *,
        alumno_id: int,
        curso_academico: str,
        responsable_id: int,
        grado_id: int,
    ) -> tuple[Matricula, bool]:
        """Devuelve el header (creándolo si no existe) y un flag `was_created`."""
        stmt = select(Matricula).where(
            Matricula.alumno_id == alumno_id,
            Matricula.curso_academico == curso_academico,
        )
        existente = (await self.session.execute(stmt)).scalar_one_or_none()
        if existente is not None:
            return existente, False
        nueva = Matricula(
            alumno_id=alumno_id,
            curso_academico=curso_academico,
            responsable_id=responsable_id,
            grado_id=grado_id,
        )
        self.session.add(nueva)
        await self.session.flush()  # asegura nueva.id sin commit
        return nueva, True

    async def crear_detalle(
        self, *, matricula_id: int, asignatura_id: int, n_matricula: int
    ) -> AsignaturaMatriculada | None:
        """Crea AsignaturaMatriculada. Si choca con UNIQUE, retorna None."""
        am = AsignaturaMatriculada(
            matricula_id=matricula_id,
            asignatura_id=asignatura_id,
            n_matricula=n_matricula,
        )
        self.session.add(am)
        try:
            await self.session.flush()
        except IntegrityError:
            await self.session.rollback()
            return None
        return am
