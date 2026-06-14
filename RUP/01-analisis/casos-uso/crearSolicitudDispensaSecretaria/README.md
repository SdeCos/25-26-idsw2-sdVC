# CGU > crearSolicitudDispensa (Secretaria) > Análisis

> | [🏠️](/README.md) | [Análisis](/RUP/01-analisis/README.md) | [Detalle](/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Secretaria/) | **Análisis** | Diseño | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Inception
- **Disciplina**: Análisis
- **Caso de uso**: `crearSolicitudDispensa()` (Secretaria)
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-05-28

## propósito

Análisis del caso de uso `crearSolicitudDispensa()` desde el rol Secretaria mediante diagrama de colaboración MVC. La Secretaria da de alta una `SolicitudDispensa` **en nombre de** un Alumno (no la suya propia). La captura del motivo y la documentación se delega a `editarSolicitudDispensa()` (Secretaria) vía `<<include>>`.

Es la **cuarta y última pieza** del polimorfismo del Controller sobre `SolicitudDispensa`, cerrando la tetrada de roles que operan sobre la misma entidad con políticas distintas.

## diagrama de colaboración

<div align=center>

|![Análisis crearSolicitudDispensa() (Secretaria)](/images/RUP/01-analisis/casos-uso/crearSolicitudDispensaSecretaria/colaboracion.svg)|
|-|
|**Disciplina**: Análisis RUP<br>**Enfoque**: Diagramas de colaboración MVC|

</div>


[Código PlantUML](/modelosUML/RUP/01-analisis/casos-uso/crearSolicitudDispensaSecretaria/colaboracion.puml)
## por qué un análisis separado del Alumno

Aunque el detallado de Secretaria [`crearSolicitudDispensa.puml`](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Secretaria/crearSolicitudDispensa.puml) es **idéntico en estructura** al del Alumno (mismos sub-estados `CapturaDatos → ValidarDatos → CreacionExitosa`), la **semántica es distinta**: la Secretaria no es la dueña del dato. El folder con sufijo `Secretaria` evita la colisión de nombre canónico con [[crearSolicitudDispensa]] del Alumno, y registra explícitamente las cuatro diferencias clave:

| # | Aspecto | Alumno | Secretaria |
|-|-|-|-|
| 1 | Propietario | Resuelto **implícitamente** desde `Sesion.usuario` | **Input explícito** en la vista (selector de Alumno) |
| 2 | Vista | `CrearSolicitudDispensaView` | `CrearSolicitudDispensaSecretariaView` (con selector de Alumno) |
| 3 | Auditoría | Sin campo de auditoría adicional | `responsable = Sesion.usuario` (Secretaria que da de alta) como side effect del Controller |
| 4 | Política del Controller | Solo si `Sesion.usuario` coincide con el `alumno` | **Sin restricción de propiedad** — la Secretaria puede crear para cualquier Alumno |

Mismo Repository (`SolicitudDispensaRepository.crear(...)` con misma firma) — coherente con el patrón ya consolidado en [[consultarSolicitudesDispensas]] y [[editarSolicitudDispensaDirector]]: **el Repository es agnóstico al rol**, las políticas de acceso viven en el Controller.

## clases de análisis identificadas

### clases model (naranja #F2AC4E)

| Clase | Responsabilidad | Trazabilidad |
|-|-|-|
| **SolicitudDispensa** | Entidad de dominio reutilizada | Debuta en [[crearSolicitudDispensa]] (Alumno) |
| **SolicitudDispensaRepository** | Persiste el alta enlazando al `alumno` propietario (input externo en este CU) | Reutilizado; misma firma `crear(alumno, asignatura, periodo, horario)` que en el bloque Alumno |

### clases view (azul #629EF9)

