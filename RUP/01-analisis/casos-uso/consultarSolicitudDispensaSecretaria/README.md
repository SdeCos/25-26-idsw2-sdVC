# CGU > consultarSolicitudDispensa (Secretaria) > Análisis

> | [🏠️](/README.md) | [Análisis](/RUP/01-analisis/README.md) | [Detalle](/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Secretaria/) | **Análisis** | Diseño | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Inception
- **Disciplina**: Análisis
- **Caso de uso**: `consultarSolicitudDispensa()` (Secretaria)
- **Actor**: Secretaria
- **Versión**: 1.0
- **Fecha**: 2026-05-28

## propósito

Análisis del caso de uso `consultarSolicitudDispensa()` desde el rol Secretaria mediante diagrama de colaboración MVC. La Secretaria abre el detalle de **cualquier** `SolicitudDispensa` (sin restricción de propiedad), con opción de transición a edición vía `<<include>>`.

**Cierre del análisis del proyecto**: con este CU se completa el bloque Secretaria (8/8) y el análisis global llega a **26/26**. Cuatro roles operan sobre `SolicitudDispensa` con cuatro políticas distintas — la entidad queda **completamente caracterizada** desde el análisis.

## diagrama de colaboración

<div align=center>

|![Análisis consultarSolicitudDispensa() (Secretaria)](/images/RUP/01-analisis/casos-uso/consultarSolicitudDispensaSecretaria/colaboracion.svg)|
|-|
|**Disciplina**: Análisis RUP<br>**Enfoque**: Diagramas de colaboración MVC|

</div>


[Código PlantUML](/modelosUML/RUP/01-analisis/casos-uso/consultarSolicitudDispensaSecretaria/colaboracion.puml)
## por qué un análisis separado del Alumno

Calcado estructural de [[consultarSolicitudDispensa]] (Alumno): 4 mensajes, 1 origen, 1 destino opcional vía `<<include>>`. La asimetría es **exclusivamente de política**:

| Aspecto | Alumno | Secretaria |
|-|-|-|
| Política del Controller | Verificación de propiedad: `solicitud.alumno == Sesion.usuario` | **Sin restricción** |
| Vista | `ConsultarSolicitudDispensaView` | `ConsultarSolicitudDispensaSecretariaView` — puede incluir badge "Editado por Secretaria X" si aplica |
| Destino del `<<include>>` | `:Collaboration EditarSolicitudDispensa` (Alumno) | `:Collaboration EditarSolicitudDispensaSecretaria` |
| Método del Controller | `cargarSolicitud` | **`cargarSolicitud`** (mismo) |

Mismo Repository, mismo método del Controller (`cargarSolicitud`), misma signatura. **Confirma la regla emergente** del bloque editar: "métodos específicos por rol" se aplica solo cuando la signatura difiere; aquí solo la política varía.

## clases de análisis identificadas

### clases model (naranja #F2AC4E)

| Clase | Responsabilidad | Trazabilidad |
|-|-|-|
| **SolicitudDispensa** | Entidad de dominio reutilizada (read-only en este CU) | Reutilizada |
| **SolicitudDispensaRepository** | Recupera por ID | Reutilizado; mismo `obtenerPorId` que el Alumno y el editar |

### clases view (azul #629EF9)

| Clase | Responsabilidad | Derivación |
|-|-|-|
| **ConsultarSolicitudDispensaSecretariaView** | Ficha read-only enriquecida con datos del Alumno titular y metadatos de auditoría | Prototipos SALT [`consultarSolicitudDispensaSecretaria1.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Secretaria/consultarSolicitudDispensaSecretaria1.png) y [`consultarSolicitudDispensaSecretaria2.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Secretaria/consultarSolicitudDispensaSecretaria2.png) |

### clases controller (verde #b5bd68)

| Clase | Responsabilidad | Casos de uso |
|-|-|-|
| **SolicitudDispensaController** | Orquestación de la consulta — **sin restricción de propiedad** | Reutilizado; **octava y novena operación** del Controller (`cargarSolicitud` ya existía desde el bloque Alumno) |

