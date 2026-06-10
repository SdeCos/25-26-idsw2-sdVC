"""Servicio de aplicación: serializa una lista de Asistencia a CSV.

Paralelo a `GeneradorArchivoDispensas`. Misma forma (`generar_csv`) pero
contratos no intercambiables (lista de entidades distintas) — por eso no se
introduce ABC `Generador<T>`: agruparía sintácticamente sin polimorfismo real.
"""

from __future__ import annotations

import csv
import io
from collections.abc import Iterable

from app.models.asistencia import Asistencia


class GeneradorArchivoAsistencias:
    CABECERAS = [
        "fecha",
        "asignatura_codigo",
        "grupos",
        "aula",
        "alumno_username",
        "alumno_nombre",
        "alumno_apellidos",
        "estado",
        "justificacion",
        "fecha_registro",
    ]

    def generar_csv(self, lista: Iterable[Asistencia]) -> bytes:
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(self.CABECERAS)
        for a in lista:
            s = a.sesion_clase
            asignatura_codigo = s.asignatura.codigo if s.asignatura else ""
            writer.writerow(
                [
                    s.fecha.isoformat() if s.fecha else "",
                    asignatura_codigo,
                    ", ".join(s.grupos or []),
                    s.aula,
                    a.alumno.username,
                    a.alumno.nombre,
                    a.alumno.apellidos,
                    a.estado,
                    a.justificacion or "",
                    a.fecha_registro.isoformat() if a.fecha_registro else "",
                ]
            )
        return buffer.getvalue().encode("utf-8-sig")
