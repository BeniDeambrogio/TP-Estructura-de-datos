class Movimiento:
    """
    Representa un hecho ocurrido sobre el inventario (un ingreso o un
    retiro). Es la clase base de la que heredan MovimientoIngreso y
    MovimientoRetiro.
    """

    def __init__(self, id, fecha, remesa, cantidad):
        self.id = id
        self.fecha = fecha
        self.remesa = remesa
        self.cantidad = cantidad

    # ---------- Getters ----------
    def get_id(self):
        return self.id

    def get_fecha(self):
        return self.fecha

    def get_remesa(self):
        return self.remesa

    def get_cantidad(self):
        return self.cantidad

    # ---------- Metodo de INSTANCIA (pensado para ser sobreescrito) ----------
    def tipo(self):
        pass


class MovimientoIngreso(Movimiento):
    """Movimiento generado al registrar el ingreso de una remesa."""

    cantidad_ingresos = 0

    def __init__(self, id, fecha, remesa, cantidad):
        super().__init__(id, fecha, remesa, cantidad)
        MovimientoIngreso.cantidad_ingresos += 1

    # ---------- Metodo de CLASE ----------
    @classmethod
    def total_ingresos(cls):
        return cls.cantidad_ingresos

    # ---------- Metodo ESTATICO ----------
    @staticmethod
    def validar_cantidad(valor):
        pass

    # ---------- Metodo de INSTANCIA (polimorfismo) ----------
    def tipo(self):
        return "INGRESO"


class MovimientoRetiro(Movimiento):
    """Movimiento generado al consumir una remesa dentro de un retiro."""

    cantidad_retiros_registrados = 0

    def __init__(self, id, fecha, remesa, cantidad, retiro):
        super().__init__(id, fecha, remesa, cantidad)
        self.retiro = retiro
        MovimientoRetiro.cantidad_retiros_registrados += 1

    # ---------- Getter propio ----------
    def get_retiro(self):
        return self.retiro

    # ---------- Metodo de CLASE ----------
    @classmethod
    def total_retiros_registrados(cls):
        return cls.cantidad_retiros_registrados

    # ---------- Metodo ESTATICO ----------
    @staticmethod
    def validar_cantidad(valor):
        pass

    # ---------- Metodo de INSTANCIA (polimorfismo) ----------
    def tipo(self):
        return "RETIRO"
