from datetime import date


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
        return sorted(
            remesas,
            key=lambda r: (
                r.get_fecha_vencimiento() is None,
                r.get_fecha_vencimiento() or date.max,
                r.get_fecha_recepcion(),
                r.get_id(),
            )
        )
