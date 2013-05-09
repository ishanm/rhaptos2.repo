#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###
# Copyright (c) Rice University 2012-13
# This software is subject to
# the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
###

"""

  * requesting_user_uri
  This is passed around a lot
  This is suboptimal, and I think should be replaced with passing around the
  environ dict as a means of linking functions with the request calling them



* Session cookie handling

  Session cookies used in repo store a random uuid, which is
  mapped to a known useruri in a lookup table on the server.

  The test-ing approach will be to send in a fixed, known cookie value
  and to then assume that the authentication and logging in has already occured
  and we are within the normal session.

  The repo will need to be able to determine the user mapped to the fixed cookie
  (again a fixed constant) and then pass that through as requesting_user

  Then session cookie will map user and place it into the environ.

  auth holds session_cookie_handler
  This runs a simple process: if a "CNXSESSIONCOOKIE" exists,
  it is extracted, the session ID is mapped to a real user and
  request.environ is updated with REMOTE_USER_URI having value like cnxuser:1234

  


Why session cookies.
Because we need some lookup mechanism. We *could* put the userID in the cookie,
but that would effectively hand over a known plain text and oracle attacks to the client.

Otehr issues

I am still passing around the userd in ``g.`` This is fairly silly
but seems consistent for flask. Will need rethink.

- secure (https) - desired future toggle
- httponly - Set on as defualt.

http://executableopinions.mikadosoftware.com/en/latest/labs/webtest-cookie/cookie_testing.html

"""

import datetime
import os
import statsd
import json
import pprint
import uuid

from rhaptos2.common.err import Rhaptos2Error
from rhaptos2.repo import get_app, dolog

import flask
from flask import request, g, session
from flaskext.openid import OpenID
import requests

from webob import Request

app = get_app()

app.config.update(
    SECRET_KEY=app.config['openid_secretkey'],
    DEBUG=app.debug
)

# setup flask-openid
oid = OpenID(app)


'''

Wanted:

onbjects to standarse the things like username lookups,
username to directory, etc etc

Tests I want to see
-------------------

* logging
* message queueing
* pygit - api



API
---

:Workspace:  a group of repos
:collection: a group of files,
             including ordering of modules
             Effectively a repo
:branch: branch of a single repo

:fork: branch of a single repo, but placed under my workspace
       github - ? clone?
:pull request: how?




ToDO:

* better CORS handling - see http://flask.pocoo.org/snippets/56/
* decorator info: http://flask.pocoo.org/docs/patterns/viewdecorators/
  http://docs.python.org/library/functools.html#functools.wraps

'''

########################
# User Auth flow
########################

### this is key found in all session cookies
CNXSESSIONID = "cnxsessionid"

### FIXME - testing purposes only
ALLZEROS = "00000000-0000-0000-0000-000000000000"
ROUSER = "00000000-0000-0000-0000-000000000001"
BADUSER = "00000000-0000-0000-0000-000000000002"


def handle_user_authentication(flask_request):
    """

    gets called before_request (which is *after* processing of HTTP headers
    but *before* __call__ on wsgi.)

    we examine the request, find session cookie,
    register any logged in user, or redirect to login pages

    """
    ### convert the cookie to a registered users details
    try:
        userdata = session_to_user(flask_request.cookies, flask_request.environ)
    except Rhaptos2Error, e:
        raise e #fixme: redirect to login should happen here

    ## We are at start of request cycle, so tell everything downstream who User is.
    if userdata:
        g.userd = userdata
        flask_request.environ['REMOTE_USER_URI'] = userdata['user_uri']
        create_session(userdata)    
    else:
        g.userd = None
        raise Rhaptos2Error("no user data, Auth ID not registerd")
    
##########################
## Session Cookie Handling
##########################
            
