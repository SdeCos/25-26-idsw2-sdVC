# Conversation log

---

### Sesión 2026-05-22

## [11:48] Creación de CLAUDE.md y README.md inicial

**Prompt:** En el siguiente commit quiero dejar configurado el inicio del CLAUDE.md y el README.md como indican las instrucciones del repo. El README debe basarse en los repos comentados (idsw2-sdVC, pySigHor como guía).

**Resultado:** Se creó `CLAUDE.md` con protocolo de inicio/cierre de sesión, formato del conversation-log, tabla de artefactos y criterios de evaluación. Se propuso un `README.md` con presentación del proyecto, tabla de estado y estructura de carpetas.

**Decisión:** `CLAUDE.md` aceptado con ajuste menor (formato del bloque de código del log). El `README.md` fue rechazado por usar una estructura de carpetas incorrecta.

---

## [11:57] Corrección de estructura de carpetas en README.md

**Prompt:** El profesor indicó en una discusión que la estructura debe seguir la de SigHor: `/RUP/00-requisitos`, `/RUP/01-analisis`, `/RUP/02-diseño`, `/RUP/03-desarrollo`, y el código en `/src`.

**Resultado:** README.md reescrito con la estructura de carpetas corregida.

**Decisión:** Aceptado. Se modificaron adicionalmente: el estado de "Requisitado" pasó a ⏳ Pendiente (la migración del SDR aún no está hecha) y se simplificó la sección "Origen" eliminando la referencia duplicada al repo.

---

### Sesión 2026-05-23

## [10:03] Migración del requisitado a RUP/00-requisitos

**Prompt:** Haz la migración del requisitado (00-requisitos) a su carpeta correspondiente en este repositorio.

**Resultado:** Copia espejo de `documents/` del SDR (`../25-26-IDSW1-SDR/documents/`) a `RUP/00-requisitos/` (carpeta `RUP/` creada). 89 archivos copiados, `diff` vacío. README actualizado: fila "Requisitado" pasa de ⏳ Pendiente a ✅ Migrado con enlace.

**Decisión:** Aceptada copia espejo preservando estructura del SDR (CasosDeUso/, ModeloDelDominio/, images/, Reuniones/, README.MD). Se incluyeron Reuniones/ y README.MD del SDR a petición explícita. Se descartó la alternativa de reestructurar separando .puml/SVG al convenio del repo (root /modelosUML, /images).

---

## [10:15] Discrepancia detectada: SDR estaba en otra rama al copiar

**Prompt:** Usando `tree -P "*.puml" --prune` me da 6 carpetas y 24 archivos en el detallado; confirma el conteo en main (mi repo SDR puede haber estado en rama distinta).

**Resultado:** Verificado contra `main` del SDR: 24 .puml en detallado (Admin 3, Alumno 3, DirectorDeGrado 2, Profesor 8, Secretaria 8). Mi copia inicial tenía 13 (Admin 5 + Profesor 8 con nombres distintos). El SDR estaba en otra rama al momento de copiar. Resync: `rm -rf RUP/00-requisitos && cp -R` desde el SDR ya en main. Resultado: 145 archivos, 24 .puml, `diff -r` vacío.

**Decisión:** Aceptado el resync completo. Se eliminaron `cerrarUsuario.puml` y `guardarUsuario.puml` (no existen en main) y se incorporaron los 11 .puml de Alumno/Secretaria/DirectorDeGrado ausentes en la primera copia.

---

## [10:25] Formato de progreso en la tabla Estado del README

**Prompt:** Modifica el README para que el estado no diga simplemente "Pendiente", sino el progreso real (con icono y x/x).

**Resultado:** Tras un primer intento mío con matriz tipo SigHor por CU (rechazado por excesivo), la tabla quedó simplificada a fracciones: Requisitado ✅ Migrado; Análisis/Diseño/Implementación ⏳ 0/24.

**Decisión:** Denominador 24 aportado por el usuario tras contar manualmente los CUs del SDR. Mi conteo inicial (32, sumando todos los CUs identificados en los .puml de rol) se descartó por usar otra base. El 24 = CUs con detalle migrados, repartidos en 5 roles.

---

## [10:40] Correcciones a CLAUDE.md y regla del conversation-log

**Prompt:** Confirma si CLAUDE.md necesita cambios tras la migración. Configura el log para que se edite mientras ocurre, no al cierre.

**Resultado:** CLAUDE.md actualizado: (1) ubicación del requisitado pasa a `RUP/00-requisitos/` (espejo de la fuente externa); (2) nueva sección "Estructura RUP" con la convención SigHor por disciplina autocontenida; (3) nueva sección "Medida de progreso" fijando el denominador en 24 CUs con desglose por rol; (4) sección "Cierre" del protocolo reemplazada por "Durante la sesión" — el log se escribe tras cada intercambio relevante.

**Decisión:** Carpetas root `/modelosUML`, `/images`, `/documents` marcadas como scaffolding "pendiente de decidir" en CLAUDE.md, sin eliminar (el usuario no se ha pronunciado). La nota de formato del log se mantiene tal cual ("se escribe mientras ocurre, o al cerrar sesión como máximo") tras rechazo explícito del usuario a simplificarla.

---

## [10:46] Cabecera de día y hora real en el conversation-log

**Prompt:** En el log no se sabe nada más que la hora; configura lo necesario para que al inicio de cada sesión se indique el día (una vez, no antes de cada entrada). Además, la hora no siempre se pone correctamente (ej: `[HH:MM]` literal).

**Resultado:** Dos cambios en `CLAUDE.md`: (1) en "Protocolo de sesión > Inicio", añadir `### Sesión YYYY-MM-DD` una vez al empezar la sesión, sin duplicar si ya existe; (2) en "Formato del conversation-log", nota explícita de que `HH:MM` y `YYYY-MM-DD` son plantillas a sustituir por valores reales del sistema (`date` si hace falta), nunca literales. Aplicado retroactivamente a esta sesión con la hora real 10:46.

**Decisión:** Rechazada la opción inicial de configurarlo vía hook `SessionStart` en `settings.json`. Se prefiere `CLAUDE.md` por ser regla del proyecto y quedar versionada junto al resto del protocolo.

---

## [10:50] Reubicación retroactiva de cabeceras de sesión en el log

**Prompt:** Las entradas `[11:48]` y `[11:57]` son del 22/05/2026; la sesión de hoy 23/05/2026 empezó en `[10:03]` (Migración del requisitado). Mueve las cabeceras para reflejarlo.

**Resultado:** Insertada `### Sesión 2026-05-22` al inicio del log (antes de `[11:48]`) y `### Sesión 2026-05-23` antes de `[10:03]`. Eliminada la cabecera duplicada que estaba justo antes de `[10:46]`.

**Decisión:** Aceptado. La cabecera marca el principio del día, no el momento en que se configuró la regla.

---

### Sesión 2026-05-25

## [09:45] Arranque de análisis y exploración de iniciarSesion()

**Prompt:** Empezar la fase de análisis basándose en el temario (`../idsw2`) y usando `../pySigHor` como guía. Añadir esos dos contextos a CLAUDE.md para no comentarlo cada sesión. Primera aproximación a `iniciarSesion()`.

**Resultado:** CLAUDE.md ampliado con sección "Contextos externos de referencia" (idsw2 y pySigHor). Detectados dos gaps al revisar el material: (1) `iniciarSesion()` aparece como transición en el diagrama de contexto pero no tiene detallado migrado del SDR; (2) el modelo del dominio no incluye una clase `Usuario`. Propuesta inicial: análisis MVC siguiendo el patrón de pySigHor (LoginView, IniciarSesionController, UsuarioRepository, Usuario, Sesion).

**Decisión:** Antes de tirar PUML/README se planteó la duda metodológica de fondo (siguiente entrada).

---

## [09:50] Decisión: ¿se crea iniciarSesion/cerrarSesion en el requisitado o se asume?

**Prompt:** ¿Qué es más correcto: crear el actor Usuario en el requisitado con los dos CUs de sesión, o mantener el requisitado tal cual y empezar el análisis directamente en SISTEMA_DISPONIBLE?

**Resultado:** Voto inicial mío por mantener el requisitado intacto y asumir la autenticación (coherencia con la migración espejo, denominador 24 ya excluye sesión, foco del análisis en las ramas con valor de dominio).

**Decisión:** Rechazado. El usuario opta por completar el requisitado: añadir el actor `Usuario` y los CUs `iniciarSesion()`/`cerrarSesion()`. Razón aportada: la diferencia es pequeña (1 actor, 2 CUs genéricos) y prima la corrección y completitud sobre la fidelidad al espejo.

---

## [09:55] Configuración del trabajo: jerarquía, prototipo y denominador

**Prompt:** Tres preguntas previas (jerarquía de Usuario en Actores.puml; prototipo de login sí/no; los 2 CUs nuevos cuentan en el denominador).

**Resultado:** Confirmadas tres decisiones:

- `Usuario` como **superclase de los 5 actores** (Alumno, Profesor, Secretaria heredan de Usuario; resto de la jerarquía existente intacta).
- **Sí** crear prototipo SALT simple del login.
- **Sí** subir el denominador a **26** (cobertura total de transiciones del diagrama de contexto).

**Decisión:** Aceptadas las tres. Defaults asumidos sin preguntar: nuevas carpetas `Usuario/` bajo `CasoDeUso/`, `DetalladoCasosDeUso/` y `Prototipos/`; arreglo masivo de links rotos `/documents/...` → `/RUP/00-requisitos/...` en todos los README del requisitado; conservar el estilo de navbar/badges del SDR.

---

## [10:00] Implementación: actor Usuario, 2 CUs, prototipo SALT y arreglo de links

**Prompt:** Ejecuta el plan; el repo tiene `plantuml` disponible para generar SVGs.

**Resultado:** Cambios aplicados:

- `Actores.puml` ampliado con `Usuario` como superclase (note: "origen común de actores autenticables").
- Nueva carpeta `CasoDeUso/Usuario/` con `Usuario.puml` (actor → 2 CUs en package "Sesión") y SVG renombrado para seguir convención del SDR (`Usuario.svg`).
- Nueva carpeta `DetalladoCasosDeUso/Usuario/` con `iniciarSesion.puml` (estados internos + choice point credenciales válidas/no válidas, basado en el patrón de pySigHor), `cerrarSesion.puml` (transiciones por acción del usuario y por inactividad) y `README.md` con la misma estructura que el de Administrador.
- Nueva carpeta `Prototipos/Usuario/` con `iniciarSesion.puml` (SALT wireframe: campos usuario/contraseña, botones, mensaje de error).
- Todos los SVG generados con `plantuml -tsvg`.
- `DetalladoCasosDeUso/README.md` y `Prototipos/README.md`: añadida sección `Usuario` (primera, antes de Alumno).
- Reescritura global en 13 README del requisitado: `/documents/` → `/RUP/00-requisitos/` y `PRIORIZACION_CASOS_DE_USO.md` → `PriorizaciónCasosDeUso.md`. Verificación: 0 ocurrencias residuales.
- README raíz: fracciones `0/24` → `0/26` (3 ocurrencias).
- CLAUDE.md: sección "Medida de progreso" actualizada (denominador 26, breakdown con Usuario(2)).

**Decisión:** Fuera de scope (pre-existente del SDR, no roto por migración): `ModeloDelDominio/README.MD` referencia diagramas de estado inexistentes (DirectorGrado, ListaAlumno, SesionDeClase). No se tocan — son aspiracionales del SDR original.

---

## [10:20] Modelo elegido para Usuario en el análisis: herencia polimórfica

**Prompt:** Cuando un usuario inicia sesión, debe detectarse su tipo concreto (Alumno, Profesor, …) y aplicársele permisos/comportamientos por tipo. Sesión gestionada por el Controller, no por el Usuario.

**Resultado:** Modelo confirmado para el análisis: `Usuario` como clase abstracta, con subclases concretas (Alumno, Profesor, Secretaria, Director, Administrador) en 1:1 con la jerarquía de `Actores.puml`. El polimorfismo entra en `UsuarioRepository.validarCredenciales(...) : Usuario` — devuelve un Usuario tipado, la instancia real es el subtipo. Permisos/comportamientos viajan con el tipo, no con un atributo `rol`. `Sesion` la crea el Controller (decisión 2a).

**Decisión:** Rechazadas (1a) atributo rol y (1b) `Usuario` con asociación a `Rol`; aceptada herencia polimórfica directa (la jerarquía de actores se materializa como jerarquía de clases). Es lo más alineado con el espíritu OO del temario IDSW2 (composición/herencia, Liskov, SOLID).

---

## [10:26] Implementación del análisis de iniciarSesion()

**Prompt:** Procede a crear los 5 archivos.

**Resultado:** Estructura nueva `RUP/01-analisis/`:

- `README.md` — presentación de la disciplina (metodología MVC, colores de estereotipos, heurísticas).
- `casos-uso/README.md` — índice de los 26 CUs con estado (1 ✅ / 25 ⏳).
- `casos-uso/iniciarSesion/colaboracion.puml` — diagrama de colaboración con 5 clases (LoginView, IniciarSesionController, UsuarioRepository, Usuario, Sesion) + colaboración `:Sistema Disponible`. Nota explícita sobre el polimorfismo del retorno de `validarCredenciales()`.
- `casos-uso/iniciarSesion/colaboracion.svg` — generado con `plantuml -tsvg` y renombrado de `iniciarSesion-analisis.svg` a `colaboracion.svg`.
- `casos-uso/iniciarSesion/README.md` — análisis completo: tablas por estereotipo, flujo principal y alternativo, sección de polimorfismo/herencia con la jerarquía visualizada, trazabilidad con cada artefacto del requisitado, principios aplicados y decisiones abiertas para 02-diseño.

Actualizaciones colaterales:

- README raíz: fracción `Análisis 0/26 → 1/26` y la celda pasa a ser enlace a `RUP/01-analisis/`.

**Decisión:** Aceptado el modelo de herencia polimórfica como base. Sin trazabilidad directa al modelo del dominio para `Usuario`/`Sesion` — explícitamente listado como deuda a reconciliar en 02-diseño (¿se promueve `Usuario` a clase de dominio o se queda como concepto de análisis/infraestructura?).

---

## [10:35] Pulido del análisis: formato pySigHor y eliminación de la nota

**Prompt:** Quita la nota del PUML (innecesaria, sustituida por la tabla). Pon debajo del diagrama una tabla "Disciplina/Enfoque" como pySigHor en lugar de los badges Ver_PUML/Ver_SVG. Reescribe el README al formato pySigHor.

**Resultado:** Tres cambios:

- `colaboracion.puml`: eliminada la nota sobre polimorfismo. SVG regenerado.
- `README.md` reestructurado al formato pySigHor: navbar superior con badges de disciplinas RUP; secciones en minúscula (información del artefacto, propósito, diagrama de colaboración, clases de análisis identificadas con subsecciones model/view/controller/colaboraciones, mensajes de colaboración, enlaces de dependencia, polimorfismo y herencia, trazabilidad con artefactos previos, principios de análisis aplicados, características del análisis, conexión con disciplinas rup, referencias). Diagrama embedido con tabla de caption "Disciplina: Análisis RUP / Enfoque: Diagramas de colaboración MVC".
- Conservada la sección "polimorfismo y herencia" (específica de este proyecto, no presente en pySigHor) — es donde vive la decisión OO clave del análisis.

**Decisión:** Aceptado el formato pySigHor como plantilla canónica para los próximos análisis de CU en `RUP/01-analisis/casos-uso/`.

---

## [10:50] Eliminación de `sesionInactiva()` del requisitado

**Prompt:** Eliminar por completo `sesionInactiva()` (cierre automático por inactividad), incluso del requisitado. No es esencial, añade complejidad y la sesión debería cerrarse solo cuando el usuario lo pida.

**Resultado:** Cambios en el requisitado:

- `DiagramaDeContexto.puml`: la línea `SISTEMA_DISPONIBLE --> SESION_CERRADA : cerrarSesion() / sesionInactiva()` pasa a `... : cerrarSesion()`.
- `DetalladoCasosDeUso/Usuario/cerrarSesion.puml`: eliminada la transición roja `SISTEMA_DISPONIBLE -[#red]---> SESION_CERRADA : sesionInactiva()` y su nota.
- Ambos SVGs regenerados. Verificación: 0 ocurrencias de `sesionInactiva` en el repo.

**Decisión:** Aceptado por las razones aportadas: (1) `sesionInactiva()` lo dispararía un "Sistema" como actor implícito que no existe en `Actores.puml`; (2) es una decisión de seguridad/configuración (cuántos minutos, cómo notificar), no un CU del negocio; (3) YAGNI — no hay requisito que lo pida. Si en algún momento se decide implementar timeout, vivirá en `02-diseño` o `03-desarrollo`, no como CU.

---

## [10:55] Análisis de `cerrarSesion()`

**Prompt:** Procede con el análisis de cerrarSesion para completar el actor Usuario.

**Resultado:** Creados `RUP/01-analisis/casos-uso/cerrarSesion/{colaboracion.puml, colaboracion.svg, README.md}`. Características:

- 3 clases de análisis: `CerrarSesionView`, `CerrarSesionController`, `Sesion` (reutilizada de iniciarSesion).
- 2 colaboraciones: `:Sistema Disponible` (origen) y `:Sesión Cerrada` (destino).
- 4 mensajes, flujo único (sin alternativo tras la eliminación de `sesionInactiva()`).
- **Sin `SesionRepository`**: por consistencia con `iniciarSesion()`, donde `Sesion` se autogestiona. pySigHor lo introduce, nosotros no.
- Sección "diferencias con `iniciarSesion()`" para hacer explícita la asimetría (validación, choice point, polimorfismo solo aplican a init).

Índices actualizados: `casos-uso/README.md` 1/26 → 2/26 y `cerrarSesion ⏳ → ✅`; README raíz 1/26 → 2/26.

**Decisión:** Actor `Usuario` queda completamente analizado (2/2 CUs). Próximo paso: arrancar análisis del actor `Administrador` (3 CUs: crearUsuario, consultarUsuario, editarUsuario), donde aparecerán los primeros patrones CRUD del proyecto.

---

### Sesión 2026-05-26

## [09:27] Análisis de `crearUsuario()` — decisión sobre el patrón de Controller

**Prompt:** Arrancar el análisis del Administrador por `crearUsuario` (los otros dos CRUD dependen temporalmente de él). Dame primera aproximación.

**Resultado:** Propuesta inicial con `UsuarioController` compartido entre los 3 CUs del Admin. Tres preguntas previas: controller compartido vs por CU, dónde vive el dispatch polimórfico al crear, y si se crea prototipo SALT (no existe en el requisitado). Tras corregir la asunción de que pySigHor usa "uno por CU" (en realidad usa **uno por entidad**: `ProfesorController` se reutiliza en `crearProfesor` y `editarProfesor`; `IniciarSesionController`/`CerrarSesionController` es una **divergencia nuestra** justificada porque Sesion no es una entidad CRUD), se acordó el patrón híbrido: **Controller por verbo** para sesión, **Controller por entidad** para CRUD de dominio.

Archivos creados en `RUP/01-analisis/casos-uso/crearUsuario/`:

- `colaboracion.puml` — 4 clases en el package (CrearUsuarioView, UsuarioController, UsuarioRepository, Usuario) + 2 colaboraciones (`:Usuarios Abierto` origen, `:Collaboration EditarUsuario` destino vía `<<include>>`). 6 mensajes: validar unicidad → consultar Repository → crear con tipo → persistir con dispatch polimórfico → include editarUsuario.
- `colaboracion.svg` generado y renombrado.
- `README.md` con secciones: clases por estereotipo, mensajes (principal + alternativos login-en-uso/cerrar-sin-guardar), polimorfismo y herencia (mensaje 5 como contraparte de escritura de `validarCredenciales`), **sección "asimetría en la elección de controlador"** justificando los dos patrones, trazabilidad y deudas para diseño.

Índices actualizados: `casos-uso/README.md` 2/26 → 3/26; README raíz `Análisis 2/26 → 3/26`.

**Decisión:**

- **Controller por entidad** (`UsuarioController`) para los 3 CUs del CRUD, coherente con pySigHor. Asimetría con sesión documentada explícitamente en el README como decisión de diseño.
- **Dispatch polimórfico en `UsuarioRepository.crear(tipo, …)`** (no en el Controller): consistente con `validarCredenciales()` que también devuelve subtipos resueltos en el Repository.
- **Sin nuevo prototipo SALT**: la `CrearUsuarioView` se deriva del estado `FormularioRegistro` del detallado y se asume formulario mínimo (tipo + login + contraseña) que delega el resto a `editarUsuario()` vía `<<include>>`.

---

## [09:32] Análisis de `editarUsuario()` — el CU de convergencia del CRUD

**Prompt:** Continuar con editarUsuario.

**Resultado:** Creados `RUP/01-analisis/casos-uso/editarUsuario/{colaboracion.puml, colaboracion.svg, README.md}`. Patrón calcado de pySigHor `editarProfesor` / `editarAula`: **tres colaboraciones de origen** (`:Usuarios Abierto`, `:Collaboration ConsultarUsuario`, `:Collaboration CrearUsuario`) que convergen en una única `EditarUsuarioView`. 5 mensajes: cargar (mensajes 2-3 condicionales según el origen) → modificar → actualizar. Reutiliza `UsuarioController` y `UsuarioRepository` de [[crearUsuario]].

Decisiones de modelado:

- **Sin `<<include>> abrirUsuarios()` al final** (a diferencia de pySigHor `editarProfesor → <<include>> abrirProfesores`): no tenemos un CU `abrirUsuarios` analizado; la vuelta al listado es transición de estado del detallado, no inclusión de CU. Modelar un include a un CU inexistente sería deshonesto.
- **Mensajes 2-3 documentados como condicionales en prosa**: cuando la entrada es desde `crearUsuario` con `usuarioNuevo`, la instancia ya está cargada y la `EditarUsuarioView` no necesita invocar `cargarUsuarioParaEdicion`. Se explica en el flujo alternativo "entrada desde crearUsuario", sin duplicar mensajes en el diagrama.
- **Invariante de subtipo durante la edición**: el `tipo` del usuario no cambia (se fijó en el alta). El polimorfismo solo se usa para que la vista presente campos específicos del subtipo cargado. Esta invariante queda como deuda para diseño ("bloqueo del `tipo` post-alta").

Sección específica "múltiples puntos de entrada" con tabla de los tres orígenes y si necesitan o no los mensajes 2-3, como característica diferenciadora del CU (vs `crearUsuario` con un único origen).

Índices actualizados: `casos-uso/README.md` 3/26 → 4/26 y `editarUsuario ⏳ → ✅`; README raíz `Análisis 3/26 → 4/26`.

**Decisión:** Patrón pySigHor de "CU de edición como punto de convergencia del CRUD" aplicado tal cual. La asimetría con pySigHor (no `<<include>> abrirUsuarios()`) está justificada por la ausencia de ese CU en el requisitado migrado y queda registrada en este log. Siguiente: `consultarUsuario` cierra el bloque Administrador (1 CU restante para 5/26).

---

## [09:39] Análisis de `consultarUsuario()` — cierre del bloque Administrador

**Prompt:** Cerrar el bloque del Administrador con el CU que falta.

**Resultado:** Creados `RUP/01-analisis/casos-uso/consultarUsuario/{colaboracion.puml, colaboracion.svg, README.md}`. Es el CU más compacto del bloque: 4 mensajes, read-only, un único origen (`:Usuarios Abierto`) y un `<<include>>` saliente opcional a `:Collaboration EditarUsuario` (si el Admin decide modificar). Reutiliza `UsuarioController` y `UsuarioRepository` (mismo método `obtenerPorId` introducido en [[editarUsuario]]).

Sección distintiva: **"comparación con los otros CUs del bloque Administrador"** con tabla resumen del CRUD completo (operaciones, puntos de entrada, mensajes al Repository, polimorfismo, includes salientes). Hace explícito el cierre coherente del bloque: crear→editar (siempre), consultar→editar (opcional), editar como convergencia.

Decisiones de modelado:

- **`<<include>>` opcional documentado en prosa**, no como mensaje aparte: el diagrama muestra la dependencia; la opcionalidad vive en el flujo alternativo del README. Coherente con cómo se modeló `cerrarUsuario()` en los otros dos CUs.
- **Sin transición `guardarUsuario()`** en el análisis (a diferencia de los otros dos): la consulta es read-only; la persistencia solo aparece si se entra a editar, y entonces vive en [[editarUsuario]].

Índices actualizados: `casos-uso/README.md` 4/26 → 5/26 y `consultarUsuario ⏳ → ✅`; README raíz `Análisis 4/26 → 5/26`.

**Decisión:** Bloque Administrador completo (3/3 CUs: crear, consultar, editar). El patrón híbrido **Controller por verbo para Sesion / Controller por entidad para CRUD** queda validado en los 5 CUs analizados hasta aquí. Próximo bloque natural: **Profesor** (8 CUs), donde aparecerán los primeros CUs no-CRUD del proyecto (`registrarTomaAsistencia`, `exportarHistorialAsistencias`).

---

## [09:45] Cambio de orden: Alumno + DirectorDeGrado antes que Profesor

**Prompt:** ¿Hay motivo para que el siguiente sea Profesor? Hoy puedo hacer más, pero Profesor (8) es mucho. ¿Puedo hacer Alumno y/o DirectorDeGrado?

**Resultado:** Confirmado que no había razón estructural — propuse Profesor por orden en el índice. Reordenado: **Alumno (3) + DirectorDeGrado (2)** tiene más sentido porque comparten la entidad `SolicitudDispensa` (Alumno la crea, Director la procesa). Misma lógica que se usó con Usuario (crear antes que consultar/editar).

**Decisión:** Hoy: Alumno (3) + Director (2) = 5 CUs → cierra a 10/26 con `SolicitudDispensa` analizada de extremo a extremo. Profesor (8) y Secretaria (8) quedan para sesiones aparte; cuando se llegue a Secretaria, sus 4 CUs de dispensas serán refrito porque la entidad ya estará modelada.

---

## [09:48] Análisis de `crearSolicitudDispensa()` — apertura del bloque Alumno

**Prompt:** Empezar Alumno por crearSolicitudDispensa, ya que los otros dos dependen de que la dispensa exista.

**Resultado:** Creados `RUP/01-analisis/casos-uso/crearSolicitudDispensa/{colaboracion.puml, colaboracion.svg, README.md}`. Plantilla del bloque Administrador aplicada con dos diferencias clave:

1. **Sin polimorfismo**: `SolicitudDispensa` es entidad concreta sin jerarquía. El método del Repository es `crear(alumno, asignatura, periodo, horario)`, sin parámetro `tipo`. Se añade sección explícita "sin polimorfismo (asimetría con crearUsuario)" documentando que `crearUsuario` fue el caso excepcional, no la regla.

2. **Resolución implícita del propietario**: la View envía 3 parámetros al Controller (`asignatura, periodo, horario`), pero el Controller envía 4 al Repository (añade `alumno`). El `alumno` se resuelve desde `Sesion` (creada en [[iniciarSesion]]), no es input externo de la vista. Razón: evita suplantación si el cliente pudiera editar quién es el propietario, y aprovecha que `Sesion` ya conoce al usuario autenticado polimórficamente. Sección dedicada "resolución implícita del Alumno propietario" justifica el contrato del Controller.

Estructura idéntica a `crearUsuario`: 5 mensajes, una colaboración origen (`:Dispensas Abierto`) y una destino (`:Collaboration EditarSolicitudDispensa` vía `<<include>>`). Se introduce `SolicitudDispensaController` (compartido entre los 3 CUs del Alumno) y `SolicitudDispensaRepository`.

Discrepancia detectada y NO arreglada: `Alumno.puml` usa "consultarEstadoDispensa" mientras que el índice y los archivos del detalle usan "consultarSolicitudDispensa". Se documentará al analizar consultar; podría ser un cambio en `Alumno.puml` (sincronizar nombres) o una diferencia semántica real (Alumno consulta "estado" — solo el atributo — vs Director consulta "solicitud" — la entidad completa).

Índices actualizados: `casos-uso/README.md` 5/26 → 6/26 y `crearSolicitudDispensa ⏳ → ✅`; README raíz `Análisis 5/26 → 6/26`.

**Decisión:** `SolicitudDispensa` debutará como **entidad clara de dominio** (a diferencia de `Usuario`, que es más infraestructura). La deuda de "promover al modelo del dominio en 02-diseño" es más directa para esta entidad. Patrón "Controller por entidad" replicado del bloque Admin sin modificaciones.

---

## [09:54] Análisis de `editarSolicitudDispensa()` y `consultarSolicitudDispensa()` — cierre del bloque Alumno

**Prompt:** Hacer los dos restantes del bloque Alumno.

**Resultado:** Cuatro archivos creados:

- `RUP/01-analisis/casos-uso/editarSolicitudDispensa/{colaboracion.puml, colaboracion.svg, README.md}` — 5 mensajes, 3 colaboraciones origen (calcado de [[editarUsuario]]).
- `RUP/01-analisis/casos-uso/consultarSolicitudDispensa/{colaboracion.puml, colaboracion.svg, README.md}` — 4 mensajes, 1 colaboración origen (calcado de [[consultarUsuario]]).

**Especificidades del bloque Alumno (vs bloque Administrador):**

1. **Verificación de propiedad como regla de seguridad** documentada en `editar` y `consultar`: el Alumno autenticado (resuelto vía Sesion) debe coincidir con el `alumno` propietario de la `SolicitudDispensa`. Es la principal asimetría con el bloque Admin, donde no había restricción de propiedad (el Admin opera sobre cualquier usuario). Se identifica como deuda para 02-diseño: la verificación vive en el Controller, no en el Repository, porque desde DirectorDeGrado (próximo bloque) el mismo Repository servirá sin esa restricción.

2. **Discrepancia detectada y documentada formalmente en `consultarSolicitudDispensa`**: `Alumno.puml` etiqueta el CU como `consultarEstadoDispensa()` mientras que el detallado, los prototipos y el índice usan `consultarSolicitudDispensa()`. Razones para adoptar el nombre del detallado: mayoría de artefactos, coherencia con `DirectorDeGrado.ConsultarSolicitudesDispensas` (plural confirma que es la entidad completa, no solo el atributo `estado`). Deuda registrada: posible renombre en `Alumno.puml`. Hipótesis: el nombre `consultarEstadoDispensa` podría ser un eco de un requisito útil (que la ficha muestre el estado pendiente/aprobada/rechazada/justificación) — documentado como decisión abierta para 02-diseño.

3. **Tabla comparativa al final de `consultarSolicitudDispensa`** mostrando que el bloque Alumno tiene **la misma estructura del bloque Admin**: crear→editar (siempre), consultar→editar (opcional), editar como convergencia. Confirma que el patrón CRUD del proyecto es uniforme.

