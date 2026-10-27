import json
from datetime import date
from decimal import Decimal

import pytest

from inventario import Deposito


def _deposito_con_operaciones():
    deposito = Deposito()
    aluminio = deposito.registrar_material("AL-01", "Aluminio AL-01", "kg", 10)
    cobre = deposito.registrar_material("CU-01", "Cobre CU-01", "kg", 5)
    proveedor = deposito.registrar_proveedor("P-1", "Metales SA", 5)
    deposito.crear_remesa("R-101", aluminio, proveedor, 8,
                           fecha_recepcion=date(2026, 3, 2), fecha_vencimiento=date(2026, 3, 20), lote="L-7")
    deposito.crear_remesa("R-102", aluminio, proveedor, 12,
                           fecha_recepcion=date(2026, 3, 4), fecha_vencimiento=date(2026, 3, 30))
    deposito.crear_remesa("R-201", cobre, proveedor, 6, fecha_recepcion=date(2026, 3, 5))
    deposito.retirar(aluminio, 10, date(2026, 3, 10))  # consume R-101 entera y 2 de R-102
    deposito.solicitar_retiro(aluminio, 50, date(2026, 3, 11))
    deposito.solicitar_retiro(cobre, 2, date(2026, 3, 11))
    return deposito


def _guardar_y_cargar(deposito, tmp_path):
    ruta = tmp_path / "deposito.json"
    deposito.guardar(ruta)
    return Deposito.cargar(ruta)


def test_guardar_genera_un_json_legible(tmp_path):
    ruta = tmp_path / "deposito.json"

    _deposito_con_operaciones().guardar(ruta)

    with open(ruta, encoding="utf-8") as archivo:
        datos = json.load(archivo)
    assert [m["id"] for m in datos["materiales"]] == ["AL-01", "CU-01"]
    assert datos["remesas"][0]["material"] == "AL-01"
    assert datos["remesas"][0]["fecha_vencimiento"] == "2026-03-20"
    assert datos["remesas"][2]["fecha_vencimiento"] is None


def test_cargar_restaura_materiales_proveedores_y_remesas(tmp_path):
    cargado = _guardar_y_cargar(_deposito_con_operaciones(), tmp_path)

    assert set(cargado.get_materiales()) == {"AL-01", "CU-01"}
    assert cargado.get_proveedores()["P-1"].get_plazo_entrega_dias() == 5
    r101 = cargado.get_remesas()["R-101"]
    assert r101.get_saldo_disponible() == 0
    assert r101.get_fecha_vencimiento() == date(2026, 3, 20)
    assert r101.obtener_dato("lote") == "L-7"
    assert cargado.get_remesas()["R-102"].get_saldo_disponible() == 10


def test_cargar_reconstruye_referencias_al_mismo_objeto(tmp_path):
    cargado = _guardar_y_cargar(_deposito_con_operaciones(), tmp_path)

    aluminio = cargado.get_materiales()["AL-01"]
    assert cargado.get_remesas()["R-101"].get_material() is aluminio
    assert cargado.get_remesas()["R-102"].get_material() is aluminio


def test_cargar_restaura_existencias_e_indice_por_material(tmp_path):
    original = _deposito_con_operaciones()
    cargado = _guardar_y_cargar(original, tmp_path)

    for id_material in ("AL-01", "CU-01"):
        assert (cargado.existencia_fisica(cargado.get_materiales()[id_material])
                == original.existencia_fisica(original.get_materiales()[id_material]))
    aluminio = cargado.get_materiales()["AL-01"]
    assert [r.get_id() for r in cargado.remesas_de_material(aluminio)] == ["R-101", "R-102"]


def test_cargar_restaura_movimientos_y_trazabilidad(tmp_path):
    cargado = _guardar_y_cargar(_deposito_con_operaciones(), tmp_path)

    assert [m.tipo() for m in cargado.get_movimientos()] == ["INGRESO", "INGRESO", "INGRESO", "RETIRO", "RETIRO"]
    retiro = cargado.get_retiros()["RET-1"]
    assert retiro.cantidad_consumida() == 10
    assert [r.get_id() for r in cargado.remesas_de_retiro(retiro)] == ["R-101", "R-102"]
    assert cargado.retiros_de_remesa(cargado.get_remesas()["R-102"]) == [retiro]


def test_cargar_respeta_el_orden_de_la_cola(tmp_path):
    cargado = _guardar_y_cargar(_deposito_con_operaciones(), tmp_path)

    assert cargado.solicitudes_pendientes() == 2
    assert [s.get_id() for s in cargado.get_solicitudes().a_lista()] == ["SOL-1", "SOL-2"]


def test_despues_de_cargar_los_ids_continuan_sin_repetirse(tmp_path):
    cargado = _guardar_y_cargar(_deposito_con_operaciones(), tmp_path)
    cobre = cargado.get_materiales()["CU-01"]

    solicitud = cargado.solicitar_retiro(cobre, 1, date(2026, 3, 12))
    retiro = cargado.retirar(cobre, 1, date(2026, 3, 12))

    assert solicitud.get_id() == "SOL-3"
    assert retiro.get_id() == "RET-2"
    assert cargado.get_movimientos()[-1].get_id() == "MOV-6"


