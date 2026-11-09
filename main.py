"""
Inventario JIT - Programa principal
===================================

Menu por consola para usar el sistema de inventario con datos propios.
Toda la logica (validaciones, FEFO, cola, trazabilidad, persistencia) la
resuelve el paquete inventario: este archivo solo pide los datos y muestra
los resultados.

Lo cargado se guarda en deposito.json (al lado de este archivo) y se vuelve a
cargar la proxima vez. Si todavia no hay datos guardados, se ofrece cargar el
ejemplo del enunciado para no arrancar con el deposito vacio.
Uso: python main.py
"""
import os
from datetime import date
from decimal import Decimal, InvalidOperation

from inventario import Deposito, ErrorInventario

# Se guarda al lado de main.py, asi funciona aunque se lo ejecute desde otra carpeta.
ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deposito.json")


# ---------- Lectura de datos por teclado ----------
def pedir_entero(mensaje):
    numero = None
    while numero is None:
        try:
            numero = int(input(mensaje))
        except ValueError:
            print("  Tiene que ser un numero entero.")
    return numero


def pedir_precio(mensaje):
    precio = None
    while precio is None:
        try:
            precio = Decimal(input(mensaje))
        except InvalidOperation:
            # Es la excepcion que lanza Decimal cuando el texto no es un numero.
            print("  Tiene que ser un numero, por ejemplo 3.50")
    return precio


def pedir_fecha(mensaje):
    fecha = None
    while fecha is None:
        try:
            fecha = date.fromisoformat(input(mensaje))
        except ValueError:
            print("  Fecha invalida. Use AAAA-MM-DD, por ejemplo 2026-03-20.")
    return fecha


def elegir(diccionario, titulo):
    """Muestra los ids cargados y devuelve el objeto elegido, o None si el id no existe."""
    print(f"  {titulo}: {list(diccionario)}")
    elegido = diccionario.get(input("  Id: "))
    if elegido is None:
        print("  No existe ese id.")
    return elegido


def mostrar_retiro(retiro):
    print(f"Retiro {retiro.get_id()}: {retiro.cantidad_consumida()} {retiro.get_material().get_unidad_medida()}"
          f" de {retiro.get_material().get_id()}")
    for movimiento in retiro.get_movimientos():
        print(f"  - {movimiento.get_cantidad()} de la remesa {movimiento.get_remesa().get_id()}")


# ---------- Opciones del menu ----------
def registrar_material(deposito):
    id = input("Id del material (ej. AL-01): ")
    nombre = input("Nombre: ")
    unidad = input("Unidad de medida (ej. kg): ")
    punto_reposicion = pedir_entero("Punto de reposicion: ")
    deposito.registrar_material(id, nombre, unidad, punto_reposicion)
    print(f"Material {id} registrado.")


def registrar_proveedor(deposito):
    id = input("Id del proveedor (ej. P-1): ")
    nombre = input("Nombre: ")
    plazo = pedir_entero("Plazo de entrega en dias: ")
    deposito.registrar_proveedor(id, nombre, plazo)
    print(f"Proveedor {id} registrado.")


def registrar_remesa(deposito):
    material = elegir(deposito.get_materiales(), "Materiales")
    if material is None:
        return
    proveedor = elegir(deposito.get_proveedores(), "Proveedores")
    if proveedor is None:
        return
    id = input("Id de la remesa (ej. R-101): ")
    cantidad = pedir_entero(f"Cantidad recibida ({material.get_unidad_medida()}): ")
    fecha_recepcion = pedir_fecha("Fecha de recepcion (AAAA-MM-DD): ")
    fecha_vencimiento = None
    if input("Tiene fecha de vencimiento? (s/n): ") == "s":
        fecha_vencimiento = pedir_fecha("Fecha de vencimiento (AAAA-MM-DD): ")
    # Datos opcionales: viajan por **kwargs y crear_remesa los guarda sin conocerlos.
    datos_extra = {}
    lote = input("Lote (Enter si no tiene): ")
    if lote != "":
        datos_extra["lote"] = lote
    deposito.crear_remesa(id, material, proveedor, cantidad,
                          fecha_recepcion=fecha_recepcion, fecha_vencimiento=fecha_vencimiento,
                          **datos_extra)
    print(f"Remesa {id} registrada.")


