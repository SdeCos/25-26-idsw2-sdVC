import type { Grado } from './grados';

export interface Asignatura {
  id: number;
  codigo: string;
  nombre: string;
  ects: number;
  caracter: 'OB' | 'OP' | 'FB';
  curso_plan: number;
  grado: Grado;
}
