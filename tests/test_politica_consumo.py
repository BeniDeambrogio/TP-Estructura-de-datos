from inventario import PoliticaConsumo, PoliticaFEFO


def test_politica_fefo_es_instancia_de_politica_consumo():
    politica = PoliticaFEFO()

    assert isinstance(politica, PoliticaConsumo)
