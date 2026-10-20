import pytest

from inventario import Cola, EstructuraVaciaError, ListaEnlazadaOrdenada, Nodo


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


# ---------- ListaEnlazadaOrdenada ----------

def test_lista_ordenada_nueva_esta_vacia():
    lista = ListaEnlazadaOrdenada(lambda x: x)

    assert lista.esta_vacia()
    assert lista.tamanio() == 0
    assert lista.a_lista() == []


def test_lista_ordenada_primero_en_lista_vacia_lanza_estructura_vacia_error():
    lista = ListaEnlazadaOrdenada(lambda x: x)

    with pytest.raises(EstructuraVaciaError):
        lista.primero()


def test_lista_ordenada_queda_ordenada_sin_importar_el_orden_de_llegada():
    lista = ListaEnlazadaOrdenada(lambda x: x)

    for numero in (5, 1, 4, 2, 3):
        lista.insertar(numero)

    assert lista.a_lista() == [1, 2, 3, 4, 5]
    assert lista.primero() == 1
    assert lista.tamanio() == 5


def test_lista_ordenada_inserta_al_principio_en_el_medio_y_al_final():
    lista = ListaEnlazadaOrdenada(lambda x: x)
    lista.insertar(20)

    lista.insertar(10)   # antes del primero
    lista.insertar(30)   # despues del ultimo
    lista.insertar(25)   # en el medio

    assert lista.a_lista() == [10, 20, 25, 30]


def test_lista_ordenada_usa_la_clave_recibida():
    lista = ListaEnlazadaOrdenada(lambda palabra: len(palabra))

    for palabra in ("hola", "a", "casas", "ab"):
        lista.insertar(palabra)

    assert lista.a_lista() == ["a", "ab", "hola", "casas"]


def test_lista_ordenada_ante_un_empate_el_nuevo_queda_despues():
    lista = ListaEnlazadaOrdenada(lambda par: par[0])

    lista.insertar((1, "primero"))
    lista.insertar((1, "segundo"))

    assert [par[1] for par in lista.a_lista()] == ["primero", "segundo"]


def test_lista_ordenada_a_lista_no_modifica_la_lista():
    lista = ListaEnlazadaOrdenada(lambda x: x)
    lista.insertar(2)
    lista.insertar(1)

    lista.a_lista()

    assert lista.tamanio() == 2
    assert lista.primero() == 1
