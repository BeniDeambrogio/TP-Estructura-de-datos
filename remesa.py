class Remesa:
    """Representa una partida especifica recibida de un proveedor."""

    cantidad_remesas = 0

    def __init__(self, id, material, proveedor, cantidad_recibida, fecha_recepcion, fecha_vencimiento=None):
        self.id = id
        self.material = material
        self.proveedor = proveedor
        self.cantidad_recibida = cantidad_recibida
        # RN12: el saldo disponible inicial coincide con la cantidad recibida.
        self.saldo_disponible = self.cantidad_recibida
        self.fecha_recepcion = fecha_recepcion
        self.fecha_vencimiento = fecha_vencimiento
        Remesa.cantidad_remesas += 1

    # ---------- Getters ----------
    def get_id(self):
        pass

    def get_material(self):
        pass

    def get_proveedor(self):
        pass

    def get_cantidad_recibida(self):
        pass

    def get_saldo_disponible(self):
        pass

    def get_fecha_recepcion(self):
        pass

    def get_fecha_vencimiento(self):
        pass

    # ---------- Metodo de CLASE ----------
    @classmethod
    def total_remesas(cls):
        pass

    # ---------- Metodo ESTATICO ----------
    @staticmethod
    def validar_cantidad(valor):
        pass

    # ---------- Metodos de INSTANCIA ----------
    def esta_vencida(self, fecha):
        pass

    def es_utilizable(self, fecha):
        pass

    def consumir(self, cantidad):
        pass