**Decisiones de modelado heredadas del bloque Admin** (sin cambios): Controller compartido por entidad (`SolicitudDispensaController`); tres entradas en editar incluyendo `:Dispensas Abierto` (siguiendo el patrón pySigHor, una pequeña extensión sobre el detallado estricto, justificado por UI con atajo de edición en cada fila); `<<include>>` opcional en consulta documentado en prosa, no como mensaje aparte.

Índices actualizados: `casos-uso/README.md` 6/26 → 8/26 (dos en la misma sesión); README raíz `Análisis 6/26 → 8/26`.

**Decisión:** Bloque Alumno completo (3/3 CUs). La regla de propiedad emerge como concepto transversal de análisis que se manejará en diseño (probablemente como middleware/decorador). Próximo bloque: **DirectorDeGrado** (2 CUs sobre `SolicitudDispensa`, sin restricción de propiedad — son el reverso del bloque Alumno).

---

### Sesión 2026-05-28

## [09:04] Análisis de `consultarSolicitudesDispensas()` — apertura del bloque DirectorDeGrado

**Prompt:** Empezar el último actor con pocos CdU, análisis de "ConsultarSolicitudAsistencia" de DirectorDeGrado (errata por `consultarSolicitudesDispensas`; el actor solo tiene 2 CUs sobre dispensas, no sobre asistencias).

**Resultado:** Creados `RUP/01-analisis/casos-uso/consultarSolicitudesDispensas/{colaboracion.puml, colaboracion.svg, README.md}`. **Patrón master-detail** en un único CU: el alcance es más amplio que el de [[consultarSolicitudDispensa]] del Alumno (que era solo la ficha) — abarca **listado completo + apertura de detalle + transición opcional a edición**. 6 mensajes, 1 colaboración origen (`:Sistema Disponible`) y una destino opcional (`:Collaboration EditarSolicitudDispensa`).

**Especificidades del bloque DirectorDeGrado (vs bloque Alumno):**

1. **Sin filtro de propiedad — asimetría clave**: el Director ve **todas** las solicitudes vía `obtenerTodas()` sin parámetro `alumno`. Confirma la decisión de análisis ya intuida en el bloque Alumno: **la verificación de propiedad vive en el Controller, no en el Repository**, porque desde DirectorDeGrado el mismo Repository sirve sin esa restricción. Si viviera en el Repository, este CU no podría reutilizarlo.

2. **Primera materialización del polimorfismo de Usuario más allá del login**: el comportamiento del `SolicitudDispensaController` debe ramificar según el subtipo de `Sesion.usuario` (Alumno filtra, Director no). Hasta ahora el subtipo de Usuario solo intervenía al construir la Sesion en [[iniciarSesion]]; aquí condiciona la operación de negocio. Tres caminos abiertos para diseño: ramificación explícita por subtipo, estrategia `PoliticaAcceso`, o métodos Controller distintos por rol.

3. **Discrepancia de nombre triple** detectada y documentada: `DirectorDeGrado.puml` usa `consultarSolicitudesDispensa()` (singular `Dispensa`); el detallado, estado interno y prototipos usan `consultarSolicitudesDispensas()` (plural `Dispensas`). Adoptado el plural como canónico (mayoría de artefactos + semántica de "lista de" más coherente). Misma lógica que aplicó [[consultarSolicitudDispensa]] del Alumno frente a `Alumno.puml`. Deuda: renombrar en `DirectorDeGrado.puml`.

4. **El detalle no es un `<<include>>` a otro CU**: el Director no tiene un CU separado `consultarSolicitudDispensa()`; el drill-down al detalle vive **dentro** de este mismo CU (mensajes 4-5). No se reutiliza el CU del Alumno porque tiene verificación de propiedad incompatible. Esto es una asimetría con el patrón pySigHor donde "abrir detalle" suele ser CU propio.

Índices actualizados: `casos-uso/README.md` 8/26 → 9/26 y `ConsultarSolicitudesDispensas() → consultarSolicitudesDispensas() ✅`; README raíz `Análisis 8/26 → 9/26`.

**Decisión:** El bloque DirectorDeGrado arranca con un CU de **mayor alcance** que sus homólogos del Alumno (master-detail en lugar de solo detalle). Patrón pySigHor de "consultar = solo ficha" no se aplica aquí porque el detallado del SDR explícitamente integra listado y detalle en un único flujo. Próximo paso: `editarSolicitudDispensa()` del Director (último CU del bloque, cerrando 10/26 con la entidad `SolicitudDispensa` analizada de extremo a extremo desde ambos roles).

---

## [09:11] Análisis de `editarSolicitudDispensa()` (Director) — cierre del bloque DirectorDeGrado y del ciclo de vida de la dispensa

**Prompt:** Ahora `editarSolicitudDispensa` del Director.

**Resultado:** Creados `RUP/01-analisis/casos-uso/editarSolicitudDispensaDirector/{colaboracion.puml, colaboracion.svg, README.md}` (folder con sufijo `Director` porque el CU comparte nombre canónico con el del Alumno pero la semántica es distinta).

**Por qué análisis separado del Alumno (8 diferencias):** orígenes (3 vs 1), mensajes (5 vs 3), carga previa (condicional vs nunca — siempre llega pre-cargado desde el master-detail de [[consultarSolicitudesDispensas]]), método del Controller (`modificarCampos` vs `modificarVeredicto`), campos editables (motivo/adjuntos vs estado/observaciones), verificación de propiedad (sí vs no), side effects (ninguno vs `fechaResolucion`+`responsable`+notificación al alumno), vista (`EditarSolicitudDispensaView` vs `EditarSolicitudDispensaDirectorView`). Adicionalmente, el requisitado ya distingue dos detallados (`EditarSolicitudDispensa.puml` Alumno vs `EditarSolicitud.puml` Director).

**Especificidades modeladas:**

1. **CU más compacto del bloque dispensas** (3 mensajes): origen → View → Controller → Repository. Sin `cargarSolicitudParaEdicion` ni `obtenerPorId` porque el origen `:Collaboration ConsultarSolicitudesDispensas` ya entrega la `solicitud` cargada en su mensaje 5. Esto es fiel al detallado, que arranca de `SOLICITUD_DISPENSA_ABIERTA_INICIAL` (estado con la solicitud ya abierta).

2. **Side effects en prosa, no como mensajes**: el detallado dice "Sistema actualiza, registra fecha y responsable, notifica al alumno". Decisiones de modelado:
   - `fechaResolucion` y `responsable` (Director que decide, resuelto desde `Sesion.usuario`) los añade el Controller antes del `actualizar()` — implícito, no mensaje aparte. Analogía con `crearSolicitudDispensa` que resolvía `alumno` propietario desde `Sesion`.
   - **Notificación al alumno declarada como deuda explícita para diseño** — no se introduce clase de notificación en análisis porque el detallado no especifica medio ni destinatario técnico. La decisión (evento de dominio + suscriptor / llamada directa / cola) pertenece a diseño.

3. **Refuerza el polimorfismo del Controller por subtipo de `Sesion.usuario`** introducido en [[consultarSolicitudesDispensas]]: ahora son **dos métodos distintos del Controller** por rol (`modificarCampos` Alumno vs `modificarVeredicto` Director). Esto sugiere que de los tres caminos abiertos en el CU anterior, **"métodos específicos por rol"** es probablemente el más limpio (vs ramificación interna o estrategia inyectada). Quedó documentado como hipótesis hacia diseño.

4. **`SolicitudDispensa` gana campos de negocio claros** (`estado`, `observaciones`, `fechaResolucion`, `responsable`) — hace más urgente la deuda de promoverla al modelo del dominio en 02-diseño.

5. **Cierre del ciclo de vida de extremo a extremo**: con este CU, `SolicitudDispensa` queda analizada como primera entidad del proyecto modelada desde dos roles con responsabilidades complementarias (Alumno crea/edita motivos/consulta lo suyo; Director consulta todo/emite veredicto). Esto **valida retroactivamente** la decisión de centralizar la regla de propiedad en el Controller (vs Repository): el mismo Repository es usado por dos roles con políticas opuestas.

Índices actualizados: `casos-uso/README.md` 9/26 → 10/26 y `EditarSolicitud() ⏳` → `editarSolicitudDispensa() (Director) ✅`; README raíz `Análisis 9/26 → 10/26`.

**Decisión:** Bloque DirectorDeGrado completo (2/2 CUs). Los próximos bloques (Profesor 8, Secretaria 8) **reutilizarán SolicitudDispensa** en sus CUs de dispensa correspondientes (Profesor: consultar; Secretaria: crear/consultar/editar/exportar) — el patrón "métodos Controller distintos por rol" se irá afinando ahí. Próximo paso natural: **Profesor (8 CUs)**, donde aparecen los primeros CUs no-CRUD (`registrarTomaAsistencia`, `exportarHistorialAsistencias`) y la entidad `SesionDeClase`.

---

## [09:15] Duda metodológica: por qué los CUs `editar` no modelan colaboración de retorno

**Prompt:** No aparece ninguna colaboración con otro CU desde el editar; no se ve cómo pasar de `editarSolicitudDispensa` a consultarla. ¿Es correcto?

**Resultado:** Explicación de la decisión de modelado consistente en todo el proyecto: los `<<include>>` representan **inclusión de lógica** (un CU usa a otro como sub-actividad), no **transiciones de navegación**. Patrón vigente: `crear → <<include>> editar` (siempre), `consultar → <<include>> editar` (opcional), `editar → (sin destino)` porque es terminal — la vuelta al listado/consulta es un cambio de estado del actor, no inclusión de CU. Esa información ya vive en el detallado (es su rol como state diagram).

**Decisión:** Mantener el diseño actual (status quo). Si en algún momento se quisiera modelar el retorno, se haría con flecha simple sin estereotipo (no como `<<include>>`) y se aplicaría retroactivamente a todos los editar para mantener simetría. Por ahora la división de responsabilidades entre artefactos (análisis = qué objetos colaboran; detallado = en qué estados navega el actor) es coherente con pySigHor y con el resto del proyecto.

---

## [09:24] Análisis de `crearSesionClase()` — apertura del bloque Profesor y entrada de `SesionDeClase`

**Prompt:** Empezar Profesor por `crearSesionClase`, ya que los demás CUs de sesión/asistencia dependen de que exista una sesión de clase.

**Resultado:** Creados `RUP/01-analisis/casos-uso/crearSesionClase/{colaboracion.puml, colaboracion.svg, README.md}`. Estructura: 5 mensajes, 1 colaboración origen (`:Asistencias Abierto`), 1 colaboración destino (`:Sesion Asistencia Abierta` — **estado activo nuevo**, no listado). Introduce las tres clases nuevas del bloque: `CrearSesionClaseView`, `SesionDeClaseController` (reutilizable en los demás CUs del bloque), `SesionDeClaseRepository`, y la entidad `SesionDeClase`.

**Especificidades del bloque Profesor (vs bloques previos):**

1. **Primera ruptura del patrón "crear → editar (siempre)"**: este `crear` configura **todos los campos** en una sola vista (asignatura, grupo, aula, fecha, hora, tema) y termina exitosamente abriendo un **estado activo nuevo** (`SESION_ASISTENCIA_ABIERTA`), no volviendo al listado. No hay `<<include>>` saliente a editar. El detallado lo modela explícitamente con la transición `iniciarSesion()` → `SESION_ACTIVA_FINAL`. Confirma que el patrón "crear → editar" no es regla universal sino consecuencia de cómo se diseñó cada formulario en el requisitado; probablemente `importarListasAlumnos` y `importarMatricula` de Secretaria serán otros contraejemplos.

2. **Colisión de nombre `iniciarSesion()`**: el detallado etiqueta la transición de cierre como `iniciarSesion()` — colisión con el CU `iniciarSesion()` del login (Usuario). **Renombrada en análisis a `iniciarSesionClase()`** para evitar ambigüedad. No es error de ejecución (operaciones distintas) pero sí confunde la lectura del modelo. Deuda para diseño: renombrar en `crearSesionClase.puml` línea 41.

3. **Resolución implícita del Profesor propietario desde `Sesion.usuario`**: idéntico patrón que [[crearSolicitudDispensa]] con el Alumno propietario. View envía 6 parámetros al Controller, Controller envía 7 al Repository (añade `profesor`). Refuerza el patrón de "propietario implícito" como decisión transversal del proyecto.

4. **Discrepancia menor detallado vs prototipo**: el detallado nombra 6 campos (asignatura, grupo, aula, fecha, hora, tema); el prototipo `crearSesionClase1.png` muestra solo 4 visibles (fecha, hora, aula, tema). Explicación: en el prototipo la asignatura es **contexto de la página** (header "Asistencias - Ingeniería de Software I") y el grupo no se ve. Análisis adopta los 6 del detallado para no perder información — decisión de UI sobre cuáles vienen del contexto pertenece a diseño.

5. **`SesionDeClase` no está en el modelo del dominio del SDR**: deuda urgente para diseño (entidad central del bloque). Los catálogos referenciados (`Asignatura`, `Grupo`, `Aula`) tampoco se modelan en análisis — deuda secundaria para decidir si son entidades propias o atributos planos.

Índices actualizados: `casos-uso/README.md` 10/26 → 11/26 y `crearSesionClase() ⏳` → `crearSesionClase() ✅`; README raíz `Análisis 10/26 → 11/26`.

**Decisión:** Abre el bloque Profesor con la entidad `SesionDeClase` y rompiendo el patrón "crear → editar" del proyecto. Próximos CUs naturales: `editarSesionClase`, `registrarTomaAsistencia` (primer CU **no-CRUD** del proyecto), `cerrarSesionClase`, `exportarHistorialAsistencias` (segundo no-CRUD), más los 3 read-only (`consultarListaAlumnos`, `consultarDetalleAlumno`, `consultarSolicitudDispensa` del Profesor).

---

## [09:37] Refactor "Introduce Parameter Object" en `crearSesionClase` — `DatosSesionClase`

**Prompt:** Code smell detectado por el usuario: los métodos tienen 6-7 parámetros (asignatura, grupo, aula, fecha, hora, tema, + profesor). ¿Cómo reducirlo?

**Resultado:** Aplicado el refactor canónico **"Introduce Parameter Object"** (Fowler, *Refactoring*) **solo a `crearSesionClase`** (donde el smell es claro). Cambios:

- **Nueva clase `DatosSesionClase`** (rectángulo naranja dentro del package): value object sin identidad que agrupa los 6 campos de configuración. Conceptualmente distinto de `SesionDeClase` (la entidad persistible).
- **Firmas reducidas**:
  - `validarDatosIniciales(datos) : boolean` (antes 6 params)
  - `crearSesionClase(datos) : SesionDeClase` (antes 6 params)
  - `crear(profesor, datos) : SesionDeClase` (antes 7 params)
- **`profesor` deliberadamente fuera de `DatosSesionClase`**: separar identidad del propietario de los datos del formulario refuerza la regla de no-falseo desde el cliente. El Controller resuelve `profesor` desde `Sesion.usuario` y lo añade en la llamada al Repository.
- **PUML actualizado** con `CrearSesionClaseView .. DatosSesionClase` (relación de construcción) y `SesionDeClaseRepository -- SesionDeClase` (gestión); SVG regenerado.
- **Nueva sección del README** "refactor Introduce Parameter Object" con tabla de antes/después, ganancias (legibilidad, extensibilidad, cohesión, trazabilidad para DTO de transporte) y coste (clase adicional).

**Alcance del refactor en el proyecto:** acordado con el usuario aplicarlo **solo a `crearSesionClase`** por ahora. Decisión sobre los otros `crear`:

| CU | Parámetros máx. | Smell | Decisión |
|-|-|-|-|
| `crearSesionClase` | 7 | Sí | Aplicado |
| `crearSolicitudDispensa` | 4 | Marginal | Pospuesto (deuda blanda) |
| `crearUsuario` | 3 | No | Sin cambios |

**Deuda blanda registrada en el README**: tras completar todos los análisis, hacer revisión transversal del patrón; si se decide uniformar (todos los `crear` con ≥4 parámetros con Parameter Object), introducir retroactivamente `DatosSolicitudDispensa`.

**Decisión:** El refactor emerge orgánicamente del análisis (no de implementación) y captura una abstracción real del dominio. Es el primer refactor aplicado a un análisis ya escrito en este proyecto, y abre la puerta a una revisión transversal futura sin forzarla ahora.

---

## [09:43] Análisis de `editarSesionClase()` y `cerrarSesionClase()` — ciclo de vida operativo de la sesión

**Prompt:** Análisis de editar y cerrar sesión de clase.

**Resultado:** Cuatro archivos creados:
- `RUP/01-analisis/casos-uso/editarSesionClase/{colaboracion.puml, colaboracion.svg, README.md}` — 3 mensajes, 1 origen (`:Sesion Asistencia Abierta`), sin destino.
- `RUP/01-analisis/casos-uso/cerrarSesionClase/{colaboracion.puml, colaboracion.svg, README.md}` — 4 mensajes, 2 colaboraciones (`:Sesion Asistencia Abierta` → `:Asistencias Abierto`).

**Especificidades de `editarSesionClase`:**

1. **Primer CU `editar` cuyo único origen es un estado activo** (no un listado). El detallado lo confirma: `SESION_ACTUAL_INICIAL = SESION_ASISTENCIA_ABIERTA`. No hay carga previa — la entidad ya está en memoria desde [[crearSesionClase]].
2. **Vista in-situ, no modal**: el prototipo muestra los 4 campos editables (Fecha, Hora, Aula, Tema) directamente en la cabecera de la pantalla de asistencias, no en un formulario aparte. Es la primera vista del proyecto con este patrón. Asimetría con todos los editar previos (modal/formulario aparte).
3. **Campos inmutables documentados**: asignatura, grupo, profesor no editables (deuda para forzarlo en diseño con sin setters o validación). El prototipo lo refleja al no mostrar esos campos en la cabecera editable.
4. **Sin Parameter Object**: respetando el alcance acordado, no se introduce `DatosSesionClase` aquí. El parámetro `cambios` queda opaco a nivel análisis.
5. **Cancelación ambigua**: el detallado no contempla cancelación explícita; el prototipo muestra un botón "Volver" cuyo comportamiento en modo edición es deuda para diseño.

**Especificidades de `cerrarSesionClase`:**

1. **Paralelismo conceptual con [[cerrarSesion]] del Usuario**: misma estructura (4 mensajes, origen + destino), niveles distintos (sesión de aula vs sesión de sistema). Valida el patrón "cerrar = transición a estado terminal con efectos de cierre persistidos".
2. **`horaFin` resuelta por el Controller como side effect implícito**: el detallado y el prototipo confirman que la hora no es input del Profesor sino determinada por el sistema. Decisión consistente con la resolución de `responsable`/`fechaResolucion` por el Controller en [[editarSolicitudDispensaDirector]] y de `alumno`/`profesor` propietario en los `crear`. Patrón "auto-poblado por Controller" ya consolidado.
3. **Sin verificación de propiedad**: por construcción, `:Sesion Asistencia Abierta` ya garantiza que es el titular (no se llega a ese estado de otra forma). Análogo al [[cerrarSesion]] del Usuario.
4. **Modal de confirmación**: a diferencia de cerrar la sesión del Usuario que era click directo, aquí el detallado y prototipo exigen confirmación explícita ("Sí, continuar" / "Cancelar"). Refleja la criticidad de la acción (se persiste el cierre).
5. **Cierre del ciclo de vida operativo**: con este CU, una `SesionDeClase` queda analizada desde alta hasta cierre. Solo `registrarTomaAsistencia` (operación principal sobre sesión activa) y `exportarHistorialAsistencias` (read-only post-cierre) quedan en el bloque.

Índices actualizados: `casos-uso/README.md` 11/26 → 13/26; README raíz `Análisis 11/26 → 13/26`. Ambos CUs marcados ✅.

**Decisión:** Bloque "ciclo de vida operativo" del Profesor completo (crear → editar → cerrar). Próximo paso natural: `registrarTomaAsistencia` — **primer CU no-CRUD** del proyecto, donde aparecerán nuevas entidades (`Asistencia`, `Alumno` como dato) y el patrón de operación principal sobre la sesión activa.

---

## [09:47] Análisis de `consultarSolicitudDispensa()` (Profesor) — tercera variante y cierre del polimorfismo del Controller

**Prompt:** Análisis de consultar solicitud dispensa para el Profesor.

**Resultado:** Creados `RUP/01-analisis/casos-uso/consultarSolicitudDispensaProfesor/{colaboracion.puml, colaboracion.svg, README.md}` (folder con sufijo `Profesor` por colisión de nombre canónico con el del Alumno). 3 mensajes, 1 origen (`:Dispensas Abierto`), sin destino.

**Especificidades del Profesor (completando la tríada de roles sobre `SolicitudDispensa`):**

1. **Read-only puro — sin `<<include>>` saliente a editar**: primera consulta del proyecto sin salida a un CU de modificación. El `Profesor.puml` solo tiene `consultarSolicitudDispensa()` en el package "Dispensas" — sin `editar` ni `crear`. Refleja la separación de responsabilidades: el Profesor es **observador** del flujo de dispensas (necesita la información para gestionar asistencias), no participante.

2. **Tercer caso del polimorfismo del Controller por subtipo de `Sesion.usuario`** — completa la tríada:
   - Alumno: ve solo las propias (verificación de propiedad)
   - Profesor: ve las **de sus asignaturas impartidas** (verificación "Profesor competente")
   - Director: ve todas (sin verificación)
   
   Con tres roles operando con políticas distintas sobre el mismo Repository, la opción **"métodos específicos por rol"** (camino (c) abierto en [[consultarSolicitudesDispensas]] y reforzado en [[editarSolicitudDispensaDirector]]) se vuelve la más limpia. Patrón ahora consolidado para diseño.

3. **Vista enriquecida con datos del solicitante**: a diferencia del Alumno (que ya sabe quién es y a qué asignaturas tiene dispensa), el Profesor necesita el contexto: nombre del alumno, grado, curso, lista de asignaturas afectadas con docente/día/hora, fechas múltiples (solicitud, edición, aprobación), comentarios. Nueva vista `ConsultarSolicitudDispensaProfesorView` distinta de la del Alumno.

4. **Nueva relación de dominio detectada**: `Profesor.asignaturasImpartidas` — necesaria para la verificación de acceso. No estaba en `iniciarSesion` (donde `Profesor` era solo subtipo de `Usuario` sin atributos). Deuda nueva para el modelo del dominio.

5. **Campos del prototipo no presentes en el detallado**: "Comentarios", "Fecha de Aprobación" (mostrada como `--/--/--` para pendientes), lista de asignaturas con docente/día/hora. Emergen como atributos del modelo del dominio. Confirma además que el Profesor ve dispensas **en cualquier estado** (no solo aprobadas).

6. **Discrepancia con prototipo gestionada como en el Alumno**: el `Profesor1.png` muestra la lista, pero el actor solo tiene un CU singular. Adoptamos misma decisión: listado pre-existente, no CU separado. Deuda blanda para consistencia con el master-detail del Director.

Índices actualizados: `casos-uso/README.md` 13/26 → 14/26 y `consultarSolicitudDispensa() (Profesor) ⏳` → `✅`; README raíz `Análisis 13/26 → 14/26`.

**Decisión:** Tríada `consultarSolicitudDispensa` cerrada — tres análisis distintos, mismo Repository, tres políticas de acceso. El patrón polimórfico del Controller queda **completamente caracterizado** para que diseño pueda escoger entre los caminos abiertos. Próximo paso natural: `registrarTomaAsistencia` y `exportarHistorialAsistencias` (los dos no-CRUD del Profesor), o los dos read-only restantes (`consultarListaAlumnos`, `consultarDetalleAlumno`).

---

## [09:53] Análisis de `consultarListaAlumnos()` y `consultarDetalleAlumno()` — debut de `Alumno` como entidad con datos propios

**Prompt:** Análisis de consultar lista y detalle de alumnos.

**Resultado:** Cuatro archivos creados:
- `RUP/01-analisis/casos-uso/consultarListaAlumnos/{colaboracion.puml, colaboracion.svg, README.md}` — 3 mensajes, origen `:Listas Abierto`.
- `RUP/01-analisis/casos-uso/consultarDetalleAlumno/{colaboracion.puml, colaboracion.svg, README.md}` — 3 mensajes, origen `:Lista Abierta`.

Ambos read-only puros, sin `<<include>>` saliente. Introducen `AlumnoController` y `AlumnoRepository` (compartidos entre los dos CUs, patrón "Controller por entidad").

**Hallazgos transversales:**

1. **`Alumno` debuta como entidad con datos propios**: hasta ahora era solo subtipo polimórfico de `Usuario` (desde [[iniciarSesion]]) o propietario referenciado en `SolicitudDispensa`. Aquí gana atributos académicos (carnet, grado, curso, estado de matrícula) en la lista, y atributos personales completos en la ficha (nombre, documento, correo, teléfono, descripción, dirección, ocupación, foto). Material rico para enriquecer el modelo del dominio en 02-diseño.

2. **Discrepancia nominal entre detallados**: `consultarListaAlumnos` termina en `LISTA_ABIERTA`, `consultarDetalleAlumno` arranca de `ALUMNOS_ABIERTO`. El prototipo confirma que son el **mismo estado** (la lista de alumnos visible y operable). Análisis los unifica como `:Lista Abierta`. Deuda de reconciliación de nombres en el SDR.

3. **Consolidación del patrón "Profesor competente"**: tercer y cuarto CU del Profesor que aplican el filtro por contexto docente (ya estaba en [[consultarSolicitudDispensaProfesor]]). Documentada la regla general: *cualquier CU del Profesor que cargue datos por asignatura debe validar que el Profesor imparte esa asignatura*. Defensa en profundidad — la UI ya filtra, el Controller revalida.

4. **`consultarListaAlumnos`**:
   - Las **pestañas del prototipo son por asignatura**: el selector emerge de `Sesion.usuario.asignaturasImpartidas`. Cómo se cargan las pestañas se deja como decisión de diseño; el CU recibe `asignatura` como input ya resuelto.
   - El detallado dice "listado de un **curso** específico", el prototipo usa "asignatura". Probable terminología solapada del SDR; no se trata como discrepancia formal.

5. **`consultarDetalleAlumno`** — dos decisiones importantes:
   - **Asistencias como agregado, no como mensaje aparte**: el `obtenerPorId(alumnoId)` retorna un `Alumno` con su lista de asistencias. La sección colapsable del prototipo es UI; el lazy loading se diferiría a diseño si el volumen lo justifica.
   - **Ambigüedad del prototipo gestionada**: muestra asistencias de dos asignaturas distintas, pero análisis aplica filtro "Profesor competente" por consistencia con [[consultarSolicitudDispensaProfesor]]. Deuda: confirmar regla con cliente (filtro estricto vs visibilidad total).

6. **`Asistencia` referenciada pero no formalmente modelada aquí**: aparece como dato en la ficha. Su modelado completo se difiere a [[registrarTomaAsistencia]] (donde se crea).

Índices actualizados: `casos-uso/README.md` 14/26 → 16/26; README raíz `Análisis 14/26 → 16/26`. Ambos CUs marcados ✅.

**Decisión:** Bloque "Listas + Alumnos" del Profesor completo (2/2). Quedan 2 CUs en el bloque: `registrarTomaAsistencia` y `exportarHistorialAsistencias` — los dos **no-CRUD** del proyecto. `Alumno` y `Asistencia` están maduras para promoverse al modelo del dominio.

---

## [10:01] Análisis de `registrarTomaAsistencia()` y `exportarHistorialAsistencias()` — cierre del bloque Profesor y los dos primeros no-CRUD del proyecto

**Prompt:** Análisis de los dos CUs restantes de Profesor.

**Resultado:** Cuatro archivos creados:
- `RUP/01-analisis/casos-uso/registrarTomaAsistencia/{colaboracion.puml, colaboracion.svg, README.md}` — 5 mensajes, debut formal de `Asistencia` como entidad.
- `RUP/01-analisis/casos-uso/exportarHistorialAsistencias/{colaboracion.puml, colaboracion.svg, README.md}` — 4 mensajes, debut del primer **servicio de aplicación** del análisis (`GeneradorArchivoAsistencias`).

Bloque Profesor completo (8/8 CUs).

**Hallazgos de `registrarTomaAsistencia` (CU principal del bloque):**

1. **Debut formal de `Asistencia` como entidad** — referenciada antes en [[consultarDetalleAlumno]], aquí emerge con atributos identificados: `sesion`, `alumno`, `estado` (Presente/Ausente/Tarde — **primer enum del análisis**), `justificacion` opcional. Restricción de unicidad por `(sesionId, alumnoId)`. Nuevo `AsistenciaController` y `AsistenciaRepository`.
2. **Operación granular vs batch — modelado como granular**: cada alumno marcado genera una persistencia individual (`registrarAsistencia` por alumno → `guardar` upsert). No hay "submit final". Coherente con el prototipo del listado de asistencias (checkboxes individuales por fila).
3. **`guardar` como upsert idempotente**: ni `crear` ni `actualizar` — la semántica de "marcar asistencia" es upsert (crea si no existía, actualiza si ya estaba). Primera operación con esta semántica en el proyecto.
4. **Interacción `Asistencia` ↔ `SolicitudDispensa` documentada como deuda crítica**: el prototipo muestra columna "Dispensa" con valor "Dispensado" para algunos alumnos. Tres opciones de modelado documentadas (independencia / pre-marca automática / exclusión del listado) — regla de negocio crítica para diseño.
5. **Vista compartida con la sesión activa**: `RegistrarTomaAsistenciaView` no es ventana nueva, es modo sobre la pantalla de asistencias. Continuidad UX con [[crearSesionClase]] y [[editarSesionClase]] — el wireframe efectivo es el listado de asistencias (sin prototipo dedicado).

**Hallazgos de `exportarHistorialAsistencias` (cierre del bloque):**

1. **Primer servicio de aplicación del análisis**: `GeneradorArchivoAsistencias` — clase distinta de Controller/Repository, con responsabilidad atómica de generar archivo a partir de datos. Color verde (lógica de aplicación) — documentado como deuda blanda introducir un cuarto color/anotación `<<service>>` si emergen muchos.
2. **Aplicación explícita del SRP** (Principio de Responsabilidad Única, IDSW2): tres razones documentadas para separar Controller / Servicio — cohesión, extensibilidad de formatos, testabilidad. Es la primera decisión de diseño OO sólida emergente del análisis.
3. **Discrepancia formatos detallado vs prototipo**: detallado dice "Excel, PDF", prototipo dropdown solo muestra "CSV". Análisis adopta conjunto unión `{Excel, PDF, CSV}`; confirmar con cliente. Deuda registrada.
4. **`AsistenciaController` no genera, delega**: orquesta (recuperar + delegar) pero la transformación vive en el servicio. Patrón generalizable: para futuros exports (`exportarDispensas` de Secretaria), el Controller de la entidad delega a un generador análogo. Evita un "ExportadorController" omnipresente.
5. **`Archivo` como tipo opaco**: cómo se materializa (stream/blob/URL temporal) es decisión de diseño. Buena ocasión para Strategy o jerarquía de generadores polimórficos en 02-diseño.

