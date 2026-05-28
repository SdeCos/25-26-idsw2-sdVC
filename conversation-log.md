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
