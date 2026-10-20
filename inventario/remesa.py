from datetime import date

from .excepciones import CantidadInvalidaError, StockInsuficienteError


class Remesa:
    """Representa una partida especifica recibida de un proveedor."""

    cantidad_remesas = 0

    def __init__(self, id, material, proveedor, cantidad_recibida, fecha_recepcion, fecha_vencimiento=None,
                 datos_adicionales=None):
        self.id = id
        self.material = material
        self.proveedor = proveedor
        self.cantidad_recibida = self.validar_cantidad(cantidad_recibida)
        # RN12: el saldo disponible inicial coincide con la cantidad recibida.
        self.saldo_disponible = self.cantidad_recibida
        self.fecha_recepcion = fecha_recepcion
        self.fecha_vencimiento = fecha_vencimiento
        # Datos opcionales que no tienen atributo propio (lote, numero de guia,
        # temperatura de recepcion, etc.). None nunca se usa como default mutable:
        # si no llega nada, se crea un diccionario vacio nuevo aca adentro.
        self.datos_adicionales = datos_adicionales if datos_adicionales is not None else {}
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

    def obtener_dato(self, clave, valor_por_defecto=None):
        return self.datos_adicionales.get(clave, valor_por_defecto)

    # ---------- Metodo de CLASE ----------
    @classmethod
    def total_remesas(cls):
        return cls.cantidad_remesas

    # ---------- Metodo ESTATICO ----------
    @staticmethod
    def validar_cantidad(valor):
        if valor <= 0:
            raise CantidadInvalidaError("La cantidad debe ser mayor que cero")
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
            raise CantidadInvalidaError("La cantidad a consumir debe ser mayor que cero")
        if cantidad > self.saldo_disponible:
            raise StockInsuficienteError("No hay saldo disponible suficiente en la remesa")
        self.saldo_disponible -= cantidad

    # ---------- Persistencia ----------
    def a_dict(self):
        # Material y proveedor se guardan por id: al cargar se buscan entre
        # los ya reconstruidos para que todas las remesas apunten al mismo objeto.
        return {
            "id": self.id,
            "material": self.material.get_id(),
            "proveedor": self.proveedor.get_id(),
            "cantidad_recibida": self.cantidad_recibida,
            "saldo_disponible": self.saldo_disponible,
            "fecha_recepcion": self.fecha_recepcion.isoformat(),
            "fecha_vencimiento": self.fecha_vencimiento.isoformat() if self.fecha_vencimiento else None,
            "datos_adicionales": self._datos_adicionales_a_json(),
        }

    @staticmethod
    def _valor_a_json(valor):
        # JSON solo sabe escribir texto, numeros, booleanos y None. Cualquier
        # otro valor que llegue por **kwargs (fechas, Decimal, etc.) se guarda
        # como texto: al cargar vuelve como texto, no como su tipo original.
        if isinstance(valor, date):
            return valor.isoformat()
        if valor is None or isinstance(valor, (str, int, float, bool)):
            return valor
        return str(valor)

    def _datos_adicionales_a_json(self):
        convertidos = {}
        for clave, valor in self.datos_adicionales.items():
            convertidos[clave] = self._valor_a_json(valor)
        return convertidos

    @classmethod
    def desde_dict(cls, datos, materiales, proveedores):
        fecha_vencimiento = datos["fecha_vencimiento"]
        remesa = cls(datos["id"], materiales[datos["material"]], proveedores[datos["proveedor"]],
                     datos["cantidad_recibida"], date.fromisoformat(datos["fecha_recepcion"]),
                     date.fromisoformat(fecha_vencimiento) if fecha_vencimiento else None,
                     datos_adicionales=datos["datos_adicionales"])
        # El constructor arranca con saldo = cantidad recibida (RN12); al
        # cargar se restaura lo que ya se habia consumido.
        remesa.saldo_disponible = datos["saldo_disponible"]
        return remesa
