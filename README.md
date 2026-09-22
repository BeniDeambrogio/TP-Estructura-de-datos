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

Actualmente, el proyecto ya esta completo acorde a las reglas de negocio. Incluimos relaciones de herencia tanto en las clases Movimiento con MovimientoIngreso y MovimientoRetiro, como en PoliticaConsumo con PoliticaFEFO. Utilizamos excepciones para validar los datos necesarios, mas que nada usando raise con ValueError. También, ya implementamos los metodos de Deposito, que coordina el programa, utilizando diccionarios para registrar y consultar. Además, usamos la funcion lambda sorted() en PoliticaFEFO, de modo que la politica ya se puede aplicar el criterio FEFO completo. El ultimo cambio que realizamos fue cambiar la función registar_remesa por crear_remesa usando kwargs que sirve para agregar datos adicionales sin cambiar la firma, que surgio a partir de una consigna dada por la catedra. También, incorporamos una serie de pytests repartidos en 8 archivos que corresponden a las clases para todos los metodos y todos corren bien.

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
- `deposito.py` — Deposito (coordina todo el inventario)

## Qué está implementado

- Herencia real: `MovimientoIngreso`/`MovimientoRetiro` heredan de `Movimiento`;`PoliticaFEFO` hereda de `PoliticaConsumo`
- Polimorfismo: `tipo()` sobreescrito en cada subclase de `Movimiento`
- Getters, setters y contadores de clase de todas las clases
- `Material.requiere_reposicion()`
- `Remesa.esta_vencida()`, `es_utilizable()`, `consumir()`
- `RenglonPedido.subtotal()`, `Pedido.agregar_renglon()`, `Pedido.importe_total()`
- `Retiro.agregar_movimiento()`, `Retiro.cantidad_consumida()`
- Excepciones (`raise ValueError`): validadores (`validar_cantidad`,`validar_punto_reposicion`, `validar_plazo_entrega`) y validación de saldo en `Remesa.consumir()`
- Todos los métodos de `Deposito` usando diccionarios: `registrar_material`, `registrar_proveedor`, `crear_remesa`, `existencia_fisica`,  `existencia_disponible`, `retirar()`, `materiales_a_reponer()`, `remesas_de_retiro()`, `retiros_de_remesa()`
- `PoliticaFEFO.ordenar()` con `sorted()` y una función `lambda`
- `Deposito.crear_remesa()` usando `**kwargs` para datos opcionales (reemplaza al anterior `registrar_remesa`)

## Qué falta y por qué

Por ahora no queda ningún método sin implementar del alcance original. Lo único pendiente es reemplazar los `ValueError` genéricos por excepciones propias del dominio si lo vemos necesario. También dependiendo de lo que nos den de teoría en las siguientes clases, evaluaremos si son necesarios cambios dentro del programa.
