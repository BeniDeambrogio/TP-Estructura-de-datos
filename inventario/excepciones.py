class ErrorInventario(Exception):
    """Excepcion base de todas las excepciones propias de este sistema."""


class CantidadInvalidaError(ErrorInventario):
    """Una cantidad debia ser mayor que cero y no lo fue."""


class StockInsuficienteError(ErrorInventario):
    """No hay saldo o existencia disponible suficiente para la operacion pedida."""


class IdDuplicadoError(ErrorInventario):
    """Se intento registrar un id que ya existe en el sistema."""


class DatoFaltanteError(ErrorInventario):
    """Falta un dato obligatorio entre los argumentos opcionales (**kwargs)."""
