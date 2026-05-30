import React, { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { isAxiosError } from 'axios';
import { dispensasService } from '../services/dispensasService';
import type {
  EditarSolicitudRequest,
  EstadoSolicitud,
  SolicitudDispensa,
} from '../types/dispensas';

type AccionVeredicto = 'aprobar' | 'rechazar';

const estadoPara = (accion: AccionVeredicto): EstadoSolicitud =>
  accion === 'aprobar' ? 'aprobada' : 'rechazada';

export const EmitirVeredictoPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [solicitud, setSolicitud] = useState<SolicitudDispensa | null>(null);
  const [observaciones, setObservaciones] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [working, setWorking] = useState(false);

  useEffect(() => {
    if (!id) return;
    dispensasService
      .obtener(Number(id))
      .then(setSolicitud)
      .catch((err) => {
        if (isAxiosError(err) && err.response?.status === 404) {
          setError('Solicitud no encontrada');
        } else {
          setError('No se pudo cargar la solicitud');
        }
      });
  }, [id]);

  const enviar = async (body: EditarSolicitudRequest) => {
    if (!solicitud) return;
    setError(null);
    setWorking(true);
    try {
      await dispensasService.actualizar(solicitud.id, body);
      navigate(`/dispensas/${solicitud.id}`);
    } catch (err) {
      if (isAxiosError(err) && err.response?.status === 422) {
        const detail = (err.response.data as { detail?: string })?.detail;
        setError(detail || 'Operación no permitida');
      } else {
        setError('No se pudo registrar el veredicto');
      }
    } finally {
      setWorking(false);
    }
  };

  const iniciarRevision = () => enviar({ estado: 'en_revision' });

  const emitirVeredicto = (e: React.FormEvent, accion: AccionVeredicto) => {
    e.preventDefault();
    const body: EditarSolicitudRequest = { estado: estadoPara(accion) };
    if (observaciones.trim()) body.observaciones = observaciones.trim();
    enviar(body);
  };

  if (error && !solicitud) {
    return (
      <div className="page">
        <div className="error">{error}</div>
        <Link to="/dispensas">← Volver al listado</Link>
      </div>
    );
  }
  if (!solicitud) return <div className="page"><p>Cargando…</p></div>;

  return (
    <div className="page">
      <header className="page-header">
        <h1>Veredicto · solicitud #{solicitud.id}</h1>
        <Link to={`/dispensas/${solicitud.id}`}>← Cancelar</Link>
      </header>

      <div className="form-card">
        <p style={{ marginBottom: '1rem', color: '#6e6e73' }}>
          {solicitud.alumno.nombre} {solicitud.alumno.apellidos} · {solicitud.asignatura} ({solicitud.periodo})
        </p>
        <p style={{ marginBottom: '1.5rem' }}>
          Estado actual:{' '}
          <span className={`estado-badge estado-${solicitud.estado}`}>
            {solicitud.estado.replace('_', ' ')}
          </span>
        </p>

        {solicitud.estado === 'pendiente' && (
          <div>
            <p style={{ marginBottom: '1rem', fontSize: '0.875rem', color: '#6e6e73' }}>
              Toma esta solicitud para revisión. Una vez en revisión podrás aprobarla o rechazarla.
            </p>
            <button type="button" onClick={iniciarRevision} disabled={working}>
              {working ? 'Iniciando…' : 'Iniciar revisión'}
            </button>
          </div>
        )}

        {solicitud.estado === 'en_revision' && (
          <form>
            <div className="field">
              <label htmlFor="obs">
                Observaciones <small style={{ color: '#6e6e73' }}>(obligatorias al rechazar)</small>
              </label>
              <textarea
                id="obs"
                value={observaciones}
                onChange={(e) => setObservaciones(e.target.value)}
                rows={4}
                placeholder="Justificación de la decisión…"
                style={{
                  width: '100%',
                  padding: '0.5rem',
                  border: '1px solid #d2d2d7',
                  borderRadius: '6px',
                  font: 'inherit',
                  resize: 'vertical',
                }}
              />
            </div>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button
                type="button"
                onClick={(e) => emitirVeredicto(e, 'aprobar')}
                disabled={working}
                style={{ background: '#0a7d28', color: 'white', borderColor: '#0a7d28' }}
              >
                {working ? 'Procesando…' : 'Aprobar'}
              </button>
              <button
                type="button"
                onClick={(e) => emitirVeredicto(e, 'rechazar')}
                disabled={working}
                style={{ background: '#c00', color: 'white', borderColor: '#c00' }}
              >
                {working ? 'Procesando…' : 'Rechazar'}
              </button>
            </div>
          </form>
        )}

        {error && <div className="error">{error}</div>}
      </div>
    </div>
  );
};
