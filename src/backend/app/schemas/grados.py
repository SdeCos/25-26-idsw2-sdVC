from pydantic import BaseModel, ConfigDict


class GradoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    nombre: str
    facultad: str


class CrearGradoRequest(BaseModel):
    codigo: str
    nombre: str
    facultad: str


class EditarGradoRequest(BaseModel):
    """`codigo` no editable post-creación; si llega se descarta."""

    model_config = ConfigDict(extra="ignore")

    nombre: str | None = None
    facultad: str | None = None
