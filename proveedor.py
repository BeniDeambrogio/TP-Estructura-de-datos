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
        return self.id

    def get_nombre(self):
        return self.nombre

    def get_plazo_entrega_dias(self):
        return self.plazo_entrega_dias

    # ---------- Setter ----------
    def set_plazo_entrega_dias(self, nuevo_plazo):
        self.plazo_entrega_dias = nuevo_plazo

    # ---------- Metodo de CLASE ----------
    @classmethod
    def total_proveedores(cls):
        return cls.cantidad_proveedores

    # ---------- Metodo ESTATICO ----------
    @staticmethod
    def validar_plazo_entrega(valor):
        pass
