from datetime import date

import pytest

from inventario import Deposito, Material, MovimientoIngreso, PoliticaFEFO, Proveedor


def test_init_crea_colecciones_vacias_y_politica_fefo():
    deposito = Deposito()

    assert deposito.materiales == {}
    assert deposito.proveedores == {}
    assert deposito.remesas == {}
    assert deposito.movimientos == []
    assert deposito.retiros == {}
    assert isinstance(deposito.politica_consumo, PoliticaFEFO)


def _deposito_con_escenario():
    """Arma el escenario del ejemplo del enunciado: AL-01 con R-101/R-102/R-103."""
    deposito = Deposito()
    material = deposito.registrar_material("AL-01", "Aluminio AL-01", "kg", 10)
    proveedor = deposito.registrar_proveedor("P-1", "Metales SA", 5)
    deposito.registrar_remesa("R-101", material, proveedor, 8, date(2026, 3, 2), date(2026, 3, 20))
    deposito.registrar_remesa("R-102", material, proveedor, 12, date(2026, 3, 4), date(2026, 3, 30))
    deposito.registrar_remesa("R-103", material, proveedor, 15, date(2026, 3, 5))
    return deposito, material


# ---------- Registro ----------

def test_registrar_material_lo_guarda_y_lo_devuelve():
    deposito = Deposito()

    material = deposito.registrar_material("AL-01", "Aluminio AL-01", "kg", 10)

    assert isinstance(material, Material)
    assert deposito.get_materiales()["AL-01"] is material


def test_registrar_material_id_duplicado_lanza_value_error():
    deposito = Deposito()
    deposito.registrar_material("AL-01", "Aluminio AL-01", "kg", 10)

    with pytest.raises(ValueError):
        deposito.registrar_material("AL-01", "otro", "kg", 5)


def test_registrar_proveedor_lo_guarda_y_lo_devuelve():
    deposito = Deposito()

    proveedor = deposito.registrar_proveedor("P-1", "Metales SA", 5)

    assert isinstance(proveedor, Proveedor)
    assert deposito.get_proveedores()["P-1"] is proveedor


def test_registrar_proveedor_id_duplicado_lanza_value_error():
    deposito = Deposito()
    deposito.registrar_proveedor("P-1", "Metales SA", 5)

    with pytest.raises(ValueError):
        deposito.registrar_proveedor("P-1", "otro", 1)


def test_registrar_remesa_lo_guarda_y_genera_movimiento_ingreso():
    deposito = Deposito()
    material = deposito.registrar_material("AL-01", "Aluminio AL-01", "kg", 10)
    proveedor = deposito.registrar_proveedor("P-1", "Metales SA", 5)

    remesa = deposito.registrar_remesa("R-101", material, proveedor, 8, date(2026, 3, 2), date(2026, 3, 20))

    assert deposito.get_remesas()["R-101"] is remesa
    ingresos = [m for m in deposito.get_movimientos() if isinstance(m, MovimientoIngreso)]
    assert len(ingresos) == 1
    assert ingresos[0].get_remesa() is remesa


def test_registrar_remesa_id_duplicado_lanza_value_error():
    deposito = Deposito()
    material = deposito.registrar_material("AL-01", "Aluminio AL-01", "kg", 10)
    proveedor = deposito.registrar_proveedor("P-1", "Metales SA", 5)
    deposito.registrar_remesa("R-101", material, proveedor, 8, date(2026, 3, 2))

    with pytest.raises(ValueError):
        deposito.registrar_remesa("R-101", material, proveedor, 1, date(2026, 3, 3))


# ---------- Existencias ----------

def test_existencia_fisica_suma_todas_las_remesas_sin_importar_vencimiento():
    deposito, material = _deposito_con_escenario()

    assert deposito.existencia_fisica(material) == 35


def test_existencia_disponible_excluye_remesas_vencidas():
    deposito, material = _deposito_con_escenario()

    disponible = deposito.existencia_disponible(material, date(2026, 4, 5))

    assert disponible == 15  # R-101 y R-102 ya vencieron, solo cuenta R-103


def test_existencia_disponible_excluye_remesas_agotadas():
    deposito, material = _deposito_con_escenario()
    deposito.get_remesas()["R-101"].consumir(8)  # agota R-101

    disponible = deposito.existencia_disponible(material, date(2026, 3, 10))

    assert disponible == 27  # 12 (R-102) + 15 (R-103)


# ---------- Reposicion ----------

