from datetime import date

from material import Material
from movimiento import Movimiento, MovimientoIngreso, MovimientoRetiro
from proveedor import Proveedor
from remesa import Remesa
from retiro import Retiro


def _remesa():
    material = Material("AL-01", "Aluminio AL-01", "kg", 10)
    proveedor = Proveedor("P-1", "Metales SA", 5)
    return Remesa("R-101", material, proveedor, 8, date(2026, 3, 2))


def test_movimiento_ingreso_es_instancia_de_movimiento():
    ingreso = MovimientoIngreso("MOV-1", date(2026, 3, 2), _remesa(), 8)

    assert isinstance(ingreso, Movimiento)


def test_movimiento_retiro_es_instancia_de_movimiento():
    retiro = Retiro("RET-1", "AL-01", date(2026, 3, 10), 5)
    movimiento = MovimientoRetiro("MOV-2", date(2026, 3, 10), _remesa(), 5, retiro)

    assert isinstance(movimiento, Movimiento)


def test_getters_heredados_en_movimiento_ingreso():
    remesa = _remesa()
    ingreso = MovimientoIngreso("MOV-1", date(2026, 3, 2), remesa, 8)

    assert ingreso.get_id() == "MOV-1"
    assert ingreso.get_fecha() == date(2026, 3, 2)
    assert ingreso.get_remesa() is remesa
    assert ingreso.get_cantidad() == 8


def test_getters_heredados_en_movimiento_retiro():
    remesa = _remesa()
    retiro = Retiro("RET-1", "AL-01", date(2026, 3, 10), 5)
    movimiento = MovimientoRetiro("MOV-2", date(2026, 3, 10), remesa, 5, retiro)

    assert movimiento.get_id() == "MOV-2"
    assert movimiento.get_fecha() == date(2026, 3, 10)
    assert movimiento.get_remesa() is remesa
    assert movimiento.get_cantidad() == 5


def test_movimiento_retiro_get_retiro_devuelve_el_retiro_asociado():
    retiro = Retiro("RET-1", "AL-01", date(2026, 3, 10), 5)
    movimiento = MovimientoRetiro("MOV-2", date(2026, 3, 10), _remesa(), 5, retiro)

    assert movimiento.get_retiro() is retiro


def test_tipo_es_polimorfico():
    ingreso = MovimientoIngreso("MOV-1", date(2026, 3, 2), _remesa(), 8)
    retiro = Retiro("RET-1", "AL-01", date(2026, 3, 10), 5)
    movimiento_retiro = MovimientoRetiro("MOV-2", date(2026, 3, 10), _remesa(), 5, retiro)

    assert ingreso.tipo() == "INGRESO"
    assert movimiento_retiro.tipo() == "RETIRO"


def test_total_ingresos_aumenta_al_crear_instancia():
    assert MovimientoIngreso.total_ingresos() == 0

    MovimientoIngreso("MOV-1", date(2026, 3, 2), _remesa(), 8)

    assert MovimientoIngreso.total_ingresos() == 1


def test_total_retiros_registrados_aumenta_al_crear_instancia():
    assert MovimientoRetiro.total_retiros_registrados() == 0

    retiro = Retiro("RET-1", "AL-01", date(2026, 3, 10), 5)
    MovimientoRetiro("MOV-2", date(2026, 3, 10), _remesa(), 5, retiro)

    assert MovimientoRetiro.total_retiros_registrados() == 1