Índices actualizados: `casos-uso/README.md` 16/26 → 18/26 (ambos ✅); README raíz `Análisis 16/26 → 18/26`.

**Decisión:** Bloque Profesor completo (8/8). Refleja la complejidad real del proyecto:
- 4 CUs de ciclo de vida (crear/editar/cerrar de `SesionDeClase` + registrar asistencia)
- 3 CUs read-only (lista alumnos, detalle alumno, consultar dispensa)
- 1 CU de exportación con servicio dedicado

`Asistencia` y `Alumno` (con datos académicos) son las dos entidades nuevas más críticas para promover al modelo del dominio en 02-diseño. Siguiente bloque natural: **Secretaria (8 CUs)** — donde aparecerán los dos CUs de **importación masiva** (primer cuello no-CRUD de carga) y los 4 CUs de dispensa desde el rol de soporte administrativo. Llegamos a 18/26 (69%) del análisis.

---

### Sesión 2026-05-28 (cont.)

## [10:09] Análisis de `importarListasAlumnos()` e `importarMatriculas()` — apertura del bloque Secretaria con el patrón de carga masiva

**Prompt:** Empezar bloque Secretaria por los dos de importar.

**Resultado:** Cuatro archivos creados:
- `RUP/01-analisis/casos-uso/importarMatriculas/{colaboracion.puml, colaboracion.svg, README.md}` — 4 mensajes, debut de la entidad `Matricula`.
- `RUP/01-analisis/casos-uso/importarListasAlumnos/{colaboracion.puml, colaboracion.svg, README.md}` — 4 mensajes, reutiliza `AlumnoRepository` ya introducido por el Profesor.

Renombrado en el índice: `importarMatricula() ⏳` → `importarMatriculas() ✅` (plural, matches actor + contenido del detallado + prototipos).

**Discrepancias gordas detectadas en el SDR:**

1. **`importarListasAlumnos.puml` tiene contenido equivocado**: su título es "Exportar listado de alumnos", su transición es `exportarListaAlumnos()` y sus sub-estados son de exportación. Es probable error de migración del SDR. Estrategia: modelar el CU **por analogía con `importarMatricula.puml`** (que sí está correcto). Documentación exhaustiva como discrepancia crítica en el README. Reparación del detallado registrada como deuda urgente.
2. **`importarMatricula.puml` está mal nombrado** (singular) cuando el contenido y el actor usan plural. Renombrado en análisis a `importarMatriculas()`. Deuda menor de renombrado del .puml.
3. **Actor `SecretariaAcademica`** en `DiagramaCompletoCasoDeUso.puml` vs `Secretaria` en el resto del proyecto. Análisis adopta `Secretaria` por consistencia.
4. **Notas de los detallados de Secretaria dicen "Alumno solicita..."** (probable copia-pega del bloque Alumno). Deuda menor.
5. **`exportarListadoAlumnosPorCurso.png`** existe como prototipo pero no hay CU correspondiente en el actor — sugiere que la exportación de listas existe pero está sin migrar. **No se modela** (fuera del denominador 26); registrado como deuda.

**Patrón consolidado: "carga masiva = Controller + Servicio Validador + Repository"**

Estructura **idéntica** en ambos CUs (4 mensajes): View → Controller → Validador → Repository. Es el patrón paralelo (inverso) de [[exportarHistorialAsistencias]] del Profesor (Repository → Servicio Generador → Archivo). Categoría operativa "I/O masiva" consolidada con dos casos ya implementados.

**Servicios de aplicación introducidos:**
- `ValidadorArchivoMatriculas` (nuevo, verde)
- `ValidadorArchivoListasAlumnos` (nuevo, verde)

Junto con `GeneradorArchivoAsistencias` ya tenemos **tres servicios** en el análisis — el patrón "Controller orquesta + Servicio especializa" (SRP del temario IDSW2) es ya el modus operandi para operaciones complejas. Deuda blanda: en revisión futura considerar color/anotación específica `<<service>>` para distinguirlos visualmente del Controller.

**Hipótesis de diseño emergente:** la estructura paralela invita a un **`ImportadorMasivo<T>`** abstracto (Template Method) con `ValidadorArchivo<T>` + `Repository<T>` como dependencias. Generalización al 2 elementos → patrón claro. Registrado como deuda hacia 02-diseño.

**Tipos opacos** `InformeImportacion` y `ResultadoValidacion`: value objects efímeros sin clase formal en el análisis. Consistencia con manejo previo de `cambios`, `datos`, `Archivo`. Reutilización confirma que son genéricos (`<T>`) en diseño.

**Entidad `Matricula` debuta** con atributos identificados del prototipo: `numIdentidad`, `alumno`, `curso` (año académico), `grado`, `fechaImportacion`. Deuda urgente: promover al modelo del dominio + resolver política "alumno no existente" (tres opciones documentadas — regla de negocio crítica).

**Dependencia funcional** detectada entre los dos CUs: `importarListasAlumnos` crea/actualiza `Alumno`s, `importarMatriculas` referencia a `Alumno` desde `Matricula` → **debe ejecutarse importarListasAlumnos antes**. Deuda: confirmar orden + política de integridad referencial.

**Múltiples archivos por importación**: el prototipo muestra 3 archivos cargados simultáneamente. Modelado con `archivos` (plural) como parámetro; el Controller invoca **una sola vez** `validar` y `guardarLote` con resultados agregados — atomicidad transaccional y informe único.

**Auto-poblado por Controller** reaplicado: `fechaImportacion = ahora`, `responsable = Sesion.usuario` (Secretaria). Patrón consolidado.

Índices actualizados: `casos-uso/README.md` 18/26 → 20/26 (ambos ✅); README raíz `Análisis 18/26 → 20/26`. Renombrado `importarMatricula()` → `importarMatriculas()` (plural).

**Decisión:** Apertura del bloque Secretaria con los dos CUs de carga masiva. Patrón de importación consolidado, deudas críticas registradas (especialmente la reparación del detallado de `importarListasAlumnos.puml`). Quedan 6 CUs en el bloque: `consultarListaAlumnos` (Secretaria), `consultarDetalleMatricula`, y los 4 de dispensa (crear/consultar/editar/exportar). Estimación: la mayoría serán **refrito** estructural de patrones ya analizados — especialmente los 4 de dispensa, que reutilizarán `SolicitudDispensaController` con cuarta política de acceso del rol Secretaria.

---

## [12:16] Análisis de `crearSolicitudDispensa()` (Secretaria) y `exportarDispensas()` — cuarta política sobre `SolicitudDispensa` y segundo CU de exportación

**Prompt:** Terminar el análisis, empezar por crear y exportar dispensa (Secretaria).

**Resultado:** Cuatro archivos creados:
- `RUP/01-analisis/casos-uso/crearSolicitudDispensaSecretaria/{colaboracion.puml, colaboracion.svg, README.md}` — 5 mensajes, sufijo `Secretaria` para evitar colisión con [[crearSolicitudDispensa]] del Alumno.
- `RUP/01-analisis/casos-uso/exportarDispensas/{colaboracion.puml, colaboracion.svg, README.md}` — 4 mensajes, debut del **tercer servicio de aplicación** del análisis (`GeneradorArchivoDispensas`).

**Especificidades de `crearSolicitudDispensaSecretaria` — ruptura del patrón "propietario implícito":**

1. **El `alumno` propietario es input EXPLÍCITO de la vista**, no resuelto desde `Sesion.usuario`. Es la primera ruptura del patrón "propietario implícito" del proyecto (consolidado desde [[crearSolicitudDispensa]] del Alumno, [[crearSesionClase]] del Profesor, [[importarMatriculas]]). Razón: la Secretaria opera **sobre un tercero**.

2. **Dos relaciones distintas en la entidad** que antes eran la misma persona:
   - `alumno` → titular de la dispensa (visible en la ficha) — input externo
   - `responsable` → quién registró el alta (auditoría) — auto-poblado desde `Sesion.usuario` (la Secretaria)
   
   Cuando un Alumno crea su propia dispensa, ambos campos apuntan a la misma persona. Cuando la Secretaria la crea en su nombre, divergen. Deuda: confirmar si `responsable` se persiste explícitamente o vive en un log de auditoría externo.

3. **Cuarta política del polimorfismo del Controller — cierre de la tetrada**: Alumno (propias) / Profesor (asignaturas impartidas, read-only) / Director (todas, edita veredicto) / **Secretaria (todas, opera en nombre de cualquier Alumno)**. Confirma que **"métodos específicos por rol"** (camino abierto en [[consultarSolicitudesDispensas]]) es el más limpio. Método del Controller deliberadamente nombrado `crearSolicitudDispensaEnNombreDe(...)` para distinguirlo semánticamente del `crearSolicitudDispensa(...)` original.

4. **Mismo Repository sin cambios** (`crear(alumno, asignatura, periodo, horario)` idéntico al del bloque Alumno) — refuerza la decisión consolidada: el Repository es agnóstico al rol, las políticas viven en el Controller.

5. **Vista distinta** (`CrearSolicitudDispensaSecretariaView`) por el selector de Alumno + validación de existencia contra `AlumnoRepository`.

**Especificidades de `exportarDispensas`:**

1. **Segundo CU de exportación del proyecto** (tras [[exportarHistorialAsistencias]] del Profesor) — **valida la hipótesis** anunciada en aquel análisis: el patrón "Controller orquesta + Servicio especializa" se generaliza a una segunda entidad sin abstracciones adicionales. Estructura idéntica: 4 mensajes, mismo flujo (vista → Controller → Repository → Servicio).

2. **`GeneradorArchivoDispensas`** — tercer servicio de aplicación del análisis (tras `GeneradorArchivoAsistencias` y los dos `ValidadorArchivo*`). Con **cuatro CUs de I/O masiva** ya analizados (1 export Asistencia, 1 export Dispensa, 2 import), la abstracción `Generador<T>` / `ImportadorMasivo<T>` (Template Method + servicio inyectable) anunciada en [[importarMatriculas]] gana solidez como hipótesis hacia 02-diseño.

3. **Quinta operación del `SolicitudDispensaController`** sumando 8 métodos en total entre los cuatro roles. Es la entidad **más operada** del proyecto. Deuda crítica para 02-diseño con la imagen completa ahora: (a) partir Controller por rol, (b) Strategy `PoliticaAcceso`, (c) Service de aplicación con métodos por intención.

4. **`obtenerPorFiltros(filtros)` vs `obtenerTodas()`** modelados como métodos distintos del Repository por honestidad con el detallado (Director sin filtros, Secretaria con filtros explícitos). Deuda blanda: unificar como `obtener(filtros?)` en 02-diseño + refactor "Introduce Parameter Object" sobre `filtros` (curso + asignatura + nombre + identificador → `FiltrosDispensa`), análogo al `DatosSesionClase` de [[crearSesionClase]].

5. **Discrepancia crítica en el actor**: `exportarDispensas()` **no aparece** en `DiagramaCompletoCasoDeUso.puml` de Secretaria (que solo lista crear/consultar/editar/guardar/cerrar). Existe detallado y prototipo, por lo que se modela y cuenta en el denominador 26. Deuda urgente registrada: añadir el CU al actor o registrar la decisión inversa.

6. **Drill-down opcional a una solicitud específica** modelado como navegación en prosa (no `<<include>>`) — misma decisión consistente con todos los `consultar→editar` del proyecto.

Índices actualizados: `casos-uso/README.md` 22/26 → 24/26 (ambos ✅); README raíz `Análisis 22/26 → 24/26`.

**Decisión:** Cuatro roles ahora caracterizados sobre `SolicitudDispensa` con políticas opuestas/complementarias compartiendo el mismo Repository. La promoción de `SolicitudDispensa` al modelo del dominio es la deuda **máxima** del proyecto. Quedan 2 CUs del bloque Secretaria: `editarSolicitudDispensa()` y `consultarSolicitudDispensa()` — refritos estructurales del bloque Alumno con la cuarta política ya caracterizada.

---

## [12:22] Análisis de `editarSolicitudDispensa()` y `consultarSolicitudDispensa()` (Secretaria) — cierre del bloque y del análisis (26/26)

**Prompt:** Hacer los 2 CUs faltantes para finalizar la sesión.

**Resultado:** Cuatro archivos creados:
- `RUP/01-analisis/casos-uso/editarSolicitudDispensaSecretaria/{colaboracion.puml, colaboracion.svg, README.md}` — 5 mensajes, 3 colaboraciones origen (calcado de [[editarSolicitudDispensa]] del Alumno).
- `RUP/01-analisis/casos-uso/consultarSolicitudDispensaSecretaria/{colaboracion.puml, colaboracion.svg, README.md}` — 4 mensajes, 1 origen, `<<include>>` opcional a editar Secretaria.

**Hallazgo más relevante: regla emergente sobre "métodos por rol"**

Tras crear (`crearSolicitudDispensaEnNombreDe` con signatura distinta) y editar/consultar (`modificarCampos`/`cargarSolicitud` con misma signatura que el Alumno), emerge una regla clara:

> El patrón "métodos específicos por rol" se aplica **solo cuando la signatura difiere**. Cuando solo la política varía con la misma signatura, un único método con dispatch interno por subtipo de `Sesion.usuario` es más limpio.

Esto **refina la deuda hacia 02-diseño**: de las tres opciones abiertas para materializar el polimorfismo del Controller —((a) métodos por rol, (b) Strategy `PoliticaAcceso`, (c) Controllers especializados)—, la **(b) gana fuerza definitiva** porque la política es ortogonal al método y debería inyectarse, no acoplarse al nombre.

**Especificidades de `editarSolicitudDispensaSecretaria`:**

1. **Estructura idéntica al editar Alumno** (5 mensajes, 3 orígenes) — confirma la separación analítica "forma vs política". Es el caso de uso que más fielmente ilustra esa separación.
2. **Mismo método `modificarCampos`** que el Alumno (vs `modificarVeredicto` del Director, que cambia campos distintos) — primera aplicación práctica de la regla emergente.
3. **Invariante `alumno`** ratificado: ni el Alumno ni la Secretaria pueden transferir una solicitud a otro titular. Si se necesitara, sería CU separado (`reasignarSolicitudDispensa`), no edición.
4. **Auditoría del editor** registrada como deuda (3 opciones: sobreescribir `responsable`, campo `ultimoEditor` separado, log de eventos externo).
5. **Mensajes 2-3 condicionales en prosa** cuando la entrada es desde crear con `solicitudNueva` (misma decisión que el editar Alumno).

**Especificidades de `consultarSolicitudDispensaSecretaria`:**

1. **Cuarta y última política sobre operaciones de lectura** de `SolicitudDispensa`: Alumno (propiedad) / Profesor (asignaturas) / Director (sin restricción) / **Secretaria (sin restricción)**. Tetrada cerrada.
2. **Vista enriquecida con datos del Alumno titular y metadatos de auditoría** — análoga a la del Profesor en [[consultarSolicitudDispensaProfesor]], pero por una razón distinta (la Secretaria no es la titular vs el Profesor no es el dueño).
3. **Salida `Guardar/Cerrar solicitud()` del detallado interpretada como navegación** (no mensaje), pese a estar pintada en rojo en el detallado — color rojo del SDR parece error. Deuda menor.
4. **Discrepancia menor**: el detallado dice "Usuario solicita" en lugar de "Secretaria solicita" — adoptado el rol concreto (coherente con la jerarquía polimórfica del Usuario).
5. **Política de auditoría de accesos** registrada como deuda sensible por RGPD (la Secretaria consulta datos personales de terceros).

**Cierre del análisis — lecciones consolidadas (insumo para 02-diseño)** documentadas en el README de `consultarSolicitudDispensaSecretaria`:

1. MVC con Controller por entidad + Servicio por operación atómica (SRP).
2. Repository agnóstico al rol; política en el Controller.
3. "Métodos específicos por rol" solo cuando la signatura difiere; cuando solo la política varía, Strategy `PoliticaAcceso`.
4. Patrón "Controller orquesta + Servicio especializa" en 4 CUs de I/O masiva — abstracción `Generador<T>` / `ImportadorMasivo<T>` viable.
5. Propietario implícito desde `Sesion.usuario` salvo cuando un rol opera sobre terceros.
6. Auto-poblado de auditoría por el Controller (fechas + responsables).
7. Refactor "Introduce Parameter Object" aplicado donde el smell es claro; candidatos pendientes (`FiltrosDispensa`).
8. Polimorfismo de Usuario materializa la jerarquía de actores como jerarquía de clases.

Índices actualizados: `casos-uso/README.md` 24/26 → **26/26 ✅**; README raíz `Análisis 24/26 → 26/26 ✅`.

**Decisión:** Análisis cerrado al 100%. La entidad `SolicitudDispensa` queda **completamente caracterizada** con 4 roles y 9 operaciones del Controller (`crearSolicitudDispensa`, `crearSolicitudDispensaEnNombreDe`, `modificarCampos`, `modificarVeredicto`, `cargarSolicitud`, `cargarSolicitudParaEdicion`, `obtenerPorAsignaturas`, `obtenerTodas`, `obtenerPorFiltros`, `exportar`). Es la entidad **más operada** del proyecto y la **deuda máxima** para 02-diseño: no está promovida al modelo del dominio del SDR pese a tener cuatro roles operando sobre ella. Próxima fase: arrancar `RUP/02-diseño` con esa promoción como primer paso.

---

### Sesión 2026-05-29

## [09:25] Cambio de modo de trabajo (cascada → ramillete por actor) y elección de stack

**Prompt:** El profesor recordó que RUP no es "todo el análisis → todo el diseño → todo el desarrollo" (eso sería cascada), sino "un ramillete de casos de uso: requisitarlos, analizarlos, **diseñarlos e implementarlos** todos; luego siguiente ramillete". Petición: a partir de ahora, **diseño + implementación por actor seguido**, y **elegir tecnologías** antes de empezar.

**Resultado:** Tres opciones planteadas con trade-offs:
1. **FastAPI + React + SQLite** (recomendada) — separación clara backend/frontend, alineada con la rama `diseño-fastapi-react` de pySigHor (que sirve de referencia metodológica), Python para continuidad con el ecosistema hermano.
2. **Django + plantillas/HTMX** — más rápido a "funciona", pero la magia del framework oculta parte del diseño OO que IDSW2 quiere visible.
3. **Spring Boot + Thymeleaf/React** — clásico de IDSW, muy OO, pero pesado para un solo desarrollador académico.

**Decisión:** Opción 1, además alineada con SigHor. SQLite (no PostgreSQL) para evitar infraestructura — connection string migrable después. El **modo de trabajo iterativo** queda fijado: cerrar diseño + implementación de un actor antes de pasar al siguiente. Próximo paso inmediato: arrancar diseño de Usuario (iniciarSesion, cerrarSesion).

## [09:49] Arranque de fase 02-diseño y diseño completo del actor Usuario (2/26)

**Prompt:** Empezar el diseño con el actor Usuario, como antes (con análogo nivel de detalle al del análisis).

**Resultado:** Estructura de la disciplina creada al estilo de la rama `diseño-fastapi-react` de pySigHor:

- `RUP/02-diseño/README.md` — portada de la disciplina, modo iterativo explicitado, tabla de progreso por actor.
- `RUP/02-diseño/configuracion-proyecto.md` — stack (FastAPI + SQLAlchemy async + JWT/bcrypt; React + TS + Vite + axios + Context), estructura de directorios `src/backend` y `src/frontend`, `pyproject.toml`, `package.json`, `vite.config.ts`, `.env.example`, esquema SQL inicial **solo de `usuarios`** (single-table inheritance con discriminator `tipo`), mapeo análisis → diseño y comandos de desarrollo.
- `RUP/02-diseño/arquitectura.puml` + `.svg` — diagrama C4 de contenedores (SPA / API REST / SQLite / almacén de ficheros).
- `RUP/02-diseño/clases-diseño.puml` + `.svg` — jerarquía Usuario + Sesion + schemas Pydantic + UsuarioRepository + AuthService + AuthRouter. **Crecerá ramillete a ramillete**, no se diseña por adelantado.
- `RUP/02-diseño/casos-uso/README.md` — índice con tabla 26 CUs (2/26 ✅).
- `RUP/02-diseño/casos-uso/iniciarSesion/{README.md, secuencia.puml, secuencia.svg}` — diagrama de secuencia con LoginPage / authService / AuthContext / AuthRouter / AuthService / UsuarioRepository / SQLite + ramas válida/inválida.
- `RUP/02-diseño/casos-uso/cerrarSesion/{README.md, secuencia.puml, secuencia.svg}` — diagrama mínimo: Layout / AuthContext / authService / AuthRouter, con `POST /auth/logout` no-op pero expuesto futuro-proof.

**Decisiones de diseño clave (consolidadas en este ramillete):**

1. **Cambio de notación de análisis → diseño**: de **diagrama de colaboración** (enlaces, intenciones) a **diagrama de secuencia** (orden temporal, tecnología concreta — endpoints HTTP, servicios, BD). Cierre del salto que pySigHor explicita en su rama.
2. **Autenticación stateless con JWT**: la `Sesion` del análisis (concepto emergente) **no se persiste**. Vive como token firmado en `localStorage` + payload validado en cada request. El método `Sesion.cerrar()` se materializa como `localStorage.removeItem` + `setUsuario(null)`. La pregunta abierta del análisis ("¿se promueve `Sesion` al dominio?") se cierra: **no**, queda como concepto técnico.
3. **`validarCredenciales` partido en dos pasos honestos**: `UsuarioRepository.obtener_por_username` (solo I/O) + `verify_password` dentro de `AuthService` (solo criptografía). Aplicación de SRP — el repositorio no debe conocer bcrypt. El nombre `validarCredenciales` desaparece pero la semántica se preserva en `AuthService.autenticar`.
4. **Polimorfismo de Usuario → single-table inheritance** en SQLAlchemy con discriminator `tipo`. Una sola tabla `usuarios`. La multi-herencia de `Administrador` (es Alumno + Profesor + Director + Secretaria) **no se materializa como herencia múltiple en ORM** (no soportada limpiamente) — se materializa como `tipo = "administrador"` + inclusión jerárquica en `AuthService.tiene_rol`.
5. **`POST /auth/logout` expuesto pese a ser no-op hoy** — punto de extensión para blacklist/auditoría sin romper contrato. Una llamada HTTP extra por logout, despreciable.
6. **Sin modal de confirmación** en cerrarSesion (consistente con la decisión explícita del análisis) — divergencia consciente con pySigHor que sí lo lleva.
7. **Token en `localStorage`** (no cookie `HttpOnly`) — trade-off documentado; asumido aceptable para el alcance académico, con expiración corta (60 min) como mitigación.

**Estructura iterativa registrada en `configuracion-proyecto.md`**: cada nuevo ramillete **extiende** `clases-diseño.puml` y el esquema SQL — no los rehace. Próximo ramillete (Administrador: crearUsuario / consultarUsuario / editarUsuario) añadirá schemas de creación/edición, endpoints y política de autorización.

Índices actualizados: README raíz `Diseño 0/26 → 2/26`; `RUP/02-diseño/casos-uso/README.md` 2/26 ✅.

**Decisión:** Usuario cerrado en diseño (2/26). Próximo paso del modo iterativo: **implementar** iniciarSesion + cerrarSesion antes de pasar al ramillete del Administrador.

## [10:10] Simplificación de 02-diseño — corrección de scope

**Prompt:** El diseño de los CUs está bien pero se podría simplificar; en cualquier caso no se entiende el sentido de los archivos extra dentro de `02-diseño/` — con un README similar al de `01-analisis/` debería bastar.

**Resultado:** Borrados los artefactos globales y recortados los READMEs por caso de uso. La disciplina queda al mismo nivel de presupuesto que análisis.

- **Eliminados**: `RUP/02-diseño/configuracion-proyecto.md`, `arquitectura.puml/svg`, `clases-diseño.puml/svg`. Toda la información de stack que vivía en `configuracion-proyecto.md` (pyproject.toml, package.json, vite.config.ts, esquema SQL, comandos `uvicorn`/`npm`) era duplicación de lo que va a existir como código real. El C4 era un diagrama de tres cajas que cabe en una frase. El diagrama de clases también se elimina por la misma razón — las clases se verán en el código.
- **Reescrito** `RUP/02-diseño/README.md` al estilo del de análisis: cambio de notación (colaboración → secuencia), modo iterativo, stack en tabla compacta, link al índice. ~15 líneas frente a las 60 anteriores.
- **Recortados** los dos READMEs de CU: eliminadas las secciones "contratos" (Pydantic schemas completos), "errores y casos no felices", "deudas registradas" y "diferencias entre CUs". Conservado: cabecera, diagrama, participantes, materialización del análisis, decisiones de diseño (3-4 bullets), referencias. De ~7-8 KB cada uno bajan a ~3 KB.

**Decisión:** Las decisiones de diseño de fondo (JWT stateless, split de validarCredenciales por SRP, single-table inheritance para Usuario, no-op logout futuro-proof) **se conservan tal cual**. Lo que cambia es el envoltorio: no se documenta nada que vaya a quedar reflejado en el código. Patrón para los próximos ramilletes: por defecto, **un README por CU + diagrama de secuencia**, sin artefactos globales adicionales salvo que aparezca una razón concreta. Memoria persistente guardada.

## [10:15] Simplificación del diagrama de secuencia de iniciarSesion

**Prompt:** ¿El diagrama de iniciarSesion no se podría simplificar más? cerrarSesion tiene un tamaño más adecuado (aunque influye que el CU sea más simple).

**Resultado:** Diagrama recortado de 24 mensajes a 17, ~56% más pequeño en PUML (1.9 KB → 1.1 KB).

- **Fuera self-calls**: `ASvc -> ASvc : verify_password`, `ASvc -> ASvc : create_access_token`, `LP -> LP : navigate`, `AC -> AC : localStorage.setItem`. Son detalles internos de cada participante, no colaboración real; viven en el README en "decisiones de diseño".
- **Mensajes en una línea** sin `\n`.
- **Bloque `alt` compacto**: la rama de error pasa de 4 mensajes con propagación back-to-back a `raise → 401 → error → mensaje`.
- **Mismos participantes** (LoginPage / authService / AuthContext / AuthRouter / AuthService / UsuarioRepository / SQLite). La complejidad inherente de iniciarSesion frente a cerrarSesion (verificación contra BD, firma JWT) no se puede eliminar honestamente — sigue necesitando Service + Repo + DB. La asimetría con cerrarSesion (4 participantes vs 7) es real, no inflada.

**Decisión:** Política para los siguientes CUs: los diagramas de secuencia muestran **quién habla con quién**, no **qué hace cada uno por dentro**. Las acciones internas (cripto, navegación, persistencia local, validación) se mencionan en el README, no en el diagrama. Self-calls solo si representan un paso del flujo que el lector necesita ver para entender el orden temporal — no como anotación de implementación.

## [10:22] Aplicación de la misma política a cerrarSesion (cohesión entre los dos CUs del actor)

**Prompt:** Hacer lo mismo con cerrarSesion: ya estaba bien de tamaño pero ahora tiene más detalles que iniciarSesion y no es cohesivo entre sí.

**Resultado:** Recortados los detalles equivalentes en cerrarSesion: fuera self-calls `AC -> AC : localStorage.removeItem`, `AC -> AC : setUsuario(null)`, `LY -> LY : navigate("/login")` y la nota inline sobre el endpoint no-op. La explicación de "cerrar sesión = borrar el token del cliente" y la justificación del endpoint expuesto siguen en el README, que es donde tienen sentido.

PUML 526 B (8 mensajes), SVG 12 KB. Asimetría final con iniciarSesion (8 vs 17 mensajes, 4 vs 7 participantes) refleja la complejidad inherente del CU, no la verbosidad del diagrama. Cohesión entre los dos CUs del actor restaurada.

**Decisión:** Política consolidada y memoria persistente actualizada — guardada por separado para que aplique también a los siguientes ramilletes (Administrador, Profesor, etc.).

## [10:45] Implementación del ramillete Usuario — iniciarSesion + cerrarSesion funcionando end-to-end

**Prompt:** Empezar la implementación de los dos CUs.

**Resultado:** Backend (16 ficheros) y frontend (18 ficheros) creados, ambos arrancando y validados vía HTTP. Los 2 CUs cierran el ramillete Usuario (Análisis ✅ 26/26, Diseño 2/26 ✅, Desarrollo 2/26 ✅).

### Backend `src/backend/`

Estructura por capas exactamente como el diseño:

```
app/
├── core/{config,database,security}.py
├── models/usuario.py                  # STI: Usuario + Alumno/Profesor/Director/Secretaria/Administrador
├── schemas/auth.py                    # LoginRequest, TokenResponse, UsuarioOut
├── repositories/usuario_repository.py # obtener_por_username, obtener_por_id
├── services/auth_service.py           # autenticar, emitir_token + excepciones
├── routers/auth.py                    # /auth/{login,logout,me}
├── dependencies.py                    # get_current_user (Bearer + JWT)
└── main.py                            # FastAPI + CORS + lifespan crea tablas
scripts/seed.py                        # 5 usuarios de prueba (admin/profesor1/alumno1/director1/secretaria1)
```

### Frontend `src/frontend/`

Estructura por responsabilidad:

```
src/
├── pages/{LoginPage,DashboardPage}.tsx
├── components/{Layout,RequireAuth}.tsx
├── context/AuthContext.tsx     # token + usuario en localStorage, persiste entre recargas
├── services/{api,authService}.ts  # axios con interceptores (inyecta Bearer, captura 401)
├── types/auth.ts               # DTOs TS espejo de los schemas Pydantic
└── App.tsx / main.tsx          # router + providers
```

### Sustituciones honestas respecto al diseño

| Diseño | Implementación | Motivo |
|---|---|---|
| `python-jose` | `PyJWT` | `python-jose` sin releases activos; PyJWT más simple y mantenida |
| `passlib[bcrypt]` | `bcrypt` directo | `passlib` rompe con `bcrypt ≥ 4.x`; el wrapper aporta poco |

Ambas preservan la decisión de fondo (JWT HS256 + bcrypt con salt). Documentadas en `RUP/03-desarrollo/casos-uso/iniciarSesion/README.md`.

### Incidentes durante la verificación

1. **`EmailStr` rechaza `.local`**: `cgu.local` es TLD reservado. Cambiados los emails del seed a `<usuario>@cgu.es` (España, encaja con el contexto). Validación `EmailStr` del diseño se conserva.
2. **Cache de SQLite tras borrar la BD**: el proceso uvicorn mantenía un file handle al inodo viejo (`@cgu.local`) tras eliminar `cgu.db`. Hizo falta reiniciar uvicorn — no es un bug, es un detalle de cómo Unix gestiona file descriptors de ficheros borrados.

### Verificación end-to-end (HTTP)