def test_materiales_a_reponer_incluye_material_bajo_el_punto():
    deposito = Deposito()
    material = deposito.registrar_material("AL-01", "Aluminio AL-01", "kg", 10)
    proveedor = deposito.registrar_proveedor("P-1", "Metales SA", 5)
    deposito.registrar_remesa("R-1", material, proveedor, 5, date(2026, 3, 1))

    assert material in deposito.materiales_a_reponer()


def test_materiales_a_reponer_no_incluye_material_con_stock_suficiente():
    deposito = Deposito()
    material = deposito.registrar_material("AL-01", "Aluminio AL-01", "kg", 10)
    proveedor = deposito.registrar_proveedor("P-1", "Metales SA", 5)
    deposito.registrar_remesa("R-1", material, proveedor, 20, date(2026, 3, 1))

    assert material not in deposito.materiales_a_reponer()


# ---------- Retirar ----------

def test_retirar_con_una_sola_remesa():
    deposito = Deposito()
    material = deposito.registrar_material("AL-01", "Aluminio AL-01", "kg", 10)
    proveedor = deposito.registrar_proveedor("P-1", "Metales SA", 5)
    remesa = deposito.registrar_remesa("R-1", material, proveedor, 20, date(2026, 3, 1))

    retiro = deposito.retirar(material, 5, date(2026, 3, 10))

    assert len(retiro.get_movimientos()) == 1
    assert remesa.get_saldo_disponible() == 15


def test_retirar_distribuido_entre_varias_remesas_respeta_fefo():
    deposito, material = _deposito_con_escenario()

    retiro = deposito.retirar(material, 18, date(2026, 3, 10))

    remesas_del_retiro = [m.get_remesa().get_id() for m in retiro.get_movimientos()]
    assert remesas_del_retiro == ["R-101", "R-102"]
    assert deposito.get_remesas()["R-101"].get_saldo_disponible() == 0
    assert deposito.get_remesas()["R-102"].get_saldo_disponible() == 2
    assert deposito.get_remesas()["R-103"].get_saldo_disponible() == 15


def test_retirar_usa_remesa_sin_vencimiento_cuando_las_otras_vencieron():
    deposito, material = _deposito_con_escenario()
    deposito.retirar(material, 18, date(2026, 3, 10))  # agota R-101, deja R-102 en saldo 2

    retiro = deposito.retirar(material, 5, date(2026, 4, 5))  # R-101 agotada, R-102 vencida

    remesas_del_retiro = {m.get_remesa().get_id() for m in retiro.get_movimientos()}
    assert remesas_del_retiro == {"R-103"}
    assert deposito.get_remesas()["R-103"].get_saldo_disponible() == 10


def test_retirar_rechaza_si_no_alcanza_la_existencia_disponible():
    deposito, material = _deposito_con_escenario()

    with pytest.raises(ValueError):
        deposito.retirar(material, 999, date(2026, 3, 10))


def test_retirar_rechazado_no_modifica_el_inventario():
    deposito, material = _deposito_con_escenario()
    saldos_antes = {
        id_remesa: remesa.get_saldo_disponible()
        for id_remesa, remesa in deposito.get_remesas().items()
    }
    cantidad_movimientos_antes = len(deposito.get_movimientos())

    with pytest.raises(ValueError):
        deposito.retirar(material, 999, date(2026, 3, 10))

    saldos_despues = {
        id_remesa: remesa.get_saldo_disponible()
        for id_remesa, remesa in deposito.get_remesas().items()
    }
    assert saldos_despues == saldos_antes
    assert len(deposito.get_movimientos()) == cantidad_movimientos_antes


# ---------- Trazabilidad ----------

def test_remesas_de_retiro_devuelve_las_remesas_correctas():
    deposito, material = _deposito_con_escenario()

    retiro = deposito.retirar(material, 18, date(2026, 3, 10))

    remesas = deposito.remesas_de_retiro(retiro)
    assert [r.get_id() for r in remesas] == ["R-101", "R-102"]


def test_retiros_de_remesa_devuelve_los_retiros_correctos():
    deposito, material = _deposito_con_escenario()
    retiro1 = deposito.retirar(material, 18, date(2026, 3, 10))  # usa R-101 y R-102
    retiro2 = deposito.retirar(material, 1, date(2026, 3, 10))   # sale de R-102 (saldo 2)

    retiros = deposito.retiros_de_remesa(deposito.get_remesas()["R-102"])

    assert retiros == [retiro1, retiro2]
