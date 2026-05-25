# Análisis

Disciplina RUP de análisis del Centro de Gestión Universitaria.

Para cada caso de uso con detalle en [`RUP/00-requisitos/`](/RUP/00-requisitos/CasosDeUso/DetalladoCasosDeUso/) se produce un **diagrama de colaboración MVC** que identifica las clases de análisis y los mensajes entre ellas. Las clases de análisis son conceptuales: aún no son clases de implementación, sino responsabilidades.

## Metodología

Patrón **MVC** con tres estereotipos:

| Estereotipo | Color | Rol |
|---|---|---|
| **View** (Boundary) | `#629EF9` | Interfaz con el actor |
| **Control** (Controller) | `#b5bd68` | Orquestación del caso de uso |
| **Entity** (Model) | `#F2AC4E` | Entidades del dominio y repositorios |
| **Collaboration** | `#CDEBA5` | Estado/CU destino tras el caso |

Heurísticas:
- **Un controlador por caso de uso.**
- **Vista derivada del prototipo** del requisitado.
- **Entidades derivadas del modelo del dominio** cuando existen; cuando no, emergen como conceptos de análisis (caso de `Sesion`).
- **Mensajes de intención**, no de implementación.

## Casos de uso analizados

Ver [índice](casos-uso/README.md).

## Referencias

- [Requisitado](/RUP/00-requisitos/)
- [pySigHor — análisis](https://github.com/mmasias/pySigHor/tree/main/RUP/01-analisis) (proyecto guía)
- [Temario IDSW2](https://github.com/mmasias/25-26-IdSw2)
