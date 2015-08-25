# Paymo API Wrapper for Python

This module wraps the Paymo API. It has some nice features:

  - the API methods are dynamically generated using reflection, 
    so any future API method will be automatically added
  - the calls are identical, but you can omit the credentials 
    for convenience
  - the docstrings for the methods are also generated using
    reflection, so you can `help(paymo.group.method)`

## What is Paymo?

Paymo is cloud based application for tracking your time and invoice
your clients. Before I started using it, I was constantly forgetting
to bill some customer for some of my time, so it rocks my universe. 
It is a must-have for freelancers, contractors and consulting business.

If you want to give it a check, use my referal link (shameless plug):

  - [http://www.paymo.biz/](http://www.paymo.biz/?utm_source=7b76bTP02Xee)

It is free for 1 user and if you are using Google Apps for your domain,
it integrates very nicely.

## Install

It is in the chese shop, so just easy_instal or pip it.

    pip install paymo
    
## Contribute

Just fork it and send pull requests.

## Example Usage

Just initialize the API with your credentials and call tha API
methods as standard python methods feeding parameters by name.

Method and parameter names are the same documented at:

  - [http://api.paymo.biz/docs/](http://api.paymo.biz/docs/)

Example:

    >>> from paymo import api
    >>> paymo = PaymoAPI('my-paymo-api-key', 'my-username', 'my-password')
    >>> # Now you can call apy methods like native python methods
    >>> paymo.users.getList()
    {u'status': u'ok',
     u'users': {u'user': [{u'active': 1,
                           u'id': u'65535',
                           u'realname': u'Enoch Root',
                           u'username': u'root@eruditorum.org'},
                          {u'active': 1,
                           u'id': u'65534',
                           u'realname': u'Thomas A. Anderson',
                           u'username': u'neo@matrix.com'}]}}
    
    >>> # you can even call help
    >>> help(paymo.users.getList)
    Help on paymo.users.getList in paymo.users object:

    class paymo.users.getList(DynamicApi)
     |  ## paymo.users.getList
     |  
     |  Get a list of users from the same company as the authenticated user's
     |  company.
     |  
     |  
     |  ### Authentication
     |  
     |  This method requires authentication .
     |  
     |  
     |  ### Arguments
     |  
     |      api_key (Required):
     |          Your application key. See here for more details.
     |      auth_token (Required):
     |          Authentication token received upon login.
     |  
     |  ### Example Response
     |  
     |  <?xml version="1.0" encoding="UTF-8"?>
     |  <response status="ok">
     |          <users>
     |                  <user id="1279" username="johndoe" realname="John Doe" active="1" />
     |                  <user id="1283" username="marydoe" realname="Mary Doe" active="0" />
     |          </users>
     |  </response>
     |  
     |  
     |  ### Error Codes
     |  
     |      101: Unknown API method:
     |          The requested method was not found.
     |      102: Unknown response format:
     |          The requested response format was not found.
     |      103: Invalid API Key:
     |          The API key passed was not valid.
     |      104: Invalid auth token / Login failed:
     |          The login details or auth token passed were invalid.
     |      105: Insufficient permissions:
     |          The user making the method call did not have the required permissions.
     |      106: Service currently unavailable:
     |          The service is temporarily unavailable.
     |      107: Too many requests for this API key:
     |          The application has reached the limit for number of API calls during a 
     |          specific time period. Wait a bit and try again.
     |
    >>> paymo.auth.logout()

## Contribute

  - Just keep the PRs flowing.
