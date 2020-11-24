# project specific exceptions for logging and error catching
from werkzeug import exceptions as http_exceptions


class SQLNotFound(http_exceptions.NotFound):
    """Raised when can't find Setor, Quadra or Lote of project"""

    code = 404
    description = 'O setor, a quadra ou o lote não foram encontrados'

class CEPNotFound(http_exceptions.NotFound):
    """Raised when can't find Setor, Quadra or Lote of project"""

    code = 404
    description = 'O cep não foi encontrado'

class UnexpectedWebserviceResponse(http_exceptions.InternalServerError):
    """Raised when the upstream webservice behaves unexpectedly"""

    code = 500
    description = 'A webservice original se comportou de forma inesperada'