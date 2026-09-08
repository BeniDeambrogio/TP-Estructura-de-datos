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
        return self.id

    def get_material(self):
        return self.material

    def get_fecha(self):
        return self.fecha

    def get_cantidad_solicitada(self):
        return self.cantidad_solicitada

    def get_movimientos(self):
        return self.movimientos

    # ---------- Metodo de CLASE ----------
    @classmethod
    def total_retiros(cls):
        return cls.cantidad_retiros

    # ---------- Metodo ESTATICO ----------
    @staticmethod
    def validar_cantidad(valor):
        pass

    # ---------- Metodos de INSTANCIA ----------
    def agregar_movimiento(self, movimiento):
        self.movimientos.append(movimiento)

    def cantidad_consumida(self):
        total = 0
        for movimiento in self.movimientos:
            total += movimiento.get_cantidad()
        return total