| Clase | Responsabilidad | Derivación |
|-|-|-|
| **CrearSolicitudDispensaSecretariaView** | Formulario inicial con **selector de Alumno** + asignatura + periodo + horario | Prototipo SALT [`guardarSolicitudDispensaSecretaria.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Secretaria/guardarSolicitudDispensaSecretaria.png) (refleja el flujo continuo crear→editar→guardar desde el rol Secretaria) |

### clases controller (verde #b5bd68)

| Clase | Responsabilidad | Casos de uso |
|-|-|-|
| **SolicitudDispensaController** | Orquestación del alta resolviendo `responsable` desde `Sesion.usuario` (la Secretaria); sin restricción de propiedad sobre `alumno` (input externo) | Reutilizado del bloque Alumno; estrena variante `crearSolicitudDispensaEnNombreDe(...)` distinta del `crearSolicitudDispensa(...)` original |

### colaboraciones (verde claro #CDEBA5)

| Colaboración | Propósito | Invocación |
|-|-|-|
| **:Dispensas Abierto** | Estado de origen — listado de dispensas (la Secretaria ve todas) | Punto de entrada |
| **:Collaboration EditarSolicitudDispensaSecretaria** | Sub-colaboración a la que se delega la carga de motivo y documentación tras crear el registro | Vía `<<include>>` al final del flujo |

## mensajes de colaboración

### flujo principal

| # | Origen | Destino | Mensaje | Intención |
|-|-|-|-|-|
| 1 | **:Dispensas Abierto** | **CrearSolicitudDispensaSecretariaView** | `crearSolicitudDispensa()` | Abrir el formulario de alta |
| 2 | **CrearSolicitudDispensaSecretariaView** | **SolicitudDispensaController** | `validarDatosIniciales(alumno, asignatura, periodo, horario) : boolean` | Validar incluyendo el Alumno (debe existir en `AlumnoRepository`) |
| 3 | **CrearSolicitudDispensaSecretariaView** | **SolicitudDispensaController** | `crearSolicitudDispensaEnNombreDe(alumno, asignatura, periodo, horario) : SolicitudDispensa` | Solicitar el alta para el Alumno indicado |
| 4 | **SolicitudDispensaController** | **SolicitudDispensaRepository** | `crear(alumno, asignatura, periodo, horario) : SolicitudDispensa` | Persistir el alta — misma firma que el bloque Alumno |
| 5 | **CrearSolicitudDispensaSecretariaView** | **:Collaboration EditarSolicitudDispensaSecretaria** | `<<include>> editarSolicitudDispensa(solicitudNueva)` | Continuar con motivo y adjuntos |

### flujo alternativo — error de validación

Si el Alumno indicado no existe (input no resuelve en `AlumnoRepository`), el mensaje 2 retorna `false` y la vista informa el error sin invocar al Controller para el alta. El detallado lo modela como transición `ValidarDatos -[#red]-> CapturaDatos`.

### flujo alternativo — cerrar sin guardar

El detallado contempla `cerrarSolicitudDispensa()` como salida sin persistir. Equivale a no llegar al mensaje 3.

## el `alumno` propietario es input externo, no input implícito — asimetría clave

En todos los CUs analizados hasta ahora con propietario, el propietario se resolvía **implícitamente** desde `Sesion.usuario`:

| CU | Propietario | Fuente |
|-|-|-|
| [[crearSolicitudDispensa]] (Alumno) | `alumno` | `Sesion.usuario` |
| [[crearSesionClase]] (Profesor) | `profesor` | `Sesion.usuario` |
| [[importarMatriculas]] (Secretaria) | `responsable` (auditoría) | `Sesion.usuario` |

En este CU, la regla **se rompe deliberadamente** porque la Secretaria opera **sobre un tercero**:

- El `alumno` viene de la vista (selector explícito) — la Secretaria elige a quién.
- `responsable` (Sesion.usuario = Secretaria) se auto-popula igual que antes — como **auditoría**, no como propietario.

Estos dos campos representan **dos relaciones distintas** de la `SolicitudDispensa`:
- `alumno` → titular de la dispensa (visible en la ficha)
- `responsable` → quién registró el alta (campo de auditoría)

Cuando el Alumno crea la suya, ambos campos apuntan a la misma persona. Cuando la Secretaria la crea en su nombre, divergen. **Deuda para diseño**: confirmar si `responsable` se persiste explícitamente o se infiere de un log de auditoría externo.

## cuarta política del polimorfismo del Controller — cierre de la tetrada

Con este CU se cierra la caracterización polimórfica del `SolicitudDispensaController` por subtipo de `Sesion.usuario`:

| Rol | Política sobre `SolicitudDispensa` |
|-|-|
| **Alumno** | Crea/edita/consulta solo las **propias** (propietario implícito) |
| **Profesor** | Consulta las de **sus asignaturas impartidas** (read-only) |
| **DirectorDeGrado** | Consulta **todas**; edita el veredicto |
| **Secretaria** | Crea/edita/consulta **cualquiera, en nombre de cualquier Alumno** |

La opción **"métodos específicos por rol"** (camino abierto en [[consultarSolicitudesDispensas]] y reforzado en [[editarSolicitudDispensaDirector]] y [[consultarSolicitudDispensaProfesor]]) se ratifica como la más limpia. El método `crearSolicitudDispensaEnNombreDe` es **deliberadamente distinto** de `crearSolicitudDispensa` para hacer explícita en la firma la diferencia semántica (delegación vs autoría propia).

**Deuda para 02-diseño**: con cuatro políticas caracterizadas, decidir si se modelan como (a) métodos distintos en el mismo Controller, (b) Controllers especializados que comparten un Service común, o (c) una Strategy `PoliticaAcceso` inyectada según el subtipo de `Sesion.usuario`. La opción (a) es la más fiel al análisis tal como está escrito.

## enlaces de dependencia

- **CrearSolicitudDispensaSecretariaView** conoce a **SolicitudDispensaController** (delegación)
- **CrearSolicitudDispensaSecretariaView** conoce a **:Collaboration EditarSolicitudDispensaSecretaria** (inclusión)
- **SolicitudDispensaController** conoce a **SolicitudDispensaRepository** (persistencia)
- **SolicitudDispensaController** conoce a **Sesion** (auditoría `responsable`; no dibujada)
- **SolicitudDispensaController** conoce a **AlumnoRepository** (validación de existencia del Alumno indicado; no dibujada — emerge en el mensaje 2 y se materializa en diseño)
- **SolicitudDispensaRepository** conoce a **SolicitudDispensa** (gestión)

## discrepancias en el requisitado

| # | Tipo | Detalle | Decisión |
|-|-|-|-|
| 1 | Notas del detallado | Las notas dicen "**Alumno solicita...**" en el detallado de Secretaria (probable copia-pega del bloque Alumno) | Documentado como deuda menor — no afecta el modelado. Ya registrada en [[importarMatriculas]] |
| 2 | Sin prototipo SALT propio del modal inicial | El prototipo `guardarSolicitudDispensaSecretaria.png` muestra el flujo completo (crear→editar→guardar), no un wireframe del formulario mínimo de alta | La vista del análisis se deriva del estado `CapturaDatos` del detallado |
| 3 | Selector de Alumno no explícito en el detallado | La nota del detallado lista "Nombre/ID, asignatura, motivo, documentos y fechas" — implica que el Alumno se identifica por Nombre o ID, pero no detalla si es selector o input libre | Análisis adopta **selector contra `AlumnoRepository`** (autocompletado / búsqueda) por consistencia con la regla de validación. Deuda para diseño |

## sin polimorfismo en la entidad (heredado del bloque Alumno)

Como en [[crearSolicitudDispensa]] (Alumno), `SolicitudDispensa` es entidad concreta sin jerarquía. El método `crear(alumno, ...)` del Repository no recibe `tipo`. El polimorfismo del proyecto vive **en el Controller** (por subtipo de `Sesion.usuario`), no en la entidad.

## trazabilidad con artefactos previos

### con especificación detallada

- **Estado `DISPENSAS_ABIERTO`** → colaboración `:Dispensas Abierto` (origen)
- **Estado compuesto `SOLICITUD_DISPENSA_NUEVA` con sub-actividad de edición** → `CrearSolicitudDispensaSecretariaView` + `<<include>> editarSolicitudDispensa()`
- **Sub-estado `CapturaDatos` con nota "Nombre/ID, asignatura, motivo, documentos y fechas"** → parámetros del mensaje 2 (la nota confirma que el Alumno es input de la vista)
- **Transición `editarSolicitudDispensa()` del detallado** → mensaje 5 (`<<include>>`)
- **Transición `cerrarSolicitudDispensa()` del detallado** → flujo alternativo "cerrar sin guardar"

### con wireframe (prototipo SALT)

- **`guardarSolicitudDispensaSecretaria.png`** → vista de la solicitud con datos cargados — refleja la fase posterior al `<<include>>` editarSolicitudDispensa. La vista del análisis (`CrearSolicitudDispensaSecretariaView`) recoge los datos iniciales antes de esa pantalla

### con actores

- **`SecretariaAcademica --> crearSolicitudDispensa()`** en package "Dispensas" del [`DiagramaCompletoCasoDeUso.puml`](/modelosUML/RUP/00-requisitos/CasosDeUso/CasoDeUso/Secretaria/DiagramaCompletoCasoDeUso.puml) → invocación del CU
- **Secretaria como subclase de `Usuario`** (jerarquía de [[iniciarSesion]]) → habilita la resolución de `responsable` vía Sesion

### con modelo del dominio

- **Sin trazabilidad directa**: `SolicitudDispensa` no aparece en `ModeloCompleto.puml` (deuda heredada del bloque Alumno). Ahora con cuatro roles operando sobre ella, la urgencia de promoverla al modelo es máxima

## comparación con los otros `crear` del proyecto

| CU | Propietario | Auditoría | Política del Controller | Polimorfismo de entidad |
|-|-|-|-|-|
| [[crearUsuario]] (Admin) | N/A (entidad sin propietario) | Implícita | Admin único | **Sí** (`tipo` en `crear`) |
| [[crearSolicitudDispensa]] (Alumno) | Implícito desde `Sesion` | Implícita | Verificación de propiedad | No |
| [[crearSesionClase]] (Profesor) | Implícito desde `Sesion` | Implícita | "Profesor competente" | No |
| **`crearSolicitudDispensa` (Secretaria)** | **Input externo** | **`responsable` desde `Sesion`** | **Sin restricción** | No |
| [[importarMatriculas]] (Secretaria) | N/A (carga masiva) | `fechaImportacion`, `responsable` | Sin restricción | No |

**Conclusión**: la Secretaria es el primer rol que rompe el patrón "propietario implícito" — natural porque su trabajo es operar sobre datos de terceros.

## principios de análisis aplicados

### patrón mvc

- **Controller por entidad reutilizado**: `SolicitudDispensaController` con un método nuevo (`crearSolicitudDispensaEnNombreDe`) — refuerza el patrón "Controller por entidad" + "métodos por rol"
- **Vista específica por rol**: `CrearSolicitudDispensaSecretariaView` distinta de `CrearSolicitudDispensaView` (Alumno) por el selector de Alumno
- **Repository compartido sin cambios**

### diagramas de colaboración

- **`<<include>>` explícito** a la sub-colaboración `:Collaboration EditarSolicitudDispensaSecretaria`
- **Mensajes de intención**: `crearSolicitudDispensaEnNombreDe` denota explícitamente la semántica delegada
- **Selector de Alumno** como dependencia conceptual (no dibujada como `AlumnoRepository` para no sobrecargar el diagrama; documentada en "enlaces de dependencia")

### análisis puro

- **Sin política de notificación**: ¿se notifica al Alumno cuando la Secretaria da de alta una dispensa en su nombre? — deuda para diseño
- **Sin validación de adjuntos** o documentación obligatoria — pertenece al editar
- **Sin gestión de borrador** intermedio

## características del análisis

### responsabilidades identificadas

- **CrearSolicitudDispensaSecretariaView**: capturar datos iniciales **incluyendo selector de Alumno**, coordinar el flujo de alta
- **SolicitudDispensaController**: validar (incluida existencia del Alumno), resolver `responsable`, orquestar la persistencia, **sin restricción de propiedad**
- **SolicitudDispensaRepository**: persistir (sin cambios respecto al bloque Alumno)
- **SolicitudDispensa**: entidad creada (con `alumno` y `responsable` posiblemente divergentes)

### relaciones conceptuales

- **Delegación**: vista → Controller → Repository (cadena estándar)
- **Inclusión**: vista incluye la colaboración `editarSolicitudDispensa()` (Secretaria) para completar el alta
- **Auto-poblado de auditoría**: `responsable` desde Sesion como side effect del Controller (no input)
- **Input externo de propietario**: `alumno` desde la vista, validado contra `AlumnoRepository`

## conexión con disciplinas rup

### desde requisitos

- **Detallado**: estado compuesto idéntico al del Alumno → mismo flujo, distinta semántica
- **Actores**: `SecretariaAcademica --> crearSolicitudDispensa()` en package "Dispensas"
- **Jerarquía de actores**: Secretaria subclase de Usuario → habilita resolución de `responsable` vía Sesion

### hacia diseño

- **Persistir `responsable`** como campo explícito de `SolicitudDispensa` o vía log de auditoría externo
- **Política de notificación al Alumno** cuando un tercero (Secretaria) da de alta en su nombre
- **Selector de Alumno**: autocompletado, búsqueda por nombre/documento, paginación
- **Política de unicidad** (¿la Secretaria puede crear duplicados para el mismo Alumno/asignatura/periodo?)
- **Materialización del polimorfismo del Controller** (a/b/c documentado arriba) — decisión central tras cerrar la tetrada
- **Promoción de `SolicitudDispensa` al modelo del dominio** (deuda máxima ya con cuatro roles)
- **Reconciliación del actor `SecretariaAcademica` ↔ `Secretaria`** (deuda registrada desde [[importarMatriculas]])

**Código fuente:** [colaboracion.puml](/modelosUML/RUP/01-analisis/casos-uso/crearSolicitudDispensaSecretaria/colaboracion.puml)

## referencias

- [Detallado `crearSolicitudDispensa()` (Secretaria)](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Secretaria/crearSolicitudDispensa.puml)
- [Prototipo SALT `guardarSolicitudDispensaSecretaria.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Secretaria/guardarSolicitudDispensaSecretaria.png)
- [Caso de uso de Secretaria](/modelosUML/RUP/00-requisitos/CasosDeUso/CasoDeUso/Secretaria/DiagramaCompletoCasoDeUso.puml)
- [Análisis `crearSolicitudDispensa()` (Alumno) — análogo del rol Alumno](/RUP/01-analisis/casos-uso/crearSolicitudDispensa/README.md)
- [Análisis `consultarSolicitudesDispensas()` (Director) — política sin restricción](/RUP/01-analisis/casos-uso/consultarSolicitudesDispensas/README.md)
- [Análisis `consultarSolicitudDispensa()` (Profesor) — política "Profesor competente"](/RUP/01-analisis/casos-uso/consultarSolicitudDispensaProfesor/README.md)
- [conversation-log.md](/conversation-log.md)
