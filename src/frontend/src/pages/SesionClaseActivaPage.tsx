import React, { useEffect, useMemo, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { isAxiosError } from 'axios';
import { sesionesClaseService } from '../services/sesionesClaseService';
import { alumnosService } from '../services/alumnosService';
import type { SesionDeClase } from '../types/sesiones_clase';
import type { AlumnoEnAsignatura } from '../types/alumnos';
import type { Asistencia, EstadoAsistencia } from '../types/asistencias';

const fmtFecha = (iso: string) => new Date(iso).toLocaleDateString();
const fmtHora = (hms: string) => hms.slice(0, 5);

export const SesionClaseActivaPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const sid = Number(id);
  const navigate = useNavigate();

  const [sesion, setSesion] = useState<SesionDeClase | null>(null);
  const [alumnos, setAlumnos] = useState<AlumnoEnAsignatura[]>([]);
  const [marcas, setMarcas] = useState<Map<number, Asistencia>>(new Map());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Modo edición in-situ
  const [editMode, setEditMode] = useState(false);
  const [borrador, setBorrador] = useState({
    fecha: '',
    hora_inicio: '',
    hora_fin: '',
    aula: '',
    tema: '',
  });
  const [guardando, setGuardando] = useState(false);

  // Modal cerrar
  const [cerrando, setCerrando] = useState(false);

  useEffect(() => {
    if (!sid) return;
    (async () => {
      try {
        const s = await sesionesClaseService.obtener(sid);
        setSesion(s);
        const [pag, asis] = await Promise.all([
          alumnosService.listarPorAsignatura(s.asignatura.id, 1, 200),
          sesionesClaseService.listarAsistencias(s.id),
        ]);
        setAlumnos(pag.items);
        const m = new Map<number, Asistencia>();
        for (const a of asis) m.set(a.alumno.id, a);
        setMarcas(m);
      } catch (err) {
        if (isAxiosError(err) && err.response?.status === 404)
          setError('Sesión no encontrada');
        else if (isAxiosError(err) && err.response?.status === 403)
          setError('No tienes permiso');
        else setError('No se pudo cargar la sesión');
      } finally {
        setLoading(false);
      }
    })();
  }, [sid]);

  const abrirEdicion = () => {
    if (!sesion) return;
    setBorrador({
      fecha: sesion.fecha,
      hora_inicio: sesion.hora_inicio.slice(0, 5),
      hora_fin: sesion.hora_fin.slice(0, 5),
      aula: sesion.aula,
      tema: sesion.tema,
    });
    setEditMode(true);
  };

  const cancelarEdicion = () => {
    if (!sesion) {
      setEditMode(false);
      return;
    }
    const cambios =
      borrador.fecha !== sesion.fecha ||
      borrador.hora_inicio !== sesion.hora_inicio.slice(0, 5) ||
      borrador.hora_fin !== sesion.hora_fin.slice(0, 5) ||
      borrador.aula !== sesion.aula ||
      borrador.tema !== sesion.tema;
    if (cambios && !window.confirm('¿Descartar los cambios sin guardar?')) {
      return;
    }
    setEditMode(false);
  };

  const guardar = async () => {
    if (!sesion) return;
    if (borrador.hora_fin <= borrador.hora_inicio) {
      setError('La hora de fin debe ser posterior a la de inicio');
      return;
    }
    setGuardando(true);
    setError(null);
    try {
      const cambios: Record<string, string> = {};
      if (borrador.fecha !== sesion.fecha) cambios.fecha = borrador.fecha;
      if (borrador.hora_inicio !== sesion.hora_inicio.slice(0, 5))
        cambios.hora_inicio = borrador.hora_inicio + ':00';
      if (borrador.hora_fin !== sesion.hora_fin.slice(0, 5))
        cambios.hora_fin = borrador.hora_fin + ':00';
      if (borrador.aula !== sesion.aula) cambios.aula = borrador.aula;
      if (borrador.tema !== sesion.tema) cambios.tema = borrador.tema;
      if (Object.keys(cambios).length === 0) {
        setEditMode(false);
        return;
      }
      const actualizada = await sesionesClaseService.actualizar(sesion.id, cambios);
      setSesion(actualizada);
      setEditMode(false);
    } catch (err) {
      const msg =
        isAxiosError(err) && err.response?.data?.detail
          ? String(err.response.data.detail)
          : 'No se pudo guardar';
      setError(msg);
    } finally {
      setGuardando(false);
    }
  };

  const cerrar = async () => {
    if (!sesion) return;
    if (!window.confirm('¿Finalizar la sesión? Se guardará la sesión en curso.'))
      return;
    setCerrando(true);
    setError(null);
    try {
      await sesionesClaseService.actualizar(sesion.id, { estado: 'cerrada' });
      navigate('/sesiones-clase');
    } catch {
      setError('No se pudo cerrar la sesión');
      setCerrando(false);
    }
  };

  const marcar = async (alumnoId: number, estado: EstadoAsistencia) => {
    if (!sesion) return;
    try {
      const a = await sesionesClaseService.marcarAsistencia(sesion.id, alumnoId, {
        estado,
      });
      setMarcas((prev) => new Map(prev).set(alumnoId, a));
    } catch (err) {
      const msg =
        isAxiosError(err) && err.response?.data?.detail
          ? String(err.response.data.detail)
          : 'No se pudo registrar la marca';
      setError(msg);
    }
  };

  const abierta = useMemo(() => sesion?.estado === 'abierta', [sesion]);

  if (loading) return <div className="page"><p>Cargando…</p></div>;
  if (error && !sesion)
    return (
      <div className="page">
        <div className="error">{error}</div>
        <Link to="/sesiones-clase">← Volver</Link>
      </div>
    );
  if (!sesion) return null;

  return (
    <div className="page">
      <header className="page-header">
        <h1>
          {sesion.asignatura.codigo} · {fmtFecha(sesion.fecha)}{' '}
          <span className={`estado-badge estado-${sesion.estado}`}>
            {sesion.estado}
          </span>
        </h1>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <Link to="/sesiones-clase">← Listado</Link>
          {abierta && !editMode && (
            <>
              <button type="button" onClick={abrirEdicion}>
                Editar
              </button>
              <button type="button" onClick={cerrar} disabled={cerrando}>
                {cerrando ? 'Cerrando…' : 'Finalizar sesión'}
              </button>
            </>
          )}
        </div>
      </header>

      {error && <div className="error">{error}</div>}

      <section className="form-card" aria-label="datos de la sesión">
        {!editMode ? (
          <dl className="ficha">
            <dt>Asignatura</dt>
            <dd>
              {sesion.asignatura.codigo} · {sesion.asignatura.nombre}
            </dd>
            <dt>Grupos</dt>
            <dd>{sesion.grupos.join(', ')}</dd>
            <dt>Aula</dt>
            <dd>{sesion.aula}</dd>
            <dt>Fecha</dt>
            <dd>{fmtFecha(sesion.fecha)}</dd>
            <dt>Horario</dt>
            <dd>
              {fmtHora(sesion.hora_inicio)} – {fmtHora(sesion.hora_fin)}
            </dd>
            <dt>Tema</dt>
            <dd>{sesion.tema}</dd>
          </dl>
        ) : (
          <>
            <label>
              Fecha
              <input
                type="date"
                value={borrador.fecha}
                onChange={(e) => setBorrador({ ...borrador, fecha: e.target.value })}
              />
            </label>
            <div style={{ display: 'flex', gap: '0.75rem' }}>
              <label style={{ flex: 1 }}>
                Hora inicio
                <input
                  type="time"
                  value={borrador.hora_inicio}
                  onChange={(e) =>
                    setBorrador({ ...borrador, hora_inicio: e.target.value })
                  }
                />
              </label>
              <label style={{ flex: 1 }}>
                Hora fin
                <input
                  type="time"
                  value={borrador.hora_fin}
                  onChange={(e) =>
                    setBorrador({ ...borrador, hora_fin: e.target.value })
                  }
                />
              </label>
            </div>
            <label>
              Aula
              <input
                type="text"
                value={borrador.aula}
                onChange={(e) => setBorrador({ ...borrador, aula: e.target.value })}
              />
            </label>
            <label>
              Tema
              <input
                type="text"
                value={borrador.tema}
                onChange={(e) => setBorrador({ ...borrador, tema: e.target.value })}
              />
            </label>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button type="button" onClick={guardar} disabled={guardando}>
                {guardando ? 'Guardando…' : 'Guardar'}
              </button>
              <button type="button" onClick={cancelarEdicion}>
                Cancelar
              </button>
            </div>
          </>
        )}
      </section>

      <section style={{ marginTop: '1.5rem' }}>
        <h2>{abierta ? 'Toma de asistencia' : 'Asistencia registrada'}</h2>
        {!abierta && (
          <p style={{ color: '#6e6e73' }}>
            Sesión cerrada — no admite más cambios.
          </p>
        )}
        {alumnos.length === 0 && (
          <p style={{ color: '#6e6e73' }}>
            No hay alumnos matriculados en esta asignatura.
          </p>
        )}
        {alumnos.length > 0 && (
          <table className="data-table">
            <thead>
              <tr>
                <th>Alumno</th>
                <th>Carnet</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              {alumnos.map((a) => {
                const marca = marcas.get(a.id);
                return (
                  <tr key={a.id}>
                    <td>
                      {a.nombre} {a.apellidos}
                    </td>
                    <td>{a.carnet}</td>
                    <td>
                      {abierta ? (
                        (['presente', 'justificado', 'ausente'] as EstadoAsistencia[]).map(
                          (e) => (
                            <button
                              key={e}
                              type="button"
                              onClick={() => marcar(a.id, e)}
                              style={{
                                marginRight: 4,
                                fontWeight: marca?.estado === e ? 'bold' : 'normal',
                                background:
                                  marca?.estado === e ? '#0071e3' : undefined,
                                color: marca?.estado === e ? '#fff' : undefined,
                              }}
                            >
                              {e}
                            </button>
                          )
                        )
                      ) : marca ? (
                        <span className={`estado-badge estado-${marca.estado}`}>
                          {marca.estado}
                        </span>
                      ) : (
                        <span style={{ color: '#6e6e73' }}>sin marcar</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
};
