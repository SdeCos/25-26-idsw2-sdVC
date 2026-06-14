# CGU > editarSolicitudDispensa (Secretaria) > Análisis

> | [🏠️](/README.md) | [Análisis](/RUP/01-analisis/README.md) | [Detalle](/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Secretaria/) | **Análisis** | Diseño | Desarrollo |
> | ----------------- | -------------------------------------- | ------------------------------------------------------------------------ | ------------ | ------ | ---------- |

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Inception
- **Disciplina**: Análisis
- **Caso de uso**: `editarSolicitudDispensa()` (Secretaria)
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-05-28

## propósito

Análisis del caso de uso `editarSolicitudDispensa()` desde el rol Secretaria mediante diagrama de colaboración MVC. La Secretaria modifica los datos de una `SolicitudDispensa` **de cualquier Alumno** (sin restricción de propiedad). Es el **CU de convergencia del CRUD Secretaria**: tres puntos de entrada (`:Dispensas Abierto`, `:Collaboration ConsultarSolicitudDispensaSecretaria`, `:Collaboration CrearSolicitudDispensaSecretaria`) convergen en una única `EditarSolicitudDispensaSecretariaView`.

Calcado estructuralmente de [[editarSolicitudDispensa]] (Alumno) — la asimetría vive en el **Controller** (sin restricción de propiedad), no en el modelado de mensajes. Confirma la hipótesis del proyecto: **la política de acceso es transversal al patrón CRUD, no estructural**.

## diagrama de colaboración

<div align=center>

| ![Análisis editarSolicitudDispensa() (Secretaria)](/images/RUP/01-analisis/casos-uso/editarSolicitudDispensaSecretaria/colaboracion.svg)     |
| -------------------------------------------------------------------------- |
| **Disciplina**: Análisis RUP<br>**Enfoque**: Diagramas de colaboración MVC |

</div>


[Código PlantUML](/modelosUML/RUP/01-analisis/casos-uso/editarSolicitudDispensaSecretaria/colaboracion.puml)
## por qué un análisis separado del Alumno

Aunque la **estructura de mensajes es idéntica** al del Alumno (mismo Controller, mismo Repository, mismo flujo con 5 mensajes y 3 colaboraciones origen), las **tres diferencias semánticas** justifican folder/análisis aparte:

| #   | Aspecto                           | Alumno                                                           | Secretaria                                                                                                                                            |
| --- | --------------------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Política de acceso del Controller | Verificación de propiedad: `solicitud.alumno == Sesion.usuario`  | **Sin restricción** — la Secretaria puede editar cualquiera                                                                                           |
| 2   | Vista                             | `EditarSolicitudDispensaView`                                    | `EditarSolicitudDispensaSecretariaView` — refleja contexto de "actuando en nombre de" (puede mostrar el alumno titular como dato visible/no editable) |
| 3   | Colaboraciones origen             | `ConsultarSolicitudDispensa` + `CrearSolicitudDispensa` (Alumno) | `ConsultarSolicitudDispensaSecretaria` + `CrearSolicitudDispensaSecretaria`                                                                           |

Mismo Controller (`SolicitudDispensaController`) y mismo método (`modificarCampos`) — distinta política interna por subtipo de `Sesion.usuario`.

## por qué el mismo método `modificarCampos` y no `modificarCamposEnNombreDe`

A diferencia de [[crearSolicitudDispensaSecretaria]] — donde el método se llamó `crearSolicitudDispensaEnNombreDe` porque la **signatura difería** (`alumno` como input explícito vs implícito desde Sesion) — aquí la signatura es **idéntica** a la del Alumno: `modificarCampos(solicitudId, cambios) : boolean`. El `alumno` no es input (es invariante post-alta, no se edita), y `cambios` no cambia su estructura entre roles.

**Regla emergente del análisis**: el patrón "métodos específicos por rol" se aplica **solo cuando la signatura difiere**. Si solo la política varía con la misma signatura, un único método con dispatch interno por subtipo de `Sesion.usuario` es suficiente y más limpio.

Esto refina la deuda hacia diseño: de las tres opciones planteadas para materializar el polimorfismo del Controller ((a) métodos por rol, (b) Strategy `PoliticaAcceso`, (c) Controllers especializados), **la (b) gana fuerza** — la política es ortogonal al método y debería inyectarse.

## clases de análisis identificadas

### clases model (naranja #F2AC4E)

| Clase                           | Responsabilidad                | Trazabilidad                                                            |
| ------------------------------- | ------------------------------ | ----------------------------------------------------------------------- |
| **SolicitudDispensa**           | Entidad de dominio reutilizada | Reutilizada del bloque Alumno                                           |
| **SolicitudDispensaRepository** | Carga por ID y actualiza       | Reutilizado; mismos métodos `obtenerPorId` y `actualizar` que el Alumno |

### clases view (azul #629EF9)

| Clase                                     | Responsabilidad                                                                                                     | Derivación                                                                                                                                          |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **EditarSolicitudDispensaSecretariaView** | Formulario de edición con campos modificables (motivo, adjuntos) + alumno titular visible como contexto no editable | Prototipo SALT [`editarSolicitudDispensaSecretaria.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Secretaria/editarSolicitudDispensaSecretaria.png) |

### clases controller (verde #b5bd68)

| Clase                           | Responsabilidad                                                                                                    | Casos de uso                                                                                     |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| **SolicitudDispensaController** | Orquestación: cargar, validar, actualizar — **sin restricción de propiedad** cuando `Sesion.usuario` es Secretaria | Reutilizado; sexto y séptimo uso de los métodos `cargarSolicitudParaEdicion` y `modificarCampos` |

### colaboraciones (verde claro #CDEBA5)

| Colaboración                                            | Propósito                                                       | Invocación       |
| ------------------------------------------------------- | --------------------------------------------------------------- | ---------------- |
| **:Dispensas Abierto**                                  | Atajo de edición desde el listado (botón "Editar" en cada fila) | Punto de entrada |
| **:Collaboration ConsultarSolicitudDispensaSecretaria** | Lectura → edición (camino más natural en la UI)                 | Punto de entrada |
| **:Collaboration CrearSolicitudDispensaSecretaria**     | Continuación del alta (vía `<<include>>` del crear)             | Punto de entrada |

## mensajes de colaboración

### flujo principal

| #   | Origen                                                                           | Destino                                   | Mensaje                                                       | Intención                                  |
| --- | -------------------------------------------------------------------------------- | ----------------------------------------- | ------------------------------------------------------------- | ------------------------------------------ |
| 1   | **:Dispensas Abierto** / **:Collaboration ConsultarSolicitudDispensaSecretaria** | **EditarSolicitudDispensaSecretariaView** | `editarSolicitudDispensa(solicitudId)`                        | Abrir el formulario de edición             |
| 1'  | **:Collaboration CrearSolicitudDispensaSecretaria**                              | **EditarSolicitudDispensaSecretariaView** | `editarSolicitudDispensa(solicitudNueva)`                     | Continuar el alta (pre-cargada)            |
| 2   | **EditarSolicitudDispensaSecretariaView**                                        | **SolicitudDispensaController**           | `cargarSolicitudParaEdicion(solicitudId) : SolicitudDispensa` | Cargar datos para mostrar en el formulario |
| 3   | **SolicitudDispensaController**                                                  | **SolicitudDispensaRepository**           | `obtenerPorId(solicitudId) : SolicitudDispensa`               | Recuperar la entidad                       |
| 4   | **EditarSolicitudDispensaSecretariaView**                                        | **SolicitudDispensaController**           | `modificarCampos(solicitudId, cambios) : boolean`             | Solicitar persistencia de los cambios      |
| 5   | **SolicitudDispensaController**                                                  | **SolicitudDispensaRepository**           | `actualizar(solicitud) : boolean`                             | Persistir                                  |

### entrada desde crearSolicitudDispensaSecretaria

Cuando la entrada es desde `:Collaboration CrearSolicitudDispensaSecretaria` con `solicitudNueva`, la instancia ya está cargada en memoria y la vista **no necesita** invocar `cargarSolicitudParaEdicion` (mensajes 2-3 se omiten). Misma decisión que en [[editarSolicitudDispensa]] (Alumno) — documentada en prosa para no duplicar mensajes en el diagrama.

### flujo alternativo — error de validación

Si `modificarCampos` retorna `false` por validación fallida, el detallado modela `ValidarModificaciones -[#red]-> PermitirModificacion` — la vista informa el error y permite corregir sin invocar `actualizar`.

### flujo alternativo — cerrar sin guardar

El detallado contempla salida sin persistir (transición `SOLICITUD_DISPENSA_ABIERTA_FINAL` sin invocar `guardarSolicitudDispensa()`). Equivale a no llegar al mensaje 4.

## invariante: `alumno` no se edita

Como en [[editarSolicitudDispensa]] (Alumno) y por las mismas razones, el `alumno` titular **no es campo editable**. Se fija en el alta y permanece estable durante toda la vida de la `SolicitudDispensa`. La Secretaria puede modificar **cualquier** solicitud, pero no puede **transferir** una solicitud entre Alumnos cambiando el titular.

Razón conceptual: una `SolicitudDispensa` pertenece semánticamente a un Alumno; transferirla sería destruir una y crear otra. Si esa operación se necesitara en el futuro, debería modelarse como CU explícito (`reasignarSolicitudDispensa`), no como edición.

**Deuda para diseño**: bloquear el `alumno` post-alta (sin setter / validación de inmutabilidad).

## auditoría: `responsable` del editar

Análogo a [[crearSolicitudDispensaSecretaria]], cuando la Secretaria edita una solicitud su identidad debería quedar registrada como auditoría. Tres opciones:

| Opción | Comportamiento                                                                                        |
| ------ | ----------------------------------------------------------------------------------------------------- |
| A      | Sobreescribir `responsable` de la solicitud con la última Secretaria que la editó                     |
| B      | Añadir campo `ultimoEditor` distinto del `responsable` original (del alta)                            |
| C      | Log de auditoría externo a la entidad (eventos de dominio: `SolicitudDispensaEditada(quien, cuando)`) |

Análisis no decide — es regla de negocio para 02-diseño. Lo análogo en [[editarSolicitudDispensaDirector]] añadía `fechaResolucion` y `responsable` al cambiar el veredicto; aquí los cambios son a `motivo`/`adjuntos`, no al veredicto, por lo que la urgencia es menor.

## enlaces de dependencia

- **EditarSolicitudDispensaSecretariaView** conoce a **SolicitudDispensaController** (delegación)
- **SolicitudDispensaController** conoce a **SolicitudDispensaRepository** (lectura + escritura)
- **SolicitudDispensaController** conoce a **Sesion** (dispatch de política por subtipo; no dibujada)
- **SolicitudDispensaRepository** conoce a **SolicitudDispensa** (gestión)

## discrepancias en el requisitado

| #   | Tipo                                              | Detalle                                                                                                         | Decisión                                                                                                                                  |
| --- | ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Notas con actor incorrecto                        | El detallado dice "**Alumno solicita** editar/registrar/modificar..."                                           | Documentado como deuda menor — copia-pega del bloque Alumno (raíz común con todas las notas del bloque Secretaria)                        |
| 2   | Salida `guardarSolicitudDispensa()` del detallado | El detallado modela `EDICION_SOLICITUD_COMP -[#green]---> DISPENSAS_ABIERTO_FINAL : guardarSolicitudDispensa()` | Modelado como mensaje 4-5 del Controller-Repository. Coherente con el resto del proyecto: "guardar" es la persistencia, no un CU separado |

## comparación con [[editarSolicitudDispensa]] (Alumno)

| Aspecto                 | Alumno                    | Secretaria                       |
| ----------------------- | ------------------------- | -------------------------------- |
| Mensajes                | 5                         | 5                                |
| Colaboraciones origen   | 3                         | 3 (las correspondientes del rol) |
| Método del Controller   | `modificarCampos`         | **`modificarCampos`** (mismo)    |
| Política del Controller | Verificación de propiedad | Sin restricción                  |
| Campos editables        | motivo, adjuntos          | motivo, adjuntos (mismos)        |
| Vista                   | Form modal                | Form modal con titular visible   |
| Invariante `alumno`     | Sí                        | Sí                               |

**Estructura clonada, política distinta**. Es el caso de uso que **más fielmente** ilustra la separación analítica entre forma (mensajes, clases) y política (verificación interna del Controller).

## principios de análisis aplicados

### patrón mvc

- **Controller por entidad reutilizado** sin métodos nuevos — mismo `cargarSolicitudParaEdicion` y `modificarCampos`
- **Vista específica por rol**: `EditarSolicitudDispensaSecretariaView` distinta por contexto, no por mensajes
- **Repository agnóstico al rol**: confirmado por sexta vez consecutiva

### diagramas de colaboración

- **Múltiples puntos de entrada**: 3 colaboraciones origen (mirror de las del Alumno)
- **Mensajes condicionales en prosa**: entrada desde crear omite carga, igual que el Alumno

### análisis puro

- **Sin política de notificación al Alumno** cuando la Secretaria edita su solicitud — deuda
- **Sin distinción entre "edición correctiva" y "edición sustantiva"** — todas son `modificarCampos` a nivel análisis

## trazabilidad con artefactos previos

### con especificación detallada

- **`SOLICITUD_DISPENSA_ABIERTA_INICIAL`** → entrada desde `:Collaboration ConsultarSolicitudDispensaSecretaria` (consulta abierta)
- **`DISPENSAS_ABIERTO_INICIAL`** (implícita en la transición de entrada) → atajo desde `:Dispensas Abierto`
- **Estado compuesto `EDICION_SOLICITUD_COMP` con `PermitirModificacion → ValidarModificaciones`** → mensajes 2-5
- **Transición `ValidarModificaciones -[#red]-> PermitirModificacion`** → flujo alternativo "error de validación"
- **Transición `guardarSolicitudDispensa()` → `DISPENSAS_ABIERTO_FINAL`** → mensaje 4-5 (persistencia)
- **Transición de salida sin guardar** → flujo alternativo "cerrar sin guardar"

### con wireframe (prototipo SALT)

- **[`editarSolicitudDispensaSecretaria.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Secretaria/editarSolicitudDispensaSecretaria.png)** → formulario con campos editables → `EditarSolicitudDispensaSecretariaView`
- **[`guardarSolicitudDispensaSecretaria.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Secretaria/guardarSolicitudDispensaSecretaria.png)** → vista tras guardar → confirmación visual del actualizar
- **[`cerrarSolicitudDispensaSecretaria.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Secretaria/cerrarSolicitudDispensaSecretaria.png)** → confirmación de cierre → flujo alternativo

### con actores

- **`SecretariaAcademica --> editarSolicitudDispensa()`** en package "Dispensas" del `DiagramaCompletoCasoDeUso.puml` → invocación

### con modelo del dominio

- **Sin trazabilidad directa** — deuda heredada del bloque Alumno (`SolicitudDispensa` no está en el modelo del SDR)

## conexión con disciplinas rup

### desde requisitos

- **Detallado**: idéntico estructuralmente al del Alumno → confirma la separación "forma vs política"
- **Prototipos SALT**: editar/guardar/cerrar del rol Secretaria
- **Actores**: presente en `DiagramaCompletoCasoDeUso.puml` (a diferencia de `exportarDispensas`)

### hacia diseño

- **Materializar la política como Strategy `PoliticaAcceso`** (opción b reforzada por este CU)
- **Bloqueo del `alumno`** post-alta (invariante)
- **Política de auditoría del editor** (tres opciones documentadas)
- **Notificación al Alumno** cuando un tercero edita su solicitud
- **Promoción de `SolicitudDispensa` al modelo del dominio** (deuda máxima)

**Código fuente:** [colaboracion.puml](/modelosUML/RUP/01-analisis/casos-uso/editarSolicitudDispensaSecretaria/colaboracion.puml)

## referencias

- [Detallado `editarSolicitudDispensa()` (Secretaria)](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Secretaria/editarSolicitudDispensa.puml)
- [Prototipo SALT `editarSolicitudDispensaSecretaria.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Secretaria/editarSolicitudDispensaSecretaria.png)
- [Caso de uso de Secretaria](/modelosUML/RUP/00-requisitos/CasosDeUso/CasoDeUso/Secretaria/DiagramaCompletoCasoDeUso.puml)
- [Análisis `editarSolicitudDispensa()` (Alumno) — análogo estructural](/RUP/01-analisis/casos-uso/editarSolicitudDispensa/README.md)
- [Análisis `editarSolicitudDispensa()` (Director) — análogo con método distinto](/RUP/01-analisis/casos-uso/editarSolicitudDispensaDirector/README.md)
- [Análisis `crearSolicitudDispensa()` (Secretaria) — origen del crear→editar](/RUP/01-analisis/casos-uso/crearSolicitudDispensaSecretaria/README.md)
- [conversation-log.md](/conversation-log.md)
