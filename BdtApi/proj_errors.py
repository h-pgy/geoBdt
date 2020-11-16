# project specific exceptions for logging and error catching
from werkzeug import exceptions as http_exceptions


class SQLNotFound(http_exceptions.NotFound):
    """Raised when can't find Setor, Quadra or Lote of project"""

    code = 404
    description = 'O setor, a quadra ou o lote não foram encontrados'
