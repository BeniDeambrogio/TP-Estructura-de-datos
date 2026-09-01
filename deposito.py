from .politica_consumo import PoliticaFEFO


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
        # Se usa directamente PoliticaFEFO (no PoliticaConsumo) porque
        # todavia no vimos polimorfismo: sin herencia/interfaces reales,
        # Deposito no puede depender de forma generica de la interfaz.
        self.politica_consumo = PoliticaFEFO()

    # ---------- Getters ----------
    def get_materiales(self):
        pass

    def get_proveedores(self):
        pass

    def get_remesas(self):
        pass

    def get_movimientos(self):
        pass

    def get_retiros(self):
        pass

    def get_politica_consumo(self):
        pass

    # ---------- Registro de entidades ----------
    def registrar_material(self, id, nombre, unidad_medida, punto_reposicion):
        pass

    def registrar_proveedor(self, id, nombre, plazo_entrega_dias):
        pass

    def registrar_remesa(self, id, material, proveedor, cantidad_recibida, fecha_recepcion, fecha_vencimiento=None):
        pass

    # ---------- Consultas de existencias ----------
    def existencia_fisica(self, material):
        pass

    def existencia_disponible(self, material, fecha):
        pass

    # ---------- Retiros ----------
    def retirar(self, material, cantidad, fecha):
        pass

    # ---------- Reposicion ----------
    def materiales_a_reponer(self):
        pass

    # ---------- Trazabilidad ----------
    def remesas_de_retiro(self, retiro):
        pass

    def retiros_de_remesa(self, remesa):
        pass
