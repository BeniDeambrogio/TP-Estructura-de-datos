from inventario import Proveedor


def test_creacion_y_getters():
    proveedor = Proveedor("P-1", "Metales SA", 5)

    assert proveedor.get_id() == "P-1"
    assert proveedor.get_nombre() == "Metales SA"
    assert proveedor.get_plazo_entrega_dias() == 5


def test_set_plazo_entrega_dias_actualiza_valor():
    proveedor = Proveedor("P-1", "Metales SA", 5)

    proveedor.set_plazo_entrega_dias(10)

    assert proveedor.get_plazo_entrega_dias() == 10


def test_total_proveedores_aumenta_al_crear_instancia():
    assert Proveedor.total_proveedores() == 0

    Proveedor("P-1", "Metales SA", 5)

    assert Proveedor.total_proveedores() == 1
