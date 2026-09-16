from decimal import Decimal

from inventario import Material, Pedido, Proveedor, RenglonPedido


def _material():
    return Material("AL-01", "Aluminio AL-01", "kg", 10)


def _proveedor():
    return Proveedor("P-1", "Metales SA", 5)


def test_renglon_pedido_subtotal_calcula_cantidad_por_precio():
    renglon = RenglonPedido(_material(), 10, Decimal("2.50"))

    assert renglon.subtotal() == Decimal("25.00")


def test_agregar_renglon_crea_y_agrega_a_la_lista():
    pedido = Pedido("PED-1", _proveedor())
    material = _material()

    renglon = pedido.agregar_renglon(material, 10, Decimal("2.50"))

    assert isinstance(renglon, RenglonPedido)
    assert pedido.get_renglones() == [renglon]
    assert renglon.get_material() is material
    assert renglon.get_cantidad() == 10
    assert renglon.get_precio_unitario() == Decimal("2.50")


def test_importe_total_suma_varios_renglones():
    pedido = Pedido("PED-1", _proveedor())
    pedido.agregar_renglon(_material(), 10, Decimal("2.50"))
    pedido.agregar_renglon(_material(), 3, Decimal("0.10"))

    assert pedido.importe_total() == Decimal("25.30")


def test_total_pedidos_aumenta_al_crear_instancia():
    assert Pedido.total_pedidos() == 0

    Pedido("PED-1", _proveedor())

    assert Pedido.total_pedidos() == 1