Backend (`curl localhost:8000`):
- `POST /auth/login admin/admin123` → 200 + JWT + `tipo: "administrador"`
- `POST /auth/login alumno1/alumno123` → 200 + `tipo: "alumno"` (**polimorfismo STI confirmado**)
- `POST /auth/login admin/WRONG` → 401 `Credenciales no válidas`
- `POST /auth/login nope/x` → 401 `Credenciales no válidas` (mismo mensaje — no filtra existencia)
- `GET /auth/me` con token → 200 con UsuarioOut completo
- `POST /auth/logout` con token → 204
- `POST /auth/logout` sin token → 401 `Token ausente`
- `POST /auth/logout` con token falseado → 401 `Token inválido`

Frontend (`curl localhost:5173`, sirve la SPA + proxy):
- `GET /` → `index.html` con React Refresh ✅
- `POST /api/auth/login` (proxy a backend) → 200 ✅
- TypeScript compila sin errores ✅

Validación a nivel navegador (form → dashboard → botón logout → login) pendiente de prueba manual del usuario. Servidores quedan corriendo en `:8000` y `:5173`.

### Metadatos `RUP/03-desarrollo/`

Creados al estilo del análisis/diseño (espejo de presupuesto):
- `README.md` de disciplina (~20 líneas)
- `casos-uso/README.md` (tabla 26 CUs, 2/26)
- `casos-uso/{iniciarSesion,cerrarSesion}/README.md` con trazabilidad código ↔ diseño y la lista de verificaciones pasadas.

### Comandos de uso

```bash
# Backend
cd src/backend && source .venv/bin/activate
python -m scripts.seed                          # crea 5 usuarios de prueba
uvicorn app.main:app --reload --port 8000       # docs en /docs

# Frontend
cd src/frontend && npm run dev                  # http://localhost:5173
```

**Decisión:** Ramillete Usuario completo (análisis → diseño → desarrollo). El JWT stateless funciona, la jerarquía polimórfica de Usuario se resuelve correctamente desde SQLAlchemy STI, y el frontend conecta vía proxy de Vite. Siguiente ramillete: **Administrador** (`crearUsuario`, `consultarUsuario`, `editarUsuario`) — primer ramillete con autorización por rol (`require_admin` sobre los endpoints), que estresará la decisión del análisis sobre cómo materializar la jerarquía de capacidades.

---

### Sesión 2026-05-30

## [10:32] Diseño de `crearUsuario()` — apertura del ramillete Administrador

**Prompt:** Empezar diseño del Administrador con primera aproximación de `crearUsuario()`. Cinco decisiones abiertas sometidas a voto, las cinco por defecto aceptadas a priori.

**Resultado:** Creados `RUP/02-diseño/casos-uso/crearUsuario/{secuencia.puml, secuencia.svg, README.md}`. Diagrama con 7 participantes (CrearUsuarioPage, usuariosService, UsuariosRouter, require_rol, UsuarioService, UsuarioRepository, SQLite) + actor Administrador. 16 mensajes, `alt` con dos ramas (username libre → 201 + navigate a editar; username en uso → 409 + mensaje inline). Sin self-calls (política consolidada del ramillete Usuario).

**Decisiones de diseño fijadas (las cinco por defecto):**

1. **Validación de unicidad sin pre-check** — un único `POST /usuarios` + `UNIQUE(username)` con captura de `IntegrityError` → 409. Evita endpoint adicional `check-username` y la race condition libre-al-perder-foco / en-uso-al-enviar.
2. **`hash_password` en `core/security`** (no en `AuthService`) — función pura reutilizable desde alta y futuro cambio de contraseña. SRP estricto; `AuthService` ya tenía `verify_password` allí.
3. **Despacho polimórfico con mapa explícito** `{"alumno": Alumno, "profesor": Profesor, ...}` en `UsuarioRepository` en lugar de introspección de `Usuario.__mapper__.polymorphic_map`. Greppeable, falla al añadir subtipo sin actualizarlo (deseable), decisión visible en código.
4. **`require_rol(["administrador"])` paramétrico** desde el primer endpoint protegido — patrón generalizable a `require_rol(["profesor"])`, etc. Sin proliferación de funciones específicas.
5. **Ruta `/usuarios/nuevo`** en lugar de modal — coherencia con `/usuarios/{id}/editar` del siguiente CU, sin problema de "cierro modal sin guardar". La `UsuariosPage` (origen `:Usuarios Abierto`) se omite del diagrama de secuencia por ser ruido UI; la transición al final es `navigate("/usuarios/{id}/editar")` (no `<<include>>` en código).

**Refinamiento sobre el análisis**: el `UsuarioController` del análisis se parte en `UsuariosRouter` (autoriza + valida formato) + `UsuarioService` (hash + reglas de negocio) + `UsuarioRepository` (solo I/O). Mismo split que `AuthRouter` / `AuthService` / `UsuarioRepository` en iniciarSesion.

Índices actualizados: `RUP/02-diseño/casos-uso/README.md` 2/26 → 3/26 y `crearUsuario() ⏳` → `✅`; `RUP/02-diseño/README.md` 2/26 → 3/26; README raíz `Diseño 2/26 → 3/26`.

**Decisión:** `crearUsuario` cerrado en diseño. Próximo paso natural en el modo iterativo: **implementar** `crearUsuario` (backend: `POST /usuarios` con `require_rol`, `UsuarioService.crear`, `UsuarioRepository.crear` con mapa polimórfico, schema `CrearUsuarioRequest`; frontend: `CrearUsuarioPage` en `/usuarios/nuevo`) — o seguir con el diseño de `consultarUsuario` + `editarUsuario` antes para tener el ramillete entero diseñado primero. A confirmar con el usuario.

---

## [10:37] Diseño de `consultarUsuario()` + `editarUsuario()` — cierre del bloque Administrador en diseño

**Prompt:** Seguir con el diseño de los dos CUs restantes antes de implementar (el ramillete entero diseñado antes de pasar a código).

**Resultado:** Creados cuatro archivos:

- `RUP/02-diseño/casos-uso/consultarUsuario/{secuencia.puml, secuencia.svg, README.md}` — 13 mensajes, `alt` con dos ramas (encontrado → 200 + ficha; no existe → 404).
- `RUP/02-diseño/casos-uso/editarUsuario/{secuencia.puml, secuencia.svg, README.md}` — dividido en dos fases con `==` separator: **carga inicial** (12 mensajes, idéntica a consultarUsuario) y **guardar cambios** (13 mensajes, PATCH a través de `UsuarioService`).

**Decisiones de diseño fijadas (defaults aceptados por adelantado):**

1. **`UsuarioService` solo donde hay lógica real** — `consultarUsuario` y la fase de carga de `editarUsuario` van `Router → Repository` directos. La fase de guardado de `editar` sí pasa por Service (hash opcional de contraseña + futuras validaciones). Inversión deliberada respecto a `crearUsuario` (que sí necesita Service por el hash). Justificación: una capa Service que solo reenvía es ruido; el patrón de capas debe seguir la lógica, no una regla uniforme.
2. **Cambio de contraseña como campo opcional del PATCH** — si el body trae `password`, `UsuarioService` lo rehash con `core/security.hash_password` antes del UPDATE. Sin endpoint aparte. Se separará si en algún momento aparece "cambiar mi propia contraseña" como CU del Usuario autenticado (semántica distinta: sujeto vía Bearer, no por id).
3. **`tipo` no editable por contrato** — el campo no existe en `EditarUsuarioRequest`. Pydantic lo descarta si llega. Materialización honesta de la invariante del análisis sin checks en el handler.
4. **`EditarUsuarioPage` siempre hace `GET` fresco** — incluso tras `crearUsuario` (mensaje 6 del análisis). Coste: un round-trip extra. Beneficio: un único code path, sin propagación de estado entre rutas. El flujo alternativo del análisis "entrada desde crearUsuario sin mensajes 2-3" se simplifica deliberadamente en diseño.
5. **`GET /usuarios` (lista) fuera del diagrama** — el CU del análisis es la ficha individual; la lista es endpoint complementario mencionado solo en el README de consultarUsuario. Sin paginación por ahora.
6. **`PATCH /usuarios/{id}` con body parcial** — semántica fiel a "modificar campos"; `None` significa "no tocar". `PUT` exigiría enviar el objeto completo y abriría sobreescritura accidental.
7. **404 honesto en consultarUsuario** — repositorio devuelve `None` → router traduce a HTTP 404 → frontend renderiza estado de error claro. No enmascarar.
8. **Render condicional por subtipo en cliente** — `UsuarioOut` lleva `tipo`; el componente React ramifica. Hoy `UsuarioOut` solo tiene campos comunes; el render condicional queda como punto de extensión documentado, no como código aún.

**Sobre la simetría con `crearUsuario`:** los tres CUs del bloque comparten `require_rol(["administrador"])` (patrón consolidado para el Profesor/Secretaria/Director). El `UsuarioRepository` solo gana un método nuevo (`actualizar`) además de los ya introducidos en sesiones anteriores (`obtener_por_id`, `obtener_por_username`, `crear`).

Índices actualizados: `RUP/02-diseño/casos-uso/README.md` 3/26 → 5/26 (ambos ✅); `RUP/02-diseño/README.md` 3/26 → 5/26; README raíz `Diseño 3/26 → 5/26`.

**Decisión:** Ramillete Administrador completo en diseño (3/3 CUs). Próximo paso del modo iterativo: **implementar los tres CUs juntos** — el alcance es coherente (un `UsuariosRouter` con 4 endpoints `POST/GET/GET-list/PATCH`, un `UsuarioService` con `crear` + `actualizar`, una `usuariosService` en frontend con 3 métodos, tres páginas React `/usuarios/nuevo`, `/usuarios/{id}`, `/usuarios/{id}/editar` + la `UsuariosPage` con el listado). Es la primera vez que se implementan endpoints protegidos por rol — `require_rol` se introduce como dependency genérica reutilizable.

---

## [10:41] Simplificación del diagrama de `editarUsuario` — drop de la fase de carga duplicada

**Prompt:** El diagrama de `editarUsuario` queda más complejo que el resto del bloque; simplificar.

**Resultado:** Recortado de 26 mensajes en dos fases (`== carga inicial ==` + `== guardar cambios ==`) a 14 mensajes en una sola fase. La fase de carga era literalmente idéntica al diagrama de `consultarUsuario` (mismo `GET /usuarios/{id}`, mismo `obtener_por_id`, mismo `require_rol`); modelarla otra vez era ruido.

Cambios concretos:

- **`secuencia.puml`** ahora muestra solo `PATCH /usuarios/{id}` (la novedad real del CU). Sin separadores `==`, sin duplicación.
- **`README.md`** ganó nota explícita debajo del diagrama: "El diagrama muestra solo la fase de guardado; la carga inicial es idéntica a [consultarUsuario] — el `EditarUsuarioPage` reutiliza `usuariosService.obtener(id)` y la misma cadena hasta la BD".
- **Tabla "materialización del análisis"**: la fila de `cargarUsuarioParaEdicion` ahora dice "No representada en el diagrama — reutiliza la secuencia de `consultarUsuario`"; la fila de `modificarCampos` dice "Lo que sí modela el diagrama".

Tamaño final aligned con el resto del bloque: cerrarSesion 8, consultarUsuario 13, editarUsuario 14, crearUsuario 16, iniciarSesion 17. La asimetría restante refleja complejidad inherente, no verbosidad de notación.

**Decisión:** Regla generalizada y guardada en memoria persistente: cuando una fase del CU es idéntica a otro CU ya modelado, no duplicar el diagrama — modelar solo lo específico y referenciar al otro README. Aplica al resto de ramilletes (probablemente reaparecerá en CUs que carguen antes de mutar: `editarSolicitudDispensa`, `editarSesionClase`, etc.).

---

## [10:51] Implementación del ramillete Administrador — 3 CUs end-to-end y app dejada corriendo para prueba manual

**Prompt:** Implementar los tres CUs y, a diferencia de la sesión anterior, dejar la app corriendo + dar instrucciones de prueba manual al usuario.

**Resultado:** Backend + frontend implementados; 15 pruebas internas vía curl pasan; uvicorn (`:8000`) y vite (`:5173`) quedan corriendo en background. Ramillete Administrador completo (Análisis 5/26 ✅, Diseño 5/26 ✅, Desarrollo 5/26 ✅).

### Backend (5 archivos nuevos/modificados)

- `app/dependencies.py` — añadido `require_rol(roles: list[str])` como factory de dependencies (patrón generalizable que se reutilizará en Profesor/Secretaria/Director).
- `app/schemas/usuarios.py` — `CrearUsuarioRequest`, `EditarUsuarioRequest` (sin campo `tipo` + `extra="ignore"` → invariante de subtipo por contrato), `UsuarioDetalleOut`.
- `app/repositories/usuario_repository.py` — añadidos `obtener_todos`, `crear(tipo, ...)` con **mapa explícito `TIPO_A_CLASE`** (decisión del diseño), `actualizar(usuario, cambios)`. Excepción `TipoUsuarioInvalido`.
- `app/services/usuario_service.py` — `UsuarioService.crear` (hash + delega) y `actualizar` (hash opcional + `exclude_unset=True` para body parcial). Excepciones `UsernameEnUso` (captura `IntegrityError`) y `UsuarioNoEncontrado`.
- `app/routers/usuarios.py` — 4 endpoints `GET/POST/GET-id/PATCH` con `dependencies=[Depends(require_rol(["administrador"]))]` a nivel router (autorización uniforme sin repetir en cada handler).
- `app/main.py` — incluye el nuevo router.

### Frontend (8 archivos nuevos/modificados)

- `src/types/usuarios.ts` — DTOs alineados con los schemas Pydantic.
- `src/services/usuariosService.ts` — métodos `listar`, `obtener`, `crear`, `actualizar`.
- `src/pages/UsuariosPage.tsx` — listado con tabla, badges por subtipo (colores), enlaces a ver/editar/nuevo.
- `src/pages/CrearUsuarioPage.tsx` — form con tipo + 5 campos comunes; navega a `/usuarios/{id}/editar` tras 201.
- `src/pages/ConsultarUsuarioPage.tsx` — ficha read-only `<dl>` con metadatos + botón "Editar".
- `src/pages/EditarUsuarioPage.tsx` — GET fresco al montar + función `diff()` cliente-side (PATCH solo con lo cambiado), checkbox `activo`, password opcional, `tipo` mostrado pero `disabled` con explicación.
- `src/components/RequireAuth.tsx` — extendido con prop opcional `roles?: TipoUsuario[]`. Si el usuario autenticado no tiene un rol permitido, redirige a `/dashboard` (no a `/login`, porque sí está autenticado).
- `src/components/Layout.tsx` — link "Usuarios" en la cabecera, visible solo si `usuario.tipo === "administrador"`.
- `src/App.tsx` — 4 rutas nuevas usando un helper `adminOnly(page)` que envuelve en `RequireAuth roles={['administrador']}` + `Layout`.
- `src/index.css` — añadidas clases `.page`, `.page-header`, `.form-card`, `.data-table`, `.tipo-badge` con colores por subtipo, `.ficha` (grid 2-col para metadata).

### Divergencias documentadas respecto al diseño

| Diseño | Implementación | Motivo |
|---|---|---|
| Form de alta mínimo (tipo + username + password) | Form con tipo + username + password + nombre + apellidos + email | `nombre/apellidos/email` son `NOT NULL` en el modelo; pedirlos al alta evita usuarios incompletos. El `<<include>> editarUsuario` sigue activo (redirige tras crear). |

Todas las decisiones de fondo se conservan: mapa polimórfico explícito, `require_rol` paramétrico, 409 por `UNIQUE` con captura, `tipo` invariante por contrato (no por check), GET fresco siempre.

### Verificación interna — 15 pruebas curl

Backend:
- 401 sin token / 403 con token de Alumno / 200 + lista con token de Admin
- 201 crear `profesor2` con datos válidos
- 409 al duplicar `username`
- 200 detalle por id / 404 por id inexistente
- 200 PATCH cambiando nombre y email
- 200 PATCH enviando `tipo` (descartado por Pydantic — `tipo` sigue siendo `"profesor"`) ✅ invariante
- 200 PATCH cambiando password → login con la nueva 200, con la antigua 401 ✅ rehash correcto
- 409 PATCH cambiando username a uno existente
- 404 PATCH a id inexistente

Frontend:
- SPA HTML carga con título correcto
- Proxy `/api/usuarios` reach backend
- Login + listado vía proxy retornan 6 usuarios (5 seed + 1 creado en prueba)

### Decisión nueva guardada en memoria persistente

`feedback-pruebas-manuales` — tras las pruebas internas, dejar uvicorn y vite corriendo en background y dar un guion paso a paso al usuario para validar en navegador. Para esta sesión: URL `http://localhost:5173`, credenciales `admin/admin123` (+ `alumno1/alumno123` para probar 403), 6 pasos del happy path (login → ver lista → crear → editar → consultar → cambiar password → relogin con nueva), 4 edge cases (403 con Alumno; 409 en username duplicado; 404 a `/usuarios/9999`; ver que el `tipo` está bloqueado en el form).

**Decisión:** Ramillete Administrador completo (3/3 desarrollo). Backend y frontend siguen corriendo (bash IDs `bpqa2iuv8` y `b7oa1y52k`). Próximo ramillete natural: **Profesor (8 CUs)** — el más grande y con la mayor variedad estructural (CRUD de sesión de clase, no-CRUD para asistencia, exportación, consultas de listas/detalle).

---

## [11:08] Diseño del ramillete DirectorDeGrado — 2 CUs sobre `SolicitudDispensa` con state machine

**Prompt:** Diseño de los dos CUs del Director. Acordado un round de votos con seis decisiones de fondo; usuario aceptó 1, 3, 5, 6 directamente, pidió aclaración del 4 (polimorfismo del Controller) y ajustó el 2 (enum de estados a 5 valores con `EN_REVISION` y `ANULADA`). Tras la aclaración, confirmó diferir cualquier abstracción polimórfica.

**Resultado:** Creados cuatro archivos:

- `RUP/02-diseño/casos-uso/consultarSolicitudesDispensas/{secuencia.puml, secuencia.svg, README.md}` — master-detail en dos fases (`==`), 23 mensajes. Sin filtros server-side por ahora (Director ve todo); cuando Alumno y Secretaria entren se añadirán query params opcionales `?estado=`, `?alumno=`.
- `RUP/02-diseño/casos-uso/editarSolicitudDispensaDirector/{secuencia.puml, secuencia.svg, README.md}` — solo fase PATCH (la carga se refiere a la fase detalle de consultar, política de no-duplicación). 17 mensajes con `alt` para transición ilegal → 422.

**Saltamos Profesor (8) y Alumno (3)**: Director va antes porque introduce la entidad `SolicitudDispensa` "limpia" (Director no tiene restricciones de propiedad) y permite que cuando Alumno entre, solo añada el caso constreñido. Mismo argumento que ordenó análisis (Alumno → Director). Profesor queda para después.

**Decisión central del ramillete — state machine de `SolicitudDispensa`:**

Cinco estados (`PENDIENTE`, `EN_REVISION`, `APROBADA`, `RECHAZADA`, `ANULADA`) con cinco transiciones legales documentadas en el README de `editarSolicitudDispensaDirector`. Razones aportadas por el usuario para subir de 3 a 5 estados:

1. **`EN_REVISION` ≠ `PENDIENTE`**: "no es lo mismo que el encargado se encuentre activamente revisando la solicitud que que la tenga en la bandeja de entrada". Modela claim explícito por el Director.
2. **`ANULADA` necesaria**: sin ese estado el Alumno no podría cancelar su propia solicitud (UX requirement para el ramillete Alumno futuro).

Implicación para el Director: el CU `editarSolicitudDispensa` modela ahora **dos transiciones** (no una): "iniciar revisión" (`PENDIENTE → EN_REVISION`) + "emitir veredicto" (`EN_REVISION → APROBADA|RECHAZADA`). Un único endpoint `PATCH /dispensas/{id}`; el Service valida la legalidad de la transición desde el estado actual + retorna 422 `TransicionNoValida` si no.

**Decisiones de diseño consolidadas en este ramillete:**

1. **`SolicitudDispensa` debuta como entidad del dominio** — tabla `solicitudes_dispensa`, FKs `alumno_id` y `responsable_id` a `usuarios.id`. Cierre de la deuda máxima del análisis. Atributos: `id, alumno_id, asignatura, periodo, horario, motivo, estado, observaciones, fecha_solicitud, fecha_resolucion (nullable), responsable_id (nullable)`.
2. **Enum `EstadoSolicitud`** con 5 valores y state machine validada en el Service (no en Router ni cliente). Cliente puede ramificar UX (mostrar botón correcto); Service es la autoridad.
3. **`PATCH /dispensas/{id}` único endpoint** para las tres transiciones del Director — coherente con `PATCH /usuarios/{id}`. Body decide la transición; Service valida.
4. **Polimorfismo del Controller diferido** — tras explicar los tres caminos del análisis (métodos por rol / Strategy `PoliticaAcceso` / Controllers especializados) con ejemplos concretos, el usuario decidió no introducir abstracción todavía. Hoy solo el Director; cuando entren Alumno y Secretaria, refactor con tres casos concretos delante. No premature abstraction.
5. **Sin notificación al Alumno por ahora** — análisis registra evento de dominio / cola / email como caminos posibles. Usuario reconoció que sería "buena adición a medio plazo" pero diferida. El Alumno verá nuevo estado al consultar.
6. **`fecha_resolucion` y `responsable_id` auto-poblados por el Service** — patrón consolidado desde `crearUsuario` (Service auto-puebla side effects, cliente no los envía). `responsable_id` se fija en la primera transición `PENDIENTE → EN_REVISION` y no cambia; `fecha_resolucion` solo al alcanzar terminal (`APROBADA`/`RECHAZADA`).
7. **`observaciones` obligatorias al rechazar, opcionales al aprobar** — validado en el Service. Razón: rechazo necesita justificación explícita.

**Sobre la simplificación del editar:** seguimos la política consolidada del ramillete anterior. `EmitirVeredictoPage` siempre hace `GET /dispensas/{id}` fresco al montar (mismo patrón que `EditarUsuarioPage`); la fase de carga no se duplica en el diagrama del editar, se refiere al de consultar.

**Naming decidido implícitamente** (sin pregunta al usuario): backend folder `dispensas`; frontend `dispensasService`, `DispensasPage` (lista), `ConsultarDispensaPage` (ficha), `EmitirVeredictoPage` (form de veredicto en `/dispensas/{id}/veredicto`). Ruta "veredicto" elegida sobre "editar" porque (a) precisa lo que el Director hace; (b) deja libre `/dispensas/{id}/editar` para Alumno futuro (editar motivo/adjuntos). Mismo principio que `/usuarios/{id}/editar` vs futuras rutas específicas.

Índices actualizados: `RUP/02-diseño/casos-uso/README.md` 5/26 → 7/26 (ambos ✅); `RUP/02-diseño/README.md` 5/26 → 7/26; README raíz `Diseño 5/26 → 7/26`.

**Decisión:** Ramillete DirectorDeGrado en diseño completo (2/2). Próximo paso del modo iterativo: **implementar los 2 CUs juntos**. Será el primer ramillete que introduce una entidad de dominio nueva (`SolicitudDispensa`) — añadirá `models/solicitud.py`, `repositories/solicitud_repository.py`, `services/solicitud_service.py`, `routers/dispensas.py`, y nueva sección al `scripts/seed.py` para crear unas solicitudes de prueba en distintos estados (sin esto el Director no tendría nada que ver al loguearse).

---

## [11:17] Simplificación del diagrama de `consultarSolicitudesDispensas` — drop de la fase de listado

**Prompt:** Otra vez veo el de consultar demasiado grande. (El de editar está bien.)

**Resultado:** Recortado de 29 mensajes en dos fases (`== listado ==` + `== detalle ==`) a 16 mensajes en una sola fase. Patrón análogo al recorte de `editarUsuario` en la sesión anterior, pero por una razón ligeramente distinta: el listado de dispensas no es una duplicación de otro CU, pero **sí es estructuralmente idéntico** al patrón genérico de cualquier list endpoint del proyecto (auth → `Repository.obtener_todas` → 200 + lista). Mismo criterio que en `consultarUsuario`, donde el `GET /usuarios` complementario solo se mencionaba en el README.

Cambios concretos:

- **`secuencia.puml`** ahora muestra solo la fase de detalle (`GET /dispensas/{id}`) con `alt` encontrada/404. Sin `==` separadores. Quedan 16 mensajes, alineado con `consultarUsuario` (13 mensajes).
- **`README.md`** — nota debajo del diagrama explicando por qué el listado no aparece y referencia al patrón ya entendido. Eliminada `DispensasPage` de la tabla de participantes (pasa a ser implícita en `dispensasService.listar()`). Tabla "materialización del análisis" reescrita: las filas del listado se marcan "fuera del diagrama" y la del detalle como "lo que sí modela el diagrama" — paraleliza la forma de la tabla del `editarUsuario` simplificado.

Tamaño final del bloque DirectorDeGrado: consultar 16, editar 20. Comparable con el resto: cerrarSesion 8, consultarUsuario 13, editarUsuario 14, crearUsuario 16, iniciarSesion 17. La asimetría restante refleja complejidad inherente, no verbosidad.

**Decisión:** Regla generalizada y guardada en memoria persistente: además de "no duplicar fases idénticas a otro CU", añadido "no modelar fases estructuralmente triviales" — list endpoints genéricos, logins estándar, etc., se documentan en prosa y se reserva el diagrama para lo específico del CU. Aplicable retroactivamente a futuros master-detail (probable que reaparezca en CUs de la Secretaria: `consultarListaAlumnos`, `exportarDispensas` y similares).

---

## [11:24] Implementación del ramillete DirectorDeGrado — entidad `SolicitudDispensa` con state machine

**Prompt:** Implementar los dos CUs del Director.

**Resultado:** Backend + frontend implementados; 15 pruebas internas vía curl pasan; uvicorn (`:8000`) y vite (`:5173`) siguen corriendo. Ramillete DirectorDeGrado completo (Análisis 10/26 ✅, Diseño 7/26 ✅, Desarrollo 7/26 ✅). **Debuta la primera entidad del dominio** (`SolicitudDispensa`) — cierre parcial de la deuda máxima del análisis.

### Backend (6 archivos nuevos + 3 editados)

- `app/models/solicitud_dispensa.py` — modelo nuevo con FKs `alumno_id` y `responsable_id` a `usuarios.id`, enum `EstadoSolicitud` (5 valores), constante `ESTADOS_TERMINALES`, relaciones `lazy="joined"` al alumno y al responsable (eager-load para evitar lazy loading dentro del response serialization).
- `app/schemas/dispensas.py` — `SolicitudDispensaOut` con `AlumnoMinOut` y `ResponsableMinOut` embebidos; `EditarVeredictoRequest` con `estado` (enum) y `observaciones?`.
- `app/repositories/solicitud_dispensa_repository.py` — `obtener_todas` con `.unique()` (necesario por el JOIN del eager-load), `obtener_por_id`, `actualizar`.
- `app/services/solicitud_dispensa_service.py` — set `TRANSICIONES_DIRECTOR` con las 3 transiciones legales del Director; `actualizar` valida transición, auto-puebla `responsable_id` (al entrar EN_REVISION) y `fecha_resolucion` (al alcanzar terminal), exige observaciones al rechazar. Excepciones `SolicitudNoEncontrada`, `TransicionNoValida`, `ObservacionesRequeridas`.
- `app/routers/dispensas.py` — `GET /dispensas`, `GET /dispensas/{id}`, `PATCH /dispensas/{id}`. Cada uno con `Depends(require_rol(["director"]))` en parámetro (no `dependencies=[...]` a nivel router como en `usuarios`, porque el PATCH necesita el `current_user` para pasárselo al Service).
- `app/main.py` — incluye el nuevo router.
- `app/models/__init__.py` — exporta el nuevo modelo (necesario para que `Base.metadata.create_all` lo registre).
- `scripts/seed.py` — nueva función `_seed_dispensas` idempotente que crea 3 solicitudes atribuidas a `alumno1` en estados `PENDIENTE`, `EN_REVISION` (con `responsable_id = director1`), `APROBADA` (con `observaciones` y `fecha_resolucion`). Permite probar las transiciones sin tener que crear datos a mano.

### Frontend (5 archivos nuevos + 3 editados)

- `src/types/dispensas.ts` — `EstadoSolicitud` como union de 5 strings; `ESTADOS_TERMINALES` como `Set` para render condicional; DTOs `SolicitudDispensa`, `AlumnoMin`, `ResponsableMin`, `EditarVeredictoRequest`.
- `src/services/dispensasService.ts` — `listar`, `obtener`, `actualizar`.
- `src/pages/DispensasPage.tsx` — tabla con badge de estado por fila + enlace "Ver".
- `src/pages/ConsultarDispensaPage.tsx` — `<dl>` con todos los campos + badge de estado + botón "Iniciar revisión" o "Emitir veredicto" según estado actual (nada si terminal) + nota "estado terminal" si aplica.
- `src/pages/EmitirVeredictoPage.tsx` — vista dual: si estado PENDIENTE muestra solo botón "Iniciar revisión"; si EN_REVISION muestra textarea de observaciones + dos botones "Aprobar"/"Rechazar" (verde/rojo). Captura el 422 del backend con su `detail` y lo muestra al usuario.
- `src/App.tsx` — helpers `gate(roles, page)`, `adminOnly`, `directorOnly`. Tres rutas nuevas para dispensas.
- `src/components/Layout.tsx` — link "Dispensas" en la cabecera, visible solo si `usuario.tipo === "director"` (paralelo al link "Usuarios" para admin).
- `src/index.css` — clases `.estado-badge` con colores por estado (amarillo PENDIENTE, azul EN_REVISION, verde APROBADA, rojo RECHAZADA, gris ANULADA); estilo para `textarea`.

### Decisiones de implementación notables

- **`Depends(require_rol(["director"]))` en parámetros del handler** (no en `router = APIRouter(..., dependencies=[...])` como en `usuarios.py`). Razón: el PATCH necesita el `current_user` para fijar `responsable_id`; cuando se declara como dependency en el router, FastAPI no la inyecta como parámetro del handler. Trade-off documentado.
- **`Admin no entra como director`** — `require_rol(["director"])` rechaza al usuario admin (verificado con curl: 403). Coherente con la decisión deferida del análisis sobre el polimorfismo Admin. Cuando se quiera permitir Admin como super-user, se cambia a `require_rol(["director", "administrador"])` o se introduce un check más elaborado. Por ahora, **director1/director123** es la cuenta de prueba del Director.
- **Eager-load con `lazy="joined"` en el modelo** — evita el problema clásico de async SQLAlchemy: cuando Pydantic serializa con `from_attributes=True` accede a `.alumno` y `.responsable`; si esas relaciones son lazy, falla porque la sesión async no permite lazy loads implícitos. `lazy="joined"` los carga con JOIN en la consulta original, sin necesidad de declarar `selectinload` en cada query.
- **`.unique().scalars().all()`** en `obtener_todas` — requerido cuando hay JOINs en eager loading, para evitar duplicados de fila por la cardinalidad del JOIN.
- **Datos reseteados antes del cierre** — mis 7 PATCH durante las pruebas dejaron las 3 dispensas en estado terminal. Para que el usuario pueda probar manualmente la state machine se ejecutó `DELETE FROM solicitudes_dispensa` + re-seed. Estados frescos al cierre: `pendiente`, `en_revision`, `aprobada`.

