import requests
import json
import urllib
import textwrap
from pyquery import PyQuery as pq

'''
PaymoAPI
========

Paymo (http://paymo.biz) is a timesheet application for
freelancers and small consulting business.

It is cloud based and it rocks my universe.

This module wraps the Paymo API (http://api.paymo.biz/docs/).

Example usage:

    >>> from paymo.api import PaymoAPI
    >>> paymo = PaymoAPI('my-paymo-api-key', 'my-username', 'my-password')
    >>> help(paymo.auth.login)
    >>> paymo.users.getList()
    >>> paymo.users.getInfo(user_id=65535)
    >>> paymo.auth.logout()

'''
INFO_CACHE = {}
DOCs = 'http://api.paymo.biz/docs/'
REQUIRED = { '0': '\n\n', '1': ' (required)\n\n'}

def make_title(s, c='='):
    return u"{0}\n{1}\n{0}\n\n".format(c * len(s), s)

def make_help(data):
    method = data['method']
    argnames = [ m['name'] for m in method['arguments']['argument']
                            if m['name'] not in ('api_key', 'auth_token') ]
    mathod_call = "{0}({1})".format(data['name'], ', '.join(argnames))
    response = u"{0}{1[description][_content]}\n\n"\
                    .format(make_title(mathod_call), method)

    if method['auth_required'] == '1':
        response += "This method requires authentication.\n\n"
    if method['admin_required'] == '1':
        response += "This method requires an administrative user.\n\n"

    if argnames:
        response += make_title("Arguments:", '-')
        for argument in method['arguments']['argument']:
            if argument['name'] in argnames:
                response += u"{0[name]}:\n    {0[_content]}{1}"\
                            .format(argument, REQUIRED[argument['required']])

    response += make_title("Errors:", '-')
    for error in method['errors']['error']:
        response += u"{0[code]}: {0[message]}\n    {0[_content]}\n\n"\
                    .format(error)

    response += u"{0}{1[example-response][_content]}"\
                    .format(make_title('Example response', '-'), method)
    return response

class PaymoAPI(object):
    """A minimal class to help with the paymo.biz API.

    Example usage:

        >>> from paymo.api import PaymoAPI
        >>> paymo = PaymoAPI('my-paymo-api-key', 'my-username', 'my-password')
        >>> help(paymo.auth.login)
        >>> paymo.users.getList()
        >>> paymo.users.getInfo(user_id=65535)
        >>> paymo.auth.logout()
    """
    _url_tmpl = 'https://api.paymo.biz/service/{method}'
    _auth_token = ''
    class DynamicApi(object):
        """Magic wrapper for API methods."""
        def __init__(self, parent, name):
            self.parent = parent
            self.name = name
        def __call__(self, *args, **kwargs):
            try:
                if self.name not in self.parent.api_method_list:
                    raise RuntimeError('Invalid method called: {0}'.format(self.name))
            except TypeError:
                print self.parent.__class__
                print self.parent.api_method_list
            r = self.parent.call_api(self.name, *args, **kwargs)
            if self.name == 'paymo.auth.login':
                try:
                    self._auth_token = r['token']['_content']
                except KeyError:
                    raise Exception(r)
            return r
        def __getattr__(self, name):
            if name == '__name__':
                return self.name
            if name.startswith('__'):
                raise AttributeError('{0} has no attribute {1}', self, name)
                return getattr(super(API, self), name)

            typename = '.'.join((self.name, name))
            info = self.parent.get_method_info(typename)
            ApiMethod = type(typename, (self.__class__,),
                             { '__doc__': info['helpstring'] })
            return ApiMethod(parent=self.parent, name=typename)

    def call_api(self, method, **params):
        """A generic call to the Paymo API."""
        params['format'] = self._format
        params['api_key'] = self._api_key
        if self._auth_token:
            params['auth_token'] = self._auth_token
        url = self._url_tmpl.format(method=method)

        r = requests.post(url, params)
        json_data = json.loads(r.text)
        return json_data

    def __init__(self, api_key, login=None, password=None, extended_info=1, fmt='json'):
        """Initialize an instance of the class with your Paymo API key
        api_key -- your Paymo API key. """
        self._api_key = api_key
        self._format = fmt
        if login:
            self.auth.login(username=login, password=password,
                                    extended_info=extended_info)
        self.api_method_list = self.get_methods()

    def __getattr__(self, name):
        """Magic stuff to map API methods."""
        if name.startswith('__'):
            return getattr(super(PaymoAPI, self), name)
        if name == 'api_method_list':
            return self.get_methods()
        return self.DynamicApi(self, '.'.join(('paymo', name)))

    def __repr__(self):
        return '<Paymo API auth={0}>'.format(self.__auth_token)

    def get_method_info(self, name):
        """Fetch help text from http://api.paymo.biz/docs/."""
        if name in INFO_CACHE:
            return INFO_CACHE[name]

        r = self.call_api('paymo.reflection.getMethodInfo', method_name=name)
        if r['status'] != 'ok':
            raise RuntimeError('Error {code}: {message}'.format(**r['error']))

        r['name'] = name
        r['helpstring'] = make_help(r)
        INFO_CACHE[name] = r
        return r

    def get_methods(self):
        r = self.call_api('paymo.reflection.getMethods')
        if r['status'] != 'ok':
            raise RuntimeError('Error {code}: {message}'.format(**r['error']))
        return [ m['_content'] for m in r['methods']['method'] ]


#if __name__ == '__main__':
#    paymo = PaymoAPI(raw_input('API Key:'), raw_input('Username:'), raw_input('password'))
#    print(paymo)

