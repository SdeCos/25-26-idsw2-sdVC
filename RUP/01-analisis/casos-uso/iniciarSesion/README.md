# CGU > iniciarSesion > Análisis

> | [🏠️](/README.md) | [Análisis](/RUP/01-analisis/README.md) | [Detalle](/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Usuario/) | **Análisis** | Diseño | Desarrollo |
> |-|-|-|-|-|-|

## información del artefacto

- **Proyecto**: Centro de Gestión Universitaria (CGU)
- **Fase RUP**: Inception
- **Disciplina**: Análisis
- **Caso de uso**: `iniciarSesion()`
- **Actor**: Usuario (superclase abstracta de Alumno, Profesor, Secretaria, Director, Administrador)
- **Versión**: 1.0
- **Fecha**: 2026-05-25

## propósito

Análisis del caso de uso `iniciarSesion()` mediante diagrama de colaboración MVC, identificando clases de análisis y sus interacciones conceptuales para realizar el caso de uso.

## diagrama de colaboración

<div align=center>

|![Análisis iniciarSesion()](/images/RUP/01-analisis/casos-uso/iniciarSesion/colaboracion.svg)|
|-|
|**Disciplina**: Análisis RUP<br>**Enfoque**: Diagramas de colaboración MVC|

</div>


[Código PlantUML](/modelosUML/RUP/01-analisis/casos-uso/iniciarSesion/colaboracion.puml)
## clases de análisis identificadas

### clases model (naranja #F2AC4E)

| Clase | Responsabilidad | Trazabilidad |
|-|-|-|
| **Usuario** | Clase abstracta; representa cualquier actor autenticable. La instancia real es siempre de un subtipo concreto (polimorfismo) | [Actores.puml](/modelosUML/RUP/00-requisitos/CasosDeUso/Actores/Actores.puml) — superclase de la jerarquía |
| **UsuarioRepository** | Verifica credenciales y devuelve la instancia concreta del `Usuario` | Análisis puro — choice point del detallado |
| **Sesion** | Estado de autenticación activa; conoce al `Usuario` autenticado | Concepto emergente del análisis |

### clases view (azul #629EF9)

| Clase | Responsabilidad | Derivación |
|-|-|-|
| **LoginView** | Ventana principal de interacción para autenticación | [Prototipo SALT](/modelosUML/RUP/00-requisitos/CasosDeUso/Prototipos/Usuario/iniciarSesion.puml) |

### clases controller (verde #b5bd68)

| Clase | Responsabilidad | Caso de uso |
|-|-|-|
| **IniciarSesionController** | Orquestación completa: validación de credenciales y creación de sesión | iniciarSesion() |

### colaboraciones (verde claro #CDEBA5)

| Colaboración | Propósito | Invocación |
|-|-|-|
| **:Sistema Disponible** | Transición al estado destino tras autenticación exitosa | Tras crear la sesión |

## mensajes de colaboración

### flujo principal

| # | Origen | Destino | Mensaje | Intención |
|-|-|-|-|-|
| 1 | **Usuario** (actor) | **LoginView** | `iniciarSesion(usuario, contraseña)` | Solicitar acceso al sistema |
| 2 | **LoginView** | **IniciarSesionController** | `autenticar(usuario, contraseña) : Sesion` | Delegar proceso de autenticación |
| 3 | **IniciarSesionController** | **UsuarioRepository** | `validarCredenciales(usuario, contraseña) : Usuario` | Verificar credenciales y obtener al usuario tipado |
| 4 | **IniciarSesionController** | **Sesion** | `crearSesion(usuario) : Sesion` | Establecer sesión activa |
| 5 | **LoginView** | **:Sistema Disponible** | `sistemaDisponible(usuario)` | Transición al sistema disponible |

### flujo alternativo — credenciales no válidas

El choice point del detallado se resuelve en el mensaje 3. Si `validarCredenciales(...)` indica fallo (return `null` o excepción), el `IniciarSesionController` propaga la condición a la `LoginView`, que vuelve al estado `SolicitandoAcceso`. Los mensajes 4 y 5 no se ejecutan. No se modela como mensaje aparte: es el comportamiento por defecto del retorno del mensaje 3.

## enlaces de dependencia

- **LoginView** conoce a **IniciarSesionController** (delegación)
- **LoginView** conoce a **:Sistema Disponible** (transición de estado)
- **IniciarSesionController** conoce a **UsuarioRepository** (validación)
- **IniciarSesionController** conoce a **Sesion** (creación)
- **IniciarSesionController** conoce a **Usuario** (manipulación entidad)
- **UsuarioRepository** conoce a **Usuario** (gestión polimórfica)

## polimorfismo y herencia

