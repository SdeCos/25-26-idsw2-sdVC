import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { isAxiosError } from 'axios';
import { dispensasService } from '../services/dispensasService';
import type { CrearSolicitudRequest } from '../types/dispensas';

export const CrearSolicitudPage: React.FC = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState<CrearSolicitudRequest>({
    asignatura: '',
    periodo: '',
    horario: '',
    motivo: '',
  });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const upd =
    <K extends keyof CrearSolicitudRequest>(key: K) =>
    (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) =>
      setForm({ ...form, [key]: e.target.value });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const creada = await dispensasService.crear(form);
      navigate(`/dispensas/${creada.id}`, { replace: true });
    } catch (err) {
      if (isAxiosError(err) && err.response?.status === 422) {
        setError('Revisa los campos: todos son obligatorios');
      } else {
        setError('No se pudo crear la solicitud');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <header className="page-header">
        <h1>Nueva solicitud de dispensa</h1>
        <Link to="/dispensas">← Volver al listado</Link>
      </header>

      <form onSubmit={handleSubmit} className="form-card">
        <div className="field">
          <label htmlFor="asignatura">Asignatura</label>
          <input id="asignatura" value={form.asignatura} onChange={upd('asignatura')} required autoFocus />
        </div>
        <div className="field">
          <label htmlFor="periodo">Periodo</label>
          <input id="periodo" value={form.periodo} onChange={upd('periodo')} required placeholder="ej. 2026-Q2" />
        </div>
        <div className="field">
          <label htmlFor="horario">Horario</label>
          <input id="horario" value={form.horario} onChange={upd('horario')} required placeholder="ej. Lunes 10:00-12:00" />
        </div>
        <div className="field">
          <label htmlFor="motivo">Motivo</label>
          <textarea
            id="motivo"
            value={form.motivo}
            onChange={upd('motivo')}
            required
            rows={4}
            placeholder="Explica brevemente la razón de la solicitud…"
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Creando…' : 'Crear solicitud'}
        </button>
        {error && <div className="error">{error}</div>}
      </form>
    </div>
  );
};
