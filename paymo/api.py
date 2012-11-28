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
DOC_CACHE = {}
DOCs = 'http://api.paymo.biz/docs/'

def get_help(name):
    """Fetch help text from http://api.paymo.biz/docs/."""
    if name in DOC_CACHE:
        return DOC_CACHE[name]

    r = requests.get('{0}{1}.html'.format(DOCs, name))
    if r.status_code != 200:
        return "\n".join([
            "Unable to retrieve the online help from {0}.".format(DOCs),
            "Are you sure this method exists in the API?\n\n",
        ])

    docstring = ""
    headers = ('h1', 'h2', 'h3', 'h4', 'h5', 'h6')
    for el in [ pq(c) for c in pq(r.text)('#container').children() ]:
        if el[0].tag in headers:
            level = int(el[0].tag[1])
            docstring += "\n{0} {1}\n\n".format('#' * level, el.text())
        elif el[0].tag == 'dl':
            for subel in [ pq(c) for c in el.children() ]:
                if subel[0].tag == 'dt':
                    docstring += "{0}{1}:\n".format(' ' * 4, subel.text())
                else:
                    docstring += "{0}{1}\n".format(' ' * 8, subel.text())
        else:
            for line in el.text().split('\n'):
                if line.strip():
                    line = textwrap.fill(line, 70)
                    docstring += line + '\n\n'
    DOC_CACHE[name] = docstring
    return docstring

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
    __url_tmpl = 'https://api.paymo.biz/service/{method}'
    __auth_token = ''
    class DynamicApi(object):
        """Magic wrapper for API methods."""
        def __init__(self, parent, name):
            self.parent = parent
            self.name = name
            self.__name__ = name
        def __call__(self, *args, **kwargs):
            return self.parent.call_api(self.name, *args, **kwargs)
        def __getattr__(self, name):
            if name == '__name__':
                return self.name
            if name.startswith('__'):
                raise AttributeError('{0} has no attribute {1}', self, name)
                return getattr(super(API, self), name)

            typename = '.'.join((self.name, name))
            ApiMethod = type(typename, (self.__class__,),
                             { '__doc__': get_help(typename) })
            return ApiMethod(self.parent, '.'.join((self.name, name)))

    def call_api(self, method, **params):
        """A generic call to the Paymo API."""
        params['format'] = self.__format
        params['api_key'] = self.__api_key
        if self.__auth_token:
            params['auth_token'] = self.__auth_token
        url = self.__url_tmpl.format(method=method)

        r = requests.post(url, params)
        json_data = json.loads(r.text)
        return json_data

    def __init__(self, api_key, login, password, extended_info=1, fmt='json'):
        """Initialize an instance of the class with your Paymo API key
        api_key -- your Paymo API key. """
        self.__api_key = api_key
        self.__format = fmt
        r = self.auth.login(username=login, password=password,
                                extended_info=extended_info)
        try:
            self.__auth_token = r['token']['_content']
        except KeyError:
            raise Exception(r)

    def __getattr__(self, name):
        """Magic stuff to map API methods."""
        if name.startswith('__'):
            return getattr(super(PaymoAPI, self), name)
        return self.DynamicApi(self, '.'.join(('paymo', name)))

    def __repr__(self):
        return '<Paymo API auth={0}>'.format(self.__auth_token)

    def __str__(self):
        return self.__repr__()

if __name__ == '__main__':
    paymo = PaymoAPI(raw_input('API Key:'), raw_input('Username:'), raw_input('password'))
    print(paymo)

