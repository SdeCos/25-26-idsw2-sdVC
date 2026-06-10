import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { isAxiosError } from 'axios';
import { matriculasService } from '../services/matriculasService';
import type { MatriculaDetalle } from '../types/matriculas';

const fmtFecha = (iso: string) => new Date(iso).toLocaleDateString();

export const ConsultarDetalleMatriculaPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [matricula, setMatricula] = useState<MatriculaDetalle | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    matriculasService
      .obtener(Number(id))
      .then(setMatricula)
      .catch((err) => {
        if (isAxiosError(err) && err.response?.status === 404)
          setError('Matrícula no encontrada');
        else setError('No se pudo cargar la matrícula');
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="page"><p>Cargando…</p></div>;
  if (error)
    return (
      <div className="page">
        <div className="error">{error}</div>
        <Link to="/matriculas">← Volver al listado</Link>
      </div>
    );
  if (!matricula) return null;

  return (
    <div className="page">
      <header className="page-header">
        <h1>Ficha Matrícula #{matricula.id}</h1>
        <Link to="/matriculas">← Listado</Link>
      </header>

      <dl className="ficha">
        <dt>Alumno</dt>
        <dd>
          {matricula.alumno.nombre} {matricula.alumno.apellidos} ({matricula.alumno.username})
        </dd>
        <dt>Curso académico</dt>
        <dd>{matricula.curso_academico}</dd>
        <dt>Grado</dt>
        <dd>{matricula.grado.codigo} · {matricula.grado.nombre}</dd>
        <dt>Facultad</dt>
        <dd>{matricula.grado.facultad}</dd>
        <dt>Fecha de importación</dt>
        <dd>{fmtFecha(matricula.fecha_importacion)}</dd>
        <dt>Responsable</dt>
        <dd>
          {matricula.responsable.nombre} {matricula.responsable.apellidos}
        </dd>
      </dl>

      <h2 style={{ marginTop: '2rem' }}>
        Asignaturas matriculadas ({matricula.asignaturas_matriculadas.length})
      </h2>
      <table className="data-table">
        <thead>
          <tr>
            <th>Código</th>
            <th>Asignatura</th>
            <th>ECTS</th>
            <th>Curso</th>
            <th>Carácter</th>
            <th>Nº matrícula</th>
          </tr>
        </thead>
        <tbody>
          {matricula.asignaturas_matriculadas.map((am) => (
            <tr key={am.id}>
              <td><strong>{am.asignatura.codigo}</strong></td>
              <td>{am.asignatura.nombre}</td>
              <td>{am.asignatura.ects}</td>
              <td>{am.asignatura.curso_plan}</td>
              <td>{am.asignatura.caracter}</td>
              <td>{am.n_matricula}ª</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
