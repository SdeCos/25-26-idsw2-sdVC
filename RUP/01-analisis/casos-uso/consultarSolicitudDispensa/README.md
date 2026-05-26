# CGU > consultarSolicitudDispensa > Análisis

> | [🏠️](/README.md) | [Análisis](/RUP/01-analisis/README.md) | [Detalle](/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Alumno/) | **Análisis** | Diseño | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Inception
- **Disciplina**: Análisis
- **Caso de uso**: `consultarSolicitudDispensa()`
- **Actor**: Alumno
- **Versión**: 1.0
- **Fecha**: 2026-05-26

## propósito

Análisis del caso de uso `consultarSolicitudDispensa()` mediante diagrama de colaboración MVC. Es el CU **read-only** del CRUD del Alumno: visualiza la ficha completa de una de sus dispensas (datos, motivo, adjuntos, estado), con opción de saltar a [[editarSolicitudDispensa]] vía `<<include>>` si decide modificar.

## diagrama de colaboración

<div align=center>

|![Análisis consultarSolicitudDispensa()](./colaboracion.svg)|
|-|
|**Disciplina**: Análisis RUP<br>**Enfoque**: Diagramas de colaboración MVC|

</div>

## discrepancia en el requisitado

El archivo [`Alumno.puml`](/RUP/00-requisitos/CasosDeUso/CasoDeUso/Alumno/Alumno.puml) etiqueta este CU como **`consultarEstadoDispensa()`**, mientras que el detallado, los prototipos y el resto del requisitado lo nombran **`consultarSolicitudDispensa()`**. El análisis adopta el nombre del detallado (`consultarSolicitudDispensa`) como canónico, por dos razones:

1. **Mayoría de artefactos**: detallado (`.puml`), prototipos (`consultarSolicitudDispensaAlumno1/2.png`) y el índice del repositorio lo nombran así.
2. **Coherencia con DirectorDeGrado**: el Director tiene `ConsultarSolicitudesDispensas` (plural), que confirma que la entidad consultada es la `SolicitudDispensa` completa, no solo su atributo `estado`.

Posible explicación de la discrepancia: borrador inicial en `Alumno.puml` no actualizado al consolidar nombres. **Deuda para 02-diseño**: reconciliar (probablemente renombrar en `Alumno.puml`).

## clases de análisis identificadas

### clases model (naranja #F2AC4E)

| Clase | Responsabilidad | Trazabilidad |
|-|-|-|
| **SolicitudDispensa** | Entidad de dominio (operación read-only sobre ella) | Reutilizada de [[crearSolicitudDispensa]] y [[editarSolicitudDispensa]] |
| **SolicitudDispensaRepository** | Recupera la solicitud por id | Reutilizado; usa `obtenerPorId(id)` ya introducido en [[editarSolicitudDispensa]] |

### clases view (azul #629EF9)

| Clase | Responsabilidad | Derivación |
|-|-|-|
| **ConsultarSolicitudDispensaView** | Ficha de visualización (solo lectura) y punto de salto a edición | [Prototipos SALT `consultarSolicitudDispensaAlumno1.png` y `consultarSolicitudDispensaAlumno2.png`](/RUP/00-requisitos/CasosDeUso/Prototipos/Alumno/) |

### clases controller (verde #b5bd68)

| Clase | Responsabilidad | Casos de uso |
|-|-|-|
| **SolicitudDispensaController** | Orquestación del CRUD individual de `SolicitudDispensa` | Compartido entre los 3 CUs del Alumno (igual que en [[crearSolicitudDispensa]] y [[editarSolicitudDispensa]]) |

### colaboraciones (verde claro #CDEBA5)

| Colaboración | Propósito | Invocación |
|-|-|-|
| **:Dispensas Abierto** | Estado de origen (listado de dispensas del alumno) | Punto de entrada del caso de uso |
| **:Collaboration EditarSolicitudDispensa** | Sub-colaboración a la que se delega la modificación si el Alumno decide editar | Vía `<<include>>` desde la vista |

## mensajes de colaboración

### flujo principal

