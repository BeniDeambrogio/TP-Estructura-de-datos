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

Actualmente, el proyecto ya esta completo acorde a las reglas de negocio. Incluimos relaciones de herencia tanto en las clases Movimiento con MovimientoIngreso y MovimientoRetiro, como en PoliticaConsumo con PoliticaFEFO. Utilizamos excepciones para validar los datos necesarios, usando excepciones propias del dominio que heredan de ErrorInventario. También, ya implementamos los metodos de Deposito, que coordina el programa, utilizando diccionarios para registrar y consultar. Además, usamos la funcion lambda sorted() en PoliticaFEFO, de modo que la politica ya se puede aplicar el criterio FEFO completo. El ultimo cambio que realizamos fue cambiar la función registar_remesa por crear_remesa usando kwargs que sirve para agregar datos adicionales sin cambiar la firma, que surgio a partir de una consigna dada por la catedra. También, incorporamos una serie de pytests repartidos en 11 archivos que corresponden a las clases para todos los metodos y todos corren bien. A partir de la clase de Pilas y Colas, agregamos una Cola implementada con nodos para atender las solicitudes de retiro por orden de llegada, y un índice de remesas por material en Deposito para que las consultas no recorran todas las remesas. Por último, agregamos persistencia en JSON: el depósito se puede guardar en un archivo y volver a cargar con todo su estado.

## Diagrama de clases

Ver `Diagrama.jpeg` en la raíz del repositorio.

Muestra las relaciones entre las clases. Estas relaciones pueden ser de composicion, asociación o herencia, lo cual esta indicado mediante el tipo de flecha utilizado.

## Estructura del proyecto

- `__init__.py` — Reexporta todas las clases del paquete
- `material.py` — Material
- `proveedor.py` — Proveedor
- `remesa.py` — Remesa
- `movimiento.py` — Movimiento (base), MovimientoIngreso, MovimientoRetiro
- `politica_consumo.py` — PoliticaConsumo (base), PoliticaFEFO
- `retiro.py` — Retiro
- `pedido.py` — RenglonPedido, Pedido
- `solicitud_retiro.py` — SolicitudRetiro
- `estructuras.py` — Nodo, Cola (implementada con nodos)
- `excepciones.py` — Excepciones propias del dominio
- `deposito.py` — Deposito (coordina todo el inventario)

## Qué está implementado

- Herencia real: `MovimientoIngreso`/`MovimientoRetiro` heredan de `Movimiento`;`PoliticaFEFO` hereda de `PoliticaConsumo`
- Polimorfismo: `tipo()` sobreescrito en cada subclase de `Movimiento`
- Getters, setters y contadores de clase de todas las clases
- `Material.requiere_reposicion()`
- `Remesa.esta_vencida()`, `es_utilizable()`, `consumir()`
- `RenglonPedido.subtotal()`, `Pedido.agregar_renglon()`, `Pedido.importe_total()`
- `Retiro.agregar_movimiento()`, `Retiro.cantidad_consumida()`
- Excepciones propias (`ErrorInventario` y sus subclases): validadores (`validar_cantidad`,`validar_punto_reposicion`, `validar_plazo_entrega`) y validación de saldo en `Remesa.consumir()`
- Todos los métodos de `Deposito` usando diccionarios: `registrar_material`, `registrar_proveedor`, `crear_remesa`, `existencia_fisica`,  `existencia_disponible`, `retirar()`, `materiales_a_reponer()`, `remesas_de_retiro()`, `retiros_de_remesa()`
- `PoliticaFEFO.ordenar()` con `sorted()` y una función `lambda`
- `Deposito.crear_remesa()` usando `**kwargs` para datos opcionales (reemplaza al anterior `registrar_remesa`)
- `Cola` (FIFO) implementada con nodos, guardando `frente` y `fin` para que `encolar()` y `desencolar()` sean O(1)
- Cola de solicitudes de retiro en `Deposito`: `solicitar_retiro()`, `atender_siguiente()`, `solicitudes_pendientes()`. Las solicitudes se atienden por orden de llegada; si no hay stock para la primera, queda esperando sin que se saltee a nadie
- Índice `remesas_por_material` en `Deposito`: las consultas de existencias y los retiros recorren solo las remesas del material consultado
- Persistencia en JSON: `Deposito.guardar(ruta)` y `Deposito.cargar(ruta)`. Cada clase sabe convertirse a diccionario (`a_dict()`) y reconstruirse (`desde_dict()`). Las referencias entre objetos se guardan por id y se resuelven al cargar; las fechas se guardan como texto ISO (`"2026-03-20"`); la cola de solicitudes se guarda y se recarga en orden FIFO

  ```python
  deposito.guardar("deposito.json")
  deposito = Deposito.cargar("deposito.json")
  ```

## Qué falta y por qué

Por ahora no queda ningún método sin implementar del alcance original. Como posible mejora, FEFO podría resolverse con una cola de prioridad en lugar de ordenar con `sorted()` en cada retiro (no usamos una cola común porque las remesas no llegan necesariamente ordenadas por vencimiento). También dependiendo de lo que nos den de teoría en las siguientes clases, evaluaremos si son necesarios cambios dentro del programa.
