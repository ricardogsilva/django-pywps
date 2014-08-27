import traceback
import types

from django.http import HttpResponse 
from django.conf import settings
import pywps
from pywps import Soap
from pywps.Exceptions import WPSException, NoApplicableCode

def index(request):
    '''
    WPS endpoint.
    '''

    to_return = None
    input_query = request.META['QUERY_STRING']
    if request.method == pywps.METHOD_GET and input_query == '':
        error = NoApplicableCode('No query string found')
        to_return = _write_response(error)
        content_type = 'text/plain'
    elif request.method == pywps.METHOD_GET:
        input_query = request.META['QUERY_STRING']
    else:
        input_query = request.body
    if to_return is None:
        try:
            wps_server = pywps.Pywps(method=request.method, 
                                     configFiles=(settings.PYWPS_SETTINGS_FILE,))
            if wps_server.parseRequest(input_query):
                pywps.debug(wps_server.inputs)
                wps_response = wps_server.performRequest()
                if wps_response:
                    to_return = _write_response(
                        wps_server.response,
                        soap_version=wps_server.parser.soapVersion,
                        is_soap=wps_server.parser.isSoap,
                        is_soap_execute=wps_server.parser.isSoapExecute
                    )
                    content_type = wps_server.request.contentType
        except WPSException as err:
            traceback.print_exc(file=pywps.logFile)
            to_return = _write_response(
                err,
                soap_version=wps_server.parser.soapVersion,
                is_soap=wps_server.parser.isSoap,
                is_soap_execute=wps_server.parser.isSoapExecute
            )
            content_type = 'application/xml'
    return HttpResponse(to_return, content_type=content_type)

def _write_response(response, soap_version=None, is_soap=False,
                    is_soap_execute=False,
                    is_promote_status=False):
    '''
    A replacement for pywps.response.response that composes the response 
    into a string instead of a file object.
    '''

    if is_soap:
        soap = Soap.SOAP()
        response = soap.getResponse(response, soap_version, is_soap_execute,
                                    is_promote_status)
    if isinstance(response, WPSException):
        response = response.__str__
    if type(response) == types.FileType:
        result = response.read()
    else:
        result = response
    return result
