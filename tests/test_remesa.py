from datetime import date

from material import Material
from proveedor import Proveedor
from remesa import Remesa


def _material():
    return Material("AL-01", "Aluminio AL-01", "kg", 10)


def _proveedor():
    return Proveedor("P-1", "Metales SA", 5)


def test_saldo_disponible_nace_igual_a_cantidad_recibida():
    remesa = Remesa("R-101", _material(), _proveedor(), 8, date(2026, 3, 2))

    assert remesa.get_saldo_disponible() == remesa.get_cantidad_recibida() == 8


def test_esta_vencida_sin_fecha_vencimiento_es_false():
    remesa = Remesa("R-101", _material(), _proveedor(), 8, date(2026, 3, 2))

    assert remesa.esta_vencida(date(2026, 12, 31)) is False


def test_esta_vencida_true_cuando_fecha_posterior_al_vencimiento():
    remesa = Remesa("R-101", _material(), _proveedor(), 8, date(2026, 3, 2), date(2026, 3, 20))

    assert remesa.esta_vencida(date(2026, 3, 21)) is True


def test_esta_vencida_false_cuando_fecha_anterior_al_vencimiento():
    remesa = Remesa("R-101", _material(), _proveedor(), 8, date(2026, 3, 2), date(2026, 3, 20))

    assert remesa.esta_vencida(date(2026, 3, 10)) is False


def test_es_utilizable_true_con_saldo_y_no_vencida():
    remesa = Remesa("R-101", _material(), _proveedor(), 8, date(2026, 3, 2), date(2026, 3, 20))

    assert remesa.es_utilizable(date(2026, 3, 10)) is True


def test_es_utilizable_false_si_esta_vencida():
    remesa = Remesa("R-101", _material(), _proveedor(), 8, date(2026, 3, 2), date(2026, 3, 20))

    assert remesa.es_utilizable(date(2026, 3, 25)) is False


def test_es_utilizable_false_si_saldo_es_cero():
    remesa = Remesa("R-101", _material(), _proveedor(), 8, date(2026, 3, 2))

    remesa.consumir(8)

    assert remesa.es_utilizable(date(2026, 3, 10)) is False


def test_consumir_resta_saldo_disponible():
    remesa = Remesa("R-101", _material(), _proveedor(), 8, date(2026, 3, 2))

    remesa.consumir(3)

    assert remesa.get_saldo_disponible() == 5


def test_total_remesas_aumenta_al_crear_instancia():
    assert Remesa.total_remesas() == 0

    Remesa("R-101", _material(), _proveedor(), 8, date(2026, 3, 2))

    assert Remesa.total_remesas() == 1