def test_deposito_vacio_se_guarda_y_carga(tmp_path):
    cargado = _guardar_y_cargar(Deposito(), tmp_path)

    assert cargado.get_materiales() == {}
    assert cargado.solicitudes_pendientes() == 0


# ---------- Datos adicionales (**kwargs) que JSON no sabe escribir ----------

def test_guardar_convierte_a_texto_los_kwargs_que_json_no_sabe_escribir(tmp_path):
    deposito = Deposito()
    material = deposito.registrar_material("AL-01", "Aluminio AL-01", "kg", 10)
    proveedor = deposito.registrar_proveedor("P-1", "Metales SA", 5)
    deposito.crear_remesa("R-1", material, proveedor, 8, fecha_recepcion=date(2026, 3, 2),
                           fecha_fabricacion=date(2026, 1, 15), temperatura=Decimal("4.5"), lote="L-7", turno=2)

    cargado = _guardar_y_cargar(deposito, tmp_path)

    remesa = cargado.get_remesas()["R-1"]
    assert remesa.obtener_dato("fecha_fabricacion") == "2026-01-15"
    assert remesa.obtener_dato("temperatura") == "4.5"
    assert remesa.obtener_dato("lote") == "L-7"
    assert remesa.obtener_dato("turno") == 2


def test_guardar_que_falla_no_deja_el_archivo_a_medio_escribir(tmp_path):
    ruta = tmp_path / "deposito.json"
    deposito = Deposito()
    material = deposito.registrar_material("AL-01", "Aluminio AL-01", "kg", 10)
    proveedor = deposito.registrar_proveedor("P-1", "Metales SA", 5)
    remesa = deposito.crear_remesa("R-1", material, proveedor, 8, fecha_recepcion=date(2026, 3, 2))
    deposito.guardar(ruta)
    contenido_bueno = ruta.read_text(encoding="utf-8")

    remesa.datos_adicionales[(1, 2)] = "una clave que JSON no puede escribir"
    with pytest.raises(TypeError):
        deposito.guardar(ruta)

    assert ruta.read_text(encoding="utf-8") == contenido_bueno
    assert Deposito.cargar(ruta).get_remesas()["R-1"].get_cantidad_recibida() == 8


# ---------- Pedidos ----------

def test_guardar_y_cargar_restauran_los_pedidos_con_su_precio_exacto(tmp_path):
    deposito = _deposito_con_operaciones()
    proveedor = deposito.get_proveedores()["P-1"]
    aluminio = deposito.get_materiales()["AL-01"]
    pedido = deposito.crear_pedido("PED-1", proveedor)
    pedido.agregar_renglon(aluminio, 20, Decimal("3.50"))
    pedido.agregar_renglon(aluminio, 3, Decimal("0.10"))

    cargado = _guardar_y_cargar(deposito, tmp_path)

    recuperado = cargado.get_pedidos()["PED-1"]
    assert recuperado.get_proveedor() is cargado.get_proveedores()["P-1"]
    assert recuperado.get_renglones()[0].get_material() is cargado.get_materiales()["AL-01"]
    assert recuperado.get_renglones()[1].get_precio_unitario() == Decimal("0.10")
    assert recuperado.importe_total() == pedido.importe_total() == Decimal("70.30")


def test_cargar_un_json_sin_pedidos_sigue_funcionando(tmp_path):
    ruta = tmp_path / "deposito.json"
    _deposito_con_operaciones().guardar(ruta)
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    del datos["pedidos"]
    ruta.write_text(json.dumps(datos), encoding="utf-8")

    cargado = Deposito.cargar(ruta)

    assert cargado.get_pedidos() == {}
    assert set(cargado.get_materiales()) == {"AL-01", "CU-01"}


# ---------- Indice ordenado ----------

def test_cargar_mantiene_el_orden_fefo_de_las_remesas_registradas_desordenadas(tmp_path):
    deposito = Deposito()
    material = deposito.registrar_material("AL-01", "Aluminio AL-01", "kg", 10)
    proveedor = deposito.registrar_proveedor("P-1", "Metales SA", 5)
    deposito.crear_remesa("R-103", material, proveedor, 15, fecha_recepcion=date(2026, 3, 5))
    deposito.crear_remesa("R-101", material, proveedor, 8,
                           fecha_recepcion=date(2026, 3, 2), fecha_vencimiento=date(2026, 3, 20))

    cargado = _guardar_y_cargar(deposito, tmp_path)

    aluminio = cargado.get_materiales()["AL-01"]
    assert [r.get_id() for r in cargado.remesas_de_material(aluminio)] == ["R-101", "R-103"]


def test_cargar_reconstruye_el_set_de_ids_de_remesas_de_cada_retiro(tmp_path):
    cargado = _guardar_y_cargar(_deposito_con_operaciones(), tmp_path)

    assert cargado.get_retiros()["RET-1"].ids_de_remesas() == {"R-101", "R-102"}


def test_remesas_sin_usar_se_conserva_al_guardar_y_cargar(tmp_path):
    original = _deposito_con_operaciones()
    cargado = _guardar_y_cargar(original, tmp_path)

    assert [r.get_id() for r in original.remesas_sin_usar()] == ["R-201"]
    assert [r.get_id() for r in cargado.remesas_sin_usar()] == ["R-201"]