### colaboraciones (verde claro #CDEBA5)

| Colaboración | Propósito | Invocación |
|-|-|-|
| **:Dispensas Abierto** | Estado de origen — listado de dispensas (la Secretaria ve todas) | Punto de entrada |
| **:Collaboration EditarSolicitudDispensaSecretaria** | Transición opcional a edición | Vía `<<include>>` opcional |

## mensajes de colaboración

### flujo principal

| # | Origen | Destino | Mensaje | Intención |
|-|-|-|-|-|
| 1 | **:Dispensas Abierto** | **ConsultarSolicitudDispensaSecretariaView** | `consultarSolicitudDispensa(solicitudId)` | Abrir el detalle |
| 2 | **ConsultarSolicitudDispensaSecretariaView** | **SolicitudDispensaController** | `cargarSolicitud(solicitudId) : SolicitudDispensa` | Solicitar los datos |
| 3 | **SolicitudDispensaController** | **SolicitudDispensaRepository** | `obtenerPorId(solicitudId) : SolicitudDispensa` | Recuperar la entidad |
| 4 | **ConsultarSolicitudDispensaSecretariaView** | **:Collaboration EditarSolicitudDispensaSecretaria** | `<<include>> editarSolicitudDispensa(solicitudId)` | Transición opcional a edición |

### flujo alternativo — guardar/cerrar (vuelta al listado)

El detallado modela explícitamente una salida `CONSULTAR_DISPENSA_COMP -[#red]---> DISPENSAS_ABIERTO_FINAL : Guardar/Cerrar solicitud()`. Análisis lo interpreta como **transición de navegación** (cerrar la ficha y volver al listado), no como inclusión de CU. Coherente con [[consultarSolicitudDispensa]] (Alumno) que aplica la misma decisión.

### opcionalidad del `<<include>> editarSolicitudDispensa`

El mensaje 4 es **opcional**: la Secretaria puede consultar sin editar. La dependencia conceptual está modelada como `<<include>>` (línea discontinua); la decisión de invocarlo o no es del actor en la UI. Modelarlo en prosa más que como mensaje separado mantiene la consistencia con todos los consultar del proyecto.

## sin filtro de propiedad — cuarta aplicación

La política "sin restricción" aplicada a este CU completa la matriz del polimorfismo del `SolicitudDispensaController` sobre operaciones de **lectura**:

| Rol | Operación de lectura | Restricción |
|-|-|-|
| Alumno | `cargarSolicitud(solicitudId)` | Verifica `solicitud.alumno == Sesion.usuario` |
| Profesor | `cargarSolicitud(solicitudId)` | Verifica `solicitud.asignatura ∈ Sesion.usuario.asignaturasImpartidas` |
| Director | `cargarSolicitud(solicitudId)` (drill-down desde master-detail) | Sin restricción |
| **Secretaria** | **`cargarSolicitud(solicitudId)`** | **Sin restricción** |

Idéntica situación que en el bloque editar: signatura idéntica, política distinta. **Refuerza definitivamente la opción (b) — Strategy `PoliticaAcceso`** como camino canónico para 02-diseño.

## la vista enriquecida — datos visibles para la Secretaria

A diferencia del Alumno (que ya sabe quién es), la Secretaria consulta dispensas de terceros. La vista debería mostrar:

- **Datos del Alumno titular**: nombre, documento, grado, curso (similar a la vista del Profesor en [[consultarSolicitudDispensaProfesor]])
- **Metadatos de auditoría**: fecha de alta, `responsable` original (quien creó), último editor (si se persiste — deuda heredada del editar Secretaria)
- **Estado actual y comentarios del Director** (si la solicitud ya fue resuelta)

Análisis identifica las relaciones pero no fija el contenido visual exacto — eso vive en el wireframe y se concretará en 02-diseño.

## enlaces de dependencia

- **ConsultarSolicitudDispensaSecretariaView** conoce a **SolicitudDispensaController** (delegación)
- **ConsultarSolicitudDispensaSecretariaView** conoce a **:Collaboration EditarSolicitudDispensaSecretaria** (transición opcional)
- **SolicitudDispensaController** conoce a **SolicitudDispensaRepository** (lectura)
- **SolicitudDispensaController** conoce a **Sesion** (dispatch de política por subtipo; no dibujada)
- **SolicitudDispensaRepository** conoce a **SolicitudDispensa** (gestión)

