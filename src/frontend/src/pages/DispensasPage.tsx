import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { dispensasService } from '../services/dispensasService';
import type { SolicitudDispensa } from '../types/dispensas';
import { useAuth } from '../context/AuthContext';

const fmtFecha = (iso: string) => new Date(iso).toLocaleDateString();

export const DispensasPage: React.FC = () => {
  const { usuario } = useAuth();
  const [dispensas, setDispensas] = useState<SolicitudDispensa[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const esAlumno = usuario?.tipo === 'alumno';

  useEffect(() => {
    dispensasService
      .listar()
      .then(setDispensas)
      .catch(() => setError('No se pudo cargar la lista de dispensas'))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="page">
      <header className="page-header">
        <h1>{esAlumno ? 'Mis dispensas' : 'Solicitudes de dispensa'}</h1>
        {esAlumno && (
          <Link to="/dispensas/nuevo">
            <button type="button">+ Nueva solicitud</button>
          </Link>
        )}
      </header>

      {loading && <p>Cargando…</p>}
      {error && <div className="error">{error}</div>}

      {!loading && !error && dispensas.length === 0 && (
        <p style={{ color: '#6e6e73' }}>
          {esAlumno
            ? 'No tienes solicitudes. Pulsa "+ Nueva solicitud" para crear la primera.'
            : 'No hay solicitudes registradas.'}
        </p>
      )}

      {!loading && !error && dispensas.length > 0 && (
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              {!esAlumno && <th>Alumno</th>}
              <th>Asignatura</th>
              <th>Periodo</th>
              <th>Fecha solicitud</th>
              <th>Estado</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {dispensas.map((d) => (
              <tr key={d.id}>
                <td>{d.id}</td>
                {!esAlumno && (
                  <td>
                    {d.alumno.nombre} {d.alumno.apellidos}
                  </td>
                )}
                <td>{d.asignatura}</td>
                <td>{d.periodo}</td>
                <td>{fmtFecha(d.fecha_solicitud)}</td>
                <td>
                  <span className={`estado-badge estado-${d.estado}`}>
                    {d.estado.replace('_', ' ')}
                  </span>
                </td>
                <td>
                  <Link to={`/dispensas/${d.id}`}>Ver</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};
