class Retiro:
    """Representa la solicitud de retiro de un material para una fecha."""

    cantidad_retiros = 0

    def __init__(self, id, material, fecha, cantidad_solicitada):
        self.id = id
        self.material = material
        self.fecha = fecha
        self.cantidad_solicitada = cantidad_solicitada
        self.movimientos = []
        Retiro.cantidad_retiros += 1

    # ---------- Getters ----------
    def get_id(self):
        pass

    def get_material(self):
        pass

    def get_fecha(self):
        pass

    def get_cantidad_solicitada(self):
        pass

    def get_movimientos(self):
        pass

    # ---------- Metodo de CLASE ----------
    @classmethod
    def total_retiros(cls):
        pass

    # ---------- Metodo ESTATICO ----------
    @staticmethod
    def validar_cantidad(valor):
        pass

    # ---------- Metodos de INSTANCIA ----------
    def agregar_movimiento(self, movimiento):
        pass

    def cantidad_consumida(self):
        pass
