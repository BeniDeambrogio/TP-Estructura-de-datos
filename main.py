"""
Main de prueba - TP Inventario JIT con Trazabilidad
=====================================================

Demo pensada para correr en vivo durante la presentacion oral (sin
diapositivas): recorre el sistema paso a paso, mostrando en cada seccion
que conceptos de la materia estan en juego.

Se puede correr entero (python main.py) o ir comentando secciones si
quieren mostrar una parte a la vez.
"""
import os
from datetime import date
from decimal import Decimal

from inventario import (
    CantidadInvalidaError,
    Cola,
    DatoFaltanteError,
    Deposito,
    ErrorInventario,
    EstructuraVaciaError,
    IdDuplicadoError,
    ListaEnlazadaOrdenada,
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
titulo("4. INDICE POR MATERIAL: ListaEnlazadaOrdenada (estructura propia con Nodo)")
# =====================================================================

print("Orden en que se REGISTRARON las remesas de AL-01: R-101, R-103, R-EXTRA, R-102")
print("Orden en que las devuelve el indice (ya ordenado por la politica FEFO):")
print("  ", [r.get_id() for r in deposito.remesas_de_material(material)])
print("\nCada insercion recorre la lista hasta encontrar su lugar (O(n)), pero despues")
print("retirar() ya la recibe ordenada: no hace falta sorted() en cada retiro.")

sub("La lista es generica: el orden lo define la clave que se le pasa (la da la politica)")
lista = ListaEnlazadaOrdenada(lambda palabra: len(palabra))
for palabra in ("hola", "a", "casas", "ab"):
    lista.insertar(palabra)
print("ListaEnlazadaOrdenada con clave=len, insertando hola, a, casas, ab ->", lista.a_lista())


# =====================================================================
titulo("5. RETIRAR: la politica da la clave de orden, Deposito aplica los cambios")
# =====================================================================

retiro1 = deposito.retirar(material, 18, f1)
print(f"Se pidieron 18 kg el {f1}. {retiro1.get_id()} genero "
      f"{len(retiro1.get_movimientos())} movimientos:")
for mov in retiro1.get_movimientos():
    print(f"  {mov.get_remesa().get_id()}: se consumieron {mov.get_cantidad()} kg "
          f"(saldo restante de esa remesa: {mov.get_remesa().get_saldo_disponible()})")

print("\nFEFO en accion: se agoto primero R-101 (vence 20/3), recien despues se tomo de "
      "R-102 (vence 30/3). R-103 (sin vencimiento) no se toco.")

sub("El reparto entre remesas es RECURSIVO (Deposito._repartir)")
print("Para repartir 18 kg entre [R-101 (8 kg), R-102 (12 kg), R-103 (15 kg), R-EXTRA (3 kg)]:")
print("  _repartir(18): toma R-101, consume 8 y reparte los 10 que faltan entre las demas")
print("    _repartir(10): toma R-102, consume 10 y reparte los 0 que faltan")
print("      _repartir(0): caso base, no queda nada por repartir -> []")
print("  Se vuelve armando la lista: [(R-101, 8), (R-102, 10)] (R-103 y R-EXTRA ni se miran)")
print("Solo calcula: las remesas se modifican despues, asi un retiro rechazado no deja cambios a medias.")

sub("Polimorfismo: recorrer TODOS los movimientos y llamar tipo() sin preguntar la clase")
for mov in deposito.get_movimientos():
    print(f"  {mov.get_id()}: tipo()={mov.tipo():<8} remesa={mov.get_remesa().get_id()} "
          f"cantidad={mov.get_cantidad()}")

sub("Trazabilidad: de un retiro a sus remesas, y de una remesa a sus retiros")
print("remesas_de_retiro(retiro1) ->", [r.get_id() for r in deposito.remesas_de_retiro(retiro1)])
print("retiros_de_remesa(R-102)   ->", [r.get_id() for r in deposito.retiros_de_remesa(r102)])

sub("Cada Retiro guarda un SET con los ids de las remesas que uso")
print("retiro1.ids_de_remesas() ->", sorted(retiro1.ids_de_remesas()), "(es un set: sin repetidos)")
print("'R-102' in retiro1.ids_de_remesas() ->", "R-102" in retiro1.ids_de_remesas())
print("'R-103' in retiro1.ids_de_remesas() ->", "R-103" in retiro1.ids_de_remesas())
print("retiros_de_remesa() usa esa pregunta (in) en vez de recorrer todos los movimientos de cada retiro.")

sub("Operaciones de conjuntos: remesas_sin_usar() (union y diferencia)")
print("Todas las remesas registradas        ->", sorted(deposito.get_remesas()))
print("Usadas por algun retiro (union)      ->", sorted(retiro1.ids_de_remesas()))
print("remesas_sin_usar() (todas - usadas)  ->", [r.get_id() for r in deposito.remesas_sin_usar()])

sub("Un retiro que pide mas de lo disponible se rechaza SIN tocar el inventario")
saldo_r103_antes = r103.get_saldo_disponible()
try:
    deposito.retirar(material, 9999, f1)
except StockInsuficienteError as e:
    print(f"Rechazado correctamente -> {type(e).__name__}: {e}")
print("Saldo de R-103 antes y despues del intento fallido:",
      saldo_r103_antes, "vs", r103.get_saldo_disponible(), "(no cambio)")


# =====================================================================
titulo("6. COLA DE SOLICITUDES: se atienden por orden de llegada (FIFO)")
# =====================================================================

sol1 = deposito.solicitar_retiro(material, 5, f1)
sol2 = deposito.solicitar_retiro(material, 60, f1)
sol3 = deposito.solicitar_retiro(material, 2, f1)
print("Solicitudes en espera (frente -> fin):",
      [s.get_id() for s in deposito.get_solicitudes().a_lista()])
print("Solicitar NO toca el inventario: existencia fisica =", deposito.existencia_fisica(material))

sub("atender_siguiente(): se atiende SOL-1 (la primera que llego)")
retiro_sol1 = deposito.atender_siguiente(f1)
print(f"Se genero {retiro_sol1.get_id()} por {retiro_sol1.cantidad_consumida()} kg. "
      f"Pendientes: {deposito.solicitudes_pendientes()}")

sub("Operaciones de conjuntos: remesas_en_comun() (interseccion de dos retiros)")
print(f"{retiro1.get_id()} uso:", sorted(retiro1.ids_de_remesas()),
      f"| {retiro_sol1.get_id()} uso:", sorted(retiro_sol1.ids_de_remesas()))
print(f"remesas_en_comun({retiro1.get_id()}, {retiro_sol1.get_id()}) ->",
      [r.get_id() for r in deposito.remesas_en_comun(retiro1, retiro_sol1)])

sub("SOL-2 pide 60 kg y no alcanza: queda primera y NO se saltea a SOL-3")
print("atender_siguiente() ->", deposito.atender_siguiente(f1), "(None: no se pudo atender)")
print("Sigue esperando (frente -> fin):",
      [s.get_id() for s in deposito.get_solicitudes().a_lista()])

sub("Llega una remesa nueva y recien ahi se pueden atender SOL-2 y SOL-3, en orden")
deposito.crear_remesa("R-NUEVA", material, proveedor, 100, fecha_recepcion=date(2026, 3, 7))
print("atender_siguiente() ->", deposito.atender_siguiente(f1).get_id(), "(SOL-2)")
print("atender_siguiente() ->", deposito.atender_siguiente(f1).get_id(), "(SOL-3)")

deposito.solicitar_retiro(material, 500, f1)  # queda esperando para mostrar la persistencia
print("Solicitudes pendientes:", deposito.solicitudes_pendientes(), "(SOL-4 pide 500 kg y espera)")

sub("Atender una cola vacia -> excepcion propia, no un error generico")
try:
    Cola().desencolar()
except EstructuraVaciaError as e:
    print(f"Rechazado correctamente -> {type(e).__name__}: {e}")


# =====================================================================
titulo("7. REPOSICION: usa existencia DISPONIBLE, no la fisica")
# =====================================================================

cobre = deposito.registrar_material("CU-01", "Cobre CU-01", "kg", punto_reposicion=5)
deposito.crear_remesa("R-201", cobre, proveedor, 2, fecha_recepcion=date(2026, 3, 6))

a_reponer = deposito.materiales_a_reponer()
print("Materiales bajo su punto de reposicion hoy:", [m.get_id() for m in a_reponer])
print(f"AL-01: disponible {deposito.existencia_disponible(material, date.today())} kg, "
      f"punto_reposicion {material.get_punto_reposicion()} kg -> no hace falta reponer")
print(f"CU-01: disponible {deposito.existencia_disponible(cobre, date.today())} kg, "
      f"punto_reposicion {cobre.get_punto_reposicion()} kg -> hay que reponer")


# =====================================================================
titulo("8. PEDIDOS: registrados en el Deposito (Decimal para dinero)")
# =====================================================================

existencia_antes_del_pedido = deposito.existencia_fisica(material)
pedido = deposito.crear_pedido("PED-1", proveedor)
renglon = pedido.agregar_renglon(material, 20, Decimal("3.50"))
print(f"Renglon: {renglon.get_cantidad()} kg x ${renglon.get_precio_unitario()} "
      f"= ${renglon.subtotal()}")
print(f"Importe total del pedido {pedido.get_id()}: ${pedido.importe_total()}")
print("Pedidos registrados en el deposito:", list(deposito.get_pedidos()))

sub("Un pedido NO incorpora existencias antes de recibirlas")
print(f"Existencia fisica de AL-01 antes del pedido: {existencia_antes_del_pedido} kg, "
      f"despues: {deposito.existencia_fisica(material)} kg (el material entra recien con una remesa)")


# =====================================================================
titulo("9. Jerarquia de excepciones propias (ErrorInventario)")
# =====================================================================

print("CantidadInvalidaError, StockInsuficienteError, IdDuplicadoError, DatoFaltanteError y")
print("EstructuraVaciaError heredan todas de ErrorInventario, que hereda de Exception.\n")

casos = [
    ("Material con punto_reposicion <= 0", lambda: Material("X", "x", "kg", -5)),
    ("Remesa.consumir() mas de lo que tiene de saldo", lambda: r103.consumir(9999)),
    ("Proveedor duplicado (P-1 ya existe)", lambda: deposito.registrar_proveedor("P-1", "otro", 1)),
    ("crear_remesa() sin fecha_recepcion", lambda: deposito.crear_remesa("R-X", material, proveedor, 1)),
    ("Desencolar de una Cola vacia", lambda: Cola().desencolar()),
    ("Pedido duplicado (PED-1 ya existe)", lambda: deposito.crear_pedido("PED-1", proveedor)),
]
for descripcion, accion in casos:
    try:
        accion()
    except ErrorInventario as e:
        print(f"  [{type(e).__name__:<22}] {descripcion} -> {e}")

print("\nComo todas heredan de ErrorInventario, un 'except ErrorInventario' las atrapa a las 5")
print("sin necesidad de escribir un except por cada una (eso es polimorfismo aplicado a excepciones).")


# =====================================================================
titulo("10. Contadores de clase (metodos de clase)")
# =====================================================================

print("Material.total_materiales()   ->", Material.total_materiales())
print("Proveedor.total_proveedores() ->", Proveedor.total_proveedores())
print("Pedido.total_pedidos()        ->", Pedido.total_pedidos())
ingresos = [m for m in deposito.get_movimientos() if isinstance(m, MovimientoIngreso)]
print("Movimientos de tipo INGRESO   ->", len(ingresos))

# =====================================================================
titulo("11. PERSISTENCIA JSON: guardar() y cargar() restauran todo el estado")
# =====================================================================

sub("Una remesa con datos extra que JSON no sabe escribir (fecha y Decimal)")
deposito.crear_remesa("R-FAB", material, proveedor, 5, fecha_recepcion=date(2026, 3, 8),
                      fecha_fabricacion=date(2026, 2, 1), temperatura=Decimal("4.5"))
print("Los **kwargs aceptan cualquier tipo, pero JSON solo escribe texto/numeros/bool/None:")
print("guardar() convierte esos valores a texto ANTES de escribir el archivo.")

RUTA = "deposito_demo.json"
deposito.guardar(RUTA)
print(f"\nSe guardo '{RUTA}' ({os.path.getsize(RUTA)} bytes)")

cargado = Deposito.cargar(RUTA)
os.remove(RUTA)

sub("El deposito cargado tiene el mismo estado que el original")
mat_c = cargado.get_materiales()["AL-01"]
print("Existencia fisica de AL-01   (original / cargado):",
      deposito.existencia_fisica(material), "/", cargado.existencia_fisica(mat_c))
print("Orden FEFO de las remesas     (original / cargado):",
      [r.get_id() for r in deposito.remesas_de_material(material)], "/",
      [r.get_id() for r in cargado.remesas_de_material(mat_c)])
print("Retiros / movimientos / pedidos (cargado):",
      len(cargado.get_retiros()), "/", len(cargado.get_movimientos()), "/", len(cargado.get_pedidos()))
print("Solicitudes pendientes        (original / cargado):",
      deposito.solicitudes_pendientes(), "/", cargado.solicitudes_pendientes())
print("Importe del pedido PED-1      (original / cargado):",
      pedido.importe_total(), "/", cargado.get_pedidos()["PED-1"].importe_total())
print("La referencia vuelve al MISMO objeto:",
      cargado.get_remesas()["R-101"].get_material() is mat_c)

sub("Los datos extra de la fecha vuelven como TEXTO (limitacion conocida)")
r_fab = cargado.get_remesas()["R-FAB"]
print("obtener_dato('fecha_fabricacion') ->", repr(r_fab.obtener_dato("fecha_fabricacion")))
print("obtener_dato('temperatura')       ->", repr(r_fab.obtener_dato("temperatura")))


print("\nFin de la demo.")
