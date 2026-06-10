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
  const [gruposUsados, setGruposUsados] = useState<string[]>([]);
  const [nuevoGrupo, setNuevoGrupo] = useState('');
  const [form, setForm] = useState({
    asignatura_id: 0,
    grupos: [] as string[],
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

  // Al cambiar de asignatura, recargar los grupos que el profesor ya ha usado
  // en ella y resetear los grupos seleccionados.
  useEffect(() => {
    if (form.asignatura_id === 0) return;
    sesionesClaseService
      .gruposUsados(form.asignatura_id)
      .then(setGruposUsados)
      .catch(() => setGruposUsados([]));
    setForm((f) => ({ ...f, grupos: [] }));
    setNuevoGrupo('');
  }, [form.asignatura_id]);

  const addGrupo = (valor: string) => {
    const limpio = valor.trim();
    if (!limpio) return;
    if (form.grupos.includes(limpio)) return;
    setForm((f) => ({ ...f, grupos: [...f.grupos, limpio] }));
    setNuevoGrupo('');
  };

  const removeGrupo = (valor: string) =>
    setForm((f) => ({ ...f, grupos: f.grupos.filter((g) => g !== valor) }));

  const gruposNoSeleccionados = gruposUsados.filter(
    (g) => !form.grupos.includes(g)
  );

  const cambiar = (campo: string, valor: string | number) =>
    setForm((f) => ({ ...f, [campo]: valor }));

  const submit = async (ev: React.FormEvent) => {
    ev.preventDefault();
    setError(null);
    if (form.asignatura_id === 0) {
      setError('Selecciona una asignatura');
      return;
    }
    if (form.grupos.length === 0) {
      setError('Añade al menos un grupo');
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
        grupos: form.grupos,
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

        <div>
          <label htmlFor="nuevo-grupo">Grupos</label>
          {form.grupos.length > 0 && (
            <div
              style={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: '0.375rem',
                margin: '0.25rem 0 0.5rem',
              }}
            >
              {form.grupos.map((g) => (
                <span
                  key={g}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '0.25rem',
                    background: '#e0e8ff',
                    color: '#0040a0',
                    padding: '0.125rem 0.5rem 0.125rem 0.625rem',
                    borderRadius: 999,
                    fontSize: '0.875rem',
                  }}
                >
                  {g}
                  <button
                    type="button"
                    onClick={() => removeGrupo(g)}
                    aria-label={`Quitar ${g}`}
                    style={{
                      background: 'none',
                      border: 'none',
                      cursor: 'pointer',
                      color: '#0040a0',
                      padding: '0 0.125rem',
                      fontSize: '1rem',
                      lineHeight: 1,
                    }}
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          )}
          <div style={{ display: 'flex', gap: '0.375rem' }}>
            <input
              id="nuevo-grupo"
              type="text"
              list="grupos-previos"
              value={nuevoGrupo}
              onChange={(e) => setNuevoGrupo(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  addGrupo(nuevoGrupo);
                }
              }}
              placeholder={
                gruposNoSeleccionados.length > 0
                  ? 'Escribe o elige de la lista'
                  : 'Nombre del grupo'
              }
            />
            <datalist id="grupos-previos">
              {gruposNoSeleccionados.map((g) => (
                <option key={g} value={g} />
              ))}
            </datalist>
            <button
              type="button"
              onClick={() => addGrupo(nuevoGrupo)}
              disabled={!nuevoGrupo.trim()}
            >
              Añadir
            </button>
          </div>
        </div>

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
