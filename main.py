"""
Main de prueba - TP Inventario JIT con Trazabilidad
=====================================================

Demo pensada para correr en vivo durante la presentacion oral (sin
diapositivas): recorre el sistema paso a paso, mostrando en cada seccion
que conceptos de la materia estan en juego.

Se puede correr entero (python main.py) o ir comentando secciones si
quieren mostrar una parte a la vez.
"""
from datetime import date
from decimal import Decimal

from inventario import (
    CantidadInvalidaError,
    DatoFaltanteError,
    Deposito,
    ErrorInventario,
    IdDuplicadoError,
    Material,
    MovimientoIngreso,
    Pedido,
    Proveedor,
    StockInsuficienteError,
)


def titulo(texto):
    print("\n" + "=" * 70)
    print(texto)
    print("=" * 70)


def sub(texto):
    print("\n--- " + texto + " ---")


# =====================================================================
titulo("1. REGISTRO: Deposito guarda todo en diccionarios (id -> objeto)")
# =====================================================================

deposito = Deposito()

material = deposito.registrar_material("AL-01", "Aluminio AL-01", "kg", punto_reposicion=10)
proveedor = deposito.registrar_proveedor("P-1", "Metales SA", plazo_entrega_dias=5)

print("Material registrado:", material)
print("dict interno deposito.materiales ->", deposito.get_materiales())
print("dict interno deposito.proveedores ->", deposito.get_proveedores())

sub("Buscar por id es directo gracias al diccionario (no se recorre nada)")
print("deposito.get_materiales()['AL-01'] es el mismo objeto:",
      deposito.get_materiales()["AL-01"] is material)

sub("Intentar registrar un id duplicado -> excepcion propia (no generica)")
try:
    deposito.registrar_material("AL-01", "otro nombre", "kg", 5)
except IdDuplicadoError as e:
    print(f"Rechazado correctamente -> {type(e).__name__}: {e}")


# =====================================================================
titulo("2. crear_remesa(): firma con **kwargs para datos opcionales")
# =====================================================================

sub("Remesa CON fecha de vencimiento")
r101 = deposito.crear_remesa(
    "R-101", material, proveedor, 8,
    fecha_recepcion=date(2026, 3, 2), fecha_vencimiento=date(2026, 3, 20),
)
print(f"{r101.get_id()}: recibida {r101.get_cantidad_recibida()} kg, "
      f"vence {r101.get_fecha_vencimiento()}")

sub("Remesa SIN fecha de vencimiento (RN13: es opcional)")
r103 = deposito.crear_remesa("R-103", material, proveedor, 15, fecha_recepcion=date(2026, 3, 5))
print(f"{r103.get_id()}: vencimiento = {r103.get_fecha_vencimiento()!r} (None esta permitido)")

sub("Remesa con datos EXTRA que ni Deposito ni Remesa conocian de antemano")
r_extra = deposito.crear_remesa(
    "R-EXTRA", material, proveedor, 3,
    fecha_recepcion=date(2026, 3, 6), lote="L-88", temperatura_recepcion=4,
)
print("obtener_dato('lote')                ->", r_extra.obtener_dato("lote"))
print("obtener_dato('temperatura_recepcion')->", r_extra.obtener_dato("temperatura_recepcion"))
print("obtener_dato('no_existe')            ->", r_extra.obtener_dato("no_existe"), "(default None)")

sub("fecha_recepcion es obligatoria aunque viaje dentro de **kwargs")
try:
    deposito.crear_remesa("R-SIN-FECHA", material, proveedor, 1)
except DatoFaltanteError as e:
    print(f"Rechazado correctamente -> {type(e).__name__}: {e}")

# completamos el escenario del enunciado para las secciones siguientes
r102 = deposito.crear_remesa(
    "R-102", material, proveedor, 12,
    fecha_recepcion=date(2026, 3, 4), fecha_vencimiento=date(2026, 3, 30),
)


# =====================================================================
titulo("3. EXISTENCIAS: fisica vs. disponible")
# =====================================================================

f1 = date(2026, 3, 10)
print(f"Existencia FISICA  el {f1} ->", deposito.existencia_fisica(material), "kg  (38 = 8+15+3+12)")
print(f"Existencia DISPONIBLE el {f1} ->", deposito.existencia_disponible(material, f1), "kg  (todas utilizables)")

f2 = date(2026, 3, 25)
print(f"\nExistencia DISPONIBLE el {f2} ->", deposito.existencia_disponible(material, f2),
      "kg  (R-101 ya vencio el 20/3, no cuenta)")