def retirar_material(deposito):
    material = elegir(deposito.get_materiales(), "Materiales")
    if material is None:
        return
    cantidad = pedir_entero(f"Cantidad a retirar ({material.get_unidad_medida()}): ")
    fecha = pedir_fecha("Fecha del retiro (AAAA-MM-DD): ")
    mostrar_retiro(deposito.retirar(material, cantidad, fecha))


def solicitar_retiro(deposito):
    material = elegir(deposito.get_materiales(), "Materiales")
    if material is None:
        return
    cantidad = pedir_entero(f"Cantidad a retirar ({material.get_unidad_medida()}): ")
    fecha = pedir_fecha("Fecha de la solicitud (AAAA-MM-DD): ")
    solicitud = deposito.solicitar_retiro(material, cantidad, fecha)
    print(f"{solicitud.get_id()} quedo en la cola. Solicitudes en espera: {deposito.solicitudes_pendientes()}")


def atender_solicitud(deposito):
    # frente() lanza EstructuraVaciaError si no hay solicitudes en espera.
    solicitud = deposito.get_solicitudes().frente()
    print(f"Primera en la cola: {solicitud.get_id()} pide {solicitud.get_cantidad()}"
          f" de {solicitud.get_material().get_id()}")
    retiro = deposito.atender_siguiente(pedir_fecha("Fecha del retiro (AAAA-MM-DD): "))
    if retiro is None:
        print("No alcanza el stock disponible: la solicitud sigue primera en la cola.")
    else:
        mostrar_retiro(retiro)


def ver_existencias(deposito):
    fecha = pedir_fecha("Fecha para calcular la existencia disponible (AAAA-MM-DD): ")
    for material in deposito.get_materiales().values():
        print(f"  {material.get_id()} - {material.get_nombre()} ({material.get_unidad_medida()}): "
              f"fisica {deposito.existencia_fisica(material)}, "
              f"disponible {deposito.existencia_disponible(material, fecha)}, "
              f"punto de reposicion {material.get_punto_reposicion()}")


def ver_a_reponer(deposito):
    a_reponer = deposito.materiales_a_reponer()
    print("Materiales por debajo de su punto de reposicion hoy:", [m.get_id() for m in a_reponer])


def ver_remesas(deposito):
    material = elegir(deposito.get_materiales(), "Materiales")
    if material is None:
        return
    print("En el orden en que se consumen (FEFO):")
    for remesa in deposito.remesas_de_material(material):
        vencimiento = remesa.get_fecha_vencimiento()
        if vencimiento is None:
            vencimiento = "no vence"
        estado = "no utilizable"
        if remesa.es_utilizable(date.today()):
            estado = "utilizable"
        lote = remesa.obtener_dato("lote", "-")
        print(f"  {remesa.get_id()}: saldo {remesa.get_saldo_disponible()} de {remesa.get_cantidad_recibida()}, "
              f"recibida {remesa.get_fecha_recepcion()}, vencimiento {vencimiento}, lote {lote}, "
              f"proveedor {remesa.get_proveedor().get_id()} -> hoy {estado}")


def ver_proveedores(deposito):
    for proveedor in deposito.get_proveedores().values():
        print(f"  {proveedor.get_id()} - {proveedor.get_nombre()}: entrega en {proveedor.get_plazo_entrega_dias()} dias")


def ver_movimientos(deposito):
    # movimientos es un diccionario {id: movimiento}; values() los recorre en el orden en que se registraron.
    for movimiento in deposito.get_movimientos().values():
        print(f"  {movimiento.get_id()}  {movimiento.get_fecha()}  {movimiento.tipo():<8} "
              f"{movimiento.get_cantidad()} de la remesa {movimiento.get_remesa().get_id()}")


