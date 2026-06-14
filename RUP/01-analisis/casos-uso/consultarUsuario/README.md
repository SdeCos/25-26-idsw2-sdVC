# CGU > consultarUsuario > Análisis

> | [🏠️](/README.md) | [Análisis](/RUP/01-analisis/README.md) | [Detalle](/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Administrador/) | **Análisis** | Diseño | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Inception
- **Disciplina**: Análisis
- **Caso de uso**: `consultarUsuario()`
- **Actor**: Administrador
- **Versión**: 1.0
- **Fecha**: 2026-05-26

## propósito

Análisis del caso de uso `consultarUsuario()` mediante diagrama de colaboración MVC. Es el CU **read-only** del CRUD: el Administrador visualiza la ficha completa de un usuario (datos, roles, permisos) desde el listado, con opción de saltar a [[editarUsuario]] vía `<<include>>` si decide modificar.

## diagrama de colaboración

<div align=center>

|![Análisis consultarUsuario()](/images/RUP/01-analisis/casos-uso/consultarUsuario/colaboracion.svg)|
|-|
|**Disciplina**: Análisis RUP<br>**Enfoque**: Diagramas de colaboración MVC|

</div>


[Código PlantUML](/modelosUML/RUP/01-analisis/casos-uso/consultarUsuario/colaboracion.puml)
## clases de análisis identificadas

### clases model (naranja #F2AC4E)

| Clase | Responsabilidad | Trazabilidad |
|-|-|-|
| **Usuario** | Clase abstracta; la instancia consultada conserva su subtipo concreto | Reutilizada de [[iniciarSesion]], [[crearUsuario]], [[editarUsuario]] |
| **UsuarioRepository** | Recupera el usuario por id (operación de solo lectura) | Reutilizado; usa `obtenerPorId(id)` ya introducido en [[editarUsuario]] |

### clases view (azul #629EF9)

| Clase | Responsabilidad | Derivación |
|-|-|-|
| **ConsultarUsuarioView** | Ficha de visualización (solo lectura) del usuario y punto de salto a edición | [Prototipos SALT `consultarUsuario1.png` y `consultarUsuario2.png`](/RUP/00-requisitos/CasosDeUso/Prototipos/Administrador/) |

### clases controller (verde #b5bd68)

| Clase | Responsabilidad | Casos de uso |
|-|-|-|
| **UsuarioController** | Orquestación del CRUD individual de `Usuario`: validación, alta, carga y modificación | Compartido entre `crearUsuario()`, `consultarUsuario()` y `editarUsuario()` (mismo controller que en [[crearUsuario]] y [[editarUsuario]]) |

### colaboraciones (verde claro #CDEBA5)

| Colaboración | Propósito | Invocación |
|-|-|-|
| **:Usuarios Abierto** | Estado de origen (listado desde el que se solicita la consulta) | Punto de entrada del caso de uso |
| **:Collaboration EditarUsuario** | Sub-colaboración a la que se delega la modificación si el Admin decide editar | Vía `<<include>>` desde la vista |

## mensajes de colaboración

### flujo principal

| # | Origen | Destino | Mensaje | Intención |
|-|-|-|-|-|
| 1 | **:Usuarios Abierto** | **ConsultarUsuarioView** | `consultarUsuario(usuarioId)` | Abrir la ficha del usuario seleccionado |
| 2 | **ConsultarUsuarioView** | **UsuarioController** | `cargarUsuario(usuarioId) : Usuario` | Recuperar la instancia tipada |
| 3 | **UsuarioController** | **UsuarioRepository** | `obtenerPorId(usuarioId) : Usuario` | Consulta al repositorio |
| 4 | **ConsultarUsuarioView** | **:Collaboration EditarUsuario** | `<<include>> editarUsuario(usuarioId)` | Saltar a edición si el Admin lo solicita |

### flujo alternativo — salir sin editar

El mensaje 4 es **opcional**: el Admin puede cerrar la consulta sin invocar la edición (transición `cerrarUsuario()` del detallado). En ese caso solo se ejecutan los mensajes 1-3 y la `ConsultarUsuarioView` se cierra volviendo a `:Usuarios Abierto`. No requiere clase adicional.

## enlaces de dependencia

- **ConsultarUsuarioView** conoce a **UsuarioController** (delegación)
- **ConsultarUsuarioView** conoce a **:Collaboration EditarUsuario** (transición/inclusión opcional)
- **UsuarioController** conoce a **UsuarioRepository** (lectura)
- **UsuarioController** conoce a **Usuario** (manipulación entidad)
- **UsuarioRepository** conoce a **Usuario** (gestión polimórfica)

## polimorfismo y herencia

`obtenerPorId(usuarioId) : Usuario` (mensaje 3) devuelve el **subtipo concreto** del usuario consultado, igual que en [[editarUsuario]]. La `ConsultarUsuarioView` puede aprovechar el subtipo para presentar campos específicos (un `Profesor` muestra su departamento; un `Alumno` su matrícula).

```
Usuario (abstract)
├── Alumno
├── Profesor
│   └── DirectorDeGrado
└── SecretariaAcademica
        └── Administrador (hereda también de Alumno, Profesor y DirectorDeGrado)
```

A diferencia de [[editarUsuario]], aquí la vista es de **solo lectura**: no hay invariantes que mantener sobre el subtipo durante la sesión de consulta (no se modifica nada).

## comparación con los otros CUs del bloque Administrador

