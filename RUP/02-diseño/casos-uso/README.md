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
| [consultarListaAlumnos()](consultarListaAlumnos/README.md)                        | Profesor        | ✅     |
| [consultarDetalleAlumno()](consultarDetalleAlumno/README.md)                      | Profesor        | ✅     |
| [crearSesionClase()](crearSesionClase/README.md)                                  | Profesor        | ✅     |
| [editarSesionClase()](editarSesionClase/README.md)                                | Profesor        | ✅     |
| [registrarTomaAsistencia()](registrarTomaAsistencia/README.md)                    | Profesor        | ✅     |
| [cerrarSesionClase()](cerrarSesionClase/README.md)                                | Profesor        | ✅     |
| [exportarHistorialAsistencias()](exportarHistorialAsistencias/README.md)          | Profesor        | ✅     |
| [consultarSolicitudDispensa() (Profesor)](consultarSolicitudDispensaProfesor/README.md) | Profesor        | ✅     |
| [crearSolicitudDispensa() (Alumno)](crearSolicitudDispensa/README.md)             | Alumno          | ✅     |
| [editarSolicitudDispensa() (Alumno)](editarSolicitudDispensa/README.md)           | Alumno          | ✅     |
| [consultarSolicitudDispensa() (Alumno)](consultarSolicitudDispensa/README.md)     | Alumno          | ✅     |
| [consultarSolicitudesDispensas()](consultarSolicitudesDispensas/README.md)        | DirectorDeGrado | ✅     |
| [editarSolicitudDispensa() (Director)](editarSolicitudDispensaDirector/README.md) | DirectorDeGrado | ✅     |
| [consultarListaAlumnos() (Secretaria)](consultarListaAlumnosSecretaria/README.md) | Secretaria      | ✅     |
| [consultarDetalleMatricula()](consultarDetalleMatricula/README.md)                | Secretaria      | ✅     |
| [importarListasAlumnos()](importarListasAlumnos/README.md)                        | Secretaria      | ✅     |
| [importarMatriculas()](importarMatriculas/README.md)                              | Secretaria      | ✅     |
| [crearAlumno()](crearAlumno/README.md)                                            | Secretaria      | ✅     |
| [crearSolicitudDispensa() (Secretaria)](crearSolicitudDispensaSecretaria/README.md)         | Secretaria      | ✅     |
| [editarSolicitudDispensa() (Secretaria)](editarSolicitudDispensaSecretaria/README.md)       | Secretaria      | ✅     |
| [consultarSolicitudDispensa() (Secretaria)](consultarSolicitudDispensaSecretaria/README.md) | Secretaria      | ✅     |
| [exportarDispensas()](exportarDispensas/README.md)                                          | Secretaria      | ✅     |
| [gestionarCatalogoGrados()](gestionarCatalogoGrados/README.md)                              | Secretaria      | ✅     |
| [gestionarCatalogoAsignaturas()](gestionarCatalogoAsignaturas/README.md)                    | Secretaria      | ✅     |
| [asignarAsignaturasAProfesor()](asignarAsignaturasAProfesor/README.md)                      | Secretaria      | ✅     |

**Progreso:** 30/30 ✅
