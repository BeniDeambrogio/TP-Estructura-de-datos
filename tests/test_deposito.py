from inventario import Deposito, PoliticaFEFO


def test_init_crea_colecciones_vacias_y_politica_fefo():
    deposito = Deposito()

    assert deposito.materiales == {}
    assert deposito.proveedores == {}
    assert deposito.remesas == {}
    assert deposito.movimientos == []
    assert deposito.retiros == {}
    assert isinstance(deposito.politica_consumo, PoliticaFEFO)