| Característica | [[crearUsuario]] | `consultarUsuario` | [[editarUsuario]] |
|-|-|-|-|
| Operaciones | Validación + escritura | Solo lectura | Lectura + escritura |
| Puntos de entrada | 1 (`:Usuarios Abierto`) | 1 (`:Usuarios Abierto`) | 3 (listado, consulta, post-crear) |
| Mensajes al Repository | `existeLogin`, `crear` | `obtenerPorId` | `obtenerPorId`, `actualizar` |
| Polimorfismo | Escritura (instancia subtipo) | Lectura (subtipo invariante) | Lectura (subtipo invariante) |
| `<<include>>` saliente | a `editarUsuario` (siempre) | a `editarUsuario` (opcional) | — |

El bloque cierra coherentemente: **crear** delega siempre a editar para completar datos; **consultar** delega opcionalmente a editar si hay cambios; **editar** es el punto de convergencia que reúne los tres flujos.

## trazabilidad con artefactos previos

### con especificación detallada

- **Estado `USUARIOS_ABIERTO`** → **colaboración `:Usuarios Abierto`** (origen)
- **Estado `VisualizacionDatos`** ("Visualización de Usuario") → **`ConsultarUsuarioView`** + mensajes 1-3 (carga read-only)
- **Nota "Administrador solicita gestionar cambios mediante `editarUsuario()`"** → **mensaje 4** (`<<include>>` opcional a edición)
- **Transición `cerrarUsuario()`** → flujo alternativo (cierre sin editar)
- **Transición `guardarUsuario()`** del detallado: **no aplica directamente** a consulta — solo cobra sentido si se entra a la edición; la persistencia sucede en [[editarUsuario]]

### con wireframe (prototipo SALT)

- **`consultarUsuario1.png`** y **`consultarUsuario2.png`** → **ConsultarUsuarioView** (dos pantallas: probablemente listado + ficha; o ficha en dos vistas)
- El subtipo concreto del usuario determina qué campos aparecen (responsabilidad de la vista en tiempo de render)

### con actores

- **Jerarquía `Usuario → {Alumno, Profesor, …}`** → invariante de subtipo durante la consulta; los campos visibles dependen del subtipo cargado

### con modelo del dominio

- **Sin trazabilidad directa**: deuda compartida con [[iniciarSesion]], [[crearUsuario]] y [[editarUsuario]].

## principios de análisis aplicados

### patrón mvc

- **Controller compartido por entidad**: `UsuarioController` (consistente con [[crearUsuario]] y [[editarUsuario]])
- **Vista específica por CU**: `ConsultarUsuarioView` es read-only, distinta de `CrearUsuarioView` y `EditarUsuarioView`
- **Modelo polimórfico**: lectura del subtipo concreto sin manipulación

### diagramas de colaboración

- **CU mínimo**: 4 mensajes, el más compacto del bloque
- **`<<include>>` opcional documentado en prosa**: el diagrama lo muestra como dependencia; la opcionalidad vive en el flujo alternativo del README

### análisis puro

- **Sin tecnología**: cómo se renderizan los campos del subtipo es decisión de diseño
- **Sin paginación ni búsqueda**: el detallado no las menciona; emergerán en diseño si el listado lo requiere

## características del análisis

### responsabilidades identificadas

- **ConsultarUsuarioView**: cargar y presentar la ficha del usuario; ofrecer salto a edición
- **UsuarioController**: mediar entre vista y repositorio para la lectura
- **UsuarioRepository**: recuperar la instancia tipada
- **Usuario**: representar la entidad consultada (subtipo invariante)

### relaciones conceptuales

- **Delegación**: vista delega lógica al controlador
- **Lectura**: controlador accede al repositorio sin modificar nada
- **Inclusión opcional**: la vista puede invocar `editarUsuario()` si el Admin lo solicita

## conexión con disciplinas rup

### desde requisitos

- **Detallado**: `VisualizacionDatos` con nota "gestionar cambios mediante `editarUsuario()`" → mensaje 4 (`<<include>>` opcional)
- **Prototipos SALT**: dos pantallas de consulta → `ConsultarUsuarioView`
- **Actores**: jerarquía → render condicional por subtipo

### hacia diseño

- Render condicional de campos por subtipo (compartido con [[editarUsuario]])
- Necesidad de listado paginado de usuarios (`:Usuarios Abierto` como CU explícito si crece el volumen)
- Auditoría de consultas (¿se registra quién consultó qué? — preocupación de seguridad si los datos son sensibles)
- Permisos finos: ¿puede un Admin consultar a otro Admin? (regla de negocio pendiente)
- Reconciliación de `Usuario` con el modelo del dominio (compartida con todo el bloque)

**Código fuente:** [colaboracion.puml](/modelosUML/RUP/01-analisis/casos-uso/consultarUsuario/colaboracion.puml)

## referencias

- [Detallado `consultarUsuario()`](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Administrador/consultarUsuario.puml)
- [Prototipo SALT `consultarUsuario1.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Administrador/consultarUsuario1.png)
- [Prototipo SALT `consultarUsuario2.png`](/images/RUP/00-requisitos/CasosDeUso/Prototipos/Administrador/consultarUsuario2.png)
- [Caso de uso del Administrador](/modelosUML/RUP/00-requisitos/CasosDeUso/CasoDeUso/Administrador/Administrador.puml)
- [Análisis `crearUsuario()`](/RUP/01-analisis/casos-uso/crearUsuario/README.md)
- [Análisis `editarUsuario()`](/RUP/01-analisis/casos-uso/editarUsuario/README.md)
- [conversation-log.md](/conversation-log.md)
