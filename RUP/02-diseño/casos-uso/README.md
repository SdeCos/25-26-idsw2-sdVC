# Diseño — Casos de uso

Diagramas de secuencia por caso de uso. Cada CU lleva los participantes concretos (componente React, endpoint FastAPI, servicio, repositorio, BD) y las decisiones de diseño que materializan el análisis.

## Estado

| Caso de uso                                                                       | Actor           | Diseño |
| --------------------------------------------------------------------------------- | --------------- | ------ |
| [iniciarSesion()](iniciarSesion/README.md)                                        | Usuario         | ✅     |
| [cerrarSesion()](cerrarSesion/README.md)                                          | Usuario         | ✅     |
| [crearUsuario()](crearUsuario/README.md)                                          | Administrador   | ✅     |
| [consultarUsuario()](consultarUsuario/README.md)                                  | Administrador   | ✅     |
| [editarUsuario()](editarUsuario/README.md)                                        | Administrador   | ✅     |
| consultarListaAlumnos()                                                           | Profesor        | ⏳     |
| consultarDetalleAlumno()                                                          | Profesor        | ⏳     |
| crearSesionClase()                                                                | Profesor        | ⏳     |
| editarSesionClase()                                                               | Profesor        | ⏳     |
| registrarTomaAsistencia()                                                         | Profesor        | ⏳     |
| cerrarSesionClase()                                                               | Profesor        | ⏳     |
| exportarHistorialAsistencias()                                                    | Profesor        | ⏳     |
| consultarSolicitudDispensa() (Profesor)                                           | Profesor        | ⏳     |
| [crearSolicitudDispensa() (Alumno)](crearSolicitudDispensa/README.md)             | Alumno          | ✅     |
| [editarSolicitudDispensa() (Alumno)](editarSolicitudDispensa/README.md)           | Alumno          | ✅     |
| [consultarSolicitudDispensa() (Alumno)](consultarSolicitudDispensa/README.md)     | Alumno          | ✅     |
| [consultarSolicitudesDispensas()](consultarSolicitudesDispensas/README.md)        | DirectorDeGrado | ✅     |
| [editarSolicitudDispensa() (Director)](editarSolicitudDispensaDirector/README.md) | DirectorDeGrado | ✅     |
| consultarListaAlumnos() (Secretaria)                                              | Secretaria      | ⏳     |
| consultarDetalleMatricula()                                                       | Secretaria      | ⏳     |
| importarListasAlumnos()                                                           | Secretaria      | ⏳     |
| importarMatriculas()                                                              | Secretaria      | ⏳     |
| crearSolicitudDispensa() (Secretaria)                                             | Secretaria      | ⏳     |
| editarSolicitudDispensa() (Secretaria)                                            | Secretaria      | ⏳     |
| consultarSolicitudDispensa() (Secretaria)                                         | Secretaria      | ⏳     |
| exportarDispensas()                                                               | Secretaria      | ⏳     |

**Progreso:** 10/26
