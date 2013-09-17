import re
from django import http
from urlparse import urlparse
from django.conf import settings


ACCESS_CONTROL_ALLOW_ORIGIN = 'Access-Control-Allow-Origin'
ACCESS_CONTROL_EXPOSE_HEADERS = 'Access-Control-Expose-Headers'
ACCESS_CONTROL_ALLOW_CREDENTIALS = 'Access-Control-Allow-Credentials'
ACCESS_CONTROL_ALLOW_HEADERS = 'Access-Control-Allow-Headers'
ACCESS_CONTROL_ALLOW_METHODS = 'Access-Control-Allow-Methods'
ACCESS_CONTROL_MAX_AGE = 'Access-Control-Max-Age'


class CorsMiddleware(object):
    '''
        Adapted from https://github.com/ottoyiu/django-cors-headers
    '''

    def process_request(self, request):
        '''
            If CORS preflight header, then create an empty body response (200 OK) and return it

            Django won't bother calling any other request view/exception middleware along with
            the requested view; it will call any response middlewares
        '''
        if (self.is_enabled(request) and
            request.method == 'OPTIONS' and
            'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META):
            response = http.HttpResponse()
            return response
        return None

    def process_response(self, request, response):
        '''
            Add the respective CORS headers
        '''
        origin = request.META.get('HTTP_ORIGIN')
        if self.is_enabled(request) and origin:

            response[ACCESS_CONTROL_ALLOW_ORIGIN] = origin

            if request.method == 'OPTIONS':
                response[ACCESS_CONTROL_ALLOW_HEADERS] = 'X-Requested-With'
                response[ACCESS_CONTROL_ALLOW_METHODS] = 'POST'

        return response

    def is_enabled(self, request):
        return re.match(settings.CORS_URLS_REGEX, request.path)