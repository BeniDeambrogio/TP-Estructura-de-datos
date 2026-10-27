from datetime import date

from inventario import Material, MovimientoRetiro, Proveedor, Remesa, Retiro


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


# ---------- set con los ids de las remesas usadas ----------

def test_retiro_nuevo_no_tiene_ids_de_remesas():
    retiro = Retiro("RET-1", "AL-01", date(2026, 3, 10), 18)

    assert retiro.ids_de_remesas() == set()


def test_agregar_movimiento_suma_el_id_de_su_remesa_al_set():
    retiro = Retiro("RET-1", "AL-01", date(2026, 3, 10), 18)

    retiro.agregar_movimiento(MovimientoRetiro("MOV-1", date(2026, 3, 10), _remesa("R-101"), 8, retiro))
    retiro.agregar_movimiento(MovimientoRetiro("MOV-2", date(2026, 3, 10), _remesa("R-102"), 10, retiro))

    assert retiro.ids_de_remesas() == {"R-101", "R-102"}
    assert "R-101" in retiro.ids_de_remesas()
    assert "R-999" not in retiro.ids_de_remesas()


def test_set_de_ids_no_repite_una_remesa_con_dos_movimientos():
    retiro = Retiro("RET-1", "AL-01", date(2026, 3, 10), 18)
    remesa = _remesa("R-101")

    retiro.agregar_movimiento(MovimientoRetiro("MOV-1", date(2026, 3, 10), remesa, 3, retiro))
    retiro.agregar_movimiento(MovimientoRetiro("MOV-2", date(2026, 3, 10), remesa, 2, retiro))

    assert len(retiro.get_movimientos()) == 2
    assert retiro.ids_de_remesas() == {"R-101"}
