import api from './api';
import type { Asignatura } from '../types/asignaturas';

export const asignaturasService = {
  async listar(): Promise<Asignatura[]> {
    const { data } = await api.get<Asignatura[]>('/asignaturas');
    return data;
  },
};
