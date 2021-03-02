from requests import Session
from requests.packages import urllib3
from zeep import Client
from zeep.cache import InMemoryCache
from zeep import Settings
import functools
from .config import p_pwd_cac,p_usr_cac, wsdl_path_intra
from .custom_transports import LoggerTransport


def create_client_intranet(auth_headers, wsdl_path_intra, cache = True, cache_timeout = 60):
    '''Creates client for working in PMSP intranet envirnoment.
    Must use intranet wsdl path'''

    # must set up transport for working inside intranet env
    session = Session()
    session.trust_env = False
    session.trust_env = False
    session.verify = False
    # disabling annoying https warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    settings = Settings(extra_http_headers=auth_headers,
                        force_https=False)
    if cache:
        cache = InMemoryCache(cache_timeout)
        client = Client(wsdl_path_intra,
                        transport=LoggerTransport(session=session, cache = cache),
                        settings=settings)
    else:
        client = Client(wsdl_path_intra,
                        transport=LoggerTransport(session=session),
                        settings=settings)
    return client

auth_headers = {
    'p_pwd_cac': p_pwd_cac,
    'p_usr_cac': p_usr_cac,
    'IdTransacao': 'BDT'
}

def create_client(auth_headers=auth_headers,
                  create_client_function=create_client_intranet,
                  wsdl_path = wsdl_path_intra):
    '''Decorator to create soap client. The auth headers and create client function
    parameters should be changed in order to use module in other environments. The
    default parameters are for working inside PMSP intranet on homolog env'''

    def create_client_decor(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            self = args[0]
            client =self.client or create_client_function(auth_headers, wsdl_path)

            result = func(*args, client=client, **kwargs)

            return result

        return wrapper

    return create_client_decor
