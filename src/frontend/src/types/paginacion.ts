export interface PaginaOut<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
}

export interface ErrorImportacion {
  archivo: string;
  fila: number;
  mensaje: string;
}

export interface InformeImportacionAlumnos {
  creados: number;
  actualizados: number;
  errores: ErrorImportacion[];
}

export interface InformeImportacionMatriculas {
  matriculas_creadas: number;
  asignaturas_matriculadas_creadas: number;
  errores: ErrorImportacion[];
}
