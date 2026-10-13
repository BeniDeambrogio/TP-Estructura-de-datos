import pytest

from inventario import Cola, EstructuraVaciaError, Nodo


def test_nodo_guarda_dato_y_siguiente():
    ultimo = Nodo("B")
    nodo = Nodo("A", ultimo)

    assert nodo.dato == "A"
    assert nodo.siguiente is ultimo
    assert ultimo.siguiente is None


def test_cola_nueva_esta_vacia():
    cola = Cola()

    assert cola.esta_vacia()
    assert cola.tamanio() == 0


def test_desencolar_respeta_orden_de_llegada():
    cola = Cola()
    cola.encolar("A")
    cola.encolar("B")
    cola.encolar("C")

    assert cola.desencolar() == "A"
    assert cola.desencolar() == "B"
    assert cola.desencolar() == "C"
    assert cola.esta_vacia()


def test_frente_consulta_sin_eliminar():
    cola = Cola()
    cola.encolar("A")
    cola.encolar("B")

    assert cola.frente() == "A"
    assert cola.frente() == "A"
    assert cola.tamanio() == 2


def test_desencolar_cola_vacia_lanza_estructura_vacia_error():
    with pytest.raises(EstructuraVaciaError):
        Cola().desencolar()


def test_frente_cola_vacia_lanza_estructura_vacia_error():
    with pytest.raises(EstructuraVaciaError):
        Cola().frente()


def test_vaciar_y_volver_a_encolar_funciona():
    """Si al vaciar la cola no se limpia el fin, el nuevo elemento se pierde."""
    cola = Cola()
    cola.encolar("A")
    cola.desencolar()

    cola.encolar("B")
    cola.encolar("C")

    assert cola.frente() == "B"
    assert cola.desencolar() == "B"
    assert cola.desencolar() == "C"
    assert cola.esta_vacia()


def test_a_lista_devuelve_del_frente_al_fin_sin_modificar():
    cola = Cola()
    cola.encolar("A")
    cola.encolar("B")

    assert cola.a_lista() == ["A", "B"]
    assert cola.tamanio() == 2
    assert cola.frente() == "A"