El mensaje 3 está tipado como `: Usuario`, pero la instancia devuelta es del **subtipo concreto** según el usuario autenticado. Permisos y comportamientos viajan con el tipo, no con un atributo `rol`:

```
Usuario (abstract)
├── Alumno
├── Profesor
│   └── DirectorDeGrado
└── SecretariaAcademica
        └── Administrador (hereda también de Alumno, Profesor y DirectorDeGrado)
```

A partir del mensaje 3 el sistema despacha comportamiento por el tipo real del `Usuario` sin condicionales sobre rol — la herencia hace el trabajo.

## trazabilidad con artefactos previos

### con especificación detallada

- **Estados internos** (`SolicitandoAcceso`, `ProporcionandoCredenciales`) → **clases de análisis** (responsabilidades en `LoginView` y `IniciarSesionController`)
- **Choice point** → **`UsuarioRepository.validarCredenciales()`**
- **Transición `SESION_CERRADA → SISTEMA_DISPONIBLE`** → **colaboración `:Sistema Disponible`**

### con wireframe (prototipo SALT)

- **Diálogo de login** → **LoginView**
- **Campos usuario/contraseña** → **atributos conceptuales de LoginView**
- **Mensaje de error** → **flujo alternativo gestionado en LoginView**

### con actores

- **Jerarquía Usuario → {Alumno, Profesor, Secretaria, Director, Admin}** → **modelo polimórfico de `Usuario`** (clase abstracta con subtipos)

### con modelo del dominio

- **Sin trazabilidad directa**: ni `Usuario` ni `Sesion` aparecen en `ModeloCompleto.puml`. Ambas emergen en análisis y se reconciliarán en diseño.

## principios de análisis aplicados

### patrón mvc

- **Un controlador por caso de uso**: IniciarSesionController
- **Vista derivada de prototipo**: LoginView desde wireframe SALT
- **Modelo polimórfico**: Usuario abstracto con subtipos

### diagramas de colaboración

- **Foco en enlaces**: dependencias conceptuales, no secuencia temporal
- **Mensajes de intención**: qué se quiere lograr, no cómo implementar
- **Trazabilidad**: cada clase identificada participa en la colaboración

### análisis puro

- **Sin tecnología**: UsuarioRepository es concepto, no implementación
- **Sin detalles de UI**: LoginView es interfaz conceptual
- **Sin implementación**: los mensajes expresan intención de negocio

## características del análisis

### responsabilidades identificadas

- **LoginView**: capturar credenciales y coordinar el flujo de autenticación
- **IniciarSesionController**: orquestar la lógica completa del caso de uso
- **UsuarioRepository**: proveer acceso conceptual con resolución polimórfica del subtipo
- **Usuario**: representar al actor autenticable (clase abstracta del análisis)
- **Sesion**: mantener el estado de autenticación activa

### relaciones conceptuales

- **Delegación**: vista delega la lógica al controlador
- **Acceso**: controlador accede al repositorio para validación
- **Creación**: controlador crea la sesión tras validación exitosa
- **Transición**: vista coordina la transición al estado `SISTEMA_DISPONIBLE`

## conexión con disciplinas rup

### desde requisitos

- **Detallado**: estados y choice point → responsabilidades de clases y mensajes
- **Prototipo SALT**: wireframe → diseño conceptual de la vista
- **Actores**: jerarquía → modelo de herencia polimórfica de `Usuario`

### hacia diseño

- Estrategia de herencia en BD para `Usuario` (single-table, joined-table, table-per-class)
- Política de gestión de `Sesion` (memoria, JWT, sesión de servidor)
- Hashing y almacenamiento seguro de contraseñas
- Inactividad y expiración (referido en el detallado como `sesionInactiva()`)
- Reconciliación con el modelo del dominio: ¿se promueve `Usuario` a clase de dominio?

**Código fuente:** [colaboracion.puml](/modelosUML/RUP/01-analisis/casos-uso/iniciarSesion/colaboracion.puml)

## referencias

- [Detallado `iniciarSesion()`](/modelosUML/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/Usuario/iniciarSesion.puml)
- [Prototipo SALT](/modelosUML/RUP/00-requisitos/CasosDeUso/Prototipos/Usuario/iniciarSesion.puml)
- [Actores.puml](/modelosUML/RUP/00-requisitos/CasosDeUso/Actores/Actores.puml)
- [Diagrama de contexto](/modelosUML/RUP/00-requisitos/CasosDeUso/DiagramaDeContexto/DiagramaDeContexto.puml)
- [Modelo del dominio](/modelosUML/RUP/00-requisitos/ModeloDelDominio/DiagramasDeClase/ModeloCompleto.puml)
- [conversation-log.md](/conversation-log.md)
