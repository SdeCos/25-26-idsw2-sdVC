import api from './api';
import type { Asignatura } from '../types/asignaturas';

export const profesoresService = {
  async misAsignaturas(): Promise<Asignatura[]> {
    const { data } = await api.get<Asignatura[]>('/profesores/yo/asignaturas');
    return data;
  },
};
