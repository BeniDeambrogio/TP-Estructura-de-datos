from datetime import date

from .material import Material
from .proveedor import Proveedor
from .remesa import Remesa
from .movimiento import MovimientoIngreso, MovimientoRetiro
from .politica_consumo import PoliticaFEFO
from .retiro import Retiro


class Deposito:
    """
    Coordina materiales, proveedores, remesas, movimientos y retiros.
    No decide automaticamente que comprar.
    """

    def __init__(self):
        self.materiales = {}
        self.proveedores = {}
        self.remesas = {}
        self.movimientos = []
        self.retiros = {}
        self.politica_consumo = PoliticaFEFO()

    # ---------- Getters ----------
    def get_materiales(self):
        return self.materiales

    def get_proveedores(self):
        return self.proveedores

    def get_remesas(self):
        return self.remesas

    def get_movimientos(self):
        return self.movimientos

    def get_retiros(self):
        return self.retiros

    def get_politica_consumo(self):
        return self.politica_consumo

    # ---------- Registro de entidades ----------
    def registrar_material(self, id, nombre, unidad_medida, punto_reposicion):
        if id in self.materiales:
            raise ValueError(f"Ya existe un material con id {id}")
        material = Material(id, nombre, unidad_medida, punto_reposicion)
        self.materiales[id] = material
        return material

    def registrar_proveedor(self, id, nombre, plazo_entrega_dias):
        if id in self.proveedores:
            raise ValueError(f"Ya existe un proveedor con id {id}")
        proveedor = Proveedor(id, nombre, plazo_entrega_dias)
        self.proveedores[id] = proveedor
        return proveedor

    def registrar_remesa(self, id, material, proveedor, cantidad_recibida, fecha_recepcion, fecha_vencimiento=None):
        if id in self.remesas:
            raise ValueError(f"Ya existe una remesa con id {id}")
        remesa = Remesa(id, material, proveedor, cantidad_recibida, fecha_recepcion, fecha_vencimiento)
        self.remesas[id] = remesa

        # RN23: registrar una remesa genera su movimiento de ingreso.
        id_movimiento = f"MOV-{len(self.movimientos) + 1}"
        movimiento_ingreso = MovimientoIngreso(id_movimiento, fecha_recepcion, remesa, cantidad_recibida)
        self.movimientos.append(movimiento_ingreso)

        return remesa

    # ---------- Consultas de existencias ----------
    def existencia_fisica(self, material):
        total = 0
        for remesa in self.remesas.values():
            if remesa.get_material().get_id() == material.get_id():
                total += remesa.get_saldo_disponible()
        return total

    def existencia_disponible(self, material, fecha):
        total = 0
        for remesa in self.remesas.values():
            if remesa.get_material().get_id() == material.get_id() and remesa.es_utilizable(fecha):
                total += remesa.get_saldo_disponible()
        return total

    # ---------- Retiros ----------
    def retirar(self, material, cantidad, fecha):
        if cantidad <= 0:
            raise ValueError("La cantidad a retirar debe ser mayor que cero")

        # RN18: se valida ANTES de tocar nada del inventario.
        disponible = self.existencia_disponible(material, fecha)
        if disponible < cantidad:
            raise ValueError("La existencia disponible es insuficiente para realizar el retiro")

        remesas_utilizables = [
            remesa for remesa in self.remesas.values()
            if remesa.get_material().get_id() == material.get_id() and remesa.es_utilizable(fecha)
        ]
        remesas_ordenadas = self.politica_consumo.ordenar(remesas_utilizables)

        # Se calcula la distribucion sin modificar todavia ninguna remesa,
        # para garantizar RN22 si algo fallara antes de este punto.
        cantidad_restante = cantidad
        distribucion = []
        for remesa in remesas_ordenadas:
            if cantidad_restante > 0:
                cantidad_a_consumir = min(remesa.get_saldo_disponible(), cantidad_restante)
                distribucion.append((remesa, cantidad_a_consumir))
                cantidad_restante -= cantidad_a_consumir

        id_retiro = f"RET-{len(self.retiros) + 1}"
        retiro = Retiro(id_retiro, material, fecha, cantidad)

        # Recien aca se aplican los cambios (RN20, RN21, RN24).
        for remesa, cantidad_a_consumir in distribucion:
            remesa.consumir(cantidad_a_consumir)
            id_movimiento = f"MOV-{len(self.movimientos) + 1}"
            movimiento_retiro = MovimientoRetiro(id_movimiento, fecha, remesa, cantidad_a_consumir, retiro)
            retiro.agregar_movimiento(movimiento_retiro)
            self.movimientos.append(movimiento_retiro)

        self.retiros[id_retiro] = retiro
        return retiro

    # ---------- Reposicion ----------
    def materiales_a_reponer(self):
        resultado = []
        for material in self.materiales.values():
            existencia = self.existencia_disponible(material, date.today())
            if material.requiere_reposicion(existencia):
                resultado.append(material)
        return resultado

    # ---------- Trazabilidad ----------
    def remesas_de_retiro(self, retiro):
        return [movimiento.get_remesa() for movimiento in retiro.get_movimientos()]

    def retiros_de_remesa(self, remesa):
        resultado = []
        for retiro in self.retiros.values():
            remesa_participo = False
            for movimiento in retiro.get_movimientos():
                if movimiento.get_remesa().get_id() == remesa.get_id():
                    remesa_participo = True
            if remesa_participo:
                resultado.append(retiro)
        return resultado
