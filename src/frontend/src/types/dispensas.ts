import type { Grado } from './grados';

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

export interface AsignaturaEmbed {
  id: number;
  codigo: string;
  nombre: string;
  ects: number;
  caracter: 'OB' | 'OP' | 'FB';
  curso_plan: number;
  grados: Grado[];
}

export interface AsignaturaMatriculadaEmbed {
  id: number;
  n_matricula: number;
  asignatura: AsignaturaEmbed;
}

export interface SolicitudDispensa {
  id: number;
  alumno: AlumnoMin;
  asignatura_matriculada: AsignaturaMatriculadaEmbed;
  motivo: string | null;
  estado: EstadoSolicitud;
  observaciones: string | null;
  fecha_solicitud: string;
  fecha_resolucion: string | null;
  responsable: ResponsableMin | null;
}

export interface CrearSolicitudRequest {
  alumno_id?: number;
  asignatura_matriculada_id: number;
  motivo: string;
}

export interface EditarSolicitudRequest {
  estado?: EstadoSolicitud;
  motivo?: string;
  asignatura_matriculada_id?: number;
  observaciones?: string;
}

export interface FiltrosDispensa {
  estado?: EstadoSolicitud;
  alumno_id?: number;
  desde?: string;
  hasta?: string;
}
