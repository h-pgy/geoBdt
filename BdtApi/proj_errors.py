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

class CPFouCNPJNotFound(http_exceptions.NotFound):
    """Raised when can't find CPF or CNPJ"""

    code = 404
    description = 'O CPf ou CNPJ não foi encontrado'

class ZonaUsoNotFound(http_exceptions.NotFound):
    """Raised when there are no parameters or can't found that
    specif zoning id"""

    code = 404
    description = 'A Zona de Uso não foi encontrada'

class UnexpectedWebserviceResponse(http_exceptions.InternalServerError):
    """Raised when the upstream webservice behaves unexpectedly"""

    code = 500
    description = 'A webservice original se comportou de forma inesperada'

class BDTNotFound(http_exceptions.InternalServerError):
    """Raised when there is no BDT with that ID in the database"""

    code = 404
    description = 'O BDT nao foi encontrado'

class ParametroInvalido(http_exceptions.InternalServerError):
    """Raised when a invalid parameter was given when consuming the service"""

    code = 500
    description = 'O parâmetro enviado é inválido'