# =====================================================================
titulo("4. RETIRAR: PoliticaFEFO decide el orden, Deposito aplica los cambios")
# =====================================================================

retiro1 = deposito.retirar(material, 18, f1)
print(f"Se pidieron 18 kg el {f1}. {retiro1.get_id()} genero "
      f"{len(retiro1.get_movimientos())} movimientos:")
for mov in retiro1.get_movimientos():
    print(f"  {mov.get_remesa().get_id()}: se consumieron {mov.get_cantidad()} kg "
          f"(saldo restante de esa remesa: {mov.get_remesa().get_saldo_disponible()})")

print("\nFEFO en accion: se agoto primero R-101 (vence 20/3), recien despues se tomo de "
      "R-102 (vence 30/3). R-103 (sin vencimiento) no se toco.")

sub("Polimorfismo: recorrer TODOS los movimientos y llamar tipo() sin preguntar la clase")
for mov in deposito.get_movimientos():
    print(f"  {mov.get_id()}: tipo()={mov.tipo():<8} remesa={mov.get_remesa().get_id()} "
          f"cantidad={mov.get_cantidad()}")

sub("Trazabilidad: de un retiro a sus remesas, y de una remesa a sus retiros")
print("remesas_de_retiro(retiro1) ->", [r.get_id() for r in deposito.remesas_de_retiro(retiro1)])
print("retiros_de_remesa(R-102)   ->", [r.get_id() for r in deposito.retiros_de_remesa(r102)])

sub("Un retiro que pide mas de lo disponible se rechaza SIN tocar el inventario")
saldo_r103_antes = r103.get_saldo_disponible()
try:
    deposito.retirar(material, 9999, f1)
except StockInsuficienteError as e:
    print(f"Rechazado correctamente -> {type(e).__name__}: {e}")
print("Saldo de R-103 antes y despues del intento fallido:",
      saldo_r103_antes, "vs", r103.get_saldo_disponible(), "(no cambio)")


# =====================================================================
titulo("5. REPOSICION: usa existencia DISPONIBLE, no la fisica")
# =====================================================================

a_reponer = deposito.materiales_a_reponer()
print("Materiales bajo su punto de reposicion hoy:", [m.get_id() for m in a_reponer])
print(f"(punto_reposicion de AL-01 = {material.get_punto_reposicion()} kg)")


# =====================================================================
titulo("6. Jerarquia de excepciones propias (ErrorInventario)")
# =====================================================================

print("CantidadInvalidaError, StockInsuficienteError, IdDuplicadoError y DatoFaltanteError")
print("heredan todas de ErrorInventario, que a su vez hereda de Exception.\n")

casos = [
    ("Material con punto_reposicion <= 0", lambda: Material("X", "x", "kg", -5)),
    ("Remesa.consumir() mas de lo que tiene de saldo", lambda: r103.consumir(9999)),
    ("Proveedor duplicado (P-1 ya existe)", lambda: deposito.registrar_proveedor("P-1", "otro", 1)),
    ("crear_remesa() sin fecha_recepcion", lambda: deposito.crear_remesa("R-X", material, proveedor, 1)),
]
for descripcion, accion in casos:
    try:
        accion()
    except ErrorInventario as e:
        print(f"  [{type(e).__name__:<22}] {descripcion} -> {e}")

print("\nComo todas heredan de ErrorInventario, un 'except ErrorInventario' las atrapa a las 4")
print("sin necesidad de escribir un except por cada una (eso es polimorfismo aplicado a excepciones).")


# =====================================================================
titulo("7. Pedido / RenglonPedido (uso de Decimal para dinero)")
# =====================================================================

pedido = Pedido("PED-1", proveedor)
renglon = pedido.agregar_renglon(material, 20, Decimal("3.50"))
print(f"Renglon: {renglon.get_cantidad()} kg x ${renglon.get_precio_unitario()} "
      f"= ${renglon.subtotal()}")
print(f"Importe total del pedido {pedido.get_id()}: ${pedido.importe_total()}")


# =====================================================================
titulo("8. Contadores de clase (metodos de clase)")
# =====================================================================

print("Material.total_materiales()   ->", Material.total_materiales())
print("Proveedor.total_proveedores() ->", Proveedor.total_proveedores())
print("Pedido.total_pedidos()        ->", Pedido.total_pedidos())
ingresos = [m for m in deposito.get_movimientos() if isinstance(m, MovimientoIngreso)]
print("Movimientos de tipo INGRESO   ->", len(ingresos))

print("\nFin de la demo.")
