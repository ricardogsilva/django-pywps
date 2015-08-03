import traceback
import types
import os
from ConfigParser import ConfigParser

from django.http import HttpResponse 
from django.conf import settings
import pywps
from pywps import Soap
from pywps.Exceptions import WPSException, NoApplicableCode

def index(request):
    """
    WPS endpoint.

    This view relays the HTTP request to PyWPS, captures its response and then
    sends it back to the web server. It is inspired by the wps.py file which is
    present in PyWPS source code repository.
    """

    to_return = None
    input_query = request.META["QUERY_STRING"]
    default_content_type = "application/xml"
    if request.method == pywps.METHOD_GET and input_query == "":
        error = NoApplicableCode("No query string found")
        to_return = _write_response(str(error))
        content_type = default_content_type
    elif request.method == pywps.METHOD_GET:
        input_query = request.META["QUERY_STRING"]
    else:
        input_query = request.body
    if to_return is None:
        try:
            wps_server = pywps.Pywps(
                method=request.method,
                configFiles=(settings.PYWPS_SETTINGS_FILE,)
            )
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
                str(err),
                soap_version=wps_server.parser.soapVersion,
                is_soap=wps_server.parser.isSoap,
                is_soap_execute=wps_server.parser.isSoapExecute
            )
            content_type = default_content_type
    return HttpResponse(to_return, content_type=content_type)

def get_status_report(request, file_name):
    """
    Return the WPS status report that is automatically generated by PyWPS when
    executing processes asynchronously.
    """

    content_type = "application/xml"
    c = ConfigParser()
    c.read(settings.PYWPS_SETTINGS_FILE)
    pywps_output_path = c.get("server", "outputpath")
    file_path = os.path.join(pywps_output_path, file_name)
    response = HttpResponse(content_type=content_type)
    with open(file_path) as fh:
        for line in fh:
            response.write(line)
    return response

def _write_response(response, soap_version=None, is_soap=False,
                    is_soap_execute=False,
                    is_promote_status=False):
    """
    A replacement for pywps.response.response that composes the response 
    into a string instead of a file object.
    """

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
