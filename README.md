# Inventario JIT

Este proyecto trata de la organización del inventario de una empresa, la cual recibe remesas y 
pedidos de material. Lo que buscamos con este proyecto es crear una estructura eficiente para 
la organización de los ingresos de material mediante las remesas y los retiros de material mediante 
los pedidos.

## Integrantes

- Margarita Blasco
- Benicio Deambrogio
- Facundo Maresca
- Felipe Siri
- Nicoletta Battaglini

## Estado actual

Actualmente, el proyecto aun esta en una etapa inicial. Hasta el momento, realizamos el UML,
y acorde al mismo, creamos las clases correspondientes. Incluimos relaciones de herencia tanto
en las clases Movimiento con MovimientoIngreso y MovimientoRetiro, como en PoliticaConsumo con 
PoliticaFEFO. También, ya codeamos algunos metodos simples en algunas de las clases. Otros metodos,
en clases como Deposito, reconocemos que requieren mas conocimientos teóricos de la materia que 
todavia no tenemos. Además, ya estan todos los atributos y todos los setters y getters de todas 
las clases. Priorizamos el hecho de no utilizar herramientas que todavía no hayamos visto en la 
parte teorica de la materia.

## Diagrama de clases

Ver `Diagrama.jpeg` en la raíz del repositorio.

Muestra las relaciones entre las clases. Estas relaciones pueden ser de composicion, ascociacion
o herencia, lo cual esta indicado mediante el tipo de flecha utilizado.

## Estructura del proyecto

inventario/
├── init.py # Reexporta todas las clases del paquete
├── material.py # Material
├── proveedor.py # Proveedor
├── remesa.py # Remesa
├── movimiento.py # Movimiento (base), MovimientoIngreso, MovimientoRetiro
├── politica_consumo.py # PoliticaConsumo (base), PoliticaFEFO
├── retiro.py # Retiro
├── pedido.py # RenglonPedido, Pedido
└── deposito.py # Deposito (coordina todo el inventario)

## Qué está implementado

- Herencia real: `MovimientoIngreso`/`MovimientoRetiro` heredan de `Movimiento`;
  `PoliticaFEFO` hereda de `PoliticaConsumo`
- Polimorfismo: `tipo()` sobreescrito en cada subclase de `Movimiento`
- Getters, setters y contadores de clase de todas las clases
- `Material.requiere_reposicion()`
- `Remesa.esta_vencida()`, `es_utilizable()`, `consumir()` (sin validar saldo todavía)
- `RenglonPedido.subtotal()`, `Pedido.agregar_renglon()`, `Pedido.importe_total()`
- `Retiro.agregar_movimiento()`, `Retiro.cantidad_consumida()`

## Qué falta y por qué
- **Depende de diccionarios** (no vistos aún en la materia): todos los métodos
  de `Deposito` (registrar materiales/proveedores/remesas, calcular existencias,
  reposición, trazabilidad, `retirar()`)
- **Depende de excepciones (`raise`)** (vistas recién, sin practicar todavía):
  los validadores estáticos (`validar_cantidad`, `validar_punto_reposicion`,
  `validar_plazo_entrega`) y la validación de saldo en `Remesa.consumir()`
- **Depende de `sorted()`/lambda** (visto recién, sin practicar todavía):
  `PoliticaFEFO.ordenar()`
