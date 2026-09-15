import pytest

from material import Material
from movimiento import MovimientoIngreso, MovimientoRetiro
from pedido import Pedido
from proveedor import Proveedor
from remesa import Remesa
from retiro import Retiro


@pytest.fixture(autouse=True)
def reset_contadores():
    """Los contadores son atributos de CLASE compartidos entre instancias.
    Sin este reset, un test contamina el conteo del siguiente."""
    Material.cantidad_materiales = 0
    Proveedor.cantidad_proveedores = 0
    Remesa.cantidad_remesas = 0
    MovimientoIngreso.cantidad_ingresos = 0
    MovimientoRetiro.cantidad_retiros_registrados = 0
    Pedido.cantidad_pedidos = 0
    Retiro.cantidad_retiros = 0
