# CGU > exportarHistorialAsistencias > Análisis

> | [🏠️](/README.md) | [Análisis](/RUP/01-analisis/README.md) | [Detalle](/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Profesor/) | **Análisis** | Diseño | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Inception
- **Disciplina**: Análisis
- **Caso de uso**: `exportarHistorialAsistencias()`
- **Actor**: Profesor
- **Versión**: 1.0
- **Fecha**: 2026-05-28

## propósito

Análisis del caso de uso `exportarHistorialAsistencias()` mediante diagrama de colaboración MVC. El Profesor genera un archivo descargable con el historial de asistencias de su asignatura para un rango de fechas, en el formato elegido. Es el **segundo CU no-CRUD** del proyecto (tras [[registrarTomaAsistencia]]) y el **primero que introduce un servicio de aplicación** distinto de Controller/Repository: el `GeneradorArchivoAsistencias`.

Es el **cierre del bloque Profesor** y completa la cadena natural: pasar lista (`registrarTomaAsistencia`) → exportar el historial acumulado.

## diagrama de colaboración

<div align=center>

|![Análisis exportarHistorialAsistencias()](/images/RUP/01-analisis/casos-uso/exportarHistorialAsistencias/colaboracion.svg)|
|-|
|**Disciplina**: Análisis RUP<br>**Enfoque**: Diagramas de colaboración MVC|

</div>


[Código PlantUML](/modelosUML/RUP/01-analisis/casos-uso/exportarHistorialAsistencias/colaboracion.puml)
## discrepancia en el requisitado — formatos de exportación

| Fuente | Formatos enumerados |
|-|-|
| [`exportarHistorialAsistencias.puml`](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Profesor/exportarHistorialAsistencias.puml) | **Excel, PDF** |
| [Prototipo SALT `exportarHistorialAsistencias.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Profesor/exportarHistorialAsistencias.png) | **CSV** (único valor visible en el dropdown) |

Análisis adopta **el conjunto unión** como hipótesis: `{Excel, PDF, CSV}`. El `formato` se modela como string/enum opaco a nivel análisis — qué formatos concretos están disponibles es decisión de diseño + producto.

**Deuda para 02-diseño**: confirmar con el cliente qué formatos se soportan (impacto: librerías de generación, casos de uso adicionales como reportes regulatorios en formato específico).

## clases de análisis identificadas

### clases model (naranja #F2AC4E)

| Clase | Responsabilidad | Trazabilidad |
|-|-|-|
| **Asistencia** | Entidad de dominio (read-only para este CU) | Reutilizada de [[registrarTomaAsistencia]] |
| **AsistenciaRepository** | Recupera asistencias por rango y asignatura | Reutilizado; estrena `obtenerPorRango(asignatura, fechaInicio, fechaFin) : List<Asistencia>` |

### clases view (azul #629EF9)

| Clase | Responsabilidad | Derivación |
|-|-|-|
| **ExportarHistorialView** | Modal con campos `Inicio` (fecha), `Fin` (fecha), `Formato` (dropdown). Botones Cancelar / Exportar | [Prototipo SALT `exportarHistorialAsistencias.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Profesor/exportarHistorialAsistencias.png) |

### clases controller / servicios (verde #b5bd68)

| Clase | Responsabilidad | Casos de uso |
|-|-|-|
| **AsistenciaController** | Orquestación del export: recuperar datos + delegar generación | Compartido con [[registrarTomaAsistencia]] |
| **GeneradorArchivoAsistencias** | **Servicio de aplicación**: convierte `List<Asistencia>` a un `Archivo` según formato | **Nuevo**; primer servicio de aplicación distinto de Controller/Repository en el análisis |

### colaboraciones (verde claro #CDEBA5)

| Colaboración | Propósito | Invocación |
|-|-|-|
| **:Asistencias Abierto** | Estado de origen — el Profesor está en el listado de sesiones | Punto de entrada |

## mensajes de colaboración

### flujo principal

| # | Origen | Destino | Mensaje | Intención |
|-|-|-|-|-|
| 1 | **:Asistencias Abierto** | **ExportarHistorialView** | `exportarHistorialAsistencias()` | Abrir modal con parámetros de exportación |
| 2 | **ExportarHistorialView** | **AsistenciaController** | `exportar(asignatura, fechaInicio, fechaFin, formato) : Archivo` | Solicitar exportación |
| 3 | **AsistenciaController** | **AsistenciaRepository** | `obtenerPorRango(asignatura, fechaInicio, fechaFin) : List<Asistencia>` | Recuperar el dataset |
| 4 | **AsistenciaController** | **GeneradorArchivoAsistencias** | `generar(asistencias, formato) : Archivo` | Convertir a formato elegido |

### flujo alternativo — cancelar

