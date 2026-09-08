class PoliticaConsumo:
    """
    Clase base que define el contrato de una politica de consumo:
    ordenar(remesas) -> List[Remesa]. PoliticaFEFO hereda de ella.
    """

    def __init__(self):
        pass

    def ordenar(self, remesas):
        pass


class PoliticaFEFO(PoliticaConsumo):
    """
    First Expired, First Out (FEFO). Hereda de PoliticaConsumo.
    """

    def __init__(self):
        super().__init__()

    def ordenar(self, remesas):
        pass
