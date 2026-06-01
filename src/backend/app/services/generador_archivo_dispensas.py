"""Servicio de aplicación: serializa una lista de SolicitudDispensa a CSV.

Tercer servicio del proyecto tras los dos validadores de importación. Pareja
conceptual de los ValidadoresArchivo* (lectura ↔ escritura).
"""

from __future__ import annotations

import csv
import io
from collections.abc import Iterable

from app.models.solicitud_dispensa import SolicitudDispensa


class GeneradorArchivoDispensas:
    CABECERAS = [
        "id",
        "alumno",
        "alumno_username",
        "asignatura_codigo",
        "asignatura",
        "ects",
        "curso_academico",
        "motivo",
        "estado",
        "observaciones",
        "fecha_solicitud",
        "fecha_resolucion",
        "responsable",
    ]

    def generar_csv(self, lista: Iterable[SolicitudDispensa]) -> bytes:
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(self.CABECERAS)
        for s in lista:
            am = s.asignatura_matriculada
            asignatura = am.asignatura
            matricula = am.matricula
            alumno_nombre = f"{s.alumno.nombre} {s.alumno.apellidos}".strip()
            responsable = ""
            if s.responsable is not None:
                responsable = (
                    f"{s.responsable.nombre} {s.responsable.apellidos}".strip()
                )
            writer.writerow(
                [
                    s.id,
                    alumno_nombre,
                    s.alumno.username,
                    asignatura.codigo,
                    asignatura.nombre,
                    asignatura.ects,
                    matricula.curso_academico,
                    s.motivo or "",
                    s.estado,
                    s.observaciones or "",
                    s.fecha_solicitud.isoformat() if s.fecha_solicitud else "",
                    (
                        s.fecha_resolucion.isoformat()
                        if s.fecha_resolucion
                        else ""
                    ),
                    responsable,
                ]
            )
        return buffer.getvalue().encode("utf-8-sig")