El prototipo muestra explícitamente un botón "Cancelar" en el modal. Si el Profesor cancela, no se invocan los mensajes 2-4. La vista se cierra y el sistema vuelve a `:Asistencias Abierto`. Mismo patrón que en los modales de creación / cierre.

## debut de servicio de aplicación — `GeneradorArchivoAsistencias`

Hasta ahora el análisis ha trabajado con tres tipos de clases: **Model** (entidades + repositorios, naranja), **View** (azul), **Controller** (verde). Este CU **introduce un cuarto tipo**: un **servicio de aplicación** — lógica que no encaja como entidad ni como Controller orquestador.

### ¿por qué no meterlo en el Controller?

Tres razones de separación:

1. **Cohesión**: la generación de un archivo a partir de datos tabulares es una responsabilidad bien definida y reutilizable. Mezclarla con el Controller acopla orquestación con conversión.
2. **Extensibilidad**: si en el futuro se añade el formato `.ods` o `.xlsx-zip-firmado`, esa decisión debe afectar a una sola clase, no al Controller.
3. **Testabilidad**: el Controller puede testarse mockeando el generador; el generador puede testarse sin Repository.

Es una aplicación del **Principio de Responsabilidad Única** (SRP) que el temario IDSW2 cubre. Documenta una decisión de diseño OO sólida ya desde el análisis.

### ¿por qué color verde como el Controller?

A nivel **lógica de aplicación** ambos son lo mismo: código que vive en la capa de aplicación (ni dominio ni presentación ni persistencia). Naranja (model) está reservado para entidades y repositorios. Azul (view) para la presentación. Verde encaja tanto para orquestación (Controller) como para servicios atómicos (generador).

**Deuda blanda**: en futuras revisiones del proyecto, si emergen muchos servicios, considerar introducir un cuarto color o anotación (`<<service>>`) para distinguirlos visualmente de los Controllers.

## verificación "Profesor competente" reaparece

El CU recibe `asignatura` como parámetro. Misma regla que en [[consultarListaAlumnos]] y [[consultarSolicitudDispensaProfesor]]: el `AsistenciaController` debe validar que `asignatura ∈ sesion.usuario.asignaturasImpartidas`. Defensa en profundidad — la UI ya restringe el selector a las asignaturas del Profesor (presumiblemente), el Controller revalida.

Implementación abierta: el modal del prototipo no muestra el selector de asignatura. Posibles interpretaciones:
- La asignatura viene del **contexto de la página** (header "Asistencias - Ingeniería de Software I")
- O bien hay un selector implícito que el prototipo no muestra

Adoptamos la primera (asignatura del contexto) — deuda blanda para confirmar con el cliente.

## ¿por qué `AsistenciaController` y no un `ExportacionController` aparte?

Decisión de diseño OO consciente:

- **Lo que se exporta** son asistencias → la orquestación pertenece naturalmente al `AsistenciaController`.
- **Cómo se genera el archivo** es responsabilidad de `GeneradorArchivoAsistencias` (servicio).
- Introducir un Controller adicional solo añadiría indirección.

El patrón puede generalizarse: para futuros exports (p.ej. `exportarDispensas` del bloque Secretaria), el Controller de la entidad delegaría a un generador análogo. Esto evita un "ExportadorController" omnipresente — cada entidad gestiona su propia exportación, reutilizando el patrón "Controller delega en servicio especializado".

## enlaces de dependencia

- **ExportarHistorialView** conoce a **AsistenciaController** (delegación)
- **AsistenciaController** conoce a **AsistenciaRepository** (lectura)
- **AsistenciaController** conoce a **GeneradorArchivoAsistencias** (servicio)
- **AsistenciaController** conoce a **Sesion** (verificación "Profesor competente"; no dibujada)
- **AsistenciaRepository** conoce a **Asistencia** (gestión)

## trazabilidad con artefactos previos

### con especificación detallada

- **`ASISTENCIAS_ABIERTO_INICIAL`** → colaboración `:Asistencias Abierto` (origen)
- **Transición `exportarHistorialAsistencias()`** → mensaje 1
- **Estado `PROCESO_EXPORTACION_COMP` con sub-estado `SeleccionParametros`** → `ExportarHistorialView` modal
- **Nota "Sistema permite introducir el formato de salida (Excel, PDF) y el rango de fechas"** → parámetros del mensaje 2
- **Nota "Sistema presenta el archivo listo para su descarga. Profesor solicita descargar el archivo"** → retorno `Archivo` del mensaje 4 + acción del Profesor (no modelada como mensaje aparte porque es UI)
- **Transición de cierre → `ASISTENCIAS_ABIERTO_FINAL`** → vuelta implícita al estado de partida

### con wireframe (prototipo SALT)

- **`exportarHistorialAsistencias.png`** → modal con `Inicio`, `Fin`, `Formato` y botones Cancelar / Exportar → `ExportarHistorialView`. Notable: dropdown de formato muestra solo "CSV" — discrepancia documentada arriba

