import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { isAxiosError } from 'axios';
import { dispensasService } from '../services/dispensasService';
import type { SolicitudDispensa } from '../types/dispensas';
import { ESTADOS_TERMINALES } from '../types/dispensas';
import { useAuth } from '../context/AuthContext';

const fmtFecha = (iso: string | null) =>
  iso ? new Date(iso).toLocaleString() : '—';

interface AccionesProps {
  rol: 'alumno' | 'director' | 'secretaria' | 'otro';
  solicitud: SolicitudDispensa;
}

const Acciones: React.FC<AccionesProps> = ({ rol, solicitud }) => {
  if (rol === 'director') {
    if (solicitud.estado === 'pendiente') {
      return (
        <Link to={`/dispensas/${solicitud.id}/veredicto`}>
          <button type="button">Iniciar revisión</button>
        </Link>
      );
    }
    if (solicitud.estado === 'en_revision') {
      return (
        <Link to={`/dispensas/${solicitud.id}/veredicto`}>
          <button type="button">Emitir veredicto</button>
        </Link>
      );
    }
    return null;
  }
  if (rol === 'alumno' || rol === 'secretaria') {
    if (solicitud.estado === 'pendiente') {
      return (
        <Link to={`/dispensas/${solicitud.id}/editar`}>
          <button type="button">Editar</button>
        </Link>
      );
    }
    return null;
  }
  return null;
};

export const ConsultarDispensaPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { usuario } = useAuth();
  const [solicitud, setSolicitud] = useState<SolicitudDispensa | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    dispensasService
      .obtener(Number(id))
      .then(setSolicitud)
      .catch((err) => {
        if (isAxiosError(err)) {
          if (err.response?.status === 404) setError('Solicitud no encontrada');
          else if (err.response?.status === 403)
            setError('No tienes permiso para ver esta solicitud');
          else setError('No se pudo cargar la solicitud');
        } else {
          setError('No se pudo cargar la solicitud');
        }
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="page"><p>Cargando…</p></div>;
  if (error)
    return (
      <div className="page">
        <div className="error">{error}</div>
        <Link to="/dispensas">← Volver al listado</Link>
      </div>
    );
  if (!solicitud) return null;

  const rol: AccionesProps['rol'] =
    usuario?.tipo === 'alumno'
      ? 'alumno'
      : usuario?.tipo === 'director'
      ? 'director'
      : usuario?.tipo === 'secretaria'
      ? 'secretaria'
      : 'otro';
  const terminal = ESTADOS_TERMINALES.has(solicitud.estado);
  const asig = solicitud.asignatura_matriculada.asignatura;

  return (
    <div className="page">
      <header className="page-header">
        <h1>Solicitud #{solicitud.id}</h1>
        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
          <Link to="/dispensas">← Listado</Link>
          <Acciones rol={rol} solicitud={solicitud} />
        </div>
      </header>

      <dl className="ficha">
        <dt>Estado</dt>
        <dd>
          <span className={`estado-badge estado-${solicitud.estado}`}>
            {solicitud.estado.replace('_', ' ')}
          </span>
        </dd>
        <dt>Alumno</dt>
        <dd>
          {solicitud.alumno.nombre} {solicitud.alumno.apellidos} ({solicitud.alumno.username})
        </dd>
        <dt>Asignatura</dt>
        <dd>
          <strong>{asig.codigo}</strong> · {asig.nombre} · {asig.ects} ECTS · {asig.caracter}
        </dd>
        <dt>Convocatoria</dt>
        <dd>{solicitud.asignatura_matriculada.n_matricula}ª</dd>
        <dt>Plan / facultad</dt>
        <dd>
          {asig.plan_estudios} — {asig.facultad}
        </dd>
        <dt>Motivo</dt>
        <dd>{solicitud.motivo || '—'}</dd>
        <dt>Fecha solicitud</dt>
        <dd>{fmtFecha(solicitud.fecha_solicitud)}</dd>
        <dt>Fecha resolución</dt>
        <dd>{fmtFecha(solicitud.fecha_resolucion)}</dd>
        <dt>Responsable</dt>
        <dd>
          {solicitud.responsable
            ? `${solicitud.responsable.nombre} ${solicitud.responsable.apellidos}`
            : '—'}
        </dd>
        <dt>Observaciones</dt>
        <dd>{solicitud.observaciones || '—'}</dd>
      </dl>

      {terminal && (
        <p style={{ marginTop: '1rem', color: '#6e6e73', fontSize: '0.875rem' }}>
          Esta solicitud está en un estado terminal. No admite más cambios.
        </p>
      )}
    </div>
  );
};