### Verificación interna — 15 pruebas curl

Backend:
- 401 sin token / 403 con Alumno / 403 con Admin / 200 + lista con Director
- 200 detalle con alumno y responsable embebidos / 404 inexistente
- 422 salto inválido `PENDIENTE → APROBADA` directo
- 200 `PENDIENTE → EN_REVISION` (responsable_id fijado)
- 422 rechazar sin observaciones
- 200 aprobar sin observaciones (fecha_resolucion sellada)
- 422 transición desde estado terminal
- 404 PATCH a id inexistente
- 200 rechazar con observaciones (fecha_resolucion sellada + observaciones guardadas)

Frontend:
- SPA carga / proxy vía Vite OK (3 solicitudes retornadas)
- TypeScript compila sin errores

**Decisión:** Ramillete DirectorDeGrado completo (2/2 desarrollo). Próximo ramillete natural: **Alumno (3 CUs sobre `SolicitudDispensa`)** — encaja perfecto porque la entidad ya existe y solo añade la perspectiva del propietario: `crearSolicitudDispensa` (POST), `consultarSolicitudDispensa` (GET con filtro propio), `editarSolicitudDispensa` (PATCH de motivo/adjuntos antes de EN_REVISION + transición `PENDIENTE → ANULADA`). Será la primera vez que el state machine se extiende con transiciones de otro rol (`PENDIENTE → ANULADA` del Alumno) — momento natural para considerar si se introduce ya el patrón `PoliticaAcceso` o se sigue diferiendo.

---

## [15:26] Ramillete Alumno completo — diseño + Strategy `PoliticaAcceso` introducida + implementación end-to-end

**Prompt:** Cierre del bloque de actores pequeños. Diseño + implementación de los 3 CUs del Alumno sobre `SolicitudDispensa`, validando el ciclo completo Alumno→Director→Alumno.

**Resultado:** 3 CUs cerrados en diseño y desarrollo (Análisis 13/26 ✅, Diseño 10/26 ✅, Desarrollo 10/26 ✅). **Primera materialización del polimorfismo del Controller como Strategy** (decisión aplazada en el ramillete Director, ejecutada ahora con los dos casos delante). 16 pruebas internas pasan incluyendo cross-rol y cross-propiedad. Backend y frontend siguen corriendo con datos reseteados a estado seed.

### Diseño (3 archivos × 3 CUs)

- `crearSolicitudDispensa/` — POST nuevo; `alumno_id` auto desde sesión (propietario implícito); navega a `/dispensas/{id}` consulta (no a editar, decisión inversa al patrón `crearUsuario` porque el form ya cubre todo).
- `consultarSolicitudDispensa/` — extiende `GET /dispensas` + `GET /dispensas/{id}` existentes; `PoliticaAlumno.puede_ver` filtra; lista (genérica) fuera del diagrama por la regla "no modelar fases triviales".
- `editarSolicitudDispensa/` — extiende `PATCH /dispensas/{id}` existente; schema unificado con Director; documenta state machine ampliada con `PENDIENTE → ANULADA` (Alumno propietario).

### Strategy `PoliticaAcceso` (decisión de fondo del ramillete)

Nuevo módulo `app/services/politica_acceso.py`:

- `PoliticaAcceso` (ABC) — contrato: `obtener_listado`, `puede_ver`, `transiciones_permitidas`, `campos_editables`, `side_effects`.
- `PoliticaAlumno` — transición `{(PENDIENTE, ANULADA)}`; campos editables `{motivo, horario, asignatura, periodo}` solo si PENDIENTE; sin side effects; listado filtrado por `alumno_id`.
- `PoliticaDirector` — 3 transiciones del veredicto; `observaciones` editable solo en EN_REVISION; side effects (`responsable_id` al entrar EN_REVISION, `fecha_resolucion` al terminal); listado sin filtro.
- `politica_para(usuario)` factory — error si rol no soportado (Profesor/Secretaria llegarán a su ramillete).

`SolicitudDispensaService` refactorizado: delega a la Política, queda como **orquestador puro** (no conoce reglas de rol). Cuando entren Secretaria y Profesor solo añaden `PoliticaSecretaria` / `PoliticaProfesor` sin tocar el Service.

### Schema unificado `EditarSolicitudRequest`

Sustituye al `EditarVeredictoRequest` del Director. Todos los campos opcionales (`estado`, `motivo`, `horario`, `asignatura`, `periodo`, `observaciones`). La Política aplica:
- Alumno: motivo/horario/asignatura/periodo si PENDIENTE; estado a ANULADA si PENDIENTE.
- Director: observaciones si EN_REVISION; estado a EN_REVISION/APROBADA/RECHAZADA según from-state.

Si el cliente envía un campo no permitido para su rol/estado → 422 `CampoNoEditable`.

### Bug arreglado en vivo

Primer borrador del Service saltaba `observaciones` siempre en el loop de campos editables. El Alumno podía enviar `{observaciones: "x"}` y recibir 200 (no-op silencioso) en lugar del 422 esperado. Detectado en prueba #6, fix aplicado: skip de `observaciones` solo cuando `datos.estado is not None` (i.e., cuando vino acompañando una transición). Confirmado tras re-run: 422 `Campo no editable: observaciones`.

### Endpoints (cambios sobre lo ya existente)

| Endpoint | Antes (ramillete Director) | Ahora |
|---|---|---|
| `GET /dispensas` | `require_rol(["director"])` | `["director", "alumno"]` — Service llama a Política |
| `GET /dispensas/{id}` | `["director"]` | `["director", "alumno"]` — Política verifica propiedad |
| `POST /dispensas` | (no existía) | `["alumno"]`, alumno_id desde sesión |
| `PATCH /dispensas/{id}` | `["director"]` + transiciones hardcodeadas | `["director", "alumno"]` + Política decide transiciones/campos |

### Frontend (5 archivos nuevos, 3 editados)

Páginas nuevas:
- `CrearSolicitudPage` (`/dispensas/nuevo`, alumnoOnly) — form 4 campos + 201 → `/dispensas/{id}`.
- `EditarSolicitudPage` (`/dispensas/{id}/editar`, alumnoOnly) — form con diff cliente-side, botón "Cancelar solicitud" con `window.confirm`, campos `disabled` + mensaje si no PENDIENTE.

Páginas ramificadas por rol:
- `DispensasPage` — título "Mis dispensas" vs "Solicitudes de dispensa"; columna "Alumno" oculta si Alumno; botón "+ Nueva solicitud" solo Alumno; mensaje "no tienes solicitudes" si Alumno+vacío.
- `ConsultarDispensaPage` — componente `<Acciones rol={...}>` decide qué botones mostrar (Alumno: Editar si PENDIENTE; Director: Iniciar revisión / Emitir veredicto según estado).

Layout extendido — link "Mis dispensas" para Alumno; mismo path `/dispensas`.

App.tsx — nuevos helpers `alumnoOnly`, `directorOrAlumno`; 5 rutas de dispensas con gates correctos.

### Verificación interna — 16 pruebas curl

Backend:
- 1-2. POST con Director 403; POST con Alumno 201 (alumno_id auto)
- 3-4. Alumno ve solo propias; Director ve todas
- 5. Alumno edita motivo en PENDIENTE → 200
- 6. **Alumno tocando observaciones → 422 (bug + fix)**
- 7. Alumno transición ilegal `aprobada` → 422
- 8. Alumno cancela PENDIENTE → ANULADA → 200
- 9. Editar tras ANULADA → 422 CampoNoEditable
- 10. Re-cancel ANULADA → 422 transición ilegal
- 11. Director ve ANULADA → 200 (sin filtro propietario)
- 12. Alumno `pendiente → en_revision` → 422 (rol equivocado)
- 13. Director toma para revisión solicitud del Alumno → 200, responsable=Carlos
- 14. Alumno edita motivo en EN_REVISION → 422 (PENDIENTE-only)
- 15. Alumno cancela en EN_REVISION → 422 transición ilegal
- 16. Cross-propiedad: Alumno intenta ver/editar dispensa ajena → 403, no aparece en su lista

### Estado tras pruebas (reseteado)

| ID | Asignatura | Estado |
|---|---|---|
| 1 | Ingeniería de Software 2 | PENDIENTE |
| 2 | Diseño de Software | EN_REVISION |
| 3 | Programación I | APROBADA |

Todas a nombre de `alumno1` (María López). Reset hecho con `DELETE FROM solicitudes_dispensa` + re-seed.

**Decisión:** Bloque de 3 actores pequeños (Usuario + Administrador + DirectorDeGrado + Alumno) **cerrado completamente** — 10/26 en las 3 disciplinas. El ciclo de vida completo de `SolicitudDispensa` está implementado de extremo a extremo: Alumno crea → Director revisa → Alumno consulta el resultado. Próximos ramilletes: **Profesor (8) + Secretaria (8)** — los dos "grandes" para sesiones futuras. Strategy `PoliticaAcceso` ya en su sitio para que cuando entren añadan `PoliticaSecretaria` y (no aplica `PoliticaProfesor` porque Profesor solo consulta dispensas, sin escrituras).

---

## [15:35] Cierre de sesión — pregunta del usuario sobre falta de selector de asignatura

**Prompt:** En la creación de solicitud por el Alumno, ¿no falta algo estilo selector de asignaturas matriculadas en lugar de un string libre? ¿Es porque el sistema todavía no está completo o un error intrínseco?

**Resultado:** Respuesta: **(a) sistema incompleto, no error intrínseco**. Explicación detallada de las tres entidades que faltan (`Asignatura`, `Matricula`, `Grupo`/`Aula`/`Horario`) y cómo se cubrirán cuando entren los dos ramilletes grandes:

- **Secretaria → `importarMatriculas`** introducirá la entidad `Matricula` (relación Alumno↔Asignatura↔Periodo) ya documentada como deuda en el análisis de ese CU.
- **Profesor → `crearSesionClase`** introducirá el catálogo `Asignatura` (+ `Grupo`, `Aula`) ya documentados como deuda secundaria en el análisis de ese CU.

Cuando ambas entren, la `CrearSolicitudPage` del Alumno se transformará: input `asignatura` → selector que muestra solo matriculaciones activas del Alumno autenticado; `horario` y `periodo` derivados de la Matricula; FK `matricula_id` reemplaza los strings. Migración pequeña, schema de respuesta y una columna.

Razón de no haberlo hecho así desde el inicio: implementar `SolicitudDispensa` con strings libres permitió cerrar el ciclo Alumno↔Director funcionalmente sin esperar a dos ramilletes grandes. Decisión iterativa consciente.

**Decisión:** Guardado como memoria persistente del proyecto (`project-deuda-asignatura-matricula`) con instrucciones explícitas de qué tocar cuando entre el ramillete Secretaria. Cierre formal de la sesión 2026-05-30: tres ramilletes completos en un día (Administrador 3 + DirectorDeGrado 2 + Alumno 3 = 8 nuevos CUs cerrados en las 3 disciplinas, llevando el proyecto de 2/26 a 10/26 en cada una).

---

## [15:42] Pregunta del usuario: ¿la migración de Asignatura/Matricula va antes o después de los 2 ramilletes restantes?

**Prompt:** Para confirmar, ¿se arregla tras implementar los 2 actores restantes o debería ser lo siguiente a modificar, previo a ellos?

**Resultado:** Respuesta: **ni antes ni después — dentro del ramillete Secretaria**, justo tras `importarMatriculas` (paso 4 del orden interno) y antes de los 4 CUs de dispensa de Secretaria.

Argumentos rechazando las dos alternativas que el usuario planteaba:

1. **No "antes de ambos"** — fixearlo ahora requeriría crear `Asignatura` y `Matricula` como entidades sin sus CUs dueños. Rompería la trazabilidad RUP (cada entidad emerge del análisis del CU que la introduce) y exigiría seed manual de matriculaciones inventadas que habría que tirar cuando Secretaria entre de verdad.
2. **No "tras ambos ramilletes"** — los **4 CUs de dispensa de Secretaria** (crearSolicitudDispensa en nombre de otro, consultar, editar, exportar) heredarían el modelo malo. Implementarlos sobre strings libres y luego migrar 4 CUs es pura deuda compuesta. Además, la Secretaria es **quien gestiona matriculaciones** — que su propio CU no use la `Matricula` que ella misma importa sería absurdo.

**Decisión de orden derivada:** **Secretaria antes que Profesor**. Razón: la Secretaria es la dueña semántica de `Asignatura` + `Matricula` (administración); el Profesor las consume (docencia). Si Profesor va primero, él introduciría `Asignatura` (raro semánticamente) y la dispensa seguiría con strings hasta después.

Orden interno del ramillete Secretaria fijado en memoria persistente:
1. `importarListasAlumnos`
2. `importarMatriculas` (introduce `Matricula` + `Asignatura`)
3. `consultarListaAlumnos` + `consultarDetalleMatricula`
4. **Migración de `SolicitudDispensa`** (interludio, ~30-45 min)
5. Los 4 CUs de dispensa de Secretaria
6. `exportarDispensas`

Después: Profesor (8 CUs) consume el catálogo ya existente.

Memoria `project-deuda-asignatura-matricula` actualizada con esta decisión. Cierre definitivo de la sesión.

---

### Sesión 2026-06-01

## [08:10] Diseño de `importarListasAlumnos()` e `importarMatriculas()` — apertura del ramillete Secretaria

**Prompt:** Empezar el ramillete Secretaria por los dos CUs de importar (paso 1-2 del orden interno fijado en memoria).

**Resultado:** Cuatro archivos creados (puml + svg + README × 2):

- `RUP/02-diseño/casos-uso/importarListasAlumnos/{secuencia.puml, secuencia.svg, README.md}` — 16 mensajes, endpoint `POST /alumnos/importar` multipart.
- `RUP/02-diseño/casos-uso/importarMatriculas/{secuencia.puml, secuencia.svg, README.md}` — 20 mensajes, endpoint `POST /matriculas/importar` multipart.

Round de 4 decisiones de fondo planteado al inicio; el usuario aceptó las 3 primeras por defecto y **corrigió la cuarta** (responsable_id en Matricula).

**Decisiones de diseño fijadas:**

1. **Upsert por `username` sin tocar password** en listas — re-importar el listado anual no destruye credenciales que el alumno ya usa. Solo se actualizan campos no sensibles (nombre, apellidos, email, teléfono).
2. **Política FK estricta + best-effort por registro** en matrículas — si `alumno_username` o `asignatura_codigo` no existen, esa fila va al informe de errores; las válidas se importan igual. **No** se crean alumnos implícitamente — refuerza la dependencia documentada (importarListasAlumnos antes que importarMatriculas).
3. **Catálogo `Asignatura` introducido en este ramillete** sin CU de gestión, sembrado por `scripts/seed.py`. Estructura mínima `{id, codigo, nombre, grado}`. Era el paso anunciado en la memoria `project-deuda-asignatura-matricula`.
4. **`responsable_id` persistido en `Matricula`** por coherencia con `SolicitudDispensa.responsable_id` (corrección del usuario sobre mi default de "no persistir"). Patrón "auditoría visible desde la propia BD" se vuelve regla del proyecto, no decisión ad-hoc por entidad.

**Materialización de las decisiones en el modelo:**

- **`Matricula`** = `(alumno_id, asignatura_id, curso_academico)` + `responsable_id` + `fecha_importacion`. `UNIQUE(alumno_id, asignatura_id, curso_academico)` — una matrícula única por trío; re-importar el mismo CSV produce `IntegrityError` que el Service traduce a error de informe ("matrícula duplicada").
- **`Asignatura`** = `{id, codigo (UNIQUE), nombre, grado}` — catálogo seed; sin CU de gestión administrativa (deuda futura).
- **Más granular que el prototipo del SDR** (que sugería 1 Matricula por grado/curso) — necesario para que en el paso 4 del orden interno `SolicitudDispensa` pueda referenciar matrícula específica de asignatura, no de grado entero.
- **Sin `responsable_id` en `Usuario`** — coherencia local con `crearUsuario` (que tampoco lo lleva). Pero la regla del responsable persistido se mantiene **donde ya existe** para una entidad hermana (la memoria que se guarda).

**Decisiones de tecnología:**

- **Endpoints específicos** `POST /alumnos/importar` y `POST /matriculas/importar` (no `POST /alumnos` batch genérico). Razón: verbo multipart, resultado informe, comportamiento upsert/strict — no encaja en CRUD genérico.
- **CSV con cabecera obligatoria** como formato único en esta fase. Listas: `username,password,nombre,apellidos,email,telefono?`. Matrículas: `alumno_username,asignatura_codigo,curso_academico`. Otros formatos = deuda.
- **`ValidadorArchivo*` consulta repositorios** (no solo formato). Resuelve FKs en una pasada batch (`obtener_por_usernames(set)`, `obtener_por_codigos(set)`) — evita N+1 lookups si el Service hiciera resolución a posteriori.
- **Transacción única por archivo** + `flush` único + informe único por request. Atomicidad documentada como decisión consciente.
- **No nuevo `AlumnoRepository`** — la STI hace que toda la persistencia de Alumno viva en `usuarios`; añadimos `upsert_lote_alumnos` al `UsuarioRepository` existente. El análisis hablaba de `AlumnoRepository` pero en diseño se materializa como método del repo del agregado padre. `AlumnoService` sí es nuevo (orquesta la importación).
- **Header malformado → 422**, **contenido inválido → 200 + informe** con sus errores por fila. Distinción "archivo roto" vs "datos malos en archivo bueno".

**Tamaños de los diagramas:** 16 (listas) vs 20 (matrículas). La asimetría refleja complejidad inherente — matrículas necesita 2 lookups FK adicionales — no verbosidad. Aligned con el resto del bloque (crearUsuario 16, consultarSolicitudesDispensas 16, editar Director 17).

Índices actualizados: `RUP/02-diseño/casos-uso/README.md` 10/26 → 12/26 (ambos ✅); `RUP/02-diseño/README.md` 10/26 → 12/26; README raíz `Diseño 10/26 → 12/26`.

**Decisión:** Apertura del ramillete Secretaria en diseño con los 2 CUs de carga masiva. Memoria nueva guardada (`feedback-auditoria-coherente-por-entidad`). Próximo paso natural del modo iterativo: o seguir el diseño del ramillete (paso 3: `consultarListaAlumnos` + `consultarDetalleMatricula`) o implementar ya los 2 importar para ver `Matricula` y `Asignatura` vivos en código. A confirmar con el usuario.

---

## [08:22] Diseño de `consultarListaAlumnos()` (Secretaria) + `consultarDetalleMatricula()` y refactor del modelo `Matricula` a agregado

**Prompt:** Continuar el ramillete Secretaria con los dos CUs read-only del paso 3 del orden interno.

**Resultado:** Tres salidas — los dos diseños nuevos + un refactor del modelo de `Matricula` hecho horas antes en este mismo ramillete.

### Decisión de fondo del round: refactor del modelo `Matricula`

El análisis de [[consultarDetalleMatricula]] modela `Matricula` como **agregado complejo** con cabecera (alumno + curso académico + facultad + plan_estudios) y colección 1:N de `AsignaturaMatriculada` (con atributo `n_matricula` = 1ª/2ª/3ª convocatoria). El prototipo confirma una ficha por (alumno, curso) con tabla de asignaturas embebida.

Mi diseño de `importarMatriculas` de la entrada anterior había modelado `Matricula` granular `(alumno, asignatura, curso)` — incompatible con la ficha agregada sin una capa de agregación virtual sucia.

Tres opciones planteadas al usuario:
1. **Refactor: header `Matricula` + detalle `AsignaturaMatriculada`** (recomendada, aceptada).
2. Mantener granular + agregado virtual en el detalle.
3. Granular + nueva entidad `MatriculaAgregada` solo de lectura (view SQL).

Razones del refactor frente a las alternativas: `n_matricula` es atributo del detalle (no del header) — modelar agregado lo refleja honestamente; `SolicitudDispensa` migrará a apuntar `AsignaturaMatriculada` (referencia precisa "alumno X intenta dispensar asignatura Y en su matrícula del curso Z"); cambiar ahora es barato (sin código todavía).

### Modelo refactorizado

| Entidad | Campos | Constraint |
|---|---|---|
| `Matricula` (header) | `id, alumno_id FK, curso_academico, responsable_id FK, fecha_importacion` | `UNIQUE(alumno_id, curso_academico)` |
| `AsignaturaMatriculada` (detalle) | `id, matricula_id FK, asignatura_id FK, n_matricula` | `UNIQUE(matricula_id, asignatura_id)` |
| `Asignatura` (catálogo, enriquecida) | `id, codigo UNIQUE, nombre, ects, caracter (enum OB/OP/FB), curso_plan, plan_estudios, facultad` | — |

`facultad` y `plan_estudios` se modelan como strings en `Asignatura` (no entidades propias) — promoción es deuda blanda (YAGNI). En la ficha del detalle se derivan tomando la primera asignatura matriculada del agregado.

CSV de `importarMatriculas` cambia de cabecera: `alumno_username,curso_academico,asignatura_codigo,n_matricula` (4 columnas). Cada fila es un `AsignaturaMatriculada`; el Service hace **get-or-create** del header `Matricula` por `(alumno_username, curso_academico)` la primera vez que aparece esa combinación, y reutiliza el id en filas siguientes.

Informe nuevo distingue `matriculas_creadas` (headers nuevos) vs `asignaturas_matriculadas_creadas` (filas de detalle) — útil para la Secretaria.

Archivos tocados del refactor: `RUP/02-diseño/casos-uso/importarMatriculas/{secuencia.puml, README.md}` (versión 1.0 → 1.1, SVG regenerado).

### Diseños nuevos

- `RUP/02-diseño/casos-uso/consultarListaAlumnosSecretaria/{secuencia.puml, secuencia.svg, README.md}` — 11 mensajes, endpoint `GET /alumnos?page&size&q`.
- `RUP/02-diseño/casos-uso/consultarDetalleMatricula/{secuencia.puml, secuencia.svg, README.md}` — 13 mensajes con `alt` 404, endpoint `GET /matriculas/{id}` retornando agregado completo.

### Decisiones de diseño (defaults aceptados por adelantado)

1. **Sin Service en ninguno de los dos** — patrón consolidado del proyecto (consultarUsuario, consultarSolicitudDispensa): `consultar` read-only va Router → Repository directo. Service solo donde hay reglas de negocio.
2. **Paginación server-side desde el día 1** en `consultarListaAlumnos` (Secretaria). El prototipo del SDR menciona 332 elementos en 24 páginas. Parámetros `?page=&size=`, schema genérico `PaginaOut[T]` (primer endpoint paginado del proyecto, reutilizable). Filtros multicolumna son deuda — hoy solo `?q=` con `LIKE %q%` sobre username/nombre/apellidos/email.
3. **`UsuarioRepository.buscar_alumnos(page, size, q)`** — método específico de la Secretaria, distinto del `obtener_todos` del Admin (que retorna todos los `Usuario`). Una sola firma cubre "listar todo" (q=None) y "buscar libre" (q=valor).
4. **Eager-load del agregado en `consultarDetalleMatricula`**: `selectinload(asignaturas_matriculadas).joinedload(asignatura)` + `joinedload(alumno)` — una request, agregado completo. Evita JOIN cartesiano de un `joinedload` directo a la colección 1:N. Sin paginación de asignaturas dentro del agregado (un plan completo cabe en una respuesta).
5. **`facultad` y `plan_estudios` derivados** de la primera asignatura matriculada del agregado, computados en el Router (no en SQL). Asume coherencia del catálogo (todas las asignaturas de un header pertenecen al mismo plan); si se rompe, se promueve a entidad. Deuda blanda.
6. **Sin paginación de asignaturas matriculadas en el detalle** — un plan de Ingeniería tiene ~40 asignaturas máximo. YAGNI.
7. **Sin defensa en profundidad en el repositorio** — la STI ya garantiza que `buscar_alumnos` filtra por `tipo='alumno'`; `require_rol("secretaria")` autoriza. Coherente con la decisión equivalente en `crearSolicitudDispensa` (Director).
8. **404 honesto** en detalle (`obtener_por_id` retorna `None` → Router traduce a HTTP 404).
9. **Ficha estrictamente read-only** — el actor Secretaria no tiene `editarMatricula` ni `anularMatricula`. Cuando entren los CUs de dispensa de Secretaria podrán aparecer acciones contextuales (iniciar dispensa desde una asignatura matriculada), pero hoy YAGNI.

### Tamaños y simetría

| CU | Mensajes | Comentario |
|---|---|---|
| consultarListaAlumnos (Sec) | 11 | Listado con paginación |
| consultarDetalleMatricula | 13 | Agregado + alt 404 |
| consultarUsuario | 13 | Patrón equivalente |
| importarMatriculas (refactor v1.1) | 20 | Misma estructura, semántica del repository ajustada |

Coherente con el resto del bloque. Asimetría justificada por la presencia/ausencia de `alt` 404.

### Decisiones que se mantienen del v1.0 de importarMatriculas

- Endpoint `POST /matriculas/importar` multipart con `List[UploadFile]`.
- Política FK estricta + best-effort por registro (alumno o asignatura inexistente → fila al informe; el resto se persiste).
- `responsable_id` en el header `Matricula` por coherencia con `SolicitudDispensa.responsable_id` (memoria `feedback-auditoria-coherente-por-entidad`).
- `Asignatura` como catálogo seed sin CU de gestión (ahora con campos enriquecidos: ects, caracter, curso_plan, plan_estudios, facultad).

Índices actualizados: `RUP/02-diseño/casos-uso/README.md` 12/26 → 14/26 (ambos ✅); `RUP/02-diseño/README.md` 12/26 → 14/26; README raíz `Diseño 12/26 → 14/26`.

**Decisión:** Diseño del paso 3 del orden interno cerrado + refactor del paso 2 al modelo agregado. Faltan 4 CUs en el ramillete (dispensa Secretaria + export). Próximo paso natural del modo iterativo: **implementar ya los 4 CUs diseñados del ramillete** (importar listas + matrículas + listado alumnos + detalle matrícula) — todos comparten infraestructura nueva (`Alumno` operacional, `Matricula` agregado, `Asignatura` catálogo) que entra mejor de una sola sentada. La migración de `SolicitudDispensa` (paso 4 del orden interno) podría hacerse en el mismo push de implementación o como interludio inmediatamente posterior.

---

## [08:33] Diseño de los 4 CUs restantes del ramillete Secretaria — cierre del diseño (18/26)

**Prompt:** "haz los 4 que quedan" — terminar el ramillete Secretaria en diseño.

**Resultado:** Cuatro archivos × 3 salidas (puml + svg + README):

- `RUP/02-diseño/casos-uso/crearSolicitudDispensaSecretaria/{secuencia.puml, secuencia.svg, README.md}` — 16 mensajes, `POST /dispensas` con `alumno_id` explícito en body, debuta `PoliticaSecretaria`.
- `RUP/02-diseño/casos-uso/editarSolicitudDispensaSecretaria/{secuencia.puml, secuencia.svg, README.md}` — 16 mensajes, `PATCH /dispensas/{id}` con `alt` 422; fase de carga referida a [[consultarSolicitudDispensaSecretaria]] (regla "no duplicar fases").
- `RUP/02-diseño/casos-uso/consultarSolicitudDispensaSecretaria/{secuencia.puml, secuencia.svg, README.md}` — 16 mensajes con `alt` 404, `GET /dispensas/{id}` con eager-load del agregado.
- `RUP/02-diseño/casos-uso/exportarDispensas/{secuencia.puml, secuencia.svg, README.md}` — 14 mensajes, `GET /dispensas/exportar` con `GeneradorArchivoDispensas` (tercer servicio de aplicación del proyecto).

**Dos defaults aceptados por adelantado** (anunciados al usuario antes de escribir):

1. **Forward-looking design** sobre la migración `SolicitudDispensa → AsignaturaMatriculada` — los 4 diseños asumen la migración hecha y usan FK `asignatura_matriculada_id` (no strings libres). Cada README documenta el prerrequisito en sección dedicada. Coherente con cómo refactorizamos `importarMatriculas` en la entrada anterior antes de tener código.
2. **`exportarDispensas` solo CSV en v1.0** — XLSX/PDF como deuda blanda. Razón: stdlib `csv` cubre el caso sin dependencias, el prototipo del SDR solo muestra CSV en su dropdown, y la abstracción de formato es prematura con un solo caso implementado.

**Decisiones de diseño consolidadas en este round:**

1. **`PoliticaSecretaria` añadida al módulo `politica_acceso.py`** (introducido en el ramillete Alumno). Contrato:
   - `obtener_listado(usuario, alumno_id_filtro?)` — sin filtro de propiedad
   - `puede_ver(...)` → `True` siempre
   - `transiciones_permitidas` → `{(PENDIENTE, ANULADA)}` (puede cancelar pero **no** emitir veredicto)
   - `campos_editables(PENDIENTE)` → `{motivo, asignatura_matriculada_id}` (mismos que Alumno)
   - Sin `side_effects`

2. **Un solo endpoint por verbo, política inyectada por rol** — `POST /dispensas`, `PATCH /dispensas/{id}`, `GET /dispensas/{id}` mantienen una sola firma para los 4 roles. La Strategy del ramillete Alumno se materializa por completo aquí.

3. **Regla emergente del análisis materializada**: "métodos específicos por rol solo cuando la signatura difiere; cuando solo la política varía, dispatch interno por subtipo". Aplicada — Secretaria edita los mismos campos que Alumno con la misma signatura → un solo método del Service con `politica_para(current_user)`. Sin proliferar métodos como `editarComoSecretaria`.

4. **Defensa contra suplantación en `crearSolicitudDispensa`**: si rol Alumno y `alumno_id` en body ≠ `current_user.id`, el Service lo **descarta silenciosamente** (no 4xx). Coherente con `crearUsuario` que descartaba `tipo`. Documentado en el schema con `extra="ignore"` semánticamente (chequeo en el Service).

5. **Validación cruzada `asignatura_matriculada_id` ↔ `alumno_id`**: el Service confirma que `AsignaturaMatriculada.matricula.alumno_id == alumno_id` antes de persistir. Si no, 422 `AsignaturaMatriculadaIncoherente`. Evita que la Secretaria solicite dispensa de asignatura no cursada por el alumno.

6. **`GET /dispensas/exportar` como endpoint dedicado**, no `GET /dispensas?formato=csv`. Razones: semánticas distintas (listado paginado JSON vs archivo completo attachment), el export no respeta paginación, cache/logging/rate-limits pueden divergir.

