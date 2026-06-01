"""Servicio de aplicación: parsea CSV(s) de listas de alumnos.

Cabecera obligatoria: `username,password,nombre,apellidos,email,telefono?`.
"""

from __future__ import annotations

import csv
import io
from collections.abc import Iterable
from dataclasses import dataclass, field

CABECERA_REQUERIDA = ["username", "password", "nombre", "apellidos", "email"]


@dataclass
class RegistroAlumnoCrudo:
    username: str
    password: str
    nombre: str
    apellidos: str
    email: str
    telefono: str | None = None


@dataclass
class ErrorImportacion:
    archivo: str
    fila: int
    mensaje: str


@dataclass
class ResultadoValidacionAlumnos:
    validos: list[RegistroAlumnoCrudo] = field(default_factory=list)
    errores: list[ErrorImportacion] = field(default_factory=list)


class CabeceraInvalida(Exception):
    """Header malformado — el archivo completo es inutilizable."""

    def __init__(self, archivo: str, mensaje: str) -> None:
        super().__init__(f"{archivo}: {mensaje}")
        self.archivo = archivo
        self.mensaje = mensaje


class ValidadorArchivoListasAlumnos:
    def validar(
        self, archivos: Iterable[tuple[str, bytes]]
    ) -> ResultadoValidacionAlumnos:
        """Cada elemento de `archivos` es `(filename, contenido_bytes)`."""
        resultado = ResultadoValidacionAlumnos()
        for filename, contenido in archivos:
            try:
                texto = contenido.decode("utf-8-sig")
            except UnicodeDecodeError as e:
                raise CabeceraInvalida(
                    filename, f"codificación no UTF-8: {e}"
                ) from e
            reader = csv.DictReader(io.StringIO(texto))
            if reader.fieldnames is None:
                raise CabeceraInvalida(filename, "archivo vacío")
            faltantes = [
                c for c in CABECERA_REQUERIDA if c not in reader.fieldnames
            ]
            if faltantes:
                raise CabeceraInvalida(
                    filename,
                    f"columnas requeridas faltan: {', '.join(faltantes)}",
                )
            for n, fila in enumerate(reader, start=2):  # 1 = header
                error = self._validar_fila(fila)
                if error:
                    resultado.errores.append(
                        ErrorImportacion(filename, n, error)
                    )
                    continue
                resultado.validos.append(
                    RegistroAlumnoCrudo(
                        username=fila["username"].strip(),
                        password=fila["password"],
                        nombre=fila["nombre"].strip(),
                        apellidos=fila["apellidos"].strip(),
                        email=fila["email"].strip(),
                        telefono=(fila.get("telefono") or "").strip() or None,
                    )
                )
        return resultado

    def _validar_fila(self, fila: dict) -> str | None:
        for campo in CABECERA_REQUERIDA:
            valor = (fila.get(campo) or "").strip()
            if not valor:
                return f"campo '{campo}' obligatorio"
        if "@" not in fila["email"]:
            return f"email inválido: {fila['email']!r}"
        return None