def ver_cola(deposito):
    print("Solicitudes en espera:", deposito.solicitudes_pendientes())
    for solicitud in deposito.get_solicitudes().a_lista():
        print(f"  {solicitud.get_id()}: {solicitud.get_cantidad()} de {solicitud.get_material().get_id()}"
              f" (solicitada el {solicitud.get_fecha_solicitud()})")


def trazabilidad_retiro(deposito):
    retiro = elegir(deposito.get_retiros(), "Retiros")
    if retiro is None:
        return
    print(f"{retiro.get_id()} uso las remesas:", [r.get_id() for r in deposito.remesas_de_retiro(retiro)])


def trazabilidad_remesa(deposito):
    remesa = elegir(deposito.get_remesas(), "Remesas")
    if remesa is None:
        return
    print(f"{remesa.get_id()} se uso en los retiros:", [r.get_id() for r in deposito.retiros_de_remesa(remesa)])


def ver_remesas_sin_usar(deposito):
    # Diferencia de sets: todas las remesas menos las usadas por algun retiro.
    print("Remesas de las que todavia no salio material:", [r.get_id() for r in deposito.remesas_sin_usar()])


def ver_remesas_en_comun(deposito):
    # Interseccion de los sets de ids de remesas de dos retiros.
    retiro_a = elegir(deposito.get_retiros(), "Primer retiro")
    if retiro_a is None:
        return
    retiro_b = elegir(deposito.get_retiros(), "Segundo retiro")
    if retiro_b is None:
        return
    print(f"Remesas que usaron {retiro_a.get_id()} y {retiro_b.get_id()}:",
          [r.get_id() for r in deposito.remesas_en_comun(retiro_a, retiro_b)])


def crear_pedido(deposito):
    proveedor = elegir(deposito.get_proveedores(), "Proveedores")
    if proveedor is None:
        return
    pedido = deposito.crear_pedido(input("Id del pedido (ej. PED-1): "), proveedor)
    otro = "s"
    while otro == "s":
        material = elegir(deposito.get_materiales(), "Materiales")
        if material is not None:
            cantidad = pedir_entero(f"Cantidad ({material.get_unidad_medida()}): ")
            precio = pedir_precio("Precio unitario (ej. 3.50): $")
            try:
                renglon = pedido.agregar_renglon(material, cantidad, precio)
                print(f"  Subtotal: ${renglon.subtotal()}")
            except ErrorInventario as e:
                print(f"  No se agrego el renglon: {e}")
        otro = input("Agregar otro renglon? (s/n): ")
    print(f"Pedido {pedido.get_id()} registrado. Importe total: ${pedido.importe_total()}")


def ver_pedidos(deposito):
    for pedido in deposito.get_pedidos().values():
        print(f"  {pedido.get_id()} a {pedido.get_proveedor().get_nombre()}: total ${pedido.importe_total()}")
        for renglon in pedido.get_renglones():
            print(f"      {renglon.get_cantidad()} de {renglon.get_material().get_id()}"
                  f" x ${renglon.get_precio_unitario()} = ${renglon.subtotal()}")


def guardar(deposito):
    deposito.guardar(ARCHIVO)
    print("Datos guardados en", ARCHIVO)


