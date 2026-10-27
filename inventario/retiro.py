from datetime import date

from .excepciones import CantidadInvalidaError


class Retiro:
    """Representa la solicitud de retiro de un material para una fecha."""

    cantidad_retiros = 0

    def __init__(self, id, material, fecha, cantidad_solicitada):
        self.id = id
        self.material = material
        self.fecha = fecha
        self.cantidad_solicitada = self.validar_cantidad(cantidad_solicitada)
        self.movimientos = []
        # Ids de las remesas de las que salio material en este retiro. Es un set:
        # no admite repetidos y preguntar si un id esta (in) no recorre nada.
        self.ids_remesas = set()
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

    def ids_de_remesas(self):
        return self.ids_remesas

    # ---------- Metodo de CLASE ----------
    @classmethod
    def total_retiros(cls):
        return cls.cantidad_retiros

    # ---------- Metodo ESTATICO ----------
    @staticmethod
    def validar_cantidad(valor):
        if valor <= 0:
            raise CantidadInvalidaError("La cantidad debe ser mayor que cero")
        return valor

    # ---------- Metodos de INSTANCIA ----------
    def agregar_movimiento(self, movimiento):
        self.movimientos.append(movimiento)
        self.ids_remesas.add(movimiento.get_remesa().get_id())

    def cantidad_consumida(self):
        total = 0
        for movimiento in self.movimientos:
            total += movimiento.get_cantidad()
        return total

    # ---------- Persistencia ----------
    def a_dict(self):
        # Los movimientos no se guardan aca: se guardan una sola vez en el
        # deposito y al cargar se vuelven a asociar a su retiro.
        return {
            "id": self.id,
            "material": self.material.get_id(),
            "fecha": self.fecha.isoformat(),
            "cantidad_solicitada": self.cantidad_solicitada,
        }

    @classmethod
    def desde_dict(cls, datos, materiales):
        return cls(datos["id"], materiales[datos["material"]], date.fromisoformat(datos["fecha"]),
                   datos["cantidad_solicitada"])
