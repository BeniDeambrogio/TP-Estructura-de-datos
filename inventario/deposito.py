import json
from datetime import date

from .material import Material
from .proveedor import Proveedor
from .remesa import Remesa
from .movimiento import MovimientoIngreso, MovimientoRetiro
from .politica_consumo import PoliticaFEFO
from .retiro import Retiro
from .pedido import Pedido
from .solicitud_retiro import SolicitudRetiro
from .estructuras import Cola, ListaEnlazadaOrdenada
from .excepciones import CantidadInvalidaError, StockInsuficienteError, IdDuplicadoError, DatoFaltanteError


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
        self.pedidos = {}
        # Indice {id_material: ListaEnlazadaOrdenada de remesas}. Evita recorrer
        # las remesas de todos los materiales al consultar uno solo, y cada lista
        # ya queda ordenada segun la politica de consumo (el primero es el que
        # se consume antes), asi retirar() no tiene que ordenar en cada retiro.
        self.remesas_por_material = {}
        # Solicitudes de retiro en espera, atendidas por orden de llegada (FIFO).
        self.solicitudes = Cola()
        self.cantidad_solicitudes = 0

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

    def get_solicitudes(self):
        return self.solicitudes

    def get_pedidos(self):
        return self.pedidos

    # ---------- Registro de entidades ----------
    def registrar_material(self, id, nombre, unidad_medida, punto_reposicion):
        if id in self.materiales:
            raise IdDuplicadoError(f"Ya existe un material con id {id}")
        material = Material(id, nombre, unidad_medida, punto_reposicion)
        self.materiales[id] = material
        return material

    def registrar_proveedor(self, id, nombre, plazo_entrega_dias):
        if id in self.proveedores:
            raise IdDuplicadoError(f"Ya existe un proveedor con id {id}")
        proveedor = Proveedor(id, nombre, plazo_entrega_dias)
        self.proveedores[id] = proveedor
        return proveedor

    def crear_remesa(self, id, material, proveedor, cantidad, **datos):
        # fecha_recepcion es obligatoria para poder registrar la remesa y su
        # movimiento de ingreso, aunque llegue por **datos y no como parametro
        # fijo (para respetar la firma pedida por la catedra).
        if "fecha_recepcion" not in datos:
            raise DatoFaltanteError("Debe indicarse fecha_recepcion")

        if id in self.remesas:
            raise IdDuplicadoError(f"Ya existe una remesa con id {id}")

        fecha_recepcion = datos.pop("fecha_recepcion")
        # RN13: fecha_vencimiento es opcional, default None si no se pasa.
        fecha_vencimiento = datos.pop("fecha_vencimiento", None)
        # Lo que sobra en datos (lote, numero de guia, temperatura de
        # recepcion, etc.) queda guardado en la remesa sin que este metodo
        # necesite conocer esos nombres de antemano.
        remesa = Remesa(id, material, proveedor, cantidad, fecha_recepcion, fecha_vencimiento,
                         datos_adicionales=datos)
        self.remesas[id] = remesa
        self._indexar_remesa(remesa)

        # RN23: registrar una remesa genera su movimiento de ingreso.
        id_movimiento = f"MOV-{len(self.movimientos) + 1}"
        movimiento_ingreso = MovimientoIngreso(id_movimiento, fecha_recepcion, remesa, cantidad)
        self.movimientos.append(movimiento_ingreso)

        return remesa

    # ---------- Consultas de existencias ----------
    def _indexar_remesa(self, remesa):
        id_material = remesa.get_material().get_id()
        if id_material not in self.remesas_por_material:
            self.remesas_por_material[id_material] = ListaEnlazadaOrdenada(self.politica_consumo.clave_orden)
        self.remesas_por_material[id_material].insertar(remesa)

    def remesas_de_material(self, material):
        """Remesas del material, ya ordenadas segun la politica de consumo."""
        lista = self.remesas_por_material.get(material.get_id())
        if lista is None:
            return []
        return lista.a_lista()

    def existencia_fisica(self, material):
        total = 0
        for remesa in self.remesas_de_material(material):
            total += remesa.get_saldo_disponible()
        return total

    def existencia_disponible(self, material, fecha):
        total = 0
        for remesa in self.remesas_de_material(material):
            if remesa.es_utilizable(fecha):
                total += remesa.get_saldo_disponible()
        return total

    # ---------- Retiros ----------
    def retirar(self, material, cantidad, fecha):
        if cantidad <= 0:
            raise CantidadInvalidaError("La cantidad a retirar debe ser mayor que cero")

        # RN18: se valida ANTES de tocar nada del inventario.
        disponible = self.existencia_disponible(material, fecha)
        if disponible < cantidad:
            raise StockInsuficienteError("La existencia disponible es insuficiente para realizar el retiro")

        # remesas_de_material ya viene ordenada por la politica (la lista enlazada
        # ordenada la mantiene asi), solo hay que quedarse con las utilizables.
        remesas_ordenadas = [
            remesa for remesa in self.remesas_de_material(material) if remesa.es_utilizable(fecha)
        ]

        # Se calcula la distribucion sin modificar todavia ninguna remesa,
        # para garantizar RN22 si algo fallara antes de este punto.
        distribucion = self._repartir(remesas_ordenadas, 0, cantidad)

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

    # ---------- Pedidos a proveedores ----------
    def crear_pedido(self, id, proveedor):
        if id in self.pedidos:
            raise IdDuplicadoError(f"Ya existe un pedido con id {id}")
        pedido = Pedido(id, proveedor)
        self.pedidos[id] = pedido
        return pedido

    @staticmethod
    def _repartir(remesas, posicion, cantidad_restante):
        """
        Reparte la cantidad entre las remesas, de la primera a la ultima, y
        devuelve una lista de (remesa, cantidad a consumir). Solo calcula:
        no modifica ninguna remesa.
        Recursiva: toma la remesa de la posicion actual y reparte lo que falta
        entre las que siguen.
        """
        # Caso base: no queda nada por repartir o se acabaron las remesas.
        if cantidad_restante == 0 or posicion == len(remesas):
            return []
        remesa = remesas[posicion]
        cantidad_a_consumir = min(remesa.get_saldo_disponible(), cantidad_restante)
        resto = Deposito._repartir(remesas, posicion + 1, cantidad_restante - cantidad_a_consumir)
        return [(remesa, cantidad_a_consumir)] + resto

    # ---------- Solicitudes de retiro (cola FIFO) ----------
    def solicitar_retiro(self, material, cantidad, fecha):
        self.cantidad_solicitudes += 1
        id_solicitud = f"SOL-{self.cantidad_solicitudes}"
        solicitud = SolicitudRetiro(id_solicitud, material, cantidad, fecha)
        self.solicitudes.encolar(solicitud)
        return solicitud

    def atender_siguiente(self, fecha):
        # frente() lanza EstructuraVaciaError si no hay solicitudes en espera.
        solicitud = self.solicitudes.frente()
        # Si no alcanza el stock, la solicitud queda primera: no se saltea a
        # nadie para respetar el orden de llegada.
        if self.existencia_disponible(solicitud.get_material(), fecha) < solicitud.get_cantidad():
            return None
        self.solicitudes.desencolar()
        return self.retirar(solicitud.get_material(), solicitud.get_cantidad(), fecha)

    def solicitudes_pendientes(self):
        return self.solicitudes.tamanio()

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
            if remesa.get_id() in retiro.ids_de_remesas():
                resultado.append(retiro)
        return resultado

    # ---------- Persistencia (JSON) ----------
    def guardar(self, ruta):
        datos = {
            "materiales": [m.a_dict() for m in self.materiales.values()],
            "proveedores": [p.a_dict() for p in self.proveedores.values()],
            "remesas": [r.a_dict() for r in self.remesas.values()],
            "retiros": [r.a_dict() for r in self.retiros.values()],
            "pedidos": [p.a_dict() for p in self.pedidos.values()],
            "movimientos": [m.a_dict() for m in self.movimientos],
            # Se guardan del frente al fin para respetar el orden FIFO al cargar.
            "solicitudes": [s.a_dict() for s in self.solicitudes.a_lista()],
            "cantidad_solicitudes": self.cantidad_solicitudes,
        }
        # Primero se arma todo el texto y recien despues se abre el archivo: si
        # algo no se puede escribir como JSON falla antes de tocar el archivo,
        # que no queda a medio escribir ni se pierde el guardado anterior.
        texto = json.dumps(datos, ensure_ascii=False, indent=2)
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(texto)

    @classmethod
    def cargar(cls, ruta):
        with open(ruta, encoding="utf-8") as archivo:
            datos = json.load(archivo)

        deposito = cls()
        # El orden importa: cada objeto se reconstruye despues de aquellos a
        # los que hace referencia por id.
        for d in datos["materiales"]:
            material = Material.desde_dict(d)
            deposito.materiales[material.get_id()] = material
        for d in datos["proveedores"]:
            proveedor = Proveedor.desde_dict(d)
            deposito.proveedores[proveedor.get_id()] = proveedor
        for d in datos["remesas"]:
            remesa = Remesa.desde_dict(d, deposito.materiales, deposito.proveedores)
            deposito.remesas[remesa.get_id()] = remesa
            deposito._indexar_remesa(remesa)
        for d in datos["retiros"]:
            retiro = Retiro.desde_dict(d, deposito.materiales)
            deposito.retiros[retiro.get_id()] = retiro
        for d in datos.get("pedidos", []):
            pedido = Pedido.desde_dict(d, deposito.materiales, deposito.proveedores)
            deposito.pedidos[pedido.get_id()] = pedido
        for d in datos["movimientos"]:
            remesa = deposito.remesas[d["remesa"]]
            fecha = date.fromisoformat(d["fecha"])
            if d["tipo"] == "INGRESO":
                movimiento = MovimientoIngreso(d["id"], fecha, remesa, d["cantidad"])
            else:
                retiro = deposito.retiros[d["retiro"]]
                movimiento = MovimientoRetiro(d["id"], fecha, remesa, d["cantidad"], retiro)
                retiro.agregar_movimiento(movimiento)
            deposito.movimientos.append(movimiento)
        for d in datos["solicitudes"]:
            deposito.solicitudes.encolar(SolicitudRetiro.desde_dict(d, deposito.materiales))
        # Para que los proximos SOL-n sigan la numeracion y no repitan ids.
        deposito.cantidad_solicitudes = datos["cantidad_solicitudes"]
        return deposito
