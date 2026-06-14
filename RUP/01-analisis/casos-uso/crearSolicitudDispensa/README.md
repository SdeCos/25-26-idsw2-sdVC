# CGU > crearSolicitudDispensa > Análisis

> | [🏠️](/README.md) | [Análisis](/RUP/01-analisis/README.md) | [Detalle](/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Alumno/) | **Análisis** | Diseño | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Inception
- **Disciplina**: Análisis
- **Caso de uso**: `crearSolicitudDispensa()`
- **Actor**: Alumno
- **Versión**: 1.0
- **Fecha**: 2026-05-26

## propósito

Análisis del caso de uso `crearSolicitudDispensa()` mediante diagrama de colaboración MVC. El Alumno inicia el alta de una nueva `SolicitudDispensa` con los datos mínimos (asignatura, periodo, horario); la captura del motivo y la documentación adjunta se delega a `editarSolicitudDispensa()` vía `<<include>>`.

## diagrama de colaboración

<div align=center>

|![Análisis crearSolicitudDispensa()](/images/RUP/01-analisis/casos-uso/crearSolicitudDispensa/colaboracion.svg)|
|-|
|**Disciplina**: Análisis RUP<br>**Enfoque**: Diagramas de colaboración MVC|

</div>


[Código PlantUML](/modelosUML/RUP/01-analisis/casos-uso/crearSolicitudDispensa/colaboracion.puml)
## clases de análisis identificadas

### clases model (naranja #F2AC4E)

| Clase | Responsabilidad | Trazabilidad |
|-|-|-|
| **SolicitudDispensa** | Entidad de dominio que representa la dispensa solicitada por un Alumno (datos iniciales + motivo + adjuntos + estado) | Nueva entidad del análisis; emerge aquí por primera vez |
| **SolicitudDispensaRepository** | Persiste el alta resolviendo el `alumno` propietario | Nuevo Repository del análisis |

### clases view (azul #629EF9)

| Clase | Responsabilidad | Derivación |
|-|-|-|
| **CrearSolicitudDispensaView** | Formulario inicial: asignatura, periodo, horario | Sin prototipo SALT específico — derivada del estado `FormularioEdicion` del [detallado](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Alumno/crearSolicitudDispensa.puml) |

### clases controller (verde #b5bd68)

| Clase | Responsabilidad | Casos de uso |
|-|-|-|
| **SolicitudDispensaController** | Orquestación del CRUD individual de `SolicitudDispensa`: validación, alta, carga, modificación | Compartido entre los 3 CUs del Alumno (crear/consultar/editar). Análogo a `UsuarioController` del bloque Administrador |

### colaboraciones (verde claro #CDEBA5)

| Colaboración | Propósito | Invocación |
|-|-|-|
| **:Dispensas Abierto** | Estado de origen (listado de dispensas del alumno desde el que se invoca el alta) | Punto de entrada del caso de uso |
| **:Collaboration EditarSolicitudDispensa** | Sub-colaboración a la que se delega la carga de motivo y documentación tras crear el registro | Vía `<<include>>` al final del flujo |

## mensajes de colaboración

### flujo principal

| # | Origen | Destino | Mensaje | Intención |
|-|-|-|-|-|
| 1 | **:Dispensas Abierto** | **CrearSolicitudDispensaView** | `crearSolicitudDispensa()` | Abrir el formulario de alta |
| 2 | **CrearSolicitudDispensaView** | **SolicitudDispensaController** | `validarDatosIniciales(asignatura, periodo, horario) : boolean` | Comprobar que los datos mínimos están presentes y son consistentes |
| 3 | **CrearSolicitudDispensaView** | **SolicitudDispensaController** | `crearSolicitudDispensa(asignatura, periodo, horario) : SolicitudDispensa` | Solicitar el alta |
| 4 | **SolicitudDispensaController** | **SolicitudDispensaRepository** | `crear(alumno, asignatura, periodo, horario) : SolicitudDispensa` | Persistir el alta enlazando al Alumno propietario |
| 5 | **CrearSolicitudDispensaView** | **:Collaboration EditarSolicitudDispensa** | `<<include>> editarSolicitudDispensa(solicitudNueva)` | Continuar con motivo y adjuntos |

