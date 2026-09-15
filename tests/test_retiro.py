from datetime import date

from material import Material
from movimiento import MovimientoRetiro
from proveedor import Proveedor
from remesa import Remesa
from retiro import Retiro


def _remesa(id_remesa):
    material = Material("AL-01", "Aluminio AL-01", "kg", 10)
    proveedor = Proveedor("P-1", "Metales SA", 5)
    return Remesa(id_remesa, material, proveedor, 8, date(2026, 3, 2))


def test_creacion_y_getters():
    retiro = Retiro("RET-1", "AL-01", date(2026, 3, 10), 18)

    assert retiro.get_id() == "RET-1"
    assert retiro.get_material() == "AL-01"
    assert retiro.get_fecha() == date(2026, 3, 10)
    assert retiro.get_cantidad_solicitada() == 18
    assert retiro.get_movimientos() == []


def test_agregar_movimiento_y_cantidad_consumida_suman_varios_movimientos():
    retiro = Retiro("RET-1", "AL-01", date(2026, 3, 10), 18)
    mov1 = MovimientoRetiro("MOV-1", date(2026, 3, 10), _remesa("R-101"), 8, retiro)
    mov2 = MovimientoRetiro("MOV-2", date(2026, 3, 10), _remesa("R-102"), 10, retiro)

    retiro.agregar_movimiento(mov1)
    retiro.agregar_movimiento(mov2)

    assert retiro.get_movimientos() == [mov1, mov2]
    assert retiro.cantidad_consumida() == 18


def test_total_retiros_aumenta_al_crear_instancia():
    assert Retiro.total_retiros() == 0

    Retiro("RET-1", "AL-01", date(2026, 3, 10), 18)

    assert Retiro.total_retiros() == 1