7. **`GeneradorArchivoDispensas` como tercer servicio de aplicación** del proyecto. Confirma el patrón "Router orquesta + Servicio especializa" introducido conceptualmente desde `exportarHistorialAsistencias` (análisis) y replicado paralelamente en los validadores de import. Abstracción `Generador<T>` **diferida** hasta que entre `GeneradorArchivoAsistencias` (futuro ramillete Profesor) — misma lección del `PoliticaAcceso` (introducido cuando hubo dos casos concretos).

8. **Filtros en `exportarDispensas` como query params simples**: `estado, alumno_id, desde, hasta`. Sin Parameter Object — la deuda blanda `FiltrosDispensa` se mantiene hasta tener un segundo endpoint que los use. Hoy solo `obtener_por_filtros` los consume.

9. **Schema único `SolicitudDispensaDetalleOut` para los 4 roles** — la UI ramifica qué muestra, no el backend. Más simple y mitigado porque el listado ya filtra por permisos antes.

10. **Sin auditoría del editor** en `editar` y sin auditoría de accesos en `consultar` (deudas RGPD del análisis) — diferidas, registradas en cada README. Hoy fuera de scope.

**Cierre del polimorfismo del Controller sobre `SolicitudDispensa`:**

Cuatro roles ahora caracterizados en código con un solo Service, un solo Repository, cuatro políticas. La entidad **más operada del proyecto** queda completamente diseñada. Lecciones aplicadas (insumo del análisis):

- MVC con Controller por entidad + Servicio por operación atómica (SRP).
- Repository agnóstico al rol; política en el Controller/Service.
- "Métodos específicos por rol" solo cuando la signatura difiere; cuando solo la política varía → Strategy `PoliticaAcceso`.
- Auto-poblado de auditoría por el Service.
- Propietario implícito desde sesión salvo cuando un rol opera sobre terceros (Secretaria).

**Tamaños de los diagramas del round:** 16 / 16 / 16 / 14. Coherente con el resto del proyecto (cerrarSesion 8 — el mínimo; iniciarSesion 17 — el más complejo). La uniformidad del bloque dispensa Secretaria refleja que los 4 CUs comparten Service + Politica + Repository — solo difieren en el verbo HTTP.

Índices actualizados: `RUP/02-diseño/casos-uso/README.md` 14/26 → 18/26 (los 4 ✅); `RUP/02-diseño/README.md` 14/26 → 18/26; README raíz `Diseño 14/26 → 18/26`.

**Decisión:** **Ramillete Secretaria completo en diseño (8/8 CUs)**. El proyecto cierra con análisis 26/26 ✅, diseño 18/26 ⏳, desarrollo 10/26 ⏳. Próximo paso del modo iterativo: implementar los 8 CUs del ramillete en un solo push, ordenados según la memoria `project-deuda-asignatura-matricula`:
1. importarListasAlumnos + importarMatriculas (`Matricula` agregado + `Asignatura` catálogo + `AlumnoService`)
2. consultarListaAlumnos (Sec) + consultarDetalleMatricula
3. **Migración `SolicitudDispensa` → `AsignaturaMatriculada`** (interludio crítico)
4. crearSolicitudDispensaSecretaria + editarSolicitudDispensaSecretaria + consultarSolicitudDispensaSecretaria
5. exportarDispensas

Cuando se cierre, el proyecto quedará en diseño 18/26 y desarrollo 18/26 — solo faltará el ramillete **Profesor (8 CUs)** para cerrar 26/26 en las tres disciplinas.

---

## [09:04] Implementación del ramillete Secretaria — 8 CUs end-to-end (18/26)

**Prompt:** "implementalo siguiendo este diseño" — implementar los 8 CUs diseñados del ramillete Secretaria, con la migración `SolicitudDispensa → AsignaturaMatriculada` como interludio según el orden interno acordado.

**Resultado:** Backend (16 archivos nuevos/editados) + frontend (15 archivos nuevos/editados) + 8 READMEs en `RUP/03-desarrollo/`. Las 12 tareas internas (`TaskList`) cierran en verde. Estado del proyecto: **análisis 26/26 ✅, diseño 18/26, desarrollo 18/26**.

### Backend `src/backend/`

Entidades nuevas:
- `app/models/asignatura.py` — catálogo `Asignatura { codigo, nombre, ects, caracter (OB/OP/FB), curso_plan, plan_estudios, facultad }`.
- `app/models/matricula.py` — agregado `Matricula (alumno_id, curso_academico, responsable_id, fecha_importacion)` UNIQUE(alumno, curso) + 1:N `AsignaturaMatriculada (matricula_id, asignatura_id, n_matricula)` UNIQUE(matricula, asignatura). Relaciones `lazy="joined"` (matricula desde AM) y `lazy="selectin"` (asignaturas desde Matricula).
- `app/models/solicitud_dispensa.py` migrada: `asignatura/periodo/horario` strings → `asignatura_matriculada_id` FK con `lazy="joined"`.

Capa de datos:
- `app/repositories/asignatura_repository.py` — `obtener_por_codigos` (batch lookup).
- `app/repositories/matricula_repository.py` — `obtener_por_id` (eager-load del agregado), `listar`, `get_or_create_header`, `crear_detalle` con captura de `IntegrityError`.
- `app/repositories/usuario_repository.py` — `+ obtener_alumnos_por_usernames` (batch lookup), `+ buscar_alumnos(page, size, q?)` con `LIKE %q%` y `count()` para total, `+ upsert_lote_alumnos` sin tocar `password_hash` en existentes.
- `app/repositories/solicitud_dispensa_repository.py` — `_eager()` helper con `joinedload(asignatura_matriculada).joinedload(asignatura)` + `joinedload(matricula)`; `obtener_por_filtros` para el export.

Servicios:
- `app/services/validador_archivo_listas_alumnos.py` — `RegistroAlumnoCrudo`, `CabeceraInvalida` (422), `ResultadoValidacion`. CSV stdlib.
- `app/services/validador_archivo_matriculas.py` — tres pasadas (sintáctico + batch lookup FK + construcción de registros) para evitar N+1.
- `app/services/alumno_service.py` — orquesta validar+upsert; usa `core/security.hash_password` por SRP.
- `app/services/matricula_service.py` — caché local `(alumno_id, curso) → matricula_id` evita re-consultas durante el lote; reporta `IntegrityError` en detalles como "ya matriculada".
- `app/services/generador_archivo_dispensas.py` — `generar_csv(lista) → bytes` con `csv.writer` + BOM `utf-8-sig` para Excel.
- `app/services/politica_acceso.py` — `+ PoliticaSecretaria` (puede_ver=True, transición {(PENDIENTE,ANULADA)}, campos {motivo, asignatura_matriculada_id} en PENDIENTE), factory `politica_para` actualizada.
- `app/services/solicitud_dispensa_service.py` — refactor a FK: `_asignatura_matriculada()` con `joinedload(matricula)`, validación cruzada `am.matricula.alumno_id == alumno_id` (excepción `AsignaturaMatriculadaIncoherente`), defensa contra suplantación (Alumno con `alumno_id` en body → ignora, usa sesión).

Schemas Pydantic:
- `app/schemas/paginacion.py` — `PaginaOut[T]` genérico, `ErrorImportacionOut`, `InformeImportacionAlumnosOut`, `InformeImportacionMatriculasOut`.
- `app/schemas/alumnos.py` — `AlumnoListaItemOut`, `AsignaturaMatriculadaDelAlumnoOut`.
- `app/schemas/matriculas.py` — `MatriculaDetalleOut` con `plan_estudios/facultad` derivados + `asignaturas_matriculadas` embed; `MatriculaListaItemOut`.
- `app/schemas/dispensas.py` — refactor: `asignatura_matriculada` embed reemplaza strings; `CrearSolicitudRequest` añade `alumno_id` opcional (Secretaria) + `asignatura_matriculada_id`; `EditarSolicitudRequest` actualiza campos editables.

Routers:
- `app/routers/alumnos.py` — `GET /alumnos?page&size&q` (Secretaria), `POST /alumnos/importar` (multipart `List[UploadFile]`), `GET /alumnos/{id}/asignaturas-matriculadas` (Alumno propietario o Secretaria, para el selector cascada).
- `app/routers/matriculas.py` — `GET /matriculas`, `POST /matriculas/importar`, `GET /matriculas/{id}`.
- `app/routers/dispensas.py` — ampliado: roles extendidos en `require_rol`, nuevo `GET /dispensas/exportar?estado&alumno_id&desde&hasta`, manejo de excepciones de FK.
- `app/main.py` — registra los dos routers nuevos.

Seed:
- `scripts/seed.py` — `_seed_asignaturas` (5 asignaturas IYA*), `_seed_matricula_alumno1` (matrícula 2025/2026 con 4 detalles), `_seed_dispensas` migrado a usar `asignatura_matriculada_id`.

### Frontend `src/frontend/`

Types:
- `types/paginacion.ts`, `types/alumnos.ts`, `types/matriculas.ts` nuevos.
- `types/dispensas.ts` refactor: `asignatura_matriculada` embed reemplaza strings; `FiltrosDispensa` añadido.

Services:
- `services/alumnosService.ts` — `listar`, `importar` (FormData multipart), `asignaturasMatriculadas`.
- `services/matriculasService.ts` — `listar`, `obtener`, `importar`.
- `services/dispensasService.ts` — `+ exportar(filtros)` con `responseType: 'blob'`.

Páginas nuevas:
- `pages/AlumnosPage.tsx` — listado paginado con búsqueda, paginador inferior.
- `pages/ImportarListasAlumnosPage.tsx` — dropzone multi-archivo + tabla de informe.
- `pages/MatriculasPage.tsx` — listado de matrículas.
- `pages/ImportarMatriculasPage.tsx` — dropzone + informe con dos contadores.
- `pages/ConsultarDetalleMatriculaPage.tsx` — ficha del agregado con tabla embebida de asignaturas matriculadas.
- `pages/CrearSolicitudDispensaSecretariaPage.tsx` — autocomplete de alumno (≥2 chars, debounce 200 ms) → selector cascada de asignaturas matriculadas → motivo.

Páginas adaptadas al nuevo modelo:
- `pages/CrearSolicitudPage.tsx` — usa `alumnosService.asignaturasMatriculadas(usuario.id)` para el selector.
- `pages/EditarSolicitudPage.tsx` — selector de asignatura matriculada; diff client-side actualizado.
- `pages/ConsultarDispensaPage.tsx` — ficha enriquecida (código, ECTS, carácter, convocatoria, plan/facultad); rol Secretaria gana botón "Editar" si PENDIENTE.
- `pages/DispensasPage.tsx` — botones "+ Nueva en nombre de" y "Exportar CSV" para Secretaria; descarga vía `URL.createObjectURL`.
- `pages/EmitirVeredictoPage.tsx` — muestra código+nombre de asignatura en lugar de string.

Layout & rutas:
- `components/Layout.tsx` — links Alumnos/Matrículas/Dispensas para Secretaria.
- `App.tsx` — helpers `secretariaOnly`, `alumnoOSecretaria`, `lectura`; 6 rutas nuevas; `/dispensas/:id/editar` abierto a Alumno+Secretaria; `/dispensas/nuevo-en-nombre-de` Secretaria.

### Bug arreglado en vivo

Primer test `POST /dispensas` con Secretaria → 500. Causa: `session.get(AsignaturaMatriculada, id)` no carga relaciones; el Service accedía a `am.matricula.alumno_id` lo que disparaba lazy load en sesión async → `sqlalchemy.exc.MissingGreenlet`. Fix: cambiar a query explícito con `joinedload(AsignaturaMatriculada.matricula)` + añadir `lazy="joined"` también a la relación back-ref en el modelo (defense in depth). Confirmado 201 tras el fix.

### Verificación interna — pruebas curl

Backend (`localhost:8000`):
- 401 sin token / 403 con token de Alumno sobre `/alumnos`
- `POST /alumnos/importar` con CSV 3 filas (2 válidas + 1 con `nombre` vacío) → `{creados:2, actualizados:0, errores:[{fila:4,mensaje:"campo 'nombre' obligatorio"}]}`
- `POST /matriculas/importar` con CSV 5 filas (3 válidas + alumno desconocido + asignatura desconocida) → `{matriculas_creadas:2, asignaturas_matriculadas_creadas:3, errores:[{fila:5,mensaje:"alumno desconocido: 'fantasma'"}, {fila:6,mensaje:"asignatura desconocida: 'XYZ'"}]}`
- `GET /alumnos?q=López` → filtra correctamente
- `GET /matriculas/1` → agregado completo con plan/facultad derivados + 4 asignaturas matriculadas
- `POST /dispensas` Secretaria con `alumno_id=6, asignatura_matriculada_id=1` (de otro alumno) → 422 `AsignaturaMatriculadaIncoherente`
- `POST /dispensas` Secretaria con FK coherente → 201
- Director NO puede exportar (403), Secretaria SÍ (200)
- Alumno NO puede listar alumnos (403)

Frontend (`localhost:5173`, vía proxy):
- TypeScript compila limpio (`npx tsc --noEmit` sin errores)
- Login Secretaria + listar alumnos + detalle matricula vía proxy `/api/...` → todos 200

### Estado de la BD reseteada al cierre

| Usuarios seed | 5 (admin, profesor1, alumno1, director1, secretaria1) |
| Asignaturas catálogo | 5 (IYA010 Programación I, IYA020 Programación II, IYA038 Ing. SW I, IYA040 Ing. SW 2, IYA041 Diseño de Software) |
| Matrículas | 1 (alumno1 · 2025/2026 · 4 asignaturas matriculadas) |
| Dispensas | 3 (PENDIENTE IYA040, EN_REVISION IYA041, APROBADA IYA010) |

### Guion de prueba manual

URL: http://localhost:5173 — uvicorn (`b7wpwmd34`) y vite (`bgi5nxli2`) siguen corriendo en background.

Credenciales:
- `secretaria1` / `secre123` — actor principal del ramillete
- `alumno1` / `alumno123` — para probar perspectiva Alumno
- `director1` / `director123` — para probar 403 en exportar

Camino feliz Secretaria (10 pasos):
1. Login `secretaria1`/`secre123` → dashboard.
2. Cabecera: links "Alumnos", "Matrículas", "Dispensas" visibles.
3. **Alumnos**: ver lista con `alumno1` (1 de 1, paginador "Página 1 de 1").
4. Click "Importar listas" → cargar un CSV con cabecera `username,password,nombre,apellidos,email,telefono` y 2-3 filas → ver informe con creados/actualizados.
5. Volver a "Alumnos" → la lista crece. Probar búsqueda libre por apellido.
6. **Matrículas** → ver 1 fila (alumno1, 2025/2026). Click "Ver" → ficha con tabla de 4 asignaturas matriculadas (códigos IYA*, ECTS, carácter).
7. Click "Importar matrículas" → cargar CSV `alumno_username,curso_academico,asignatura_codigo,n_matricula` → informe con dos contadores (headers vs detalles).
8. **Dispensas** → ver las 3 seed. Click "+ Nueva en nombre de" → buscar `alumno2` (si lo importaste), seleccionar, elegir asignatura matriculada del cascada, escribir motivo, crear.
9. Click "Editar" en una dispensa PENDIENTE → cambiar el motivo o cancelar la solicitud (botón rojo).
10. "Exportar CSV" en `/dispensas` → descarga `dispensas-2026-06-01.csv` con todas las columnas.

Edge cases a verificar:
- Login con `alumno1` → solo ve "Mis dispensas". `/alumnos` y `/matriculas` no aparecen en el menú; el acceso directo redirige.
- Login con `director1` → "Dispensas" sí, "Alumnos/Matrículas" no. El botón "Exportar CSV" no aparece para él.
- En "Nueva en nombre de", al elegir un alumno sin matrícula → mensaje de error.
- Re-importar el mismo CSV de matrículas → el informe reporta "asignatura ya matriculada en este curso" para los detalles repetidos.

Índices actualizados: `RUP/03-desarrollo/casos-uso/README.md` 10/26 → **18/26** (los 8 nuevos ✅); `RUP/03-desarrollo/README.md` 2/26 → 18/26; README raíz `Desarrollo 10/26 → 18/26`.

**Decisión:** Ramillete Secretaria **completo en las 3 disciplinas** (8/8 análisis + diseño + desarrollo). El proyecto cierra el día con 18/26 en desarrollo y diseño. Solo queda el ramillete **Profesor (8 CUs)** para alcanzar 26/26 en las 3 disciplinas — primer CU no-CRUD del proyecto (`registrarTomaAsistencia`) y segundo export (`exportarHistorialAsistencias`, donde se verá si introducir abstracción `Generador<T>`).

---

## [09:09] Cierre de sesión

**Prompt:** "finaliza la sesion".

**Resultado:** Servidores en background parados (`uvicorn` y `vite`). BD en estado seed limpio (5 usuarios, 5 asignaturas, 1 matrícula con 4 detalles, 3 dispensas en PENDIENTE/EN_REVISION/APROBADA). Sin cambios sin commitear pendientes de log; ningún proceso huérfano.

**Decisión:** Cierre formal de la sesión 2026-06-01. Resumen del día:
- Diseño: 10/26 → **18/26** (8 CUs de Secretaria diseñados, refactor de `Matricula` a agregado, memoria `feedback-auditoria-coherente-por-entidad` guardada).
- Desarrollo: 10/26 → **18/26** (los mismos 8 CUs implementados end-to-end con migración `SolicitudDispensa → AsignaturaMatriculada` como interludio).
- El proyecto cierra el día con análisis 26/26 ✅, diseño 18/26, desarrollo 18/26 — solo queda el ramillete **Profesor (8 CUs)** para alcanzar 26/26 en las 3 disciplinas.

---

### Sesión 2026-06-02

## [08:25] Diseño de `crearSesionClase()` y `editarSesionClase()` — apertura del ramillete Profesor

**Prompt:** "vamos, por ultimo con lo que queda de hacer, profesor, empezemos con los 2 relacionados con la sesion de clase (crear y editar), haz el diseno".

**Resultado:** Seis archivos creados (puml + svg + README × 2):

- `RUP/02-diseño/casos-uso/crearSesionClase/{secuencia.puml, secuencia.svg, README.md}` — 13 mensajes, endpoint `POST /sesiones-clase` con propietario implícito desde sesión y transición a estado activo `/sesiones-clase/{id}`.
- `RUP/02-diseño/casos-uso/editarSesionClase/{secuencia.puml, secuencia.svg, README.md}` — 18 mensajes con `alt` para "no propietario o estado CERRADA"; fase de carga referida implícitamente al `GET /sesiones-clase/{id}` futuro (regla "no duplicar fases").

**Decisiones de fondo del ramillete consolidadas (defaults aceptados por adelantado, anunciadas al usuario antes de escribir):**

1. **`SesionDeClase` debuta como entidad de dominio** — cierre de la deuda urgente del análisis. Tabla `sesiones_clase` con FKs `profesor_id` (auto-poblado desde sesión) y `asignatura_id` (al catálogo introducido por `importarMatriculas`), enum `EstadoSesionClase = {ABIERTA, CERRADA}` con state machine, sin UNIQUE adicional (solapamiento horario es regla de negocio abierta, deuda blanda).
2. **`grupo` y `aula` como strings libres** — YAGNI. No hay CU de gestión administrativa para ellos; si entra "gestionar aulas" en el futuro, se promueven a catálogos. Coherente con cómo `SolicitudDispensa` arrancó con strings antes de `AsignaturaMatriculada`.
3. **`profesor.asignaturas_impartidas` diferida** — hoy el Profesor puede elegir cualquier asignatura del catálogo. La restricción se materializará cuando entre `consultarListaAlumnos` del Profesor (donde la relación es crítica para el filtrado).
4. **Sin `PoliticaAcceso` para `SesionDeClase`** — solo un rol participa. La Strategy nació en el ramillete Alumno con dos roles concretos; introducirla aquí sería abstracción prematura. Defensa de propiedad (`sesion.profesor_id == current_user.id`) y de estado (`== ABIERTA`) viven directamente en `SesionClaseService` — el paralelo a la regla de propiedad de `PoliticaAlumno` sin Strategy intermedia.
5. **`DatosSesionClase` del análisis → `CrearSesionClaseRequest` Pydantic** — el value object queda materializado como schema de transporte, sin dataclass interno adicional. Es el Parameter Object real en código.
6. **`EditarSesionClaseRequest` sin `asignatura_id`/`grupo`/`profesor_id`** — invariantes materializadas por contrato (`extra="ignore"`), mismo patrón que `tipo` en `EditarUsuarioRequest`. Defensa silenciosa, sin checks explícitos.
7. **Edición in-situ, no ruta separada** — `/sesiones-clase/{id}` es **una sola** página con dos modos (ver / editar); respeta literalmente el análisis ("el Profesor no abandona la pantalla de asistencias para tocar metadatos"). El botón "Cancelar" usa `window.confirm` si hay cambios sin guardar (resuelve la deuda del análisis).
8. **Tras 201 en `crearSesionClase`, navega a `/sesiones-clase/{id}`** (estado activo), no a un listado. Materializa la asimetría del análisis "crear → estado activo nuevo" frente a "crear → editar (siempre)" de los CRUDs previos. Esta vista será la base para `editarSesionClase` (in-situ), `registrarTomaAsistencia` y `cerrarSesionClase`.

**Entidades nuevas introducidas (a materializar en implementación):**
- `app/models/sesion_clase.py` — `SesionDeClase` + enum `EstadoSesionClase`
- `app/schemas/sesiones_clase.py` — `CrearSesionClaseRequest`, `EditarSesionClaseRequest`, `SesionDeClaseOut`
- `app/services/sesion_clase_service.py` — `crear`, `actualizar` con excepciones `SesionClaseInvalida`/`SesionClaseNoEncontrada`/`SesionClaseNoEditable`
- `app/repositories/sesion_clase_repository.py` — `crear`, `obtener_por_id`, `listar_por_profesor`
- Catálogo `GET /asignaturas` ligero (lectura del seed)

**Tamaños de los diagramas:** 13 (crear) vs 18 (editar con `alt`). Alineados con el resto del proyecto (cerrarSesion 8 — el mínimo; iniciarSesion 17 — el más complejo). La asimetría refleja complejidad inherente (alt-block en editar, no en crear), no verbosidad.

Índices actualizados: `RUP/02-diseño/casos-uso/README.md` 18/26 → 20/26 (ambos ✅); `RUP/02-diseño/README.md` 18/26 → 20/26; README raíz `Diseño 18/26 → 20/26`.

**Decisión:** Apertura del ramillete Profesor en diseño con los 2 CUs de "ciclo de vida operativo" de la sesión de clase. Próximos pasos naturales del modo iterativo: o seguir el diseño del ramillete con `cerrarSesionClase` (que cierra el ciclo de vida — transición `ABIERTA → CERRADA`) + `registrarTomaAsistencia` (primer CU no-CRUD del proyecto, debuta `Asistencia`), o implementar ya estos 2 para ver `SesionDeClase` viva. A confirmar con el usuario.

---

## [08:30] Diseño de `consultarListaAlumnos()` y `consultarDetalleAlumno()` (Profesor) — debut de la relación `profesor_asignaturas`

**Prompt:** "perfecto, ahora vamos con los 2 relacionados con los alumnos".

**Resultado:** Seis archivos creados (puml + svg + README × 2):

- `RUP/02-diseño/casos-uso/consultarListaAlumnos/{secuencia.puml, secuencia.svg, README.md}` — 14 mensajes con `alt` "asignatura no impartida → 403"; endpoint `GET /alumnos?asignatura_id&page&size` extendido.
- `RUP/02-diseño/casos-uso/consultarDetalleAlumno/{secuencia.puml, secuencia.svg, README.md}` — 17 mensajes con tres ramas `alt` (encontrado / 404 / 403); endpoint nuevo `GET /alumnos/{id}`.

**Decisión central del ramillete — debut de la tabla `profesor_asignaturas`:**

Cierre de la deuda diferida en [crearSesionClase] ("`profesor.asignaturas_impartidas` diferida hasta consultarListaAlumnos"). Es la primera vez que la relación es **load-bearing** en código: sin ella no se puede aplicar la regla emergente "Profesor competente" (regla del análisis que se repite en 3 CUs del Profesor: `consultarSolicitudDispensaProfesor`, `consultarListaAlumnos`, `consultarDetalleAlumno`).

- Estructura: tabla N:M `(profesor_id PK→usuarios.id, asignatura_id PK→asignaturas.id)`, sin atributos adicionales. Acceso desde Python como relación `Usuario.asignaturas_impartidas` (`lazy="selectin"`, `secondary=`).
- Seed: pobla `profesor1 → IYA038, IYA040, IYA041` para que la prueba manual funcione.
- Endpoint auxiliar `GET /profesores/yo/asignaturas` para que el frontend cargue las pestañas al montar.

**Decisiones de fondo consolidadas (defaults aceptados por adelantado, anunciadas al usuario):**

1. **`GET /alumnos` extendido** con `["secretaria", "profesor"]` y `?asignatura_id?` opcional. Service ramifica por rol: Secretaria opcional sin restricción; Profesor requerido + defensa "Profesor competente" (422 si falta, 403 si no imparte). El `?q=` de Secretaria sigue funcionando.
2. **`GET /alumnos/{id}` nuevo** con `["profesor", "secretaria"]` — recurso distinto de `/usuarios/{id}` (vista admin) y `/matriculas/{id}` (ficha de la matrícula). La Secretaria salta la verificación competente; el Profesor exige al menos una asignatura compartida (404 si no existe el alumno; 403 si existe pero no comparte asignatura — distinción honesta sin enmascaramiento).
3. **`AlumnoService` introducido aquí** — orquesta verificación competente + filtrado de asistencias. Es el primer Service que materializa la regla del análisis "regla del Profesor competente en defensa en profundidad".
4. **Sin Strategy `PoliticaAcceso`** — aunque hay dos roles operando sobre Alumno, las firmas del Repository difieren (`buscar_alumnos(page, size, q)` Secretaria vs `buscar_por_asignatura(asignatura_id, page, size)` Profesor). Aplica la regla emergente del proyecto: cuando la signatura difiere → métodos específicos del Service; cuando solo la política varía → Strategy. Misma lección que en `crearSolicitudDispensaSecretaria`. Sin abstracción prematura.
5. **Schema `AlumnoEnAsignaturaOut`** distinto del `AlumnoListaItemOut` de Secretaria — campos académicos del prototipo (`carnet`/`curso_academico`/`estado_matricula`) derivados del join con `Matricula`. Dos schemas honestos en vez de unión con `Optional` siempre llenos en un rol y `None` en otro.
6. **Schema `AlumnoDetalleOut`** distinto del `MatriculaDetalleOut` — el primero es la ficha de **una persona** (Profesor consulta personas), el segundo de **una matrícula** (Secretaria consulta matrículas). Aunque comparten datos, las audiencias y entradas difieren.
7. **`Asistencia` diferida al CU dueño `registrarTomaAsistencia`** — el schema reserva `asistencias: List[AsistenciaResumenOut]` pero hoy retorna `[]`. Mismo enfoque que `Matricula` con `importarMatriculas` (la entidad emerge del CU dueño semántico). Evita seed manual de asistencias inventadas y no rompe la trazabilidad RUP.
8. **Filtro de asistencias en el Service**, no en el Repository — el Repository devuelve el agregado completo; el Service filtra por las asignaturas del Profesor antes de serializar. Resuelve la ambigüedad del prototipo del análisis en favor del filtro estricto.
9. **Eager-load del agregado del alumno** — `selectinload(matriculas).selectinload(asignaturas_matriculadas).joinedload(asignatura)` para evitar el problema de lazy-load en sesión async (conocido del ramillete Director). Una request, agregado completo.

**Entidades nuevas introducidas en este ramillete:**

- Tabla N:M `profesor_asignaturas` + relación `Usuario.asignaturas_impartidas`
- `AlumnoService` (`app/services/alumno_service.py`) — el actual `app/services/alumno_service.py` del bloque Secretaria (que solo importa CSVs) probablemente se renombra a `AlumnoImportService` o se fusiona, deuda blanda
- `AlumnoRepository` métodos nuevos: `buscar_por_asignatura(asignatura_id, page, size)`, `obtener_alumno_con_matricula(id)`
- Endpoint auxiliar `GET /profesores/yo/asignaturas`
- Schemas: `AlumnoEnAsignaturaOut`, `AlumnoDetalleOut`, `AsistenciaResumenOut` (placeholder hasta `registrarTomaAsistencia`)

**Tamaños de los diagramas:** 14 (lista) vs 17 (detalle con 3 ramas alt). Alineados con el resto del proyecto. La asimetría refleja que el detalle tiene tres caminos honestos (200/404/403), no verbosidad.

Índices actualizados: `RUP/02-diseño/casos-uso/README.md` 20/26 → 22/26 (ambos ✅); `RUP/02-diseño/README.md` 20/26 → 22/26; README raíz `Diseño 20/26 → 22/26`.

**Decisión:** Segundo paso del ramillete Profesor en diseño. La relación `profesor_asignaturas` queda definida y disponible para los próximos CUs del bloque. Quedan **4 CUs del Profesor en diseño** (`registrarTomaAsistencia`, `cerrarSesionClase`, `exportarHistorialAsistencias`, `consultarSolicitudDispensa` del Profesor) y **8/26 en desarrollo**. Próximo paso natural: o seguir con el diseño de los 4 restantes, o implementar ya estos 4 diseñados (Sesión×2 + Alumnos×2) en un push.

---

## [08:46] Diseño de los 4 CUs restantes del Profesor — cierre del diseño 26/26

**Prompt:** "haz los disenos restantes".

**Resultado:** Doce archivos creados (puml + svg + README × 4):

- `RUP/02-diseño/casos-uso/cerrarSesionClase/{secuencia.puml, secuencia.svg, README.md}` — 17 mensajes con `alt`, `PATCH /sesiones-clase/{id}` con `{estado: "CERRADA"}` y side effect `hora_fin = now`.
- `RUP/02-diseño/casos-uso/registrarTomaAsistencia/{secuencia.puml, secuencia.svg, README.md}` — 16 mensajes con `alt`, `PUT /sesiones-clase/{id}/asistencias/{alumno_id}` upsert granular idempotente; debuta `Asistencia`.
- `RUP/02-diseño/casos-uso/exportarHistorialAsistencias/{secuencia.puml, secuencia.svg, README.md}` — 17 mensajes con `alt`, `GET /asistencias/exportar?asignatura_id&desde&hasta`; segundo servicio generador del proyecto.
- `RUP/02-diseño/casos-uso/consultarSolicitudDispensaProfesor/{secuencia.puml, secuencia.svg, README.md}` — 21 mensajes con 3 ramas `alt` (200/404/403), `GET /dispensas/{id}` extendido; debuta `PoliticaProfesor` (cuarta política del módulo).

**Decisiones de fondo consolidadas (defaults aceptados por adelantado):**