### flujo alternativo — cerrar sin guardar

El detallado contempla `cerrarSolicitudDispensa()` como salida sin persistir. En el análisis equivale a no llegar al mensaje 3: la `CrearSolicitudDispensaView` se cierra y se vuelve a `:Dispensas Abierto` sin invocar al Controller. No requiere clase adicional.

## enlaces de dependencia

- **CrearSolicitudDispensaView** conoce a **SolicitudDispensaController** (delegación)
- **CrearSolicitudDispensaView** conoce a **:Collaboration EditarSolicitudDispensa** (transición/inclusión)
- **SolicitudDispensaController** conoce a **SolicitudDispensaRepository** (persistencia)
- **SolicitudDispensaController** conoce a **SolicitudDispensa** (manipulación entidad)
- **SolicitudDispensaRepository** conoce a **SolicitudDispensa** (gestión de la entidad)

## resolución implícita del Alumno propietario

El mensaje 3 envía 3 parámetros (`asignatura, periodo, horario`), pero el mensaje 4 envía 4 (`alumno, asignatura, periodo, horario`). El `SolicitudDispensaController` resuelve el `alumno` propietario consultando la `Sesion` activa (creada en [[iniciarSesion]]). Esto es deliberado:

- La vista **no recibe** el alumno como input — sería redundante y abriría una vulnerabilidad de suplantación si fuera modificable desde el cliente.
- El Controller **es quien sabe** quién está autenticado vía Sesion.
- La instancia de `Usuario` recuperada por `Sesion` es polimórficamente un `Alumno` (de la jerarquía analizada en [[iniciarSesion]]).

Cómo se realiza esa lectura de la sesión (inyección, contexto del request, …) es una decisión de diseño. En análisis basta con que el contrato del Controller deje claro que el `alumno` no es input externo.

## sin polimorfismo (asimetría con crearUsuario)

A diferencia de [[crearUsuario]], `crearSolicitudDispensa` **no tiene parámetro `tipo`** ni despacho polimórfico en `crear(…)`. Razón: `SolicitudDispensa` es una entidad concreta sin jerarquía de subtipos — todas las dispensas comparten estructura. El estado (pendiente/aprobada/rechazada) es un atributo, no un subtipo.

Este es el patrón **típico CRUD del proyecto**. El polimorfismo de `crearUsuario` fue el caso excepcional, justificado por la jerarquía de actores.

## trazabilidad con artefactos previos

### con especificación detallada

- **Estado `DISPENSAS_ABIERTO`** → **colaboración `:Dispensas Abierto`** (origen)
- **Estado compuesto `SOLICITUD_DISPENSA_ABIERTA` con `FormularioEdicion` ("Edición de Dispensa")** → **`CrearSolicitudDispensaView` + `<<include>> editarSolicitudDispensa()`**
- **Transición `guardarSolicitudDispensa()`** → **mensaje 4 `crear(…)`** (la persistencia efectiva)
- **Transición `cerrarSolicitudDispensa()`** → flujo alternativo

### sin wireframe (prototipo SALT) propio

- No hay prototipo específico de `crearSolicitudDispensa` en el requisitado. La `CrearSolicitudDispensaView` se deriva del estado `FormularioEdicion` del detallado. Los prototipos `guardarSolicitudDispensaAlumno1/2.png` y `editarSolicitudDispensaAlumno.png` representan el flujo continuo crear→editar→guardar.

### con actores

- **`Alumno --> CrearSolicitudDispensa`** en [`Alumno.puml`](/modelosUML/RUP/00-requisitos/CasosDeUso/CasoDeUso/Alumno/Alumno.puml) → invocación del CU desde el actor (implícita en la colaboración `:Dispensas Abierto`)
- **Alumno como subclase de `Usuario`** (jerarquía de [[iniciarSesion]]) → habilita la resolución implícita del propietario vía Sesion

