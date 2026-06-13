import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { isAxiosError } from 'axios';
import { alumnosService } from '../services/alumnosService';
import type { AlumnoDetalle } from '../types/alumnos';

export const DetalleAlumnoPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [alumno, setAlumno] = useState<AlumnoDetalle | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState({ adicional: false, asistencias: false });

  useEffect(() => {
    if (!id) return;
    alumnosService
      .obtener(Number(id))
      .then(setAlumno)
      .catch((err) => {
        if (isAxiosError(err) && err.response?.status === 404)
          setError('Alumno no encontrado');
        else if (isAxiosError(err) && err.response?.status === 403)
          setError('No impartes ninguna asignatura de este alumno');
        else setError('No se pudo cargar la ficha');
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="page"><p>Cargando…</p></div>;
  if (error)
    return (
      <div className="page">
        <div className="error">{error}</div>
        <Link to="/alumnos">← Volver</Link>
      </div>
    );
  if (!alumno) return null;

  return (
    <div className="page">
      <header className="page-header">
        <h1>
          {alumno.nombre} {alumno.apellidos}
        </h1>
        <Link to="/alumnos">← Volver al listado</Link>
      </header>

      <dl className="ficha">
        <dt>Carnet</dt>
        <dd>{alumno.username}</dd>
        <dt>Email</dt>
        <dd>{alumno.email}</dd>
        <dt>Activo</dt>
        <dd>{alumno.activo ? 'Sí' : 'No'}</dd>
      </dl>

      <section style={{ marginTop: '1.5rem' }}>
        <h2 style={{ cursor: 'pointer' }} onClick={() =>
          setExpanded((e) => ({ ...e, adicional: !e.adicional }))
        }>
          {expanded.adicional ? '▾' : '▸'} Asignaturas matriculadas ({alumno.asignaturas_matriculadas.length})
        </h2>
        {expanded.adicional && alumno.asignaturas_matriculadas.length > 0 && (
          <table className="data-table">
            <thead>
              <tr>
                <th>Código</th>
                <th>Asignatura</th>
                <th>Curso</th>
                <th>Convocatoria</th>
                <th>Asistencia</th>
              </tr>
            </thead>
            <tbody>
              {alumno.asignaturas_matriculadas.map((am) => {
                const pct = am.porcentaje_asistencia;
                const cumple = pct !== null && pct >= 70;
                return (
                  <tr key={am.id}>
                    <td>{am.codigo}</td>
                    <td>{am.nombre}</td>
                    <td>{am.curso_academico}</td>
                    <td>{am.n_matricula}ª</td>
                    <td>
                      {pct === null ? (
                        <span style={{ color: '#6e6e73' }}>—</span>
                      ) : (
                        <span
                          title={`${am.presentes} de ${am.total_sesiones} sesiones cerradas`}
                          style={{
                            color: cumple ? '#1d8348' : '#b03a2e',
                            fontWeight: 600,
                          }}
                        >
                          {pct}% {cumple ? '✓' : '✗'}
                        </span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </section>

      <section style={{ marginTop: '1.5rem' }}>
        <h2 style={{ cursor: 'pointer' }} onClick={() =>
          setExpanded((e) => ({ ...e, asistencias: !e.asistencias }))
        }>
          {expanded.asistencias ? '▾' : '▸'} Asistencias ({alumno.asistencias.length})
        </h2>
        {expanded.asistencias && alumno.asistencias.length === 0 && (
          <p style={{ color: '#6e6e73' }}>
            Sin asistencias registradas.
          </p>
        )}
        {expanded.asistencias && alumno.asistencias.length > 0 && (
          <table className="data-table">
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Asignatura</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              {alumno.asistencias.map((a) => (
                <tr key={a.id}>
                  <td>{a.fecha}</td>
                  <td>{a.asignatura_codigo}</td>
                  <td>
                    <span className={`estado-badge estado-${a.estado}`}>
                      {a.estado}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
};