def cargar_ejemplo(deposito):
    """Carga el ejemplo del enunciado (AL-01 con R-101, R-102 y R-103) y un segundo material."""
    if deposito.get_materiales():
        print("El deposito ya tiene datos: el ejemplo solo se carga en un deposito vacio.")
        return
    aluminio = deposito.registrar_material("AL-01", "Aluminio AL-01", "kg", 10)
    cobre = deposito.registrar_material("CU-01", "Cobre CU-01", "kg", 5)
    metales = deposito.registrar_proveedor("P-1", "Metales SA", 5)
    cobres = deposito.registrar_proveedor("P-2", "Cobres del Norte", 3)
    deposito.crear_remesa("R-101", aluminio, metales, 8, fecha_recepcion=date(2026, 3, 2),
                          fecha_vencimiento=date(2026, 3, 20), lote="L-001")
    deposito.crear_remesa("R-102", aluminio, metales, 12, fecha_recepcion=date(2026, 3, 4),
                          fecha_vencimiento=date(2026, 3, 30), lote="L-002")
    deposito.crear_remesa("R-103", aluminio, metales, 15, fecha_recepcion=date(2026, 3, 5))
    deposito.crear_remesa("R-201", cobre, cobres, 2, fecha_recepcion=date(2026, 3, 6))
    print("Se cargaron 2 materiales (AL-01, CU-01), 2 proveedores (P-1, P-2) y 4 remesas.")
    print("Para repetir el ejemplo del enunciado: opcion 4, AL-01, 18 kg, fecha 2026-03-10.")


# Cada numero del menu se asocia a su texto y a la funcion que lo resuelve.
OPCIONES = {
    "1": ("Registrar material", registrar_material),
    "2": ("Registrar proveedor", registrar_proveedor),
    "3": ("Registrar remesa (ingreso de material)", registrar_remesa),
    "4": ("Retirar material", retirar_material),
    "5": ("Agregar solicitud de retiro a la cola", solicitar_retiro),
    "6": ("Atender siguiente solicitud de la cola", atender_solicitud),
    "7": ("Ver existencias", ver_existencias),
    "8": ("Ver materiales a reponer", ver_a_reponer),
    "9": ("Ver remesas de un material", ver_remesas),
    "10": ("Ver proveedores", ver_proveedores),
    "11": ("Ver movimientos", ver_movimientos),
    "12": ("Ver cola de solicitudes", ver_cola),
    "13": ("Trazabilidad de un retiro", trazabilidad_retiro),
    "14": ("Trazabilidad de una remesa", trazabilidad_remesa),
    "15": ("Ver remesas sin usar", ver_remesas_sin_usar),
    "16": ("Ver remesas en comun entre dos retiros", ver_remesas_en_comun),
    "17": ("Crear pedido a proveedor", crear_pedido),
    "18": ("Ver pedidos", ver_pedidos),
    "19": ("Cargar datos de ejemplo", cargar_ejemplo),
    "20": ("Guardar", guardar),
}


def iniciar_deposito():
    if not os.path.exists(ARCHIVO):
        deposito = Deposito()
        if input("No hay datos guardados. Cargar los datos de ejemplo? (s/n): ") == "s":
            cargar_ejemplo(deposito)
        return deposito
    try:
        deposito = Deposito.cargar(ARCHIVO)
        print("Se cargaron los datos guardados en", ARCHIVO)
        return deposito
    except (ValueError, KeyError):
        # ValueError incluye el error de JSON mal escrito; KeyError, un dato que falta.
        print(f"No se pudo leer {ARCHIVO}: se empieza con un deposito vacio.")
        print("Ojo: si guarda, ese archivo se reemplaza.")
        return Deposito()


def main():
    deposito = iniciar_deposito()

    opcion = ""
    while opcion != "0":
        print("\n============ INVENTARIO JIT ============")
        for numero, opcion_menu in OPCIONES.items():
            print(f"{numero}. {opcion_menu[0]}")
        print("0. Salir")
        opcion = input("Elija una opcion: ")

        if opcion in OPCIONES:
            texto, accion = OPCIONES[opcion]
            print(f"\n--- {texto} ---")
            try:
                accion(deposito)
            except ErrorInventario as e:
                # Las reglas del negocio las valida el paquete inventario; aca
                # solo se muestra el motivo y se vuelve al menu.
                print(f"No se pudo completar la operacion: {e}")
        elif opcion != "0":
            print("Opcion invalida.")

    if input("Guardar los cambios antes de salir? (s/n): ") == "s":
        guardar(deposito)


if __name__ == "__main__":
    main()
