class Movimiento:
    """
    Representa un hecho ocurrido sobre el inventario (un ingreso o un
    retiro). En el diagrama, MovimientoIngreso y MovimientoRetiro
    heredan de esta clase. Como todavia no vimos herencia en clase,
    se declaran como clases concretas independientes mas abajo,
    duplicando los mismos atributos.
    """

    def __init__(self, id, fecha, remesa, cantidad):
        self.id = id
        self.fecha = fecha
        self.remesa = remesa
        self.cantidad = cantidad

    # ---------- Getters ----------
    def get_id(self):
        pass

    def get_fecha(self):
        pass

    def get_remesa(self):
        pass

    def get_cantidad(self):
        pass

    # ---------- Metodo de INSTANCIA ----------
    def tipo(self):
        pass


class MovimientoIngreso:
    """
    Version concreta e independiente del movimiento de ingreso.
    En el diagrama hereda de Movimiento; aca se declara aparte porque
    todavia no vimos herencia.
    """

    cantidad_ingresos = 0

    def __init__(self, id, fecha, remesa, cantidad):
        self.id = id
        self.fecha = fecha
        self.remesa = remesa
        self.cantidad = cantidad
        MovimientoIngreso.cantidad_ingresos += 1

    # ---------- Getters ----------
    def get_id(self):
        pass

    def get_fecha(self):
        pass

    def get_remesa(self):
        pass

    def get_cantidad(self):
        pass

    # ---------- Metodo de CLASE ----------
    @classmethod
    def total_ingresos(cls):
        pass

    # ---------- Metodo ESTATICO ----------
    @staticmethod
    def validar_cantidad(valor):
        pass

    # ---------- Metodo de INSTANCIA ----------
    def tipo(self):
        pass


class MovimientoRetiro:
    """
    Version concreta e independiente del movimiento de retiro.
    Ademas de id/fecha/remesa/cantidad, agrega el atributo propio
    "retiro" que muestra el diagrama para esta clase.
    """

    cantidad_retiros_registrados = 0

    def __init__(self, id, fecha, remesa, cantidad, retiro):
        self.id = id
        self.fecha = fecha
        self.remesa = remesa
        self.cantidad = cantidad
        self.retiro = retiro
        MovimientoRetiro.cantidad_retiros_registrados += 1

    # ---------- Getters ----------
    def get_id(self):
        pass

    def get_fecha(self):
        pass

    def get_remesa(self):
        pass

    def get_cantidad(self):
        pass

    def get_retiro(self):
        pass

    # ---------- Metodo de CLASE ----------
    @classmethod
    def total_retiros_registrados(cls):
        pass

    # ---------- Metodo ESTATICO ----------
    @staticmethod
    def validar_cantidad(valor):
        pass

    # ---------- Metodo de INSTANCIA ----------
    def tipo(self):
        pass