1. **`cerrarSesionClase` reutiliza `PATCH /sesiones-clase/{id}`** con `{estado: "CERRADA"}` — coherencia con la state machine de `SolicitudDispensa` (un solo endpoint para transiciones). El Service detecta la transición por el body y sella `hora_fin = now`. Sin endpoint dedicado `POST /sesiones-clase/{id}/cerrar`. Patrón "PATCH con state machine inferida" sólidamente consolidado en el proyecto (Director, Alumno y ahora Profesor).
2. **`Asistencia` debuta como entidad** — cierre de la última deuda urgente del análisis. Tabla `asistencias` con UNIQUE `(sesion_clase_id, alumno_id)`, enum `EstadoAsistencia = {PRESENTE, AUSENTE, TARDE}`, `justificacion` y `fecha_registro` opcionales. La unicidad compuesta es la base del upsert idempotente.
3. **`PUT /sesiones-clase/{id}/asistencias/{alumno_id}` (granular)** — semántica HTTP correcta para upsert con identidad conocida. El análisis adoptó granular sobre batch; el diseño lo respeta. Sin "submit final"; cada cambio del Profesor persiste inmediatamente. Concurrencia trivial (último-en-escribir-gana).
4. **Interacción `Asistencia ↔ SolicitudDispensa`: opción A** (independencia con vista combinada). El backend retorna ambas entidades por separado; el frontend muestra una columna "Dispensa" derivada cruzando `SolicitudDispensa.APROBADA` con `(alumno_id, asignatura)`. La columna no se persiste; es presentación pura.
5. **`GeneradorArchivoAsistencias` paralelo a `GeneradorArchivoDispensas`** — segundo servicio del proyecto. **Sin abstracción `Generador<T>`** (anunciada como deuda blanda en `exportarDispensas` y en el análisis). Razón: dos generadores con misma forma pero **no contrato formal** (`generar_csv(List[Dispensa])` vs `generar_csv(List[Asistencia])` — no intercambiables). Introducir ABC sería agrupación sintáctica sin polimorfismo real. Coherente con la lección "abstracción solo cuando hay un caso polimórfico real".
6. **CSV único en v1.0** — XLSX/PDF como deuda blanda. `csv` stdlib cubre el caso sin dependencias. Mismo enfoque que `exportarDispensas`.
7. **`PoliticaProfesor` introducida** — cuarta y última política sobre `SolicitudDispensa`. Contrato: `obtener_listado` filtra por join con `profesor_asignaturas`; `puede_ver` exige asignatura impartida; transiciones y campos editables vacíos (read-only puro, sin write paths). Cierre del polimorfismo del Controller sobre la entidad **más operada** del proyecto: cuatro políticas inyectables, **un único Service + un único Repository**.
8. **`require_rol(["alumno", "secretaria", "director", "profesor"])`** en `GET /dispensas` y `GET /dispensas/{id}` — el dispatch vive en la Política. PATCH/POST/exportar quedan sin cambios (siguen en sus subconjuntos previos).
9. **404 vs 403 honestos en consultarSolicitudDispensa (Profesor)** — si no existe la dispensa → 404; si existe pero la asignatura no es impartida → 403. Sin enmascaramiento por privacidad. Coherente con la decisión paralela del Profesor sobre `consultarDetalleAlumno`.
10. **Sub-recurso `/sesiones-clase/{id}/asistencias`** (no `/asistencias` plano) — refleja la jerarquía conceptual (asistencia pertenece a sesión). Coherente con `asignaturas_matriculadas` que cuelga de `matriculas`.

**Cierre del polimorfismo del Controller sobre `SolicitudDispensa`:** Con la cuarta política se completa la entidad más operada del proyecto:

| Rol | Política | Listado | `puede_ver` | Transiciones | Campos editables |
|---|---|---|---|---|---|
| Alumno | `PoliticaAlumno` | propias | propietario | `{(PENDIENTE, ANULADA)}` | motivo, asig_matr (si PENDIENTE) |
| Director | `PoliticaDirector` | sin filtro | siempre | 3 (veredicto) | observaciones (si EN_REVISION) |
| Secretaria | `PoliticaSecretaria` | sin filtro | siempre | `{(PENDIENTE, ANULADA)}` | motivo, asig_matr (si PENDIENTE) |
| Profesor | `PoliticaProfesor` | join con `profesor_asignaturas` | asignatura impartida | vacío | vacío |

Sin proliferación de Controllers. Sin if-else por rol en el código de aplicación.

**Entidades introducidas en este round:**

- `Asistencia` + enum `EstadoAsistencia` (modelo, schemas, service, repository)
- Endpoints nuevos: `PUT /sesiones-clase/{id}/asistencias/{alumno_id}`, `GET /sesiones-clase/{id}/asistencias`, `GET /asistencias/exportar`
- `AsistenciaService`, `AsistenciaRepository` (con `upsert` y `obtener_por_rango`)
- `GeneradorArchivoAsistencias` (paralelo a `GeneradorArchivoDispensas`)
- `PoliticaProfesor` en `app/services/politica_acceso.py`

**Tamaños de los diagramas:** 17 (cerrar) / 16 (registrar) / 17 (exportar) / 21 (consultar dispensa). Alineados con el resto del proyecto. La asimetría del último refleja que tiene tres ramas `alt` (200/404/403), no verbosidad.

Índices actualizados: `RUP/02-diseño/casos-uso/README.md` 22/26 → **26/26 ✅**; `RUP/02-diseño/README.md` 22/26 → **26/26 ✅**; README raíz `Diseño 22/26 → 26/26 ✅`.

**Decisión:** **Disciplina de Diseño cerrada al 100%** (26/26). El proyecto cierra el día con análisis 26/26 ✅, **diseño 26/26 ✅**, desarrollo 18/26 ⏳. Próximo paso natural: implementar los 8 CUs restantes del ramillete Profesor (2 Sesión + 2 Alumnos + cerrar + registrar + exportar + consultar dispensa) en un push, con la migración de:
- Tabla N:M `profesor_asignaturas` + seed
- Entidad `SesionDeClase` + state machine
- Entidad `Asistencia` con UNIQUE compuesto
- Extensión de endpoints existentes (`/alumnos`, `/dispensas`) con nuevos roles y filtros
- `PoliticaProfesor` añadida al módulo
- Segundo servicio generador (`GeneradorArchivoAsistencias`)

Cuando se cierre, el proyecto quedará en **26/26 en las tres disciplinas**.

---

## [10:07] Implementación del ramillete Profesor — 8 CUs end-to-end (cierre 26/26)

**Prompt:** "perfecto, implementalos".

**Resultado:** Backend + frontend implementados; 18/18 pruebas internas vía curl pasan; uvicorn (`:8000`) y vite (`:5173`) corriendo con BD reseteada al estado seed. **Ramillete Profesor completo** (Análisis 26/26 ✅, Diseño 26/26 ✅, **Desarrollo 26/26 ✅**). El proyecto cierra al 100% en las tres disciplinas.

### Backend (16 archivos nuevos / 9 editados)

Entidades nuevas y relaciones:
- `app/models/profesor_asignatura.py` — tabla N:M (sin clase de dominio independiente).
- `app/models/sesion_clase.py` — `SesionDeClase` + enum `EstadoSesionClase = {ABIERTA, CERRADA}`.
- `app/models/asistencia.py` — `Asistencia` con UNIQUE compuesto `(sesion_clase_id, alumno_id)` + enum `{PRESENTE, AUSENTE, TARDE}`.
- `app/models/usuario.py` — añadido `asignaturas_impartidas` (`relationship` con `secondary=profesor_asignaturas`, `lazy="selectin"`).
- `app/models/__init__.py` — registros nuevos.

Capa de datos:
- `app/repositories/sesion_clase_repository.py` — `crear`, `obtener_por_id`, `listar_por_profesor`, `actualizar`.
- `app/repositories/asistencia_repository.py` — `upsert` con `sqlite_insert(...).on_conflict_do_update(...)`, `listar_por_sesion`, `obtener_por_rango`.
- `app/repositories/asignatura_repository.py` — extendido con `obtener_todas`, `obtener_por_id`.
- `app/repositories/usuario_repository.py` — extendido con `buscar_por_asignatura` (join `matriculas`+`asignaturas_matriculadas`) y `obtener_alumno_con_matricula` (eager-load).
- `app/repositories/solicitud_dispensa_repository.py` — añadido `obtener_por_asignaturas` para PoliticaProfesor.

Servicios:
- `app/services/sesion_clase_service.py` — `crear`/`obtener`/`listar`/`actualizar`; state machine `ABIERTA → CERRADA`; defensa de propiedad y de estado; excepciones `SesionClaseNoEncontrada`, `SesionClaseInvalida`, `SesionClaseNoEditable`.
- `app/services/asistencia_service.py` — `marcar` (propietario + estado + alumno matriculado) y `listar_por_sesion`.
- `app/services/generador_archivo_asistencias.py` — CSV con BOM utf-8-sig, paralelo a `GeneradorArchivoDispensas`.
- `app/services/politica_acceso.py` — `PoliticaProfesor` añadida (cuarta política); factory actualizada.
- `app/services/alumno_service.py` — extendido con `listar_por_asignatura` y `obtener_detalle` (defensa "Profesor competente").

Schemas:
- `app/schemas/asignaturas.py` — `AsignaturaOut`.
- `app/schemas/sesiones_clase.py` — `CrearSesionClaseRequest`, `EditarSesionClaseRequest`, `SesionDeClaseOut`. Invariantes materializadas por `extra="ignore"` (igual que `tipo` en `EditarUsuarioRequest`).
- `app/schemas/asistencias.py` — `AsistenciaIn`, `AsistenciaOut`.
- `app/schemas/alumnos.py` — añadidos `AlumnoEnAsignaturaOut` (Profesor) y `AlumnoDetalleOut`.

Routers nuevos y extensiones:
- `app/routers/sesiones_clase.py` — `GET/POST /sesiones-clase`, `GET/PATCH /sesiones-clase/{id}`, sub-recurso `GET/PUT /sesiones-clase/{id}/asistencias[/{alumno_id}]`.
- `app/routers/asistencias.py` — `GET /asistencias/exportar`.
- `app/routers/asignaturas.py` — `GET /asignaturas` (catálogo).
- `app/routers/profesores.py` — `GET /profesores/yo/asignaturas`.
- `app/routers/alumnos.py` — extendido: `GET /alumnos?asignatura_id` con dispatch por rol, `GET /alumnos/{id}` nuevo.
- `app/routers/dispensas.py` — `require_rol` extendido a `["director","alumno","secretaria","profesor"]` en `GET /dispensas` y `GET /dispensas/{id}`.
- `app/main.py` — registra los 4 routers nuevos.

Seed:
- `scripts/seed.py` — añadidas tres funciones: `_seed_profesor_asignaturas` (profesor1 → IYA038/IYA040/IYA041), `_seed_sesiones_clase` (una ABIERTA hoy, una CERRADA ayer), `_seed_asistencias_demo`.

### Frontend (12 archivos nuevos / 5 editados)

Types:
- `types/asignaturas.ts`, `types/sesiones_clase.ts`, `types/asistencias.ts` nuevos.
- `types/alumnos.ts` extendido con `AlumnoEnAsignatura`, `AlumnoDetalle`, `AsistenciaEnFicha`.

Services:
- `services/asignaturasService.ts`, `services/profesoresService.ts`, `services/sesionesClaseService.ts`, `services/asistenciasService.ts` nuevos.
- `services/alumnosService.ts` extendido con `listarPorAsignatura`, `obtener`.

Páginas nuevas (Profesor):
- `SesionesClasePage.tsx` — listado + selector de asignatura + botón export CSV.
- `CrearSesionClasePage.tsx` — form con select de asignaturas impartidas.
- `SesionClaseActivaPage.tsx` — vista + edición in-situ + toma de asistencia + cerrar (modal `window.confirm`).
- `ListaAlumnosPage.tsx` — con pestañas por asignatura impartida.
- `DetalleAlumnoPage.tsx` — ficha con secciones colapsables.

Navegación y bifurcación:
- `App.tsx` — añadidos `profesorOnly`, `profesorOSecretaria`. `/alumnos` ramifica con `BifurcacionAlumnos` (Profesor → `ListaAlumnosPage`; Secretaria → `AlumnosPage`).
- `Layout.tsx` — link "Sesiones", "Alumnos", "Dispensas" para Profesor.
- `DispensasPage.tsx` — adaptada para mostrar "Dispensas de mis asignaturas" con rol Profesor; sin botones de creación/export.
- `ConsultarDispensaPage.tsx` — ya estaba: el rol Profesor cae en `'otro'` → componente `<Acciones>` retorna `null` (read-only puro). Sin cambios necesarios.

### Bug detectado y arreglado en vivo

1. **`hora_fin` sobrescrita al cerrar**: la primera implementación sellaba `hora_fin = datetime.now().time()` al cerrar, perdiendo la hora planeada. Decisión revisada: el cierre solo cambia el estado; `hora_fin` se preserva. Divergencia documentada en el README de desarrollo de `cerrarSesionClase`. Razón: sobrescribir hora planeada con `now()` pierde información útil sin ganar nada (el cierre se identifica por `estado=cerrada`).
2. **`PoliticaProfesor.obtener_listado` no filtraba**: el primer `obtener_por_asignaturas` usaba `joinedload` y un `where(AsignaturaMatriculada.asignatura_id.in_(ids))` sin JOIN explícito → SQLAlchemy ignoraba el filtro. El listado del Profesor devolvía 3 dispensas en vez de 2. Fix: JOIN explícito `solicitudes_dispensa JOIN asignaturas_matriculadas`. Confirmado 2 dispensas tras el fix.

### Decisiones de diseño consolidadas

- **`SesionDeClase` y `Asistencia` debutan como entidades** del dominio — cierre de las dos deudas urgentes del análisis.
- **State machine `ABIERTA → CERRADA`** con un solo PATCH; misma forma que `SolicitudDispensa`.
- **Tabla N:M `profesor_asignaturas`** introducida como load-bearing en `consultarListaAlumnos` (cierre de la deuda diferida en `crearSesionClase`).
- **`Asistencia ↔ SolicitudDispensa`: opción A** (independientes); frontend cruza si necesita.
- **`PoliticaProfesor`** cuarta y última política sobre `SolicitudDispensa` — read-only puro (transiciones y campos editables vacíos).
- **Sin abstracción `Generador<T>`** — dos generadores con misma forma pero contratos no intercambiables. Diferida.
- **Sub-recurso `/sesiones-clase/{id}/asistencias`** — refleja la jerarquía conceptual.
- **`BifurcacionAlumnos`** en `/alumnos` — Profesor y Secretaria comparten ruta con pages distintas.

### Verificación interna — 18 pruebas curl

Backend (todos OK):
- `/profesores/yo/asignaturas` Profesor (3 asignaturas seed); Alumno 403.
- `/sesiones-clase` GET, POST, PATCH (editar), PATCH (cerrar), PATCH (editar cerrada=422), PATCH (reabrir=422).
- `/alumnos` sin asignatura_id (422), con IYA040 (200), con IYA010=403.
- `/alumnos/{id}` 200/404.
- `PUT /sesiones-clase/{id}/asistencias/{alumno_id}` marcar 200, upsert 200, sesión cerrada 422.
- `/dispensas` Profesor (2 filtradas), dispensa IYA010=403, PATCH=422.
- `/asistencias/exportar` CSV OK 200 con BOM; IYA010 403.
- Cross-rol: Alumno en `/sesiones-clase` 403; Director ve 3 dispensas; Alumno ve sus 3.

Frontend:
- `npx tsc --noEmit` limpio (sin errores).
- vite (`:5173`) sirve la SPA; proxy `/api` → backend OK.

### Estado de la BD reseteada al cierre

| Recurso | Estado seed |
|---|---|
| Usuarios | 5 (admin/profesor1/alumno1/director1/secretaria1) |
| Asignaturas catálogo | 5 (IYA010, IYA020, IYA038, IYA040, IYA041) |
| Profesor → asignaturas | profesor1 imparte IYA038, IYA040, IYA041 |
| Matrículas | 1 (alumno1 · 2025/2026 · 4 asignaturas matriculadas) |
| Dispensas | 3 (IYA040 pendiente, IYA041 en_revision, IYA010 aprobada) |
| Sesiones de clase | 2 (IYA040 hoy abierta, IYA040 ayer cerrada) |
| Asistencias | 1 (alumno1 presente en la sesión cerrada) |

### Guion de prueba manual

URL: http://localhost:5173 — uvicorn (bplnq92xj) y vite (ba4g55i2y) siguen corriendo en background.

Credenciales:
- `profesor1` / `profe123` — actor principal del ramillete
- `alumno1` / `alumno123` — para probar visibilidad cruzada de dispensas
- `director1` / `director123` — para confirmar que el flujo de veredicto sigue funcionando
- `secretaria1` / `secre123` — para confirmar que el listado de Alumnos no se rompió

Camino feliz Profesor (10 pasos):
1. Login `profesor1`/`profe123` → dashboard.
2. Cabecera: ver links "Sesiones", "Alumnos", "Dispensas".
3. **Sesiones** → ver 2 sesiones (una abierta hoy, una cerrada ayer).
4. Click "+ Nueva sesión" → form con select IYA038/IYA040/IYA041, completar y crear → navega a la vista activa.
5. En la vista activa: pulsar "Editar", cambiar `aula`/`tema`, "Guardar".
6. Probar "Cancelar" tras editar → `window.confirm` pide confirmación.
7. Marcar alumno1 como Presente → Tarde → Ausente (cada click persiste).
8. "Finalizar sesión" → modal de confirmación → estado pasa a `cerrada`, navega al listado.
9. **Alumnos** → pestañas IYA038/IYA040/IYA041; click pestaña → carga alumnos matriculados. Click "Ver ficha".
10. **Dispensas** → ver solo IYA040 + IYA041 (2 dispensas, IYA010 oculta). Click "Ver" → ficha sin botones de acción.

Edge cases:
- Selector de export en `/sesiones-clase` → exporta CSV (descarga `asistencias-{codigo}-{fecha}.csv`).
- Login con `alumno1` → solo "Mis dispensas" visible; acceso directo a `/sesiones-clase` redirige a dashboard.
- Login con `secretaria1` → ve "Alumnos", "Matrículas", "Dispensas"; `/alumnos` muestra el listado paginado de la Secretaria (no las pestañas del Profesor).

### Estado del proyecto al cierre

| Disciplina | Estado |
|---|---|
| Análisis | ✅ 26/26 |
| Diseño | ✅ 26/26 |
| Desarrollo | ✅ 26/26 |

**El proyecto está completo en las tres disciplinas RUP.**

---

## [10:13] Cierre de sesión

**Prompt:** "perfecto, finaliza la sesion".

**Resultado:** Servidores en background parados (`uvicorn` y `vite`). BD en estado seed limpio. Sin procesos huérfanos. Cambios sin commitear (a la espera de commit manual del usuario): 21 archivos modificados + 35 archivos nuevos cubriendo backend, frontend y READMEs de `RUP/03-desarrollo` para los 8 CUs del ramillete Profesor.

**Decisión:** Cierre formal de la sesión 2026-06-02. Resumen del día:

- Diseño: 18/26 → **26/26 ✅** (los 8 CUs del Profesor: sesión×2, alumnos×2, cerrar, registrar, exportar, dispensa Profesor).
- Desarrollo: 18/26 → **26/26 ✅** (los mismos 8 CUs implementados end-to-end con `SesionDeClase`, `Asistencia`, tabla N:M `profesor_asignaturas`, `PoliticaProfesor` y `GeneradorArchivoAsistencias` como entidades/servicios nuevos).
- Bugs detectados y resueltos en vivo: `hora_fin` sobrescrita al cerrar (decisión revertida a preservar la planeada) y filtrado de `PoliticaProfesor.obtener_listado` sin JOIN explícito.

El proyecto cierra el día — y la disciplina RUP — al **100% en análisis, diseño y desarrollo** (26/26 en las tres).

---

### Sesión 2026-06-10

## [09:30] Script de arranque unificado

**Prompt:** "dame un script que inicie todo lo necesario para que la aplicación funcione, ubícalo donde creas que es más acertado".

**Resultado:** `scripts/start.sh` en la raíz. Crea venv si falta, instala backend y frontend solo si hace falta, copia `.env.example→.env`, ejecuta `seed.py` (idempotente), lanza `uvicorn :8000` y `vite :5173` en background, y los mata a ambos con `trap` al Ctrl+C.

**Decisión:** Carpeta `scripts/` nueva en la raíz (convención habitual; no contamina `src/`). Validado por el usuario.

## [09:40] Guion de pruebas manuales por rol

**Prompt:** "se me ha olvidado un poco toda la estructura y pruebas que debo hacer, dame una lista de pruebas para comprobar que todo funcione correctamente".

**Resultado:** Checklist por rol (Administrador, Profesor, Alumno, Director, Secretaria) + bloque transversal Usuario + smoke API rápido con `curl`, ajustado a los datos sembrados (`alumno1` en IYA040 con 4 asignaturas matriculadas, 3 dispensas en distintos estados, 2 sesiones de IYA040).

## [09:50] Aclaraciones tras pruebas + creación de CSVs

**Prompt:** Lista de dudas tras la batería de pruebas: (1) quién asigna asignaturas al Profesor; (2) si el desplegable de `/sesiones-clase` debería filtrar; (3) si "Grupo" debería ser desplegable; (4) por qué la ficha del alumno muestra `Asistencias (0)` aun tras cerrar sesiones; (5) por qué la Secretaria importa pero no crea alumnos/matrículas individualmente; (6) crear CSVs de prueba para los botones de importar.

**Resultado:**
1. Hoy nadie — `profesor_asignaturas` solo se siembra en `seed.py`, no hay endpoint para gestionarla. Tampoco hay CRUD de asignaturas. Cabo suelto del SDR.
2. El `<select>` actual es solo selector de exportación, no filtro. UX confusa.
3. `SesionDeClase.grupo` es `String(50)` libre; no existe entidad `Grupo` ni catálogo del que tirar.
4. Bug conocido: `routers/alumnos.py:214-224` devuelve `asistencias=[]` hardcodeado con comentario "Se rellenará cuando…". Las asistencias sí se persisten.
5. Diseño deliberado: las matrículas tienen fuente externa (Universitas), por eso solo se importan; el alta masiva de alumnos por CSV refleja el flujo real de inicio de curso. El `crearUsuario` del Administrador es alta puntual de cualquier rol como efecto del subtipado STI.
6. Cuatro CSVs en `/tmp/cgu-test-csv/`: `alumnos-ok.csv` y `alumnos-mal.csv` (4 errores distintos, uno por fila), `matriculas-ok.csv` y `matriculas-mal.csv` (5 errores distintos, uno por fila). Cada CSV "mal" mantiene cabecera válida para forzar errores por fila visibles en el informe.

**Decisión:** Aclaración como Q&A, sin tocar código.

## [09:55] Plan de mejoras post-base

**Prompt:** Acuerdo con (1), (2), (3 opción ligera) y (4). Pidió plan de acción paso a paso en archivo a elegir, y revisión del razonamiento.

**Resultado:** Aviso de contradicción en (5): si la Secretaria gana el catálogo de asignaturas por ser "operadora académica", el alta individual de alumnos a mitad de curso debería ser también suya por el mismo argumento, no del Administrador. Plan creado en `RUP/PLAN-MEJORAS.md` (movido aquí desde `RUP/03-desarrollo/` por atravesar las tres disciplinas) con 5 items (M1 asistencias, M2 filtro sesiones, M3 grupo derivado, M4 mover alta alumno a Secretaria, M5 catálogo asignaturas + asignar profesor↔asignatura), orden por coste creciente, qué disciplinas RUP toca cada uno, y nota de que ejecutarlo completo sube el denominador de 26 a 29 CUs.

**Decisión:** El plan documenta las decisiones, no se ejecuta todavía. Espera confirmación del usuario sobre la corrección en M4 (mover alta de alumno individual a Secretaria) antes de empezar.

## [09:58] Mover el plan a la raíz de RUP

**Prompt:** "como veo que varios de estos puntos requiren modificacion de analisis y diseno a parte de desarrollo, mueve el archivo de desarrollo a la raiz, u otra carpeta mas apropiada".

**Resultado:** Movido a `RUP/PLAN-MEJORAS.md` (sibling de las cuatro disciplinas). El plan atraviesa 01/02/03 en M4 y M5, así que no pertenece a ninguna disciplina concreta.

**Decisión:** Confirmado por el usuario implícitamente al pasar a ejecutar M1.

## [10:10] M1 — Asistencias en la ficha del alumno (hecho)

**Prompt:** "vamos a empezar con la mejora 1, que por lo que veo en el readme, solo requiere modificacion de 03 diseno, no?".

**Resultado:** Corrección de nomenclatura (03 es desarrollo, no diseño; diseño es 02). Tras leer el código se descubrió que el plan tenía un error menor: dije que el frontend "ya pintaba asistencias si venían rellenas", pero `DetalleAlumnoPage.tsx:87-98` solo tenía rama para `length === 0`. M1 toca también frontend.

Cambios:
- `repositories/asistencia_repository.py` — nuevo `listar_por_alumno(alumno_id)` con JOIN a `sesiones_clase`, ordenado por fecha desc + hora_inicio desc.
- `routers/alumnos.py` — usa el repositorio en `obtener_alumno`, construye `AsistenciaEnFichaOut` por fila (con `fecha=...isoformat()` y `asignatura_codigo` desde `sesion_clase.asignatura.codigo`), borra el comentario "Se rellenará cuando…".
- `schemas/alumnos.py` — quita la nota de placeholder del docstring de `AsistenciaEnFichaOut`.
- `frontend/pages/DetalleAlumnoPage.tsx` — añade tabla (Fecha · Asignatura · Estado con `estado-badge`) para el caso `length > 0`.

Verificación: `GET /alumnos/3` (alumno1) devuelve 4 asistencias con orden correcto (2 de hoy 2026-06-10 en IYA040/IYA041 ABIERTAS + 2 de fechas anteriores en IYA040). UI confirmada por el usuario.

**Decisión:** M1 marcado como `hecho (2026-06-10)` en `RUP/PLAN-MEJORAS.md`. Siguiente: M2 cuando el usuario lo indique.

## [10:15] M2 (hecho) + M3 (en revisión por bug de layout)

**Prompt:** "haz las mejoras 2 y 3, que son aparentemente sencillas y no requieren mucho tiempo".

**Resultado:**

- **M2 — Filtro en `/sesiones-clase`:** un único archivo `SesionesClasePage.tsx`. Etiqueta "Exportar:" delante del selector existente, nuevo `<select>` "Filtrar por asignatura:" sobre la tabla con opción "Todas" por defecto, `.filter()` aplicado al `.map()` del `<tbody>`. Confirmado por el usuario.
- **M3 — Grupo derivado:** nuevo endpoint `GET /sesiones-clase/grupos?asignatura_id=N` (insertado **antes** de `GET /{sesion_id}` para que FastAPI no lo intente parsear como id), repositorio con `grupos_distintos(profesor_id, asignatura_id)` usando `SELECT DISTINCT s.grupo`. Frontend: `CrearSesionClasePage` recarga grupos al cambiar de asignatura, muestra `<select>` con valores previos + opción "+ Nuevo grupo…", o `<input>` directo si no hay previos. Verificado por curl (IYA040 → `["2a","II3201"]`, IYA041 → `["3A","prueba"]`, IYA038 → `[]`).

## [10:20] Arreglo de layout en M3

**Prompt:** "en m3, al seleccionar nueva sesion, el boton volver al listado de grupos aparece a la izquierda de 'Aula'".

**Resultado:** Causa identificada — el `<label>` es inline; `input/select { width: 100% }` fuerza wrap a línea propia, pero el botón es `display: inline-block` por defecto, así que se quedaba al final de la línea y el `<label>` siguiente ("Aula") seguía inline a su derecha.

Arreglo: envolver `<label>` y el botón en un `<div>` para aislarlos, y `display: block` explícito en el botón como defensa. Una sola edición en `CrearSesionClasePage.tsx`.

**Decisión:** M2 marcado como `hecho (2026-06-10)`. M3 espera nueva confirmación del usuario tras el arreglo.

## [10:21] M3 confirmado

**Prompt:** "funciona, marca m3 como hecho".

**Resultado:** M3 marcado como `hecho (2026-06-10)` en `RUP/PLAN-MEJORAS.md` (tabla resumen + cabecera de sección + "Resumen de la ejecución" con los 4 archivos tocados).

**Decisión:** Las tres mejoras "ligeras" del plan (M1, M2, M3) están cerradas. Quedan M4 (alta individual de alumno por Secretaria, requiere 01+02+03) y M5 (catálogo de asignaturas + asignar profesor↔asignatura, requiere 01+02+03).

## [10:25] M6 detectado — sesiones con múltiples grupos

**Prompt:** "el m2 no es correcto del todo, porque algunas asignatura (ingles por ejemplo) pueden tener varios grupos asignados, por ejemplo en ingles acutalmente en mi universidad, estamos ADE, Ing Informatica e Ingenieria Organizacion industrial en la misma sesion".

**Resultado:** Explicado que es un cambio de cardinalidad (1 → N grupos por sesión) que afecta al modelo, no solo a M2. Presentadas 3 opciones con coste (JSON list, tabla N:M, comma-separated string).

**Decisión:** Tras pedir el usuario justificación de mi recomendación, expuestas las razones para JSON list sobre tabla N:M (un grupo no tiene identidad reusable cross-asignatura, no tiene atributos propios, no hay CU de gestión, la promoción posterior es barata). Usuario confirma: opción 1 (JSON list).

## [10:38] M6 implementado

**Resultado:** Cambios en 13 archivos (7 backend + 4 frontend + 2 RUP) + regenerado el SVG del secuencia.puml + recreada la BD (la migración de `String` a `JSON` en SQLite no la hace `Base.metadata.create_all`, así que se borró `cgu.db` y se re-ejecutó `seed.py`).

Backend:
- `models/sesion_clase.py` — `grupos: list[str]` con columna JSON.
- `schemas/sesiones_clase.py` — `grupos: list[str]` en Out y CrearRequest; comentario de EditarRequest actualizado.
- `services/sesion_clase_service.py` — `_normalizar_grupos` (strip + dedupe orden-preservante + exige len >= 1; lanza `SesionClaseInvalida` "indica al menos un grupo").
- `repositories/sesion_clase_repository.py` — `crear()` con `datos.grupos`; `grupos_distintos()` aplana las listas en Python (escala pequeña, evita acoplamiento a `JSON_EACH`).
- `services/generador_archivo_asistencias.py` y `services/asistencia_service.py` — cabecera CSV `grupo` → `grupos`, valor `", ".join(s.grupos)`.
- `scripts/seed.py` — `grupos=["3A"]` en las dos sesiones demo.

