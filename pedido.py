class RenglonPedido:
    """Cantidad solicitada de un material junto con el precio acordado."""

    def __init__(self, material, cantidad, precio_unitario):
        self.material = material
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

    # ---------- Getters ----------
    def get_material(self):
        pass

    def get_cantidad(self):
        pass

    def get_precio_unitario(self):
        pass

    # ---------- Metodo ESTATICO ----------
    @staticmethod
    def validar_cantidad(valor):
        pass

    # ---------- Metodo de INSTANCIA ----------
    def subtotal(self):
        pass


class Pedido:
    """Solicitud dirigida a un unico proveedor, compuesta por renglones."""

    cantidad_pedidos = 0

    def __init__(self, id, proveedor):
        self.id = id
        self.proveedor = proveedor
        self.renglones = []
        Pedido.cantidad_pedidos += 1

    # ---------- Getters ----------
    def get_id(self):
        pass

    def get_proveedor(self):
        pass

    def get_renglones(self):
        pass

    # ---------- Metodo de CLASE ----------
    @classmethod
    def total_pedidos(cls):
        pass

    # ---------- Metodos de INSTANCIA ----------
    def agregar_renglon(self, material, cantidad, precio_unitario):
        pass

    def importe_total(self):
        pass
