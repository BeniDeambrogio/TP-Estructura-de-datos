from datetime import date

from inventario import Material, PoliticaConsumo, PoliticaFEFO, Proveedor, Remesa


def _material():
    return Material("AL-01", "Aluminio AL-01", "kg", 10)


def _proveedor():
    return Proveedor("P-1", "Metales SA", 5)


def test_politica_fefo_es_instancia_de_politica_consumo():
    politica = PoliticaFEFO()

    assert isinstance(politica, PoliticaConsumo)


def test_ordenar_respeta_fefo_por_vencimiento():
    material = _material()
    proveedor = _proveedor()
    r101 = Remesa("R-101", material, proveedor, 8, date(2026, 3, 2), date(2026, 3, 20))
    r102 = Remesa("R-102", material, proveedor, 12, date(2026, 3, 4), date(2026, 3, 30))
    r103 = Remesa("R-103", material, proveedor, 15, date(2026, 3, 5))

    orden = PoliticaFEFO().ordenar([r103, r102, r101])

    assert [r.get_id() for r in orden] == ["R-101", "R-102", "R-103"]


def test_ordenar_desempata_por_fecha_recepcion_si_vencimiento_es_igual():
    material = _material()
    proveedor = _proveedor()
    vencimiento = date(2026, 3, 20)
    recibida_primero = Remesa("R-1", material, proveedor, 5, date(2026, 3, 1), vencimiento)
    recibida_despues = Remesa("R-2", material, proveedor, 5, date(2026, 3, 3), vencimiento)

    orden = PoliticaFEFO().ordenar([recibida_despues, recibida_primero])

    assert [r.get_id() for r in orden] == ["R-1", "R-2"]


def test_ordenar_deja_remesas_sin_vencimiento_al_final():
    material = _material()
    proveedor = _proveedor()
    con_vencimiento = Remesa("R-1", material, proveedor, 5, date(2026, 3, 1), date(2026, 3, 20))
    sin_vencimiento = Remesa("R-2", material, proveedor, 5, date(2026, 3, 1))

    orden = PoliticaFEFO().ordenar([sin_vencimiento, con_vencimiento])

    assert [r.get_id() for r in orden] == ["R-1", "R-2"]
