from .excepciones import EstructuraVaciaError


class Nodo:
    """Guarda un dato y la referencia al siguiente nodo."""

    def __init__(self, dato, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente


class Cola:
    """
    Cola (FIFO) implementada con nodos.
    Se guardan el frente y el fin para que encolar y desencolar sean O(1):
    se desencola por el frente y se encola por el fin, sin recorrer los nodos.
    """

    def __init__(self):
        self._frente = None
        self._fin = None
        self._tamanio = 0

    def encolar(self, dato):
        nuevo = Nodo(dato)
        if self.esta_vacia():
            # Unico elemento: es a la vez el frente y el fin.
            self._frente = nuevo
        else:
            self._fin.siguiente = nuevo
        self._fin = nuevo
        self._tamanio += 1

    def desencolar(self):
        if self.esta_vacia():
            raise EstructuraVaciaError("La cola esta vacia")
        dato = self._frente.dato
        self._frente = self._frente.siguiente
        # Si se saco el ultimo elemento, el fin tambien tiene que quedar vacio;
        # si no, el proximo encolar se engancharia a un nodo que ya no esta.
        if self._frente is None:
            self._fin = None
        self._tamanio -= 1
        return dato

    def frente(self):
        if self.esta_vacia():
            raise EstructuraVaciaError("La cola esta vacia")
        return self._frente.dato

    def esta_vacia(self):
        return self._frente is None

    def tamanio(self):
        return self._tamanio

    def a_lista(self):
        """Devuelve los datos del frente al fin, sin modificar la cola."""
        datos = []
        actual = self._frente
        while actual is not None:
            datos.append(actual.dato)
            actual = actual.siguiente
        return datos
