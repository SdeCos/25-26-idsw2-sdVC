import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { sesionesClaseService } from '../services/sesionesClaseService';
import { asistenciasService } from '../services/asistenciasService';
import { profesoresService } from '../services/profesoresService';
import type { SesionDeClase } from '../types/sesiones_clase';
import type { Asignatura } from '../types/asignaturas';

const fmtFecha = (iso: string) => new Date(iso).toLocaleDateString();
const fmtHora = (hms: string) => hms.slice(0, 5);

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

export const SesionesClasePage: React.FC = () => {
  const [sesiones, setSesiones] = useState<SesionDeClase[]>([]);
  const [asignaturas, setAsignaturas] = useState<Asignatura[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [asigExport, setAsigExport] = useState<number | null>(null);
  const [exportando, setExportando] = useState(false);

  useEffect(() => {
    Promise.all([
      sesionesClaseService.listar(),
      profesoresService.misAsignaturas(),
    ])
      .then(([s, a]) => {
        setSesiones(s);
        setAsignaturas(a);
        if (a.length > 0) setAsigExport(a[0].id);
      })
      .catch(() => setError('No se pudo cargar el listado'))
      .finally(() => setLoading(false));
  }, []);

  const exportar = async () => {
    if (!asigExport) return;
    setExportando(true);
    setError(null);
    try {
      const blob = await asistenciasService.exportar({
        asignatura_id: asigExport,
      });
      const cod = asignaturas.find((a) => a.id === asigExport)?.codigo ?? 'asig';
      const hoy = new Date().toISOString().slice(0, 10);
      descargar(blob, `asistencias-${cod}-${hoy}.csv`);
    } catch {
      setError('No se pudo exportar el historial');
    } finally {
      setExportando(false);
    }
  };

  return (
    <div className="page">
      <header className="page-header">
        <h1>Sesiones de clase</h1>
        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
          <Link to="/sesiones-clase/nuevo">
            <button type="button">+ Nueva sesión</button>
          </Link>
          {asignaturas.length > 0 && (
            <>
              <select
                value={asigExport ?? ''}
                onChange={(e) => setAsigExport(Number(e.target.value))}
                aria-label="asignatura a exportar"
              >
                {asignaturas.map((a) => (
                  <option key={a.id} value={a.id}>
                    {a.codigo}
                  </option>
                ))}
              </select>
              <button type="button" onClick={exportar} disabled={exportando}>
                {exportando ? 'Exportando…' : 'Exportar historial CSV'}
              </button>
            </>
          )}
        </div>
      </header>

      {loading && <p>Cargando…</p>}
      {error && <div className="error">{error}</div>}

      {!loading && !error && sesiones.length === 0 && (
        <p style={{ color: '#6e6e73' }}>
          Sin sesiones registradas. Pulsa "+ Nueva sesión" para empezar.
        </p>
      )}

      {!loading && !error && sesiones.length > 0 && (
        <table className="data-table">
          <thead>
            <tr>
              <th>Fecha</th>
              <th>Hora</th>
              <th>Asignatura</th>
              <th>Grupo</th>
              <th>Aula</th>
              <th>Tema</th>
              <th>Estado</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {sesiones.map((s) => (
              <tr key={s.id}>
                <td>{fmtFecha(s.fecha)}</td>
                <td>
                  {fmtHora(s.hora_inicio)} – {fmtHora(s.hora_fin)}
                </td>
                <td>
                  {s.asignatura.codigo} · {s.asignatura.nombre}
                </td>
                <td>{s.grupo}</td>
                <td>{s.aula}</td>
                <td>{s.tema}</td>
                <td>
                  <span className={`estado-badge estado-${s.estado}`}>
                    {s.estado}
                  </span>
                </td>
                <td>
                  <Link to={`/sesiones-clase/${s.id}`}>Abrir</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};
