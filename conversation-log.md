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
