from datetime import date

from .excepciones import CantidadInvalidaError


class SolicitudRetiro:
    """Pedido de retiro de un material que espera en la cola del deposito."""

    def __init__(self, id, material, cantidad, fecha_solicitud):
        self.id = id
        self.material = material
        self.cantidad = self.validar_cantidad(cantidad)
        self.fecha_solicitud = fecha_solicitud

    # ---------- Getters ----------
    def get_id(self):
        return self.id

    def get_material(self):
        return self.material

    def get_cantidad(self):
        return self.cantidad

    def get_fecha_solicitud(self):
        return self.fecha_solicitud

    # ---------- Metodo ESTATICO ----------
    @staticmethod
    def validar_cantidad(valor):
        if valor <= 0:
            raise CantidadInvalidaError("La cantidad debe ser mayor que cero")
        return valor

    # ---------- Persistencia ----------
    def a_dict(self):
        return {
            "id": self.id,
            "material": self.material.get_id(),
            "cantidad": self.cantidad,
            "fecha_solicitud": self.fecha_solicitud.isoformat(),
        }

    @classmethod
    def desde_dict(cls, datos, materiales):
        return cls(datos["id"], materiales[datos["material"]], datos["cantidad"],
                   date.fromisoformat(datos["fecha_solicitud"]))
