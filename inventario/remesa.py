class Remesa:
    """Representa una partida especifica recibida de un proveedor."""

    cantidad_remesas = 0

    def __init__(self, id, material, proveedor, cantidad_recibida, fecha_recepcion, fecha_vencimiento=None):
        self.id = id
        self.material = material
        self.proveedor = proveedor
        self.cantidad_recibida = self.validar_cantidad(cantidad_recibida)
        # RN12: el saldo disponible inicial coincide con la cantidad recibida.
        self.saldo_disponible = self.cantidad_recibida
        self.fecha_recepcion = fecha_recepcion
        self.fecha_vencimiento = fecha_vencimiento
        Remesa.cantidad_remesas += 1

    # ---------- Getters ----------
    def get_id(self):
        return self.id

    def get_material(self):
        return self.material

    def get_proveedor(self):
        return self.proveedor

    def get_cantidad_recibida(self):
        return self.cantidad_recibida

    def get_saldo_disponible(self):
        return self.saldo_disponible

    def get_fecha_recepcion(self):
        return self.fecha_recepcion

    def get_fecha_vencimiento(self):
        return self.fecha_vencimiento

    # ---------- Metodo de CLASE ----------
    @classmethod
    def total_remesas(cls):
        return cls.cantidad_remesas

    # ---------- Metodo ESTATICO ----------
    @staticmethod
    def validar_cantidad(valor):
        if valor <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")
        return valor

    # ---------- Metodos de INSTANCIA ----------
    def esta_vencida(self, fecha):
        if self.fecha_vencimiento is None:
            return False
        return fecha > self.fecha_vencimiento

    def es_utilizable(self, fecha):
        return self.saldo_disponible > 0 and not self.esta_vencida(fecha)

    def consumir(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad a consumir debe ser mayor que cero")
        if cantidad > self.saldo_disponible:
            raise ValueError("No hay saldo disponible suficiente en la remesa")
        self.saldo_disponible -= cantidad
