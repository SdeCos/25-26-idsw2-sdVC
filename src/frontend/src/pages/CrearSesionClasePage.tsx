import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { isAxiosError } from 'axios';
import { profesoresService } from '../services/profesoresService';
import { sesionesClaseService } from '../services/sesionesClaseService';
import type { Asignatura } from '../types/asignaturas';

const hoyISO = () => new Date().toISOString().slice(0, 10);

export const CrearSesionClasePage: React.FC = () => {
  const navigate = useNavigate();
  const [asignaturas, setAsignaturas] = useState<Asignatura[]>([]);
  const [form, setForm] = useState({
    asignatura_id: 0,
    grupo: '',
    aula: '',
    fecha: hoyISO(),
    hora_inicio: '09:00',
    hora_fin: '10:30',
    tema: '',
  });
  const [error, setError] = useState<string | null>(null);
  const [guardando, setGuardando] = useState(false);

  useEffect(() => {
    profesoresService
      .misAsignaturas()
      .then((a) => {
        setAsignaturas(a);
        if (a.length > 0) setForm((f) => ({ ...f, asignatura_id: a[0].id }));
      })
      .catch(() => setError('No se pudieron cargar las asignaturas'));
  }, []);

  const cambiar = (campo: string, valor: string | number) =>
    setForm((f) => ({ ...f, [campo]: valor }));

  const submit = async (ev: React.FormEvent) => {
    ev.preventDefault();
    setError(null);
    if (form.asignatura_id === 0) {
      setError('Selecciona una asignatura');
      return;
    }
    if (form.hora_fin <= form.hora_inicio) {
      setError('La hora de fin debe ser posterior a la de inicio');
      return;
    }
    setGuardando(true);
    try {
      const sesion = await sesionesClaseService.crear({
        asignatura_id: form.asignatura_id,
        grupo: form.grupo,
        aula: form.aula,
        fecha: form.fecha,
        hora_inicio: form.hora_inicio + ':00',
        hora_fin: form.hora_fin + ':00',
        tema: form.tema,
      });
      navigate(`/sesiones-clase/${sesion.id}`);
    } catch (err) {
      const msg =
        isAxiosError(err) && err.response?.data?.detail
          ? String(err.response.data.detail)
          : 'No se pudo crear la sesión';
      setError(msg);
    } finally {
      setGuardando(false);
    }
  };

  return (
    <div className="page">
      <header className="page-header">
        <h1>Nueva sesión de clase</h1>
        <Link to="/sesiones-clase">← Listado</Link>
      </header>

      <form onSubmit={submit} className="form-card">
        {error && <div className="error">{error}</div>}

        <label>
          Asignatura
          <select
            value={form.asignatura_id}
            onChange={(e) => cambiar('asignatura_id', Number(e.target.value))}
            required
          >
            <option value={0} disabled>
              — selecciona —
            </option>
            {asignaturas.map((a) => (
              <option key={a.id} value={a.id}>
                {a.codigo} · {a.nombre}
              </option>
            ))}
          </select>
        </label>

        <label>
          Grupo
          <input
            type="text"
            value={form.grupo}
            onChange={(e) => cambiar('grupo', e.target.value)}
            required
          />
        </label>

        <label>
          Aula
          <input
            type="text"
            value={form.aula}
            onChange={(e) => cambiar('aula', e.target.value)}
            required
          />
        </label>

        <label>
          Fecha
          <input
            type="date"
            value={form.fecha}
            onChange={(e) => cambiar('fecha', e.target.value)}
            required
          />
        </label>

        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <label style={{ flex: 1 }}>
            Hora inicio
            <input
              type="time"
              value={form.hora_inicio}
              onChange={(e) => cambiar('hora_inicio', e.target.value)}
              required
            />
          </label>
          <label style={{ flex: 1 }}>
            Hora fin
            <input
              type="time"
              value={form.hora_fin}
              onChange={(e) => cambiar('hora_fin', e.target.value)}
              required
            />
          </label>
        </div>

        <label>
          Tema
          <input
            type="text"
            value={form.tema}
            onChange={(e) => cambiar('tema', e.target.value)}
            required
          />
        </label>

        <button type="submit" disabled={guardando}>
          {guardando ? 'Creando…' : 'Crear sesión'}
        </button>
      </form>
    </div>
  );
};
