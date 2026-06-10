import type { Asignatura } from './asignaturas';

export type EstadoSesionClase = 'abierta' | 'cerrada';

export interface ProfesorMin {
  id: number;
  nombre: string;
  apellidos: string;
}

export interface SesionDeClase {
  id: number;
  profesor: ProfesorMin;
  asignatura: Asignatura;
  grupo: string;
  aula: string;
  fecha: string; // ISO date
  hora_inicio: string; // HH:MM:SS
  hora_fin: string;
  tema: string;
  estado: EstadoSesionClase;
  fecha_creacion: string;
}

export interface CrearSesionClaseRequest {
  asignatura_id: number;
  grupo: string;
  aula: string;
  fecha: string;
  hora_inicio: string;
  hora_fin: string;
  tema: string;
}

export interface EditarSesionClaseRequest {
  fecha?: string;
  hora_inicio?: string;
  hora_fin?: string;
  aula?: string;
  tema?: string;
  estado?: EstadoSesionClase;
}
