from pydantic import BaseModel, ConfigDict


class AlumnoListaItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    nombre: str
    apellidos: str
    email: str
    activo: bool


class AsignaturaMatriculadaDelAlumnoOut(BaseModel):
    """Vista plana de una AsignaturaMatriculada para el selector de dispensa.

    Permite que `CrearSolicitudDispensaSecretariaPage` y `CrearSolicitudPage`
    (Alumno) consuman el mismo endpoint para listar las asignaturas en las que
    el alumno está matriculado.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    nombre: str
    curso_academico: str
    n_matricula: int
