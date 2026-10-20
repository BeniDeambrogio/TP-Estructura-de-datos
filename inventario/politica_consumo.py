from datetime import date


class PoliticaConsumo:
    """
    Clase base que define el contrato de una politica de consumo:
    clave_orden(remesa) -> valor comparable (la menor se consume primero) y
    ordenar(remesas) -> List[Remesa]. PoliticaFEFO hereda de ella.
    """

    def __init__(self):
        pass

    def clave_orden(self, remesa):
        pass

    def ordenar(self, remesas):
        pass


class PoliticaFEFO(PoliticaConsumo):
    """
    First Expired, First Out (FEFO). Hereda de PoliticaConsumo.
    """

    def __init__(self):
        super().__init__()

    def clave_orden(self, remesa):
        # Tupla de criterios en cascada: Python compara de izquierda a derecha.
        return (
            remesa.get_fecha_vencimiento() is None,
            remesa.get_fecha_vencimiento() or date.max,
            remesa.get_fecha_recepcion(),
            remesa.get_id(),
        )

    def ordenar(self, remesas):
        return sorted(remesas, key=self.clave_orden)
