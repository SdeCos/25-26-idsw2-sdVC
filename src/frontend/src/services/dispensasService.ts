import api from './api';
import type {
  CrearSolicitudRequest,
  EditarSolicitudRequest,
  FiltrosDispensa,
  SolicitudDispensa,
} from '../types/dispensas';

export const dispensasService = {
  async listar(params: { alumno_id?: number } = {}): Promise<SolicitudDispensa[]> {
    const { data } = await api.get<SolicitudDispensa[]>('/dispensas', {
      params,
    });
    return data;
  },

  async obtener(id: number): Promise<SolicitudDispensa> {
    const { data } = await api.get<SolicitudDispensa>(`/dispensas/${id}`);
    return data;
  },

  async crear(body: CrearSolicitudRequest): Promise<SolicitudDispensa> {
    const { data } = await api.post<SolicitudDispensa>('/dispensas', body);
    return data;
  },

  async actualizar(
    id: number,
    body: EditarSolicitudRequest
  ): Promise<SolicitudDispensa> {
    const { data } = await api.patch<SolicitudDispensa>(`/dispensas/${id}`, body);
    return data;
  },

  async exportar(filtros: FiltrosDispensa = {}): Promise<Blob> {
    const { data } = await api.get('/dispensas/exportar', {
      params: filtros,
      responseType: 'blob',
    });
    return data as Blob;
  },
};
