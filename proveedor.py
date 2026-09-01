class Proveedor:
    """Representa a una empresa que suministra materiales."""

    cantidad_proveedores = 0

    def __init__(self, id, nombre, plazo_entrega_dias):
        self.id = id
        self.nombre = nombre
        self.plazo_entrega_dias = plazo_entrega_dias
        Proveedor.cantidad_proveedores += 1

    # ---------- Getters ----------
    def get_id(self):
        pass

    def get_nombre(self):
        pass

    def get_plazo_entrega_dias(self):
        pass

    # ---------- Setter ----------
    def set_plazo_entrega_dias(self, nuevo_plazo):
        pass

    # ---------- Metodo de CLASE ----------
    @classmethod
    def total_proveedores(cls):
        pass

    # ---------- Metodo ESTATICO ----------
    @staticmethod
    def validar_plazo_entrega(valor):
        pass