### con actores

- **`Profesor --> exportarHistorialAsistencias`** en package "Asistencias" → invocación del CU

### con modelo del dominio

- **Sin trazabilidad directa** (deuda heredada de `Asistencia` no estando en el modelo del SDR — se levantará al promover la entidad).

## comparación con los otros CUs del Profesor

| Característica | Otros CUs del Profesor | `exportarHistorialAsistencias` |
|-|-|-|
| Operación | CRUD / consulta / toma | **Exportación de datos derivados** |
| Output | Pantalla / estado | **Archivo descargable** |
| Servicios externos al Controller | No | **`GeneradorArchivoAsistencias`** |
| Mensajes | 3-5 | 4 |
| Parámetros del CU | Mínimos | 4 (asignatura, rango, formato) |
| Side effect | Nuevo dato persistido | **Generar artefacto efímero** (el archivo no se persiste) |

Es **el CU más distinto** del bloque Profesor. Refleja una **categoría operativa nueva**: generación de reportes / exportación, que probablemente reaparecerá en el bloque Secretaria con `exportarDispensas()`.

## principios de análisis aplicados

### patrón mvc

- **Controller por entidad**: `AsistenciaController` con responsabilidades de orquestación (no de generación)
- **Servicio de aplicación**: `GeneradorArchivoAsistencias` separado — primera aplicación explícita del **Principio de Responsabilidad Única** (SRP) en el análisis
- **Vista modal**: `ExportarHistorialView` autocontenida

### diagramas de colaboración

- **4 mensajes**: balance entre brevedad y honestidad con la separación de responsabilidades
- **Sin destino**: el archivo es efímero, la sesión vuelve al estado de partida
- **`Archivo` como tipo de retorno opaco**: cómo se materializa (stream, blob, URL temporal) es decisión de diseño

### análisis puro

- **Sin librerías de generación específicas**: Excel/PDF/CSV son labels, la materialización vive en diseño
- **Sin política de almacenamiento del archivo generado**: ¿se cachea? ¿se elimina al cerrar sesión? — deuda
- **Sin manejo de errores específicos**: rangos vacíos, formatos inválidos — emergerán en diseño

## características del análisis

### responsabilidades identificadas

- **ExportarHistorialView**: recoger parámetros, presentar archivo descargable al Profesor
- **AsistenciaController**: orquestar (recuperar datos + delegar generación), aplicar "Profesor competente"
- **AsistenciaRepository**: consulta por rango
- **GeneradorArchivoAsistencias**: generar el archivo según formato
- **Asistencia**: dato de entrada para la generación

### relaciones conceptuales

- **Delegación a servicio**: el Controller no genera, **delega** la generación a una clase especializada
- **Composición de capas**: Repository (datos) → Controller (orquestación) → Servicio (transformación) → View (entrega)

## conexión con disciplinas rup

### desde requisitos

- **Detallado**: `PROCESO_EXPORTACION_COMP` → modal de exportación; nota de formatos → parámetro `formato`
- **Prototipo SALT**: modal con campos Inicio/Fin/Formato → `ExportarHistorialView`
- **Actores**: `Profesor --> exportarHistorialAsistencias()` en package "Asistencias"

### hacia diseño

- **Confirmar conjunto de formatos** con el cliente (Excel/PDF del detallado vs CSV del prototipo)
- **Materializar `GeneradorArchivoAsistencias`**: ¿una clase con `if formato`, una jerarquía polimórfica `GeneradorCSV/PDF/Excel`, una factory? — buena ocasión para aplicar Strategy o un patrón equivalente
- **Definir tipo `Archivo`**: stream, blob, URL temporal, ruta temporal en disco
- **Política de retención** del archivo generado
- **Validaciones de parámetros**: rango razonable (¿máximo? ¿pre-validar que hay datos?), formato soportado, asignatura válida
- **Reutilizar el patrón en `exportarDispensas()` (Secretaria)**: estructura paralela esperada
- **Auditoría**: ¿se registra quién exportó qué y cuándo? (relevante si los datos son sensibles)

**Código fuente:** [colaboracion.puml](/modelosUML/RUP/01-analisis/casos-uso/exportarHistorialAsistencias/colaboracion.puml)

## referencias

- [Detallado `exportarHistorialAsistencias()`](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Profesor/exportarHistorialAsistencias.puml)
- [Prototipo SALT `exportarHistorialAsistencias.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Profesor/exportarHistorialAsistencias.png)
- [Caso de uso del Profesor](/modelosUML/RUP/00-requisitos/CasosDeUso/CasoDeUso/Profesor/Profesor.puml)
- [Análisis `registrarTomaAsistencia()`](/RUP/01-analisis/casos-uso/registrarTomaAsistencia/README.md)
- [conversation-log.md](/conversation-log.md)
