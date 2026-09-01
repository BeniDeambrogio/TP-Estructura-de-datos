class Material:
    """
    Representa un tipo de insumo utilizado por la empresa
    (por ejemplo "Aluminio AL-01").
    """

    cantidad_materiales = 0

    def __init__(self, id, nombre, unidad_medida, punto_reposicion):
        self.id = id
        self.nombre = nombre
        self.unidad_medida = unidad_medida
        self.punto_reposicion = punto_reposicion
        Material.cantidad_materiales += 1

    # ---------- Getters ----------
    def get_id(self):
        pass

    def get_nombre(self):
        pass

    def get_unidad_medida(self):
        pass

    def get_punto_reposicion(self):
        pass

    # ---------- Setter ----------
    def set_punto_reposicion(self, nuevo_punto_reposicion):
        pass

    # ---------- Metodo de CLASE ----------
    @classmethod
    def total_materiales(cls):
        pass

    # ---------- Metodo ESTATICO ----------
    @staticmethod
    def validar_punto_reposicion(valor):
        pass

    # ---------- Metodo de INSTANCIA ----------
    def requiere_reposicion(self, existencia_disponible):
        pass