| # | Origen | Destino | Mensaje | Intención |
|-|-|-|-|-|
| 1 | **:Dispensas Abierto** | **ConsultarSolicitudDispensaView** | `consultarSolicitudDispensa(solicitudId)` | Abrir la ficha de la solicitud seleccionada |
| 2 | **ConsultarSolicitudDispensaView** | **SolicitudDispensaController** | `cargarSolicitud(solicitudId) : SolicitudDispensa` | Recuperar la instancia |
| 3 | **SolicitudDispensaController** | **SolicitudDispensaRepository** | `obtenerPorId(solicitudId) : SolicitudDispensa` | Consulta al repositorio |
| 4 | **ConsultarSolicitudDispensaView** | **:Collaboration EditarSolicitudDispensa** | `<<include>> editarSolicitudDispensa(solicitudId)` | Saltar a edición si el Alumno lo solicita |

### flujo alternativo — salir sin editar

El mensaje 4 es **opcional**: el Alumno puede cerrar la consulta sin invocar la edición (transición `cerrarSolicitudDispensa()` del detallado). En ese caso solo se ejecutan los mensajes 1-3 y la `ConsultarSolicitudDispensaView` se cierra volviendo a `:Dispensas Abierto`. Mismo patrón que [[consultarUsuario]].

## enlaces de dependencia

- **ConsultarSolicitudDispensaView** conoce a **SolicitudDispensaController** (delegación)
- **ConsultarSolicitudDispensaView** conoce a **:Collaboration EditarSolicitudDispensa** (transición/inclusión opcional)
- **SolicitudDispensaController** conoce a **SolicitudDispensaRepository** (lectura)
- **SolicitudDispensaController** conoce a **SolicitudDispensa** (manipulación entidad)
- **SolicitudDispensaRepository** conoce a **SolicitudDispensa** (gestión)

## verificación de propiedad (regla de seguridad)

Aunque la operación es read-only, **debe verificarse** que la `SolicitudDispensa` consultada pertenece al Alumno autenticado (resuelto vía `Sesion`). Un Alumno no debería poder consultar dispensas de otros, igual que no debería poder editarlas (ver [[editarSolicitudDispensa]]).

La verificación vive en el `SolicitudDispensaController` (en o tras el mensaje 3). Cómo se realiza es decisión de diseño. En análisis basta con declarar la regla.

Esta es **una asimetría con DirectorDeGrado**: el Director consultará las dispensas de **todos** los alumnos. La misma operación de Repository (`obtenerPorId`) se usa desde ambos roles, pero la regla de propiedad solo aplica al Alumno. Esto sugiere que la verificación no es responsabilidad del Repository sino del Controller (o de una capa de autorización superior).

## comparación con los otros CUs del bloque Alumno

| Característica | [[crearSolicitudDispensa]] | `consultarSolicitudDispensa` | [[editarSolicitudDispensa]] |
|-|-|-|-|
| Operaciones | Validación + escritura | Solo lectura | Lectura + escritura |
| Puntos de entrada | 1 (`:Dispensas Abierto`) | 1 (`:Dispensas Abierto`) | 3 (listado, consulta, post-crear) |
| Mensajes al Repository | `crear` | `obtenerPorId` | `obtenerPorId`, `actualizar` |
| `<<include>>` saliente | a `editar` (siempre) | a `editar` (opcional) | — |
| Verificación de propiedad | Por construcción (el Alumno se autorrellena) | Sí (regla de seguridad) | Sí (regla de seguridad) |

El bloque cierra con la **misma estructura que el de Administrador**: crear→editar (siempre), consultar→editar (opcional), editar como convergencia. Es la confirmación de que el patrón CRUD del proyecto es uniforme.

## trazabilidad con artefactos previos

### con especificación detallada

- **Estado `DISPENSAS_ABIERTO`** → **colaboración `:Dispensas Abierto`** (origen)
- **Estado `SolicitarEditarSolicitud`** ("Visualización y Edición") → **`ConsultarSolicitudDispensaView`** + mensajes 1-3 (carga read-only)
- **Nota "Alumno solicita modificar campos mediante `editarSolicitudDispensa()`"** → **mensaje 4** (`<<include>>` opcional a edición)
- **Transición `cerrarSolicitudDispensa()`** → flujo alternativo
- **Transición `guardarSolicitudDispensa()`** del detallado: **no aplica directamente** a consulta — solo cobra sentido si se entra a la edición

