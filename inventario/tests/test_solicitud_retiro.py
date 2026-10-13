from datetime import date

import pytest

from inventario import CantidadInvalidaError, Material, SolicitudRetiro


def test_crear_solicitud_guarda_sus_datos():
    material = Material("AL-01", "Aluminio AL-01", "kg", 10)

    solicitud = SolicitudRetiro("SOL-1", material, 5, date(2026, 3, 10))

    assert solicitud.get_id() == "SOL-1"
    assert solicitud.get_material() is material
    assert solicitud.get_cantidad() == 5
    assert solicitud.get_fecha_solicitud() == date(2026, 3, 10)


def test_cantidad_no_positiva_lanza_cantidad_invalida_error():
    material = Material("AL-01", "Aluminio AL-01", "kg", 10)

    with pytest.raises(CantidadInvalidaError):
        SolicitudRetiro("SOL-1", material, 0, date(2026, 3, 10))
