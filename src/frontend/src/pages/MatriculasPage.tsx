import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { matriculasService } from '../services/matriculasService';
import type { MatriculaListaItem } from '../types/matriculas';

const fmtFecha = (iso: string) => new Date(iso).toLocaleDateString();

export const MatriculasPage: React.FC = () => {
  const [matriculas, setMatriculas] = useState<MatriculaListaItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    matriculasService
      .listar()
      .then(setMatriculas)
      .catch(() => setError('No se pudo cargar el listado de matrículas'))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="page">
      <header className="page-header">
        <h1>Matrículas</h1>
        <Link to="/matriculas/importar">
          <button type="button">Importar matrículas</button>
        </Link>
      </header>

      {loading && <p>Cargando…</p>}
      {error && <div className="error">{error}</div>}

      {!loading && !error && matriculas.length === 0 && (
        <p style={{ color: '#6e6e73' }}>
          No hay matrículas registradas. Importa un CSV para empezar.
        </p>
      )}

      {!loading && !error && matriculas.length > 0 && (
        <table className="data-table">
          <thead>
            <tr>
              <th>Alumno</th>
              <th>Username</th>
              <th>Curso académico</th>
              <th>Grado</th>
              <th>Asignaturas</th>
              <th>Fecha import</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {matriculas.map((m) => (
              <tr key={m.id}>
                <td>
                  {m.alumno.nombre} {m.alumno.apellidos}
                </td>
                <td>{m.alumno.username}</td>
                <td>{m.curso_academico}</td>
                <td>{m.grado || '—'}</td>
                <td>{m.num_asignaturas}</td>
                <td>{fmtFecha(m.fecha_importacion)}</td>
                <td>
                  <Link to={`/matriculas/${m.id}`}>Ver</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};
