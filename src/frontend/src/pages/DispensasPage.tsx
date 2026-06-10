import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { dispensasService } from '../services/dispensasService';
import type { SolicitudDispensa } from '../types/dispensas';
import { useAuth } from '../context/AuthContext';

const fmtFecha = (iso: string) => new Date(iso).toLocaleDateString();

const descargar = (blob: Blob, filename: string) => {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
};

export const DispensasPage: React.FC = () => {
  const { usuario } = useAuth();
  const [dispensas, setDispensas] = useState<SolicitudDispensa[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [exportando, setExportando] = useState(false);

  const esAlumno = usuario?.tipo === 'alumno';
  const esSecretaria = usuario?.tipo === 'secretaria';
  const esProfesor = usuario?.tipo === 'profesor';

  useEffect(() => {
    dispensasService
      .listar()
      .then(setDispensas)
      .catch(() => setError('No se pudo cargar la lista de dispensas'))
      .finally(() => setLoading(false));
  }, []);

  const exportar = async () => {
    setExportando(true);
    setError(null);
    try {
      const blob = await dispensasService.exportar();
      const fecha = new Date().toISOString().slice(0, 10);
      descargar(blob, `dispensas-${fecha}.csv`);
    } catch {
      setError('No se pudo exportar el listado');
    } finally {
      setExportando(false);
    }
  };

  return (
    <div className="page">
      <header className="page-header">
        <h1>
          {esAlumno
            ? 'Mis dispensas'
            : esProfesor
            ? 'Dispensas de mis asignaturas'
            : 'Solicitudes de dispensa'}
        </h1>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          {esAlumno && (
            <Link to="/dispensas/nuevo">
              <button type="button">+ Nueva solicitud</button>
            </Link>
          )}
          {esSecretaria && (
            <>
              <Link to="/dispensas/nuevo-en-nombre-de">
                <button type="button">+ Nueva en nombre de</button>
              </Link>
              <button type="button" onClick={exportar} disabled={exportando}>
                {exportando ? 'Exportando…' : 'Exportar CSV'}
              </button>
            </>
          )}
        </div>
      </header>

      {loading && <p>Cargando…</p>}
      {error && <div className="error">{error}</div>}

      {!loading && !error && dispensas.length === 0 && (
        <p style={{ color: '#6e6e73' }}>
          {esAlumno
            ? 'No tienes solicitudes. Pulsa "+ Nueva solicitud" para crear la primera.'
            : esProfesor
            ? 'No hay dispensas en tus asignaturas.'
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
                <td>
                  {d.asignatura_matriculada.asignatura.codigo}{' '}
                  · {d.asignatura_matriculada.asignatura.nombre}
                </td>
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