### con wireframe (prototipo SALT)

- **`consultarSolicitudDispensaAlumno1.png`** y **`consultarSolicitudDispensaAlumno2.png`** → **ConsultarSolicitudDispensaView** (dos pantallas: probablemente listado de dispensas + ficha detalle)

### con actores

- **`Alumno --> ConsultarEstadoDispensa`** en `Alumno.puml` → invocación del CU (discrepancia de nombre documentada arriba)

### con modelo del dominio

- **Sin trazabilidad directa**: deuda compartida con todo el bloque Alumno y Administrador.

## principios de análisis aplicados

### patrón mvc

- **Controller compartido por entidad**: `SolicitudDispensaController`
- **Vista específica por CU**: `ConsultarSolicitudDispensaView` es read-only
- **Sin polimorfismo**: entidad concreta

### diagramas de colaboración

- **CU mínimo**: 4 mensajes (el más compacto del bloque, igual que [[consultarUsuario]])
- **`<<include>>` opcional documentado en prosa**: el diagrama lo muestra como dependencia; la opcionalidad vive en el flujo alternativo

### análisis puro

- **Sin tecnología**: cómo se renderiza la ficha es decisión de diseño
- **Sin paginación**: el detallado no la menciona; emergerá si el volumen lo justifica

## características del análisis

### responsabilidades identificadas

- **ConsultarSolicitudDispensaView**: cargar y presentar la ficha; ofrecer salto a edición
- **SolicitudDispensaController**: mediar entre vista y repositorio; aplicar la regla de propiedad
- **SolicitudDispensaRepository**: recuperar la instancia
- **SolicitudDispensa**: representar la entidad consultada

### relaciones conceptuales

- **Delegación**: vista delega lógica al controlador
- **Lectura**: controlador accede al repositorio sin modificar
- **Inclusión opcional**: la vista puede invocar `editarSolicitudDispensa()` si el Alumno lo solicita

## conexión con disciplinas rup

### desde requisitos

- **Detallado**: `SolicitarEditarSolicitud` con nota a `editarSolicitudDispensa()` → mensaje 4 opcional
- **Prototipos SALT**: dos pantallas → `ConsultarSolicitudDispensaView`
- **Actores**: discrepancia de nombre con `Alumno.puml` (deuda de reconciliación)

### hacia diseño

- Reconciliar el nombre del CU en `Alumno.puml` (`consultarEstadoDispensa` → `consultarSolicitudDispensa`)
- Verificación de propiedad (compartida con [[editarSolicitudDispensa]])
- Decidir si el Alumno puede ver el `estado` de la dispensa en su ficha (pendiente/aprobada/rechazada/justificación del Director) — esto reconcilia el nombre `consultarEstadoDispensa` que el `Alumno.puml` sugería
- Paginación / búsqueda en el listado de dispensas del alumno (si el volumen crece)

**Código fuente:** [colaboracion.puml](colaboracion.puml)

## referencias

- [Detallado `consultarSolicitudDispensa()`](/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Alumno/consultarSolicitudDispensa.puml)
- [Prototipo SALT `consultarSolicitudDispensaAlumno1.png`](/RUP/00-requisitos/CasosDeUso/Prototipos/Alumno/consultarSolicitudDispensaAlumno1.png)
- [Prototipo SALT `consultarSolicitudDispensaAlumno2.png`](/RUP/00-requisitos/CasosDeUso/Prototipos/Alumno/consultarSolicitudDispensaAlumno2.png)
- [Caso de uso del Alumno](/RUP/00-requisitos/CasosDeUso/CasoDeUso/Alumno/Alumno.puml)
- [Análisis `crearSolicitudDispensa()`](/RUP/01-analisis/casos-uso/crearSolicitudDispensa/README.md)
- [Análisis `editarSolicitudDispensa()`](/RUP/01-analisis/casos-uso/editarSolicitudDispensa/README.md)
- [conversation-log.md](/conversation-log.md)