Frontend:
- `types/sesiones_clase.ts` — `grupos: string[]` (replace_all).
- `pages/SesionesClasePage.tsx` y `pages/SesionClaseActivaPage.tsx` — columna/etiqueta "Grupos", render con `.join(', ')`.
- `pages/CrearSesionClasePage.tsx` — reescritura del bloque de selección: chips removibles con `×` para los grupos añadidos, `<input list="grupos-previos">` con `<datalist>` autocompletando los previos no seleccionados, botón "Añadir" (también Enter). Eliminado el flag `grupoLibre` y el botón "Volver al listado" (no aplica con chips).

RUP:
- `01-analisis/.../crearSesionClase/README.md` — actualizada la intro y las definiciones canónicas de `SesionDeClase` y `DatosSesionClase`. Añadida nota "Evolución post-base" remitiendo al plan. Sección histórica "Long Parameter List" se preserva tal cual (narrativa pedagógica, no canónica).
- `02-diseño/.../crearSesionClase/README.md` — `participantes`, body del POST y decisión "grupos/aula strings libres" actualizados con la justificación de por qué JSON list y no entidad.
- `02-diseño/.../crearSesionClase/secuencia.puml` — parámetro renombrado; SVG regenerado.
- `RUP/PLAN-MEJORAS.md` — añadido M6 (marcado `hecho (2026-06-10)`) tras M3 en la tabla resumen y con sección detallada explicando síntoma, decisión de modelado y verificación.

Verificación curl:
- `GET /sesiones-clase` → `grupos` array.
- `POST` con `grupos: []` → 422 "indica al menos un grupo".
- `POST` con `grupos: ["ADE","INF"]` → 201.
- `GET /sesiones-clase/grupos?asignatura_id=...` sigue funcionando con la nueva implementación que aplana JSON.

**Decisión:** M6 marcado `hecho (2026-06-10)`. Falta confirmación del usuario en la UI (chips + datalist), pero la lógica está completa.

## [10:48] M6 confirmado + M7 añadido al plan

**Prompt:** "funciona, marca m6 como hecho, al hacer pruebas, se me ha venido a la cabeza otra duda... el director de grado, en el sistema aparentemente es generico, no pertenece a ningun grado concreto, mientras que en la realidad cada grado tiene uno...".

**Resultado:** M6 confirmado por validación UI del usuario. Sobre la duda del Director: confirmado revisando `RUP/00-requisitos/ModeloDelDominio/DiagramasDeClase/ModeloCompleto.puml` que el **SDR sí modeló `Grado` como entidad** con relaciones explícitas a Director, Secretaria, Matricula y Asignatura. La implementación lo aplanó (`Asignatura.plan_estudios: str`), perdiendo el scoping. Es por tanto una **desviación del SDR**, no algo fuera de alcance.

Sorpresa al revisar el modelo: `DirectorDeGrado(Profesor)` en `models/usuario.py:57` **ya hereda de Profesor**. La STI anidada del SDR ya está. Mi preocupación inicial sobre ese tema era infundada.

Usuario pide implementar tal cual el SDR. Antes de codear, pide que primero se añada M7 al plan como item — la implementación irá después.

**Decisión:** M7 añadido a `RUP/PLAN-MEJORAS.md`:
- Tabla resumen: M7 entre M6 y M4, alto coste, 01+02+03, estado pendiente.
- Sección detallada: síntoma (PoliticaDirector.puede_ver siempre True), causa raíz (SDR aplanado), decisiones, cambios por disciplina, decisiones abiertas (¿catálogo de grados como CU nuevo? ¿cascada del scoping de Secretaria a alumnos/matrículas? ¿migrar Asignatura.facultad limpio?).
- Denominador potencial: 26 → 30 CUs si se añade `gestionarCatalogoGrados`, 29 si los grados quedan seed-only.

Implementación pendiente — próximo paso.

## [11:01] M7 — 01-analisis hecho

**Prompt:** "vamos a empezar con la implementacion de m7, empieza con el analisis".

**Resultado:** Análisis de M7 cerrado siguiendo el principio de [[feedback_scope_minimo_disciplinas]] (no rehacer 10 CUs, solo lo canónico):

- **Nuevo CU `gestionarCatalogoGrados`** en `RUP/01-analisis/casos-uso/gestionarCatalogoGrados/` — README.md detallado + colaboracion.puml + colaboracion.svg. Documenta el CRUD de Grados por Secretaria, justifica por qué Grado sí merece entidad (los 4 criterios del análisis "promover a entidad" se cumplen, contrastando con M6 donde no aplicaba a Grupo) y por qué el catálogo queda global (no scoped) frente al resto de operaciones.
- **4 notas "Evolución post-base"** insertadas al principio del propósito de los CUs con cambio sustantivo de comportamiento:
  - `consultarSolicitudesDispensas` — Director ya no ve "todas" sino las de su grado.
  - `editarSolicitudDispensaDirector` — solo emite veredicto sobre dispensas de su grado.
  - `consultarListaAlumnosSecretaria` — Secretaria ve solo alumnos de su grado.
  - `crearSesionClase` — añadida sección M7 a la nota existente de M6: la decisión "string libre" de Asignatura (deuda señalada en su día para 02-diseño) queda revertida; `plan_estudios` y `facultad` desaparecen y se reemplazan por FK `grado_id`.
- **Índice de la disciplina** (`01-analisis/casos-uso/README.md`) actualizado con sección "Post-base (plan de mejoras)" listando el nuevo CU y bloque "Evolución post-base — CUs con cambio de comportamiento" enumerando los 4 CUs anotados. Progreso ajustado a `26/26 base + 1/3 post-base`.

CUs derivados que no se reescriben (importarMatriculas, consultarDetalleMatricula, exportarDispensas, etc.): el cambio es solo "ahora hay grado_id en la entidad que ya conocían", y se cubre con la referencia al CU `gestionarCatalogoGrados`. Estructura MVC sin cambios.

**Decisión:** Siguiente paso: 02-diseño cuando el usuario lo indique.

## [11:10] Limpieza del análisis tras feedback

**Prompt:** "no los dividas a post-base ... quita todas las referencias al archivo de plan de mejoras ... el diagrama de colaboración me parece muchísimo más complejo que el de el resto de cdu, es necesario o se puede simplificar?".

**Resultado:**
- **Diagrama simplificado**: el `colaboracion.puml` de `gestionarCatalogoGrados` pasó de 6 cajas + 14 flechas a 4 cajas (`GradosView`, `GradoController`, `GradoRepository`, `Grado`) + 6 flechas, mismo orden visual que `crearUsuario`. SVG bajó de 18KB a 8KB.
- **README del CU nuevo rehecho**: una sola `GradosView` (las 3 sub-vistas — listado/formulario/ficha — quedan para 02-diseño). Quitada toda mención a M7 y al `PLAN-MEJORAS.md`. Cabecera "información del artefacto" sin "Origen".
- **4 notas de evolución reescritas**: en `consultarSolicitudesDispensas`, `editarSolicitudDispensaDirector`, `consultarListaAlumnosSecretaria` y `crearSesionClase`. Sin marcadores M6/M7, sin enlaces al plan. Explican el cambio sustantivo de comportamiento de forma autosuficiente.
- **Índice de disciplina** (`01-analisis/casos-uso/README.md`): nuevo CU integrado como una fila más (`27/27 ✅`). Eliminadas sección "Post-base" y lista de CUs con cambio de comportamiento.

`grep -rln "PLAN-MEJORAS" RUP/` confirma cero referencias.

## [11:17] M7 — 02-diseño hecho

**Resultado:** Diseño de M7 cerrado siguiendo el mismo patrón que el análisis (un CU nuevo + 4 notas + índice):

- **Nuevo CU `gestionarCatalogoGrados`** en `RUP/02-diseño/casos-uso/gestionarCatalogoGrados/` — `secuencia.puml` mostrando el flujo de **alta** (operación más representativa, con la validación `UNIQUE(codigo)` → 409, mismo patrón que `crearUsuario`/`username`), README con participantes (`GradosPage`, `gradosService`, `GradosRouter`, `require_rol`, `GradoService`, `GradoRepository`, `SQLite`), tabla de materialización que mapea las 4 operaciones del análisis a `GET/POST/PATCH/DELETE /grados`, y 7 decisiones de diseño (CU agregado en un solo endpoint base, `GradoService` aunque la lógica sea fina, validación de unicidad sin pre-check, validación de referencias en service, `codigo` no editable post-creación, `require_rol(["secretaria"])` sin scoping, `GradosPage` única con sub-vistas).
- **4 notas "Nota — scoping por grado" / "Nota — Asignatura promovida con FK a Grado"** insertadas entre "información del artefacto" y "diagrama de secuencia" (no hay `## propósito` en diseño) en `consultarSolicitudesDispensas`, `editarSolicitudDispensaDirector`, `consultarListaAlumnosSecretaria` y `crearSesionClase`. Cada una concreta qué cambia a nivel de diseño (renombrado de método de repo, guarda adicional en service, WHERE en queries, FK `grado_id` en lugar de `plan_estudios`/`facultad`).
- **Índice de disciplina** (`02-diseño/casos-uso/README.md`) actualizado a `27/27 ✅` con el CU nuevo como fila adicional.

**Decisión:** Siguiente paso: 03-desarrollo cuando el usuario lo indique (modelo `Grado`, FKs, políticas, schemas, frontend, seed, BD reseed).

## [12:17] M7 — 03-desarrollo hecho

**Prompt:** "vamos con el desarrollo".

**Resultado:** M7 implementado completo, tasks #1-#8 cerradas.

Backend:
- `models/grado.py` nuevo (`Grado` con codigo único). FKs añadidas en `Asignatura.grado_id` (sustituye `plan_estudios`/`facultad`), `Matricula.grado_id`, y `Usuario.grado_id` (nullable a nivel STI; solo aplica a Director/Secretaria).
- `schemas/grados.py` (GradoOut, CrearGradoRequest, EditarGradoRequest), `schemas/asignaturas.py` (`grado: GradoOut`), `schemas/usuarios.py` (`grado_id: int | None` con `model_validator` que exige grado_id para tipo ∈ {director, secretaria} y lo prohíbe en los demás; `UsuarioDetalleOut.grado: GradoOut | None`), `schemas/dispensas.py` y `schemas/matriculas.py` (mismo cambio).
- `repositories/grado_repository.py` (CRUD + `referencias` que comprueba asignaturas/matriculas/usuarios). `services/grado_service.py` con `CodigoEnUso`, `GradoNoEncontrado`, `GradoConReferencias`. `routers/grados.py` con CRUD bajo `require_rol(["secretaria"])` registrado en `main.py`.
- `UsuarioService.crear` propaga `grado_id`. `UsuarioRepository.crear` también.
- `PoliticaDirector.puede_ver` y `obtener_listado` filtran por grado vía nuevo `SolicitudDispensaRepository.obtener_por_grado` (JOIN asignaturas_matriculadas + asignaturas). `PoliticaSecretaria` análogo (cascada completa: dispensas, alumnos, matrículas).
- `UsuarioRepository.buscar_alumnos` acepta `grado_id` opcional → subquery sobre `Matricula.grado_id`. `MatriculaRepository.listar` y `get_or_create_header` también. Routers de alumnos y matrículas pasan `usuario.grado_id`. `MatriculaService.importar` exige `grado_id`. `consultar_detalle_matricula` rechaza con 403 si la matrícula no es del grado del usuario.
- `seed.py` rehecho: 2 grados (INF, ADE), 2 directores (`director1`/INF, `director2`/ADE), 2 secretarias (`secretaria1`/INF, `secretaria2`/ADE), 2 alumnos (`alumno1`/INF, `alumno2`/ADE) con matrículas cruzadas (4 asignaturas IYA* en INF, 2 ADE* en ADE) y 1 dispensa adicional en ADE para verificar el scoping cross-grado. Mantiene idempotencia.

Verificación curl tras `rm cgu.db && start.sh`:
- `director1` ve 3 dispensas (todas INF); `director2` ve 1 (ADE). ✓
- `secretaria1` ve 1 alumno (alumno1); `secretaria2` ve 1 (alumno2). ✓
- `POST /grados {codigo: INF}` → 409 "Código de grado en uso". ✓
- `POST /grados` con nuevo MED → 201. ✓
- `DELETE /grados/1` → 409 "tiene referencias en ['asignaturas', 'matriculas', 'usuarios']". ✓
- `POST /usuarios {tipo: "director", ...}` sin grado_id → 422 con mensaje de validador. ✓

Frontend:
- `types/grados.ts`, `services/gradosService.ts` (CRUD).
- `pages/GradosPage.tsx` con tabla + form inline (alta/edición) + delete con confirm. Maneja 409 mostrando el `detail` del backend.
- Ruta `/grados` en `App.tsx` con `secretariaOnly`. Link "Grados" en el nav de Secretaria en `Layout.tsx`.
- `types/asignaturas.ts`, `types/matriculas.ts`, `types/dispensas.ts`, `types/usuarios.ts`: `plan_estudios`/`facultad` → `grado: Grado`. `UsuarioDetalle.grado: Grado | null`. Requests con `grado_id?: number | null`.
- `CrearUsuarioPage.tsx`: select de grado condicional (visible solo si tipo ∈ {director, secretaria}); carga grados al montar; muestra el `detail.msg` del 422 si llega.
- `EditarUsuarioPage.tsx`: idem; lee `original.grado?.id` en el `FormState`; el `diff()` incluye `grado_id` solo si el usuario tiene rol scopable.
- `ConsultarUsuarioPage.tsx`: muestra el grado en la ficha si existe.
- `ConsultarDispensaPage.tsx`: "Plan / facultad" → "Grado: nombre — facultad".
- `ConsultarDetalleMatriculaPage.tsx`: "Plan de estudios"/"Facultad" → "Grado: codigo · nombre"/"Facultad" (ambos desde `matricula.grado`).
- `MatriculasPage.tsx`: columna Grado renderea `m.grado.codigo`.
- `tsc --noEmit` pasa sin errores.

**Decisión:** M7 funcional. Falta confirmación visual del usuario en la UI. App corriendo en http://localhost:5173 y :8000.

## [13:18] M7 corrección: Secretaría como departamento colectivo

**Prompt:** "porque secretaria esta dividida en inf y ade, no deberia ser la misma? ... creo que es un problema de gramatica, el SDR se refería a secretaría (el departamento completo), no a una en concreto".

**Resultado:** Reinterpretación correcta del SDR. La relación `Grado --> SecretariaAcademica : Gestionado por` lee como "gestionado por (el departamento de) Secretaría Académica", no "por una secretaria concreta". Coherente con que `Dispensa --> SecretariaAcademica : Gestionada por` significa "tramitada por Secretaría", no por una cuenta específica.

Mantenido el scoping del Director (es individual: cada grado tiene **su** Director). Revertido el scoping de la Secretaria.

Cambios:
- `schemas/usuarios.py` — `_ROLES_CON_GRADO = {"director"}` (era `{"director","secretaria"}`). El validador exige `grado_id` solo para Director y lo rechaza para Secretaria (y los demás).
- `services/politica_acceso.py::PoliticaSecretaria` — `puede_ver` vuelve a `True`; `obtener_listado` vuelve a `obtener_todas` / `obtener_por_alumno` (sin filtro de grado).
- `routers/alumnos.py::listar_alumnos` — la Secretaria no pasa `grado_id` (ve todos los alumnos).
- `routers/matriculas.py::listar_matriculas`, `consultar_detalle_matricula`, `importar_matriculas` — quita el filtro y la guarda 403 por grado.
- `services/matricula_service.py::importar` — refactorizado para **derivar el grado de la matrícula desde sus asignaturas**: agrupa filas por `(alumno, curso_academico)`, comprueba que todas las asignaturas del header pertenecen al mismo grado (si no, error inline) y usa ese grado para la fila de Matricula.
- `scripts/seed.py` — una sola Secretaría (`secretaria1`, sin grado). `secretaria2` eliminada. Las dos matrículas (alumno1/INF, alumno2/ADE) tienen a `secretaria1` como responsable.
- Frontend `CrearUsuarioPage.tsx` y `EditarUsuarioPage.tsx` — `ROLES_CON_GRADO` reducido a `['director']`. El selector de grado desaparece para Secretaria.

Verificación curl tras reseed:
- `director1` ve 3 dispensas (INF), `director2` ve 1 (ADE). ✓
- `secretaria1` (sin grado) ve **todos**: 2 alumnos, 2 matrículas (INF+ADE), 4 dispensas. ✓
- `POST /usuarios` con `tipo: "secretaria"` + `grado_id` → 422 "`grado_id` no aplica cuando tipo='secretaria'". ✓
- Sin `grado_id` → 201 con `grado: null`. ✓
- `tsc --noEmit` pasa.

**Decisión:** Modelo final: Director scopeado por grado (relación 1:1 con identidad), Secretaría global (departamento colectivo). Coherente con la lectura natural del SDR.

## [13:21] Cierre de sesión

**Prompt:** "finaliza la sesion".

**Resultado:** Servidores en background parados (`uvicorn` y `vite`). BD en estado seed limpio tras la última reescritura del scoping. Cambios sin commitear, listos para que el usuario haga `git commit` con uno de los títulos sugeridos (recomendado: "implementacion cdu gestionarCatalogoGrados + scoping director por grado"). 41 archivos pendientes — 7 nuevos + 34 modificados.

**Decisión:** Cierre formal de la sesión 2026-06-10. Resumen del día:

- M1 (asistencias en ficha del alumno), M2 (filtro en /sesiones-clase), M3 (grupos derivados del historial) — implementados, validados y marcados hechos.
- M6 (sesiones con N grupos en JSON list) — implementado tras detectar el caso real de Inglés con varios grados.
- M7 (entidad Grado del SDR restaurada + scoping del Director por grado) — implementado completo en las tres disciplinas RUP. La Secretaría queda como departamento colectivo (sin scoping) tras revisión lingüística del SDR.
- 1 CU nuevo añadido al sistema: `gestionarCatalogoGrados` (CRUD por Secretaría sobre el catálogo de grados). Total: 26 → 27 CUs.
- Plan de mejoras (`RUP/PLAN-MEJORAS.md`) ya solo lo usa el usuario como tracking personal; las referencias en RUP están limpias (grep confirma 0).

Estado del proyecto al cierre: M1, M2, M3, M6 y M7 cerrados. Quedan en el plan personal del usuario M4 (alta individual de alumno por Secretaria) y M5 (catálogo de asignaturas + asignar profesor↔asignatura).

---

### Sesión 2026-06-11

## [10:18] Apertura + corrección de PLAN-MEJORAS

**Prompt:** "vamos a empezar con la siguiente mejora de las propuestas anteriormente, imagino que me recomiendes empezar por la m7, no?, y como veo que involucra todas las etapas de RUP, vamos a empezar por el analisis".

**Resultado:** Aviso de que M7 quedó hecha ayer; la siguiente en el orden recomendado del plan (M1→M2→M3→M6→M7→M4→M5) es **M4 — alta individual de alumno por Secretaria**. Al ver que el archivo no reflejaba M7 como hecha, el usuario pidió arreglarlo. En `RUP/PLAN-MEJORAS.md`:
- Fila de la tabla resumen: M7 marcada `hecho (2026-06-10)`.
- Título de la sección M7: añadido `· **hecho (2026-06-10)**` (mismo formato que M1/M2/M3/M6).
- Resumen de ejecución de M7 insertado en la sección: bloque enumerando análisis/diseño/desarrollo + la corrección lingüística del SDR (Secretaría como departamento colectivo, scoping solo para Director).

**Decisión:** Arrancamos M4 por la disciplina 01-analisis. Antes de redactar, dos preguntas zanjadas con el usuario:
1. Forma del CU `crearAlumno` → **espejo literal de `crearUsuario`** (mismo flujo, actor Secretaria, tipo fijo `alumno`).
2. CU `crearUsuario` tras M4 → **mantener el nombre** con una nota de evolución que recorta su alcance (excluye `tipo=alumno`).

## [10:21] M4 — 01-analisis hecho

**Resultado:** Análisis de M4 cerrado siguiendo [[feedback_scope_minimo_disciplinas]] (un CU nuevo + una nota de evolución + índice):

- **Nuevo CU `crearAlumno`** en `RUP/01-analisis/casos-uso/crearAlumno/` — `colaboracion.puml` con 4 cajas (`CrearAlumnoView`, `AlumnoController`, `UsuarioRepository`, `Alumno`) + 5 mensajes (mismo esqueleto que `crearUsuario` pero sin el `<<include>> editarUsuario`: como el `tipo` está fijo y los campos personales son pocos, se capturan todos en el formulario único). README explicando por qué se reutiliza `AlumnoController` (Controller por entidad ya consolidado en consultarListaAlumnos / consultarDetalleAlumno / importarListasAlumnos), por qué la persistencia sigue en `UsuarioRepository` (mantener ahí el punto único de despacho polimórfico establecido en `crearUsuario`) y formalizando el reparto Administrador (cuentas de personal) ↔ Secretaria (datos académicos) como principio subyacente al plan post-base.
- **Nota "Nota — alcance"** insertada al principio del `## propósito` de `crearUsuario`: el dominio del parámetro `tipo` se reduce (ya no admite `alumno`), Profesor/DirectorDeGrado/Secretaria/Administrador siguen. Sin marcadores M4 ni enlaces al plan, autosuficiente (mismo patrón que las notas de M7).
- **Índice de la disciplina** (`01-analisis/casos-uso/README.md`): fila de `crearAlumno` añadida bajo el bloque de Secretaria; progreso `27/27` → `28/28`.

**Decisión:** Siguiente paso: 02-diseño cuando el usuario lo indique.

## [10:29] M4 análisis — limpieza tras feedback

**Prompt:** "elimina la nota que has puesto en crearUsuario, no son necesarias y lo unico que hacen es complicar las cosas, y, en crear alumno, veo un code smell de demasiados parametros de un metodo, no? se podria arreglar o es intrinseco al sistema?".

**Resultado:**
- **Nota de alcance eliminada** del `## propósito` de [[crearUsuario]]. La enumeración del propósito ya refleja sólo {Profesor, Secretaria, DirectorDeGrado, Administrador}; eso basta como reflejo del estado actual. Política reafirmada: el análisis se lee como verdad presente, no como diario de cambios. (Para cambios sustantivos de comportamiento sí queda nota, como las de M7 — la diferencia es que en M4 `crearUsuario` no cambia su flujo MVC, solo se reduce el dominio del parámetro.)
- **Smell "Long Parameter List" confirmado** en `crearAlumno` (6 parámetros). No es intrínseco — el proyecto ya tiene precedente: [[crearSesionClase]] aplicó "Introduce Parameter Object" (Fowler) con `DatosSesionClase` para el mismo smell, y dejó registrada como "deuda blanda" la extensión a otros CUs con ≥4 parámetros. `crearAlumno` consume parte de esa deuda.
- **Refactor aplicado** en `crearAlumno`: nuevo value object `DatosPersonalesAlumno` agrupa los 4 campos personales (nombre, apellidos, email, teléfono). Las credenciales (login, contraseña) quedan **fuera del DTO** para preservar la simetría con [[crearUsuario]] (donde auth y datos personales también van separados, vía `<<include>> editarUsuario`). Firmas resultantes: mensaje 4 `crearAlumno(login, contraseña, datos) : Alumno` (3 params); mensaje 5 `crear(tipo, login, contraseña, datos) : Alumno` (4 params).
- **Diagrama actualizado** (5 cajas + DatosPersonalesAlumno) y **sección "refactor Introduce Parameter Object"** añadida al README con tabla antes/después, qué entra/no entra en el DTO y un cuadro de alcance comparando los 4 `crear*` del proyecto.

**Decisión:** 01-analisis de M4 cerrado limpio. Esperando luz verde para 02-diseño.

## [10:39] M4 — 02-diseño hecho

**Prompt:** "perfecto, vamos con el diseno".

**Resultado:** Diseño de M4 cerrado:

- **Nuevo CU `crearAlumno`** en `RUP/02-diseño/casos-uso/crearAlumno/` — `secuencia.puml` con frontend (`CrearAlumnoPage`, `alumnosService`), backend (`AlumnosRouter POST /alumnos`, `require_rol`, `UsuarioService`, `UsuarioRepository`) y SQLite; rama `alt` para login libre / login en uso (mismo patrón que `crearUsuario`). README con participantes, tabla de materialización del análisis (5 mensajes) y 7 decisiones de diseño:
  - **Canal HTTP separado**: `POST /alumnos` (no `/usuarios`); `POST /usuarios` rechaza `tipo="alumno"` con 422.
  - **`UsuarioService.crear` reutilizado** con `tipo="alumno"` fijado por el router; el polimorfismo de instanciación sigue siendo single-source en `UsuarioRepository`. Justificado el preferir reuse vs. nuevo `AlumnoService` (a diferencia de `GradoService` donde no había alternativa).
  - **`require_rol(["secretaria"])` sin scoping por grado** (la Secretaría es departamento colectivo desde [[gestionarCatalogoGrados]]; el grado del alumno se deriva luego desde sus matrículas).
  - **`DatosPersonalesAlumno` se materializa como `CrearAlumnoRequest` (Pydantic)**, viaja aplanado en el wire por ergonomía del formulario pero se pasa como unidad entre service y repository. Precedente: `crearSesionClase` con `CrearSesionClaseRequest`.
  - **Ruta `/alumnos/nuevo`** (no modal), coherencia con `/usuarios/nuevo`.
  - **Validación de unicidad sin pre-check** (UNIQUE+IntegrityError → 409), mismo patrón.
  - **Doble defensa cliente+servidor** al retirar `alumno` del `<select>` de `CrearUsuarioPage`.
- **Índice de la disciplina** (`02-diseño/casos-uso/README.md`): fila de `crearAlumno` añadida; progreso `27/27` → `28/28`.

**Decisión:** Siguiente paso: 03-desarrollo cuando el usuario lo indique.

## [11:18] M4 — 03-desarrollo hecho

**Prompt:** "perfecto, vamos por ultimo con el desarrollo".

**Resultado:** M4 implementado completo. Tasks #4–#9 cerradas.

Backend (3 archivos tocados):
- `schemas/alumnos.py` — nuevo `CrearAlumnoRequest` (username, password, nombre, apellidos, email). Sin `telefono` porque el modelo `Usuario` no lo tiene; añadirlo excede el alcance del CU (registrado como divergencia en el README de 03-desarrollo).
- `routers/alumnos.py` — nuevo `POST /alumnos` protegido por `require_rol(["secretaria"])`. Construye internamente un `CrearUsuarioRequest` con `tipo="alumno"` fijo + `grado_id=None` y delega en `UsuarioService.crear`. El polimorfismo de instanciación queda single-source en `UsuarioRepository.crear`.
- `routers/usuarios.py` — guarda en `crear_usuario` que rechaza `tipo="alumno"` con 422 ("El alta de alumno corresponde a Secretaría (POST /alumnos).") antes de invocar al service. Doble defensa.

Frontend (5 archivos tocados):
- `types/alumnos.ts` — `CrearAlumnoRequest` añadida.
- `services/alumnosService.ts` — método `crear(datos)` → `POST /alumnos` devuelve `UsuarioDetalle`.
- `pages/CrearAlumnoPage.tsx` — nueva página. Form con 5 campos, maneja 409 (username en uso) y 422 (validación), `navigate("/alumnos")` al éxito.
- `App.tsx` — ruta `/alumnos/nuevo` con `secretariaOnly`. Import del nuevo componente.
- `pages/AlumnosPage.tsx` — botón "+ Nuevo alumno" añadido al header, visible solo cuando `usuario.tipo === 'secretaria'` (vía `useAuth`). El botón "Importar listas" sigue donde estaba, también gated.
- `pages/CrearUsuarioPage.tsx` — `'alumno'` retirado de `TIPOS`; `tipo` por defecto cambiado a `'profesor'`. Comentario explicando que el alta de alumno la opera Secretaria por `/alumnos`.

Verificación curl (`secretaria1`/`secre123`, `admin`/`admin123`):
- `POST /alumnos` con datos válidos → 201 + `{id, tipo:"alumno", grado:null, …}`. ✓
- `POST /alumnos` con username duplicado → 409 "El username ya está en uso". ✓
- `POST /usuarios` con `tipo="alumno"` → 422 con mensaje explícito. ✓
- `POST /alumnos` con token de admin → 403 "No autorizado para esta operación". ✓
- `POST /usuarios` con `tipo="profesor"` → 201 (no regresión). ✓
- `GET /alumnos?q=alumno9` → el alumno recién creado aparece. ✓
- `tsc --noEmit` pasa sin errores.

Documentación:
- Nuevo README en `RUP/03-desarrollo/casos-uso/crearAlumno/` con trazabilidad código↔diseño, una divergencia documentada (sin teléfono) y verificación.
- Índice de la disciplina actualizado a `27/27 ✅` (faltaba reflejar también el `gestionarCatalogoGrados` de M7 — deuda menor del cierre anterior; no se toca ahora para no mezclar mejoras).

**Decisión:** M4 funcional. App corriendo en http://localhost:5173 y :8000 para la confirmación visual del usuario.

**Guion de prueba manual sugerido:**
1. Login como `secretaria1`/`secre123`. Navegar a `/alumnos`. Confirmar que aparecen los botones "+ Nuevo alumno" e "Importar listas".
2. Click "+ Nuevo alumno" → pantalla `/alumnos/nuevo` con form de 5 campos.
3. Crear `alumno10` con datos cualesquiera. Tras el alta, vuelve al listado y el alumno aparece (puede requerir search por nombre).
4. Repetir el alta con el mismo username → mensaje "Ese username ya está en uso" inline.
5. Logout. Login como `admin`/`admin123`. Navegar a `/usuarios/nuevo`. El `<select>` de tipo ya no muestra "alumno"; el resto sigue.
6. Logout. Login como `profesor1`/`profe123`. Navegar a `/alumnos?asignatura_id=1`. El botón "+ Nuevo alumno" NO debe aparecer (solo Secretaria).

## [11:21] Deuda menor de M7 saldada — README de gestionarCatalogoGrados

**Prompt:** "ahora que lo veo del apartado 03 desarrollo falta gestionar catalogo grado, no?, solo falta en el 03 de RUP o tambien falta el codigo? ... sí, redáctalo".

**Resultado:** Confirmado por inspección que el código de `gestionarCatalogoGrados` está completo desde M7 (backend: `models/grado.py`, `schemas/grados.py`, `repositories/grado_repository.py`, `services/grado_service.py`, `routers/grados.py`; frontend: `types/grados.ts`, `services/gradosService.ts`, `pages/GradosPage.tsx`, ruta `/grados` en `App.tsx:75`, enlace "Grados" en `Layout.tsx:59`). Solo faltaba la documentación. Añadido `RUP/03-desarrollo/casos-uso/gestionarCatalogoGrados/README.md` con trazabilidad código↔diseño, divergencia documentada (`PoliticaSecretaria` sin scoping por la revisión lingüística del SDR de ayer) y tabla de verificación curl. Índice de 03-desarrollo a `28/28 ✅`.

**Decisión:** Deuda saldada sin tocar código. Las tres disciplinas RUP ahora cuadran (`28/28` en 01-analisis, 02-diseño y 03-desarrollo).