def session_to_user(flask_request_cookiedict, flask_request_environ):
    """
   
    >>> cookies = {"cnxsessionid": "00000000-0000-0000-0000-000000000000",}
    >>> env = {}
    >>> outenv = session_to_user(cookies, env)
    >>> outenv["REMOTE_USER"]["name"]
    'Paul'

    """
    print flask_request_cookiedict
    print flask_request_environ
    if CNXSESSIONID in flask_request_cookiedict:
        sessid = flask_request_cookiedict[CNXSESSIONID]
    else:
        raise Rhaptos2Error("NO SESSION - REDIRECT TO LOGIN")
        
    userdata = lookup_session(sessid)
    return userdata
    

def lookup_session(sessid):
    """
    We would expect this to be redis-style cache in production
    """

    onehour = datetime.timedelta(hours=1)
    d0 = datetime.datetime.utcnow()
    d1 = datetime.datetime.utcnow() + onehour
                         
    developercache = {ALLZEROS:
#                       {"interests": null, "identifiers": [{"identifierstring": "https://edwoodward.myopenid.com", "user_id": "cnxuser:75e06194-baee-4395-8e1a-566b656f6922", "identifiertype": "openid"}],
#                        "user_id": "cnxuser:75e06194-baee-4395-8e1a-566b656f6922", "suffix": null, "firstname": null, "title": null, "middlename": null, "lastname": null, "imageurl": null, "otherlangs": null, "affiliationinstitution_url": null, "email": null, "version": null, "location": null, "recommendations": null, "preferredlang": null, "fullname": "Ed Woodward", "homepage": null, "affiliationinstitution": null, "biography": null}
                       {'name': 'PaulRW',
                        'user_uri':"cnxuser:75e06194-baee-4395-8e1a-566b656f6920",
                        'id':"cnxuser:75e06194-baee-4395-8e1a-566b656f6920",
                        'starttimeUTC': d0.isoformat(),
                        'endtimeUTC': d1.isoformat(),
                       },

                      ROUSER:
                       {'name': 'Ross',
                        'user_uri':"cnxuser:75e06194-baee-4395-8e1a-566b656f6921",
                        'id':"cnxuser:75e06194-baee-4395-8e1a-566b656f6921",                        
                        'starttimeUTC': d0.isoformat(),
                        'endtimeUTC': d1.isoformat(),
                        },
                      
                      BADUSER:
                       {'name': 'BaDuSer',
                        'user_uri':"cnxuser:75e06194-baee-4395-8e1a-566b656f6922",
                        'id':"cnxuser:75e06194-baee-4395-8e1a-566b656f6922",                        
                        'starttimeUTC': d0.isoformat(),
                        'endtimeUTC': d1.isoformat(),
                       },
    }
    try:
        dolog("INFO", "We attempted to look up sessid %s in cache SUCCESS" % sessid)
        return developercache[sessid]

    except:
        dolog("INFO", "We attempted to look up sessid %s in cache FAILED" % sessid)          
        return None
        #in reality here we might want to try the redis chace or contact user server
        
def authenticated_identifier_to_registered_user_details(ai):
    """
    Given an ``authenticated_identifier (ai)`` request full user details from
    the ``user service``


    returns dict of userdetails (success),
            None (user not registerd)
            or error (user service down).
    
    """
    payload = {'user': authenticated_identifier}
    ### Fixme - the whole app global thing is annoying me now.
    user_server_url = app.config['globals'][u'userserver'].replace("/user", "/openid")

    dolog("INFO", "user info - from url %s and query string %s" %
                  (user_server_url, repr(payload)))

    try:
        r = requests.get(user_server_url, params=payload)
        userdetails = r.json()
    except Exception, e:
        #.. todo:: not sure what to do here ... the user dbase is down
        dolog("INFO", e)
        userdetails = None

    dolog("INFO", "Got back %s " % str(userdetails))
    if userdetails and r.status_code == 200:
        return userdetails
    else:
        raise Rhaptos2Error("Not a known user")

def create_session(userdata):
    """
    """
    sessionid = uuid.uuid4()
    sessionid = ALLZEROS
    def begin_session(resp):
        resp.set_cookie('cnxsessionid',sessionid)
        return resp
        
    g.deferred_callbacks.append(begin_session)
    ### Now at end of request we will call begin_session() and its closure will set sessionid correctly.
    

        
        
