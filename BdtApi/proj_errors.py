# project specific exceptions for logging and error catching

class SQLNotFound(ValueError):
    """Raised when can't find Setor, Quadra or Lote of project"""
    pass