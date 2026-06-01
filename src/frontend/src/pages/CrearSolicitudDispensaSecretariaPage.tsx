import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { isAxiosError } from 'axios';
import { dispensasService } from '../services/dispensasService';
import { alumnosService } from '../services/alumnosService';
import type {
  AlumnoListaItem,
  AsignaturaMatriculadaDelAlumno,
} from '../types/alumnos';

export const CrearSolicitudDispensaSecretariaPage: React.FC = () => {
  const navigate = useNavigate();

  const [busqueda, setBusqueda] = useState('');
  const [resultados, setResultados] = useState<AlumnoListaItem[]>([]);
  const [alumnoSeleccionado, setAlumnoSeleccionado] =
    useState<AlumnoListaItem | null>(null);
  const [asignaturas, setAsignaturas] = useState<
    AsignaturaMatriculadaDelAlumno[]
  >([]);
  const [asignaturaId, setAsignaturaId] = useState<number | ''>('');
  const [motivo, setMotivo] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (busqueda.length < 2) {
      setResultados([]);
      return;
    }
    const t = setTimeout(() => {
      alumnosService
        .listar({ page: 1, size: 10, q: busqueda })
        .then((r) => setResultados(r.items))
        .catch(() => setError('No se pudo buscar el alumno'));
    }, 200);
    return () => clearTimeout(t);
  }, [busqueda]);

  const seleccionarAlumno = async (alumno: AlumnoListaItem) => {
    setAlumnoSeleccionado(alumno);
    setBusqueda('');
    setResultados([]);
    setAsignaturas([]);
    setAsignaturaId('');
    try {
      const lista = await alumnosService.asignaturasMatriculadas(alumno.id);
      setAsignaturas(lista);
      if (lista.length > 0) setAsignaturaId(lista[0].id);
      else setError('Este alumno no tiene asignaturas matriculadas');
    } catch {
      setError('No se pudieron cargar las asignaturas matriculadas');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!alumnoSeleccionado || !asignaturaId) return;
    setError(null);
    setLoading(true);
    try {
      const creada = await dispensasService.crear({
        alumno_id: alumnoSeleccionado.id,
        asignatura_matriculada_id: Number(asignaturaId),
        motivo,
      });
      navigate(`/dispensas/${creada.id}`, { replace: true });
    } catch (err) {
      const detail =
        isAxiosError(err) && err.response?.data
          ? (err.response.data as { detail?: string }).detail
          : null;
      setError(detail || 'No se pudo crear la solicitud');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <header className="page-header">
        <h1>Nueva solicitud (en nombre de un alumno)</h1>
        <Link to="/dispensas">← Volver al listado</Link>
      </header>

      <form onSubmit={handleSubmit} className="form-card">
        <div className="field">
          <label>Alumno</label>
          {alumnoSeleccionado ? (
            <div
              style={{
                display: 'flex',
                gap: '0.5rem',
                alignItems: 'center',
                marginBottom: '0.5rem',
              }}
            >
              <strong>
                {alumnoSeleccionado.nombre} {alumnoSeleccionado.apellidos}
              </strong>
              <span style={{ color: '#6e6e73' }}>({alumnoSeleccionado.username})</span>
              <button
                type="button"
                onClick={() => {
                  setAlumnoSeleccionado(null);
                  setAsignaturas([]);
                  setAsignaturaId('');
                }}
              >
                Cambiar
              </button>
            </div>
          ) : (
            <>
              <input
                type="search"
                value={busqueda}
                onChange={(e) => setBusqueda(e.target.value)}
                placeholder="Buscar por nombre, apellidos, username, email…"
              />
              {resultados.length > 0 && (
                <ul
                  style={{
                    border: '1px solid #d2d2d7',
                    borderRadius: '4px',
                    padding: 0,
                    marginTop: '0.25rem',
                    listStyle: 'none',
                  }}
                >
                  {resultados.map((r) => (
                    <li
                      key={r.id}
                      style={{
                        padding: '0.5rem',
                        cursor: 'pointer',
                        borderBottom: '1px solid #f5f5f7',
                      }}
                      onClick={() => seleccionarAlumno(r)}
                    >
                      <strong>
                        {r.nombre} {r.apellidos}
                      </strong>{' '}
                      <span style={{ color: '#6e6e73' }}>({r.username})</span>
                    </li>
                  ))}
                </ul>
              )}
            </>
          )}
        </div>

        {alumnoSeleccionado && asignaturas.length > 0 && (
          <>
            <div className="field">
              <label htmlFor="am">Asignatura matriculada</label>
              <select
                id="am"
                value={asignaturaId}
                onChange={(e) => setAsignaturaId(Number(e.target.value))}
                required
              >
                {asignaturas.map((am) => (
                  <option key={am.id} value={am.id}>
                    {am.codigo} · {am.nombre} ({am.curso_academico}, {am.n_matricula}ª)
                  </option>
                ))}
              </select>
            </div>
            <div className="field">
              <label htmlFor="motivo">Motivo</label>
              <textarea
                id="motivo"
                value={motivo}
                onChange={(e) => setMotivo(e.target.value)}
                required
                rows={4}
                placeholder="Razón de la solicitud…"
              />
            </div>
            <button type="submit" disabled={loading}>
              {loading ? 'Creando…' : 'Crear solicitud'}
            </button>
          </>
        )}

        {error && <div className="error" style={{ marginTop: '1rem' }}>{error}</div>}
      </form>
    </div>
  );
};
