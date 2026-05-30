export type EstadoSolicitud =
  | 'pendiente'
  | 'en_revision'
  | 'aprobada'
  | 'rechazada'
  | 'anulada';

export const ESTADOS_TERMINALES: ReadonlySet<EstadoSolicitud> = new Set([
  'aprobada',
  'rechazada',
  'anulada',
]);

export interface AlumnoMin {
  id: number;
  username: string;
  nombre: string;
  apellidos: string;
}

export interface ResponsableMin {
  id: number;
  nombre: string;
  apellidos: string;
}

export interface SolicitudDispensa {
  id: number;
  alumno: AlumnoMin;
  asignatura: string;
  periodo: string;
  horario: string;
  motivo: string | null;
  estado: EstadoSolicitud;
  observaciones: string | null;
  fecha_solicitud: string;
  fecha_resolucion: string | null;
  responsable: ResponsableMin | null;
}

export interface CrearSolicitudRequest {
  asignatura: string;
  periodo: string;
  horario: string;
  motivo: string;
}

export interface EditarSolicitudRequest {
  estado?: EstadoSolicitud;
  motivo?: string;
  horario?: string;
  asignatura?: string;
  periodo?: string;
  observaciones?: string;
}
