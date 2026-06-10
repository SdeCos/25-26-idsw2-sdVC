import api from './api';
import type {
  CrearSesionClaseRequest,
  EditarSesionClaseRequest,
  SesionDeClase,
} from '../types/sesiones_clase';
import type { Asistencia, AsistenciaIn } from '../types/asistencias';

export const sesionesClaseService = {
  async listar(): Promise<SesionDeClase[]> {
    const { data } = await api.get<SesionDeClase[]>('/sesiones-clase');
    return data;
  },

  async obtener(id: number): Promise<SesionDeClase> {
    const { data } = await api.get<SesionDeClase>(`/sesiones-clase/${id}`);
    return data;
  },

  async crear(body: CrearSesionClaseRequest): Promise<SesionDeClase> {
    const { data } = await api.post<SesionDeClase>('/sesiones-clase', body);
    return data;
  },

  async actualizar(
    id: number,
    body: EditarSesionClaseRequest
  ): Promise<SesionDeClase> {
    const { data } = await api.patch<SesionDeClase>(
      `/sesiones-clase/${id}`,
      body
    );
    return data;
  },

  async listarAsistencias(sesionId: number): Promise<Asistencia[]> {
    const { data } = await api.get<Asistencia[]>(
      `/sesiones-clase/${sesionId}/asistencias`
    );
    return data;
  },

  async marcarAsistencia(
    sesionId: number,
    alumnoId: number,
    body: AsistenciaIn
  ): Promise<Asistencia> {
    const { data } = await api.put<Asistencia>(
      `/sesiones-clase/${sesionId}/asistencias/${alumnoId}`,
      body
    );
    return data;
  },
};
