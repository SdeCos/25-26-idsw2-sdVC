import React, { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { isAxiosError } from 'axios';
import { dispensasService } from '../services/dispensasService';
import type {
  EditarSolicitudRequest,
  SolicitudDispensa,
} from '../types/dispensas';

interface FormState {
  asignatura: string;
  periodo: string;
  horario: string;
  motivo: string;
}

const desdeSolicitud = (s: SolicitudDispensa): FormState => ({
  asignatura: s.asignatura,
  periodo: s.periodo,
  horario: s.horario,
  motivo: s.motivo || '',
});

export const EditarSolicitudPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [original, setOriginal] = useState<SolicitudDispensa | null>(null);
  const [form, setForm] = useState<FormState | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [cancelando, setCancelando] = useState(false);

  useEffect(() => {
    if (!id) return;
    dispensasService
      .obtener(Number(id))
      .then((s) => {
        setOriginal(s);
        setForm(desdeSolicitud(s));
      })
      .catch((err) => {
        if (isAxiosError(err)) {
          if (err.response?.status === 404) setError('Solicitud no encontrada');
          else if (err.response?.status === 403) setError('No tienes permiso para esta solicitud');
          else setError('No se pudo cargar la solicitud');
        } else {
          setError('No se pudo cargar la solicitud');
        }
      });
  }, [id]);

  const diff = (): EditarSolicitudRequest => {
    if (!original || !form) return {};
    const cambios: EditarSolicitudRequest = {};
    if (form.asignatura !== original.asignatura) cambios.asignatura = form.asignatura;
    if (form.periodo !== original.periodo) cambios.periodo = form.periodo;
    if (form.horario !== original.horario) cambios.horario = form.horario;
    if (form.motivo !== (original.motivo || '')) cambios.motivo = form.motivo;
    return cambios;
  };

  const guardar = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!original) return;
    const cambios = diff();
    if (Object.keys(cambios).length === 0) {
      navigate(`/dispensas/${original.id}`);
      return;
    }
    setSaving(true);
    setError(null);
    try {
      await dispensasService.actualizar(original.id, cambios);
      navigate(`/dispensas/${original.id}`);
    } catch (err) {
      const detail =
        isAxiosError(err) && err.response?.data
          ? (err.response.data as { detail?: string }).detail
          : null;
      setError(detail || 'No se pudo guardar la solicitud');
    } finally {
      setSaving(false);
    }
  };

  const cancelar = async () => {
    if (!original) return;
    if (!window.confirm('¿Seguro que quieres cancelar esta solicitud? Esta acción no se puede deshacer.')) {
      return;
    }
    setCancelando(true);
    setError(null);
    try {
      await dispensasService.actualizar(original.id, { estado: 'anulada' });
      navigate(`/dispensas/${original.id}`);
    } catch (err) {
      const detail =
        isAxiosError(err) && err.response?.data
          ? (err.response.data as { detail?: string }).detail
          : null;
      setError(detail || 'No se pudo cancelar la solicitud');
    } finally {
      setCancelando(false);
    }
  };

  if (error && !original) {
    return (
      <div className="page">
        <div className="error">{error}</div>
        <Link to="/dispensas">← Volver al listado</Link>
      </div>
    );
  }
  if (!form || !original) return <div className="page"><p>Cargando…</p></div>;

  const editable = original.estado === 'pendiente';

  return (
    <div className="page">
      <header className="page-header">
        <h1>Editar solicitud #{original.id}</h1>
        <Link to={`/dispensas/${original.id}`}>← Cancelar edición</Link>
      </header>

      {!editable && (
        <div className="error" style={{ marginBottom: '1rem' }}>
          Solo se pueden editar solicitudes en estado PENDIENTE. Esta está en{' '}
          <strong>{original.estado.replace('_', ' ')}</strong>.
        </div>
      )}

      <form onSubmit={guardar} className="form-card">
        <div className="field">
          <label htmlFor="asignatura">Asignatura</label>
          <input
            id="asignatura"
            value={form.asignatura}
            onChange={(e) => setForm({ ...form, asignatura: e.target.value })}
            disabled={!editable}
            required
          />
        </div>
        <div className="field">
          <label htmlFor="periodo">Periodo</label>
          <input
            id="periodo"
            value={form.periodo}
            onChange={(e) => setForm({ ...form, periodo: e.target.value })}
            disabled={!editable}
            required
          />
        </div>
        <div className="field">
          <label htmlFor="horario">Horario</label>
          <input
            id="horario"
            value={form.horario}
            onChange={(e) => setForm({ ...form, horario: e.target.value })}
            disabled={!editable}
            required
          />
        </div>
        <div className="field">
          <label htmlFor="motivo">Motivo</label>
          <textarea
            id="motivo"
            value={form.motivo}
            onChange={(e) => setForm({ ...form, motivo: e.target.value })}
            disabled={!editable}
            required
            rows={4}
          />
        </div>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button type="submit" disabled={!editable || saving}>
            {saving ? 'Guardando…' : 'Guardar cambios'}
          </button>
          <button
            type="button"
            onClick={cancelar}
            disabled={!editable || cancelando}
            style={{ background: '#c00', color: 'white', borderColor: '#c00' }}
          >
            {cancelando ? 'Cancelando…' : 'Cancelar solicitud'}
          </button>
        </div>
        {error && <div className="error">{error}</div>}
      </form>
    </div>
  );
};
