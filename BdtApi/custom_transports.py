from zeep import transports


class LoggerTransport(transports.Transport):
    """Override used to make the raw request and response XML acessible"""
    def post(self, address, message, headers):
        self.xml_request = message.decode('utf-8')
        self.request_headers = str(headers)
        response = super().post(address, message, headers)
        self.xml_response = response.text

        return response