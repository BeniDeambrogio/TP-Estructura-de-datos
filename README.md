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

Actualmente, el proyecto está completo respecto de las reglas de negocio y funciona de punta a punta: se pueden registrar materiales, proveedores y remesas, retirar material respetando el orden FEFO, ver la trazabilidad de cada retiro y detectar qué materiales hay que reponer. Usamos herencia en Movimiento (con MovimientoIngreso y MovimientoRetiro) y en PoliticaConsumo (con PoliticaFEFO), y excepciones propias que heredan de ErrorInventario para avisar cuando algo no corresponde, por ejemplo un id repetido o un stock insuficiente. Deposito coordina todo usando diccionarios, y crear_remesa recibe los datos opcionales con kwargs, de modo que se pueden agregar datos nuevos sin cambiar su firma (surgió a partir de una consigna de la cátedra). A partir de la clase de Pilas y Colas agregamos una Cola hecha con nodos para atender las solicitudes de retiro por orden de llegada, y una lista enlazada ordenada que guarda las remesas de cada material en el orden en que se consumen, así retirar() no tiene que ordenarlas cada vez. Los pedidos a proveedores ahora quedan registrados en el depósito, y todo el estado se puede guardar y volver a cargar desde un archivo JSON. Además, hay 104 tests con pytest repartidos en 11 archivos y todos pasan, y un main.py que recorre el funcionamiento paso a paso. Lo único que quedó desactualizado es el diagrama de clases, que vamos a rehacer.

## Diagrama de clases

Ver `Diagrama.jpeg` en la raíz del repositorio.

Muestra las relaciones entre las clases. Estas relaciones pueden ser de composicion, asociación o herencia, lo cual esta indicado mediante el tipo de flecha utilizado.

**Aviso:** con los cambios nuevos el diagrama ya no refleja el funcionamiento actual del programa (por ejemplo, no incluye la cola de solicitudes, la lista ordenada, los pedidos dentro del depósito ni el cambio a `crear_remesa`). En breve lo vamos a rehacer para que sí lo refleje.

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
- `estructuras.py` — Nodo, Cola y ListaEnlazadaOrdenada (implementadas con nodos)
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
- Política de consumo (`clave_orden()`): cada política indica cómo se ordenan las remesas para decidir cuál se consume primero. FEFO mira primero la fecha de vencimiento y, si empatan, la de recepción. `ordenar()` usa ese mismo criterio. Para sumar otra política alcanza con definir su propio criterio
- `Deposito.crear_remesa()` usando `**kwargs` para datos opcionales (reemplaza al anterior `registrar_remesa`)
- `Cola`: una fila donde el primero que llega es el primero que sale. `encolar()` agrega al final, `desencolar()` saca del principio y `frente()` muestra quién está primero. Está armada con nodos, que son piezas chiquitas donde cada una apunta a la siguiente
- Cola de solicitudes de retiro (`SolicitudRetiro`): una solicitud es un pedido de retiro que todavía no se hizo. `solicitar_retiro()` la anota en la fila sin tocar el stock, `atender_siguiente()` hace el retiro de la que está primera y `solicitudes_pendientes()` dice cuántas esperan. Si no alcanza el stock para la primera, se queda esperando y no se atiende a las de atrás
- `ListaEnlazadaOrdenada`: una lista que siempre se mantiene en orden. Cuando se agrega algo nuevo, se coloca en el lugar que le corresponde
- Remesas por material (`remesas_por_material` en `Deposito`): el depósito guarda aparte las remesas de cada material, ya en el orden en que se consumen según la política. Así, al consultar o retirar solo se miran las remesas de ese material y no hace falta ordenarlas en cada retiro. Igual se revisa cuáles se pueden usar, porque la primera podría estar vencida o sin saldo
- Pedidos en `Deposito`: `crear_pedido()` registra un pedido a un proveedor (no se puede repetir el id) y `get_pedidos()` los devuelve. Un pedido no cambia el stock
- Reparto recursivo (`Deposito._repartir()`): calcula cuánto se saca de cada remesa para un retiro. Toma la primera remesa, saca lo que puede y se vuelve a llamar con la cantidad que falta y las remesas que siguen. Se detiene cuando no falta nada o cuando no quedan remesas. Solo calcula: las remesas se modifican recién después
- Set de remesas en cada retiro (`Retiro.ids_de_remesas()`): cada retiro guarda un conjunto (set) con los ids de las remesas de las que sacó material. Un set no repite elementos y preguntar si un id está ahí es directo, así `retiros_de_remesa()` ya no recorre todos los movimientos de cada retiro
- Operaciones de conjuntos entre retiros: `Deposito.remesas_sin_usar()` devuelve las remesas de las que todavía no salió material en ningún retiro (a todas las remesas se les restan las usadas por los retiros), y `Deposito.remesas_en_comun(retiro_a, retiro_b)` devuelve las remesas que usaron los dos retiros (lo que tienen en común sus conjuntos de ids)
- Guardar y cargar: `Deposito.guardar(ruta)` guarda todo el depósito en un archivo (formato JSON) y `Deposito.cargar(ruta)` lo vuelve a armar igual que estaba: materiales, proveedores, remesas, retiros, movimientos, pedidos y la fila de solicitudes. Para eso cada clase sabe pasarse a un diccionario (`a_dict()`) y volver a armarse desde uno (`desde_dict()`). Los datos extra de una remesa se guardan como texto, así que al cargar vuelven como texto y no con su tipo original. Además, el archivo se prepara completo antes de escribirse, por lo que si hay un error no queda a medias

  ```python
  deposito.guardar("deposito.json")
  deposito = Deposito.cargar("deposito.json")
  ```

## Qué falta y por qué

Por ahora no queda ningún método sin implementar del alcance original. Como posible mejora, en lugar de la lista ordenada se podría usar una estructura llamada cola de prioridad (heap), que agrega las remesas más rápido. Los datos extra de las remesas vuelven como texto al cargar el archivo; si hiciera falta que conserven su tipo original, habría que guardar también ese dato. También dependiendo de lo que nos den de teoría en las siguientes clases, evaluaremos si son necesarios cambios dentro del programa.
