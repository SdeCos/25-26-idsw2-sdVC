import api from './api';
import type {
  Asignatura,
  CrearAsignaturaRequest,
  EditarAsignaturaRequest,
} from '../types/asignaturas';

export const asignaturasService = {
  async listar(): Promise<Asignatura[]> {
    const { data } = await api.get<Asignatura[]>('/asignaturas');
    return data;
  },

  async crear(body: CrearAsignaturaRequest): Promise<Asignatura> {
    const { data } = await api.post<Asignatura>('/asignaturas', body);
    return data;
  },

  async actualizar(
    id: number,
    body: EditarAsignaturaRequest
  ): Promise<Asignatura> {
    const { data } = await api.patch<Asignatura>(`/asignaturas/${id}`, body);
    return data;
  },

  async eliminar(id: number): Promise<void> {
    await api.delete(`/asignaturas/${id}`);
  },
};
