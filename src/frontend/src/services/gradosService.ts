import api from './api';
import type { CrearGradoRequest, EditarGradoRequest, Grado } from '../types/grados';

export const gradosService = {
  async listar(): Promise<Grado[]> {
    const { data } = await api.get<Grado[]>('/grados');
    return data;
  },

  async crear(body: CrearGradoRequest): Promise<Grado> {
    const { data } = await api.post<Grado>('/grados', body);
    return data;
  },

  async actualizar(id: number, body: EditarGradoRequest): Promise<Grado> {
    const { data } = await api.patch<Grado>(`/grados/${id}`, body);
    return data;
  },

  async eliminar(id: number): Promise<void> {
    await api.delete(`/grados/${id}`);
  },
};
