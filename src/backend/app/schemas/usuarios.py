from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr

TipoUsuario = Literal["alumno", "profesor", "director", "secretaria", "administrador"]


class CrearUsuarioRequest(BaseModel):
    tipo: TipoUsuario
    username: str
    password: str
    nombre: str
    apellidos: str
    email: EmailStr


class EditarUsuarioRequest(BaseModel):
    """Body parcial — todos los campos opcionales.

    `None` significa "no tocar". `tipo` no aparece deliberadamente:
    el subtipo del usuario es invariante post-alta (decisión del análisis).
    """

    model_config = ConfigDict(extra="ignore")

    username: str | None = None
    password: str | None = None
    nombre: str | None = None
    apellidos: str | None = None
    email: EmailStr | None = None
    activo: bool | None = None


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