## discrepancias en el requisitado

| # | Tipo | Detalle | Decisión |
|-|-|-|-|
| 1 | Nota genérica del actor | El detallado dice "**Usuario solicita**" (no "Alumno" como en los otros del bloque Secretaria) | Análisis adopta literalmente el rol del actor (Secretaria). El "Usuario" del detallado es ambiguo pero coherente con la jerarquía polimórfica |
| 2 | Transición `Guardar/Cerrar solicitud()` con color rojo | El detallado usa `-[#red]-` lo que en la convención del proyecto indica error/alternativo, pero la nota describe la transición como "FINALIZAR" | Interpretado como **transición de navegación normal** (cerrar la ficha) — el color rojo parece erróneo. Deuda menor de corrección del detallado |

## comparación con los otros tres consultar de `SolicitudDispensa`

| Rol | Mensajes | Restricción | Include opcional | Vista |
|-|-|-|-|-|
| Alumno ([[consultarSolicitudDispensa]]) | 4 | Propiedad | `editar` (Alumno) | Ficha simple |
| Profesor ([[consultarSolicitudDispensaProfesor]]) | 3 | Profesor competente | — (read-only puro) | Ficha enriquecida con datos del Alumno |
| Director (drill-down dentro de [[consultarSolicitudesDispensas]]) | (dentro de master-detail) | — | `editar` (Director) | Ficha enriquecida |
| **Secretaria** (este CU) | **4** | **—** | **`editar` (Secretaria)** | **Ficha enriquecida con auditoría** |

Cuatro variantes del mismo CU, cuatro políticas, cuatro vistas. Es la entidad **más completamente caracterizada** del análisis.

## principios de análisis aplicados

### patrón mvc

- **Controller por entidad** reutilizado (sin métodos nuevos)
- **Vista específica por rol** con contenido enriquecido
- **Repository agnóstico al rol** — séptima vez consolidada

### diagramas de colaboración

- **4 mensajes**: mismo que el del Alumno
- **`<<include>>` opcional** documentado en prosa
- **Sin destino terminal**: la vista cierra y vuelve al listado (navegación, no CU)

### análisis puro

- **Sin política de notificación al Alumno** sobre consultas de terceros (¿registrar accesos para LOPD/RGPD?) — deuda sensible
- **Sin caché de consultas** — irrelevante para análisis

## trazabilidad con artefactos previos

### con especificación detallada

- **`DISPENSA_ABIERTO_INICIAL`** → colaboración `:Dispensas Abierto`
- **Transición `consultarSolicitudDispensa()`** → mensaje 1
- **Estado compuesto `CONSULTAR_DISPENSA_COMP` con `MostrarSolicitud` (Modo Lectura)** → mensajes 2-3 (carga read-only)
- **Salida `editarSolicitudDispensa()` → `SOLICITUD_DISPENSA_EDITAR`** → mensaje 4 (`<<include>>`)
- **Salida `Guardar/Cerrar solicitud()` → `DISPENSAS_ABIERTO_FINAL`** → navegación de cierre (no mensaje)

### con wireframe (prototipo SALT)

- **[`consultarSolicitudDispensaSecretaria1.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Secretaria/consultarSolicitudDispensaSecretaria1.png)** — vista de detalle
- **[`consultarSolicitudDispensaSecretaria2.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Secretaria/consultarSolicitudDispensaSecretaria2.png)** — variante con scroll o sección adicional

### con actores

- **`SecretariaAcademica --> consultarSolicitudDispensa()`** en package "Dispensas" → invocación

### con modelo del dominio

- **Sin trazabilidad directa** — `SolicitudDispensa` no está en el modelo del SDR. Deuda **máxima**: se cierra el análisis sin esta entidad promovida pese a ser la más operada del proyecto

## conexión con disciplinas rup

### desde requisitos

