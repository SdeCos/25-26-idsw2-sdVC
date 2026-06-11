import type { Grado } from './grados';

export type CaracterAsignatura = 'FB' | 'OB' | 'OP';

export interface Asignatura {
  id: number;
  codigo: string;
  nombre: string;
  ects: number;
  caracter: CaracterAsignatura;
  curso_plan: number;
  grados: Grado[];
}

export interface CrearAsignaturaRequest {
  codigo: string;
  nombre: string;
  ects: number;
  caracter: CaracterAsignatura;
  curso_plan: number;
  grado_ids: number[];
}

export interface EditarAsignaturaRequest {
  nombre?: string;
  ects?: number;
  caracter?: CaracterAsignatura;
  curso_plan?: number;
  grado_ids?: number[];
}
