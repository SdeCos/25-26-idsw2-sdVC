"""Servicio de aplicación: parsea CSV(s) de matrículas y resuelve FKs.

Cabecera obligatoria: `alumno_username,curso_academico,asignatura_codigo,n_matricula`.

Cada fila válida produce un `RegistroMatriculaCrudo` con `alumno_id` y
`asignatura_id` ya resueltos contra los repositorios.
"""

from __future__ import annotations

import csv
import io
from collections.abc import Iterable
from dataclasses import dataclass, field

from app.repositories.asignatura_repository import AsignaturaRepository
from app.repositories.usuario_repository import UsuarioRepository

CABECERA_REQUERIDA = [
    "alumno_username",
    "curso_academico",
    "asignatura_codigo",
    "n_matricula",
]


@dataclass
class RegistroMatriculaCrudo:
    alumno_id: int
    asignatura_id: int
    curso_academico: str
    n_matricula: int


@dataclass
class ErrorImportacion:
    archivo: str
    fila: int
    mensaje: str


@dataclass
class ResultadoValidacionMatriculas:
    validos: list[RegistroMatriculaCrudo] = field(default_factory=list)
    errores: list[ErrorImportacion] = field(default_factory=list)


class CabeceraInvalida(Exception):
    def __init__(self, archivo: str, mensaje: str) -> None:
        super().__init__(f"{archivo}: {mensaje}")
        self.archivo = archivo
        self.mensaje = mensaje


class ValidadorArchivoMatriculas:
    def __init__(
        self,
        usuario_repo: UsuarioRepository,
        asignatura_repo: AsignaturaRepository,
    ) -> None:
        self.usuario_repo = usuario_repo
        self.asignatura_repo = asignatura_repo

    async def validar(
        self, archivos: Iterable[tuple[str, bytes]]
    ) -> ResultadoValidacionMatriculas:
        # Primera pasada: parsing + chequeos sintácticos + agregar usernames y
        # códigos para batch lookup.
        archivos_parseados: list[tuple[str, list[tuple[int, dict]]]] = []
        usernames: set[str] = set()
        codigos: set[str] = set()
        errores: list[ErrorImportacion] = []

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
            filas: list[tuple[int, dict]] = []
            for n, fila in enumerate(reader, start=2):
                error = self._validar_sintactico(fila)
                if error:
                    errores.append(ErrorImportacion(filename, n, error))
                    continue
                filas.append((n, fila))
                usernames.add(fila["alumno_username"].strip())
                codigos.add(fila["asignatura_codigo"].strip())
            archivos_parseados.append((filename, filas))

        # Segunda pasada: batch lookup contra repositorios.
        alumnos_map = await self.usuario_repo.obtener_alumnos_por_usernames(
            list(usernames)
        )
        asignaturas_map = await self.asignatura_repo.obtener_por_codigos(
            list(codigos)
        )

        # Tercera pasada: resolución de FKs + construcción de registros válidos.
        validos: list[RegistroMatriculaCrudo] = []
        for filename, filas in archivos_parseados:
            for n, fila in filas:
                username = fila["alumno_username"].strip()
                codigo = fila["asignatura_codigo"].strip()
                alumno = alumnos_map.get(username)
                asignatura = asignaturas_map.get(codigo)
                if alumno is None:
                    errores.append(
                        ErrorImportacion(
                            filename, n, f"alumno desconocido: {username!r}"
                        )
                    )
                    continue
                if asignatura is None:
                    errores.append(
                        ErrorImportacion(
                            filename, n, f"asignatura desconocida: {codigo!r}"
                        )
                    )
                    continue
                try:
                    n_matricula = int(fila["n_matricula"].strip())
                except ValueError:
                    errores.append(
                        ErrorImportacion(
                            filename, n, "n_matricula debe ser entero"
                        )
                    )
                    continue
                if n_matricula < 1:
                    errores.append(
                        ErrorImportacion(filename, n, "n_matricula >= 1")
                    )
                    continue
                validos.append(
                    RegistroMatriculaCrudo(
                        alumno_id=alumno.id,
                        asignatura_id=asignatura.id,
                        curso_academico=fila["curso_academico"].strip(),
                        n_matricula=n_matricula,
                    )
                )

        return ResultadoValidacionMatriculas(validos=validos, errores=errores)

    def _validar_sintactico(self, fila: dict) -> str | None:
        for campo in CABECERA_REQUERIDA:
            valor = (fila.get(campo) or "").strip()
            if not valor:
                return f"campo '{campo}' obligatorio"
        return None
