from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, model_validator

from app.schemas.grados import GradoOut

TipoUsuario = Literal["alumno", "profesor", "director", "secretaria", "administrador"]

# Solo el Director es individual y se scopea por grado. La Secretaría es un
# departamento colectivo — cualquier cuenta de tipo secretaria opera todos los
# grados. Coherente con la lectura del SDR: `Grado → SecretariaAcademica`
# significa "gestionado por (el departamento de) Secretaría", no por una
# secretaria nombrada.
_ROLES_CON_GRADO = {"director"}


class CrearUsuarioRequest(BaseModel):
    tipo: TipoUsuario
    username: str
    password: str
    nombre: str
    apellidos: str
    email: EmailStr
    grado_id: int | None = None

    @model_validator(mode="after")
    def _grado_id_obligatorio_para_director(self):
        if self.tipo in _ROLES_CON_GRADO and self.grado_id is None:
            raise ValueError(f"`grado_id` es obligatorio cuando tipo='{self.tipo}'")
        if self.tipo not in _ROLES_CON_GRADO and self.grado_id is not None:
            raise ValueError(f"`grado_id` no aplica cuando tipo='{self.tipo}'")
        return self


class EditarUsuarioRequest(BaseModel):
    """Body parcial — todos los campos opcionales.

    `None` significa "no tocar". `tipo` no aparece deliberadamente:
    el subtipo del usuario es invariante post-alta (decisión del análisis).
    `grado_id` solo se considera si el usuario es director o secretaria
    (validación en el service).
    """

    model_config = ConfigDict(extra="ignore")

    username: str | None = None
    password: str | None = None
    nombre: str | None = None
    apellidos: str | None = None
    email: EmailStr | None = None
    activo: bool | None = None
    grado_id: int | None = None


class UsuarioDetalleOut(BaseModel):
    """Ficha completa del usuario (consulta + edición)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    tipo: str
    username: str
    nombre: str
    apellidos: str
    email: EmailStr
    activo: bool
    grado: GradoOut | None = None
