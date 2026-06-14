export type EstadoAsistencia = 'presente' | 'ausente' | 'justificado';

export interface AlumnoEnAsistencia {
  id: number;
  username: string;
  nombre: string;
  apellidos: string;
}

export interface Asistencia {
  id: number;
  sesion_clase_id: number;
  alumno: AlumnoEnAsistencia;
  estado: EstadoAsistencia;
  justificacion: string | null;
  fecha_registro: string;
}

export interface AsistenciaIn {
  estado: EstadoAsistencia;
  justificacion?: string | null;
}
