import datetime
import functools
from models import BdtRequestLog, db
from .custom_transports import LoggerTransport

def log_request(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        self = args[0]

        if self.log_requests == True:
            client = kwargs.get('client')
            agora = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
            if type(client.transport) is LoggerTransport:
                result = func(*args, **kwargs)
                bdt_log = BdtRequestLog(
                    request_headers = client.transport.request_headers,
                    request_xml = client.transport.xml_request,
                    response_xml = client.transport.xml_response,
                    request_datetime = agora,
                    bdt_id = self.bdt_id
                )
                print('HEADERS')
                print(client.transport.request_headers)
                print('REQUEST')
                print(client.transport.xml_request)
                print('RESPONSE')
                print(client.transport.xml_response)
                db.session.add(bdt_log)
                db.session.commit()
                return result

            else:
                raise RuntimeError('For logging must use LoggerTransport on zeep client ')

        result = func(*args, **kwargs)
        return result

    return wrapper