- **Detallado**: estructura idéntica a `consultarSolicitudDispensa` del Alumno
- **Prototipos SALT**: dos vistas de la ficha → variantes UI
- **Actores**: presente en `DiagramaCompletoCasoDeUso.puml`

### hacia diseño

- **Strategy `PoliticaAcceso`**: ratificada como camino canónico tras 4 análisis con misma signatura y distintas políticas
- **Promoción de `SolicitudDispensa` al modelo del dominio**: **deuda crítica del cierre del análisis** — primera prioridad de 02-diseño
- **Política de auditoría de accesos**: relevante por RGPD si la Secretaria consulta datos personales
- **Vista enriquecida**: definir el conjunto exacto de campos visibles (deuda compartida con consultarSolicitudDispensaProfesor)

## cierre del bloque Secretaria y del análisis

Con este CU se cierran simultáneamente:

- **Bloque Secretaria (8/8 CUs)**: 2 importar + 2 consultar (lista alumnos + detalle matrícula) + 4 dispensas (crear + editar + consultar + exportar)
- **Tetrada `SolicitudDispensa`**: 4 roles, 4 políticas, mismo Repository, mismo Controller con dispatch por subtipo
- **Análisis global (26/26 CUs)**: cobertura completa del denominador

**Lecciones consolidadas del análisis** (insumo para 02-diseño):

1. **MVC con Controller por entidad + Servicio por operación atómica** (SRP) — patrón maestro del proyecto.
2. **Repository agnóstico al rol; política en el Controller** — confirmado en 7 CUs.
3. **"Métodos específicos por rol" solo cuando la signatura difiere**; cuando solo la política varía, Strategy `PoliticaAcceso` es la opción más limpia (opción b).
4. **Patrón "Controller orquesta + Servicio especializa"** en 4 CUs de I/O masiva (1 export Asistencia, 1 export Dispensa, 2 import) — abstracción `Generador<T>` / `ImportadorMasivo<T>` viable.
5. **Propietario implícito desde `Sesion.usuario`** salvo cuando un rol opera sobre terceros (Secretaria en crear/editar de dispensas).
6. **Auto-poblado de auditoría por el Controller** consolidado (`fechaResolucion`, `responsable`, `fechaImportacion`, `horaFin`).
7. **Refactor "Introduce Parameter Object"** aplicado donde el smell es claro (`DatosSesionClase`); pendientes candidatos (`FiltrosDispensa`).
8. **Polimorfismo de Usuario** materializa la jerarquía de actores como jerarquía de clases — habilita los dispatchs por rol.

**Código fuente:** [colaboracion.puml](/modelosUML/RUP/01-analisis/casos-uso/consultarSolicitudDispensaSecretaria/colaboracion.puml)

## referencias

- [Detallado `consultarSolicitudDispensa()` (Secretaria)](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Secretaria/consultarSolicitudDispensa.puml)
- [Prototipo SALT `consultarSolicitudDispensaSecretaria1.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Secretaria/consultarSolicitudDispensaSecretaria1.png)
- [Prototipo SALT `consultarSolicitudDispensaSecretaria2.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Secretaria/consultarSolicitudDispensaSecretaria2.png)
- [Caso de uso de Secretaria](/modelosUML/RUP/00-requisitos/CasosDeUso/CasoDeUso/Secretaria/DiagramaCompletoCasoDeUso.puml)
- [Análisis `consultarSolicitudDispensa()` (Alumno)](/RUP/01-analisis/casos-uso/consultarSolicitudDispensa/README.md)
- [Análisis `consultarSolicitudDispensa()` (Profesor)](/RUP/01-analisis/casos-uso/consultarSolicitudDispensaProfesor/README.md)
- [Análisis `consultarSolicitudesDispensas()` (Director)](/RUP/01-analisis/casos-uso/consultarSolicitudesDispensas/README.md)
- [Análisis `editarSolicitudDispensa()` (Secretaria) — destino del `<<include>>`](/RUP/01-analisis/casos-uso/editarSolicitudDispensaSecretaria/README.md)
- [conversation-log.md](/conversation-log.md)
