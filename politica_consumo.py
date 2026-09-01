class PoliticaConsumo:
    """
    Define el "contrato" que cualquier politica de consumo deberia
    cumplir: ordenar(remesas) -> List[Remesa]. En el diagrama,
    PoliticaFEFO implementa esta interfaz. Como interfaces y
    polimorfismo todavia no se vieron en clase, esta clase se deja
    como esqueleto.
    """

    def __init__(self):
        pass

    def ordenar(self, remesas):
        pass


class PoliticaFEFO:
    """
    Version concreta e independiente del criterio First Expired,
    First Out (FEFO). En el diagrama implementa PoliticaConsumo; aca
    se declara aparte porque todavia no vimos interfaces.
    """

    def __init__(self):
        pass

    def ordenar(self, remesas):
        pass
