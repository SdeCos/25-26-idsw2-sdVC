import api from './api';
import type { Asignatura } from '../types/asignaturas';
import type { UsuarioDetalle } from '../types/usuarios';

export const profesoresService = {
  async misAsignaturas(): Promise<Asignatura[]> {
    const { data } = await api.get<Asignatura[]>('/profesores/yo/asignaturas');
    return data;
  },

  async listar(): Promise<UsuarioDetalle[]> {
    const { data } = await api.get<UsuarioDetalle[]>('/profesores');
    return data;
  },

  async impartidas(profesorId: number): Promise<Asignatura[]> {
    const { data } = await api.get<Asignatura[]>(
      `/usuarios/${profesorId}/asignaturas-impartidas`
    );
    return data;
  },

  async asignarImpartida(profesorId: number, asignaturaId: number): Promise<void> {
    await api.post(
      `/usuarios/${profesorId}/asignaturas-impartidas/${asignaturaId}`
    );
  },

  async desasignarImpartida(
    profesorId: number,
    asignaturaId: number
  ): Promise<void> {
    await api.delete(
      `/usuarios/${profesorId}/asignaturas-impartidas/${asignaturaId}`
    );
  },
};
