import React, { useEffect, useState } from 'react';
import { isAxiosError } from 'axios';
import { profesoresService } from '../services/profesoresService';
import { asignaturasService } from '../services/asignaturasService';
import type { Asignatura } from '../types/asignaturas';
import type { UsuarioDetalle } from '../types/usuarios';

export const AsignarAsignaturasProfesorPage: React.FC = () => {
  const [profesores, setProfesores] = useState<UsuarioDetalle[]>([]);
  const [asignaturas, setAsignaturas] = useState<Asignatura[]>([]);
  const [profesorId, setProfesorId] = useState<number | null>(null);
  const [impartidas, setImpartidas] = useState<Set<number>>(new Set());
  const [loading, setLoading] = useState(true);
  const [cargandoProfesor, setCargandoProfesor] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([profesoresService.listar(), asignaturasService.listar()])
      .then(([profes, asigs]) => {
        setProfesores(profes);
        setAsignaturas(asigs);
        if (profes.length > 0) setProfesorId(profes[0].id);
      })
      .catch(() => setError('No se pudieron cargar profesores o asignaturas'))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (profesorId === null) return;
    // Cambiar de profesor dispara un fetch nuevo antes de que el anterior
    // responda. Sin esta bandera, una respuesta tardía pisa el estado del
    // profesor actual (set incorrecto) o aplica el error de uno antiguo.
    let cancelled = false;
    setCargandoProfesor(true);
    setError(null);
    profesoresService
      .impartidas(profesorId)
      .then((as) => {
        if (cancelled) return;
        setImpartidas(new Set(as.map((a) => a.id)));
      })
      .catch(() => {
        if (cancelled) return;
        setError('No se pudieron cargar las asignaturas impartidas');
      })
      .finally(() => {
        if (cancelled) return;
        setCargandoProfesor(false);
      });
    return () => {
      cancelled = true;
    };
  }, [profesorId]);

  const toggle = async (asignaturaId: number) => {
    if (profesorId === null) return;
    const yaMarcada = impartidas.has(asignaturaId);
    // UI optimista: aplicar el cambio antes de la respuesta
    setImpartidas((prev) => {
      const next = new Set(prev);
      if (yaMarcada) next.delete(asignaturaId);
      else next.add(asignaturaId);
      return next;
    });
    setError(null);
    try {
      if (yaMarcada) {
        await profesoresService.desasignarImpartida(profesorId, asignaturaId);
      } else {
        await profesoresService.asignarImpartida(profesorId, asignaturaId);
      }
    } catch (err) {
      // Revertir
      setImpartidas((prev) => {
        const next = new Set(prev);
        if (yaMarcada) next.add(asignaturaId);
        else next.delete(asignaturaId);
        return next;
      });
      const msg =
        isAxiosError(err) && err.response?.data?.detail
          ? String(err.response.data.detail)
          : 'No se pudo actualizar la asignación';
      setError(msg);
    }
  };

  return (
    <div className="page">
      <header className="page-header">
        <h1>Asignaciones profesor ↔ asignatura</h1>
      </header>

      {error && <div className="error">{error}</div>}

      {loading && <p>Cargando…</p>}

      {!loading && profesores.length === 0 && (
        <p style={{ color: '#6e6e73' }}>
          No hay profesores dados de alta todavía.
        </p>
      )}

      {!loading && profesores.length > 0 && (
        <>
          <div className="field" style={{ marginBottom: '1rem' }}>
            <label htmlFor="profesor">Profesor</label>
            <select
              id="profesor"
              value={profesorId ?? ''}
              onChange={(e) => setProfesorId(Number(e.target.value))}
            >
              {profesores.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.apellidos}, {p.nombre} ({p.username})
                </option>
              ))}
            </select>
          </div>

          {cargandoProfesor && <p>Cargando asignaciones del profesor…</p>}

          {!cargandoProfesor && asignaturas.length === 0 && (
            <p style={{ color: '#6e6e73' }}>
              No hay asignaturas en el catálogo todavía.
            </p>
          )}

          {!cargandoProfesor && asignaturas.length > 0 && (
            <table className="data-table">
              <thead>
                <tr>
                  <th style={{ width: '4rem' }}>Imparte</th>
                  <th>Código</th>
                  <th>Nombre</th>
                  <th>Grado</th>
                </tr>
              </thead>
              <tbody>
                {asignaturas.map((a) => (
                  <tr key={a.id}>
                    <td>
                      <input
                        type="checkbox"
                        checked={impartidas.has(a.id)}
                        onChange={() => toggle(a.id)}
                      />
                    </td>
                    <td>{a.codigo}</td>
                    <td>{a.nombre}</td>
                    <td>{a.grados.map((g) => g.codigo).join(', ')}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </>
      )}
    </div>
  );
};
