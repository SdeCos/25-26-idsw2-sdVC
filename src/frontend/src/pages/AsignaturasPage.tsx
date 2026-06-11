import React, { useEffect, useState } from 'react';
import { isAxiosError } from 'axios';
import { asignaturasService } from '../services/asignaturasService';
import { gradosService } from '../services/gradosService';
import type {
  Asignatura,
  CaracterAsignatura,
  CrearAsignaturaRequest,
} from '../types/asignaturas';
import type { Grado } from '../types/grados';

type Modo =
  | { tipo: 'lista' }
  | { tipo: 'alta' }
  | { tipo: 'edicion'; asignatura: Asignatura };

const FORM_VACIO: CrearAsignaturaRequest = {
  codigo: '',
  nombre: '',
  ects: 6,
  caracter: 'OB',
  curso_plan: 1,
  grado_ids: [],
};

const CARACTERES: CaracterAsignatura[] = ['FB', 'OB', 'OP'];

export const AsignaturasPage: React.FC = () => {
  const [asignaturas, setAsignaturas] = useState<Asignatura[]>([]);
  const [grados, setGrados] = useState<Grado[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modo, setModo] = useState<Modo>({ tipo: 'lista' });
  const [form, setForm] = useState<CrearAsignaturaRequest>(FORM_VACIO);
  const [guardando, setGuardando] = useState(false);

  const cargar = () => {
    setLoading(true);
    Promise.all([asignaturasService.listar(), gradosService.listar()])
      .then(([as, gs]) => {
        setAsignaturas(as);
        setGrados(gs);
      })
      .catch(() => setError('No se pudo cargar el catálogo'))
      .finally(() => setLoading(false));
  };

  useEffect(cargar, []);

  const abrirAlta = () => {
    setForm({
      ...FORM_VACIO,
      grado_ids: grados[0] ? [grados[0].id] : [],
    });
    setError(null);
    setModo({ tipo: 'alta' });
  };

  const abrirEdicion = (a: Asignatura) => {
    setForm({
      codigo: a.codigo,
      nombre: a.nombre,
      ects: a.ects,
      caracter: a.caracter,
      curso_plan: a.curso_plan,
      grado_ids: a.grados.map((g) => g.id),
    });
    setError(null);
    setModo({ tipo: 'edicion', asignatura: a });
  };

  const toggleGrado = (gradoId: number) => {
    setForm((prev) => {
      const set = new Set(prev.grado_ids);
      if (set.has(gradoId)) set.delete(gradoId);
      else set.add(gradoId);
      return { ...prev, grado_ids: Array.from(set) };
    });
  };

  const cancelar = () => {
    setForm(FORM_VACIO);
    setError(null);
    setModo({ tipo: 'lista' });
  };

  const submit = async (ev: React.FormEvent) => {
    ev.preventDefault();
    setError(null);
    setGuardando(true);
    try {
      if (form.grado_ids.length === 0) {
        setError('Selecciona al menos un grado');
        setGuardando(false);
        return;
      }
      if (modo.tipo === 'alta') {
        await asignaturasService.crear(form);
      } else if (modo.tipo === 'edicion') {
        await asignaturasService.actualizar(modo.asignatura.id, {
          nombre: form.nombre,
          ects: form.ects,
          caracter: form.caracter,
          curso_plan: form.curso_plan,
          grado_ids: form.grado_ids,
        });
      }
      setModo({ tipo: 'lista' });
      cargar();
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

  const eliminar = async (a: Asignatura) => {
    if (!window.confirm(`¿Eliminar asignatura ${a.codigo} (${a.nombre})?`)) return;
    setError(null);
    try {
      await asignaturasService.eliminar(a.id);
      cargar();
    } catch (err) {
      const msg =
        isAxiosError(err) && err.response?.data?.detail
          ? String(err.response.data.detail)
          : 'No se pudo eliminar';
      setError(msg);
    }
  };

  return (
    <div className="page">
      <header className="page-header">
        <h1>Asignaturas</h1>
        {modo.tipo === 'lista' && (
          <button type="button" onClick={abrirAlta} disabled={grados.length === 0}>
            + Nueva asignatura
          </button>
        )}
      </header>

      {grados.length === 0 && !loading && (
        <div className="error">
          No hay grados dados de alta — añade uno antes de crear asignaturas.
        </div>
      )}

      {error && <div className="error">{error}</div>}

      {(modo.tipo === 'alta' || modo.tipo === 'edicion') && (
        <form
          onSubmit={submit}
          className="form-card"
          style={{ marginBottom: '1.5rem' }}
        >
          <h2 style={{ fontSize: '1.125rem', marginBottom: '1rem' }}>
            {modo.tipo === 'alta'
              ? 'Nueva asignatura'
              : `Editando ${modo.asignatura.codigo}`}
          </h2>

          <label>
            Código
            <input
              type="text"
              value={form.codigo}
              onChange={(e) => setForm({ ...form, codigo: e.target.value })}
              disabled={modo.tipo === 'edicion'}
              required
            />
          </label>

          <label>
            Nombre
            <input
              type="text"
              value={form.nombre}
              onChange={(e) => setForm({ ...form, nombre: e.target.value })}
              required
            />
          </label>

          <label>
            ECTS
            <input
              type="number"
              step="0.5"
              min="0.5"
              value={form.ects}
              onChange={(e) =>
                setForm({ ...form, ects: Number(e.target.value) })
              }
              required
            />
          </label>

          <label>
            Carácter
            <select
              value={form.caracter}
              onChange={(e) =>
                setForm({ ...form, caracter: e.target.value as CaracterAsignatura })
              }
              required
            >
              {CARACTERES.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </label>

          <label>
            Curso del plan
            <input
              type="number"
              min="1"
              max="6"
              value={form.curso_plan}
              onChange={(e) =>
                setForm({ ...form, curso_plan: Number(e.target.value) })
              }
              required
            />
          </label>

          <div className="field">
            <label style={{ display: 'block', marginBottom: '0.25rem' }}>
              Grados (marca uno o varios)
            </label>
            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '0.25rem',
                padding: '0.5rem',
                border: '1px solid #d1d1d6',
                borderRadius: '4px',
              }}
            >
              {grados.map((g) => (
                <label
                  key={g.id}
                  style={{ display: 'flex', gap: '0.5rem', cursor: 'pointer' }}
                >
                  <input
                    type="checkbox"
                    checked={form.grado_ids.includes(g.id)}
                    onChange={() => toggleGrado(g.id)}
                  />
                  <span>
                    {g.codigo} · {g.nombre}
                  </span>
                </label>
              ))}
            </div>
          </div>

          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button type="submit" disabled={guardando}>
              {guardando ? 'Guardando…' : 'Guardar'}
            </button>
            <button type="button" onClick={cancelar}>
              Cancelar
            </button>
          </div>
        </form>
      )}

      {loading && <p>Cargando…</p>}

      {!loading && (
        <table className="data-table">
          <thead>
            <tr>
              <th>Código</th>
              <th>Nombre</th>
              <th>ECTS</th>
              <th>Carácter</th>
              <th>Curso</th>
              <th>Grados</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {asignaturas.map((a) => (
              <tr key={a.id}>
                <td>{a.codigo}</td>
                <td>{a.nombre}</td>
                <td>{a.ects}</td>
                <td>{a.caracter}</td>
                <td>{a.curso_plan}</td>
                <td>{a.grados.map((g) => g.codigo).join(', ')}</td>
                <td>
                  <button
                    type="button"
                    onClick={() => abrirEdicion(a)}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: '#0066cc',
                      cursor: 'pointer',
                      padding: 0,
                    }}
                  >
                    Editar
                  </button>
                  {' · '}
                  <button
                    type="button"
                    onClick={() => eliminar(a)}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: '#c00',
                      cursor: 'pointer',
                      padding: 0,
                    }}
                  >
                    Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};