### con modelo del dominio

- **Sin trazabilidad directa**: `SolicitudDispensa` no aparece en `ModeloCompleto.puml`. Misma deuda que con `Usuario` — emerge en análisis. A diferencia de `Usuario`, `SolicitudDispensa` es **claramente entidad de dominio** (no infraestructura), por lo que su promoción al modelo en 02-diseño es más directa.

## principios de análisis aplicados

### patrón mvc

- **Controller por entidad**: `SolicitudDispensaController` reutilizado en los 3 CUs del Alumno (mismo patrón que `UsuarioController` en el Admin)
- **Vista específica por CU**: `CrearSolicitudDispensaView` se diferencia de `ConsultarSolicitudDispensaView` / `EditarSolicitudDispensaView`
- **Sin polimorfismo**: entidad concreta, sin jerarquía

### diagramas de colaboración

- **Foco en enlaces**: dependencias conceptuales, no secuencia temporal
- **`<<include>>` explícito**: la delegación a `editarSolicitudDispensa()` está modelada como dependencia entre colaboraciones
- **Mensajes de intención**: `validarDatosIniciales`, `crear`, no detalles de implementación

### análisis puro

- **Sin tecnología**: `SolicitudDispensaRepository` es concepto, no implementación
- **Sin detalles de UI**: `CrearSolicitudDispensaView` es interfaz conceptual
- **Sin gestión de adjuntos**: el almacenamiento de documentación se deja al diseño

## características del análisis

### responsabilidades identificadas

- **CrearSolicitudDispensaView**: capturar datos iniciales y coordinar el flujo de alta
- **SolicitudDispensaController**: validar, resolver el alumno propietario, orquestar la persistencia
- **SolicitudDispensaRepository**: persistir el alta enlazando al Alumno
- **SolicitudDispensa**: representar la entidad creada

### relaciones conceptuales

- **Delegación**: vista delega lógica al controlador
- **Acceso**: controlador accede al repositorio para persistencia
- **Inclusión**: la vista incluye la colaboración `editarSolicitudDispensa()` para completar el alta
- **Resolución implícita**: el Controller resuelve el Alumno propietario vía Sesion (sin parámetro explícito)

## conexión con disciplinas rup

### desde requisitos

- **Detallado**: estado compuesto `SOLICITUD_DISPENSA_ABIERTA` con sub-actividad de edición → `<<include>> editarSolicitudDispensa()`
- **Actores**: Alumno subclase de Usuario → habilita la resolución del propietario vía Sesion

### hacia diseño

- Modelo de almacenamiento de adjuntos (filesystem, blob storage, BD)
- Estado inicial de la `SolicitudDispensa` (pendiente, borrador, …)
- Regla de unicidad: ¿puede un Alumno tener varias dispensas para la misma sesión? (no especificado en el requisitado)
- Validaciones de negocio sobre asignatura/periodo/horario (¿el Alumno está matriculado en esa asignatura?)
- Transaccionalidad del par `crear()` + `editarSolicitudDispensa(solicitudNueva)`
- Promoción de `SolicitudDispensa` al modelo del dominio (deuda compartida con el bloque Administrador para `Usuario`)

**Código fuente:** [colaboracion.puml](/modelosUML/RUP/01-analisis/casos-uso/crearSolicitudDispensa/colaboracion.puml)

## referencias

- [Detallado `crearSolicitudDispensa()`](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Alumno/crearSolicitudDispensa.puml)
- [Caso de uso del Alumno](/modelosUML/RUP/00-requisitos/CasosDeUso/CasoDeUso/Alumno/Alumno.puml)
- [Actores.puml](/modelosUML/RUP/00-requisitos/CasosDeUso/Actores/Actores.puml)
- [Análisis `crearUsuario()`](/RUP/01-analisis/casos-uso/crearUsuario/README.md)
- [Análisis `iniciarSesion()`](/RUP/01-analisis/casos-uso/iniciarSesion/README.md)
- [conversation-log.md](/conversation-log.md)
