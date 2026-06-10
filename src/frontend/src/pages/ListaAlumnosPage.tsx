import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { isAxiosError } from 'axios';
import { profesoresService } from '../services/profesoresService';
import { alumnosService } from '../services/alumnosService';
import type { Asignatura } from '../types/asignaturas';
import type { AlumnoEnAsignatura } from '../types/alumnos';

export const ListaAlumnosPage: React.FC = () => {
  const [asignaturas, setAsignaturas] = useState<Asignatura[]>([]);
  const [asigActiva, setAsigActiva] = useState<number | null>(null);
  const [alumnos, setAlumnos] = useState<AlumnoEnAsignatura[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    profesoresService
      .misAsignaturas()
      .then((a) => {
        setAsignaturas(a);
        if (a.length > 0) setAsigActiva(a[0].id);
        else setLoading(false);
      })
      .catch(() => {
        setError('No se pudieron cargar las asignaturas');
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    if (asigActiva === null) return;
    setLoading(true);
    setError(null);
    alumnosService
      .listarPorAsignatura(asigActiva, 1, 200)
      .then((pag) => {
        setAlumnos(pag.items);
        setTotal(pag.total);
      })
      .catch((err) => {
        if (isAxiosError(err) && err.response?.status === 403)
          setError('No impartes esta asignatura');
        else setError('No se pudo cargar la lista de alumnos');
      })
      .finally(() => setLoading(false));
  }, [asigActiva]);

  return (
    <div className="page">
      <header className="page-header">
        <h1>Alumnos</h1>
      </header>

      <div role="tablist" style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
        {asignaturas.map((a) => (
          <button
            key={a.id}
            type="button"
            role="tab"
            aria-selected={a.id === asigActiva}
            onClick={() => setAsigActiva(a.id)}
            style={{
              fontWeight: a.id === asigActiva ? 'bold' : 'normal',
              background: a.id === asigActiva ? '#0071e3' : undefined,
              color: a.id === asigActiva ? '#fff' : undefined,
            }}
          >
            {a.codigo} · {a.nombre}
          </button>
        ))}
      </div>

      {loading && <p>Cargando…</p>}
      {error && <div className="error">{error}</div>}

      {!loading && !error && (
        <>
          <p style={{ color: '#6e6e73' }}>{total} alumnos matriculados</p>
          <table className="data-table">
            <thead>
              <tr>
                <th>Carnet</th>
                <th>Nombre</th>
                <th>Apellidos</th>
                <th>Email</th>
                <th>Curso</th>
                <th>Estado</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {alumnos.map((a) => (
                <tr key={a.id}>
                  <td>{a.carnet}</td>
                  <td>{a.nombre}</td>
                  <td>{a.apellidos}</td>
                  <td>{a.email}</td>
                  <td>{a.curso_academico}</td>
                  <td>{a.estado_matricula}</td>
                  <td>
                    <Link to={`/alumnos/${a.id}`}>Ver ficha</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
};
