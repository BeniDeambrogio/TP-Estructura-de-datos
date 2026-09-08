from decimal import Decimal


class RenglonPedido:
    """Cantidad solicitada de un material junto con el precio acordado."""

    def __init__(self, material, cantidad, precio_unitario):
        self.material = material
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

    # ---------- Getters ----------
    def get_material(self):
        return self.material

    def get_cantidad(self):
        return self.cantidad

    def get_precio_unitario(self):
        return self.precio_unitario

    # ---------- Metodo ESTATICO ----------
    @staticmethod
    def validar_cantidad(valor):
        pass

    # ---------- Metodo de INSTANCIA ----------
    def subtotal(self):
        return self.precio_unitario * Decimal(str(self.cantidad))


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
        return self.id

    def get_proveedor(self):
        return self.proveedor

    def get_renglones(self):
        return self.renglones

    # ---------- Metodo de CLASE ----------
    @classmethod
    def total_pedidos(cls):
        return cls.cantidad_pedidos

    # ---------- Metodos de INSTANCIA ----------
    def agregar_renglon(self, material, cantidad, precio_unitario):
        renglon = RenglonPedido(material, cantidad, precio_unitario)
        self.renglones.append(renglon)
        return renglon

    def importe_total(self):
        total = Decimal("0")
        for renglon in self.renglones:
            total += renglon.subtotal()
        return total