def after_authentication(authenticated_identifier, method):
    """Called after a user has provided a validated ID (openid or peresons)

    method either openid, or persona

    Here we have several choices:

    * User is registered
      - attempt to lookup validatedID against ``user.cnx.org service``.
      - capture the details,
      - create a sessionID
      - apply details to session-store under the sessionID
      - set-cookie with sessionid
      - redirect to rooturl
    
    
    * User is not registered
      - attempt to lookup validatedID against ``user.cnx.org service``.
      - redirect to the (TBC) ``/register/`` page
    
       
    
    """
    if method not in ('openid', 'persona'):
        raise Rhaptos2Error("Incorrect method of authenticating ID")
    
    dolog("INFO", "in after auth - %s %s" % (authenticated_identifier, method))
    userdetails = authenticated_identifier_to_registered_user_details(authenticated_identifier)
    return userdetails




def whoami():
    '''
    
    based on session cookie
    returns userd dict of user details, equivalent to mediatype from service / session
    
    '''
    return g.userd
    
    # if (HTTPHEADER_STORING_USERAUTH in request.headers
    #      and app.debug is True
    #        and 'authenticated_identifier' not in session):
    #     fakeuserauth = request.headers.get(HTTPHEADER_STORING_USERAUTH)
    #     ident = after_authentication(fakeuserauth, "openid")
    #     dolog("INFO", "FAKING USER LOGIN - %s" % fakeuserauth)
    #     return ident

    # elif 'authenticated_identifier' in session:
    #     ident = Identity(session['authenticated_identifier'])
    #     g.userID = ident.userID
    #     dolog("INFO", "Session active user is - %s" % ident.userID)
    #     return ident
    # else:
    #     callstatsd("rhaptos2.repo.notloggedin")
    #     dolog("INFO", "not headers, not session")        
    #     g.userID = None
    #     return None


## .. todo:: why is there a view in here??
@app.route("/me/", methods=['GET'])
def whoamiGET():
    '''

    returns
    Either 401 if OpenID not available or JSON document of form

    {"openid_url": "https://www.google.com/accounts/o8/id?id=AItOawlWRa8JTK7NyaAvAC4KrGaZik80gsKfe2U",  # noqa
     "email": "Not Implemented",
     "name": "Not Implemented"}

    I expect we shall want to shift to a User.JSON document...


    '''
    ### todo: return 401 code and let ajax client put up login.
    userd = whoami()

    if userd:
        jsond = asjson(userd)
        ### make decorators !!!
        resp = flask.make_response(jsond)
        resp.content_type = 'application/json'
        resp = apply_cors(resp)
        return resp
    else:
        return("Not logged in", 401)


def apply_cors(resp):
    '''  '''
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Credentials"] = "true"
    return resp


def add_location_header_to_response(fn):
    '''add Location: header

        from: http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
        For 201 (Created) responses, the Location is that of the new
        resource which was created by the request


    decorator that assumes we are getting a flask response object

    '''

    resp = fn()
    resp.headers["Location"] = "URL NEEDED FROM HASHID"


#@property ## need to evolve a class here I feel...
def userspace():
    ''' '''
    userspace = app.config['repodir']

    if os.path.isdir(userspace):
        return userspace
    else:
        try:
            os.makedirs(userspace)
            return userspace
        except Exception, e:
            raise Rhaptos2Error('cannot create repo \
                                or userspace %s - %s' % (
                                userspace, e))


def callstatsd(dottedcounter):
    ''' '''
    # Try to call logging. If not connected to a network this throws
    # "socket.gaierror: [Errno 8] nodename nor servname provided, or not known"
    try:
        c = statsd.StatsClient(app.config['globals']['statsd_host'],
                               int(app.config['globals']['statsd_port']))
        c.incr(dottedcounter)
        # todo: really return c and keep elsewhere for efficieny I suspect
    except:
        pass


def asjson(pyobj):
    '''just placeholder


    >>> x = {'a':1}
    >>> asjson(x)
    '{"a": 1}'

    '''
    return json.dumps(pyobj)


def gettime():
    return datetime.datetime.today().isoformat()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
