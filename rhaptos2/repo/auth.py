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

from rhaptos2.repo.err import Rhaptos2Error, Rhaptos2NoSessionCookieError
from rhaptos2.repo import get_app, dolog, sessioncache

import flask
from flask import request, g, session, redirect
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

########################
# User Auth flow
########################

### this is key found in all session cookies
### It is hardcoded here not config.
CNXSESSIONID = "cnxsessionid"


def handle_user_authentication(flask_request):
    """Correctly perform all authentication workflows
    
    This gets called before_request (which is *after* processing of HTTP headers
    but *before* __call__ on wsgi.)

    All the functions in sessioncache, and auth, should be called from here
    (maybe in a chain) and raise errors or other signals to allow this function
    to take action, not to presume on some action (like a redirect)
    themselves. (todo-later: such late decisions are well suited for deferred
    callbacks)

    The flow (state diagram later)

    A. Registered User
    B. Temp-Registered User
    C. UnRegistered User

    1. User with valid cookie
    2. User with no cookie / invalid cookie
    
    A.2. A user who has previously registered but has a expired cookie or cleared cache.

    Arrives at /
    
    

    we examine the request, find session cookie,
    register any logged in user, or redirect to login pages


    1. If no session cookie provided (ie browser never visited us)
       -> Create a temporary session id and temporary user.
    2. If session cookie provided but the lookup fails (out of date?)
       -> they have visited before, redirect to login with "session expired"
    3. If session cookie provided, and lookup is ok,
       -> return the ``user_dict`` and let auth-flow take care of it

    """
    ### convert the cookie to a registered users details
    try:
        userdata = session_to_user(flask_request.cookies, flask_request.environ)
    except Rhaptos2NoSessionCookieError, e:
        return redirect("/login_greeting")
        #We end here for now - later we shall fix tempsessions
        #userdata = set_temp_session()
        
    ## We are at start of request cycle, so tell everything downstream who User is.
    if userdata is not None:
        userdata['user_uri'] = userdata['user_id']
        g.userd = userdata
        flask_request.environ['REMOTE_USER_URI'] = userdata['user_uri']
    else:
        g.userd = None
        raise Rhaptos2Error("no user data, Auth ID not registerd - redirerct to login")
    
##########################
## Session Cookie Handling
##########################
            
def session_to_user(flask_request_cookiedict, flask_request_environ):
    """
   
    >>> cookies = {"cnxsessionid": "00000000-0000-0000-0000-000000000000",}
    >>> env = {}
    >>> userd = session_to_user(cookies, env)
    >>> outenv["fullname"]
    'pbrian'

    Returns: Err, None if lookup fails, userdict if not

    todo: I prefer having failure to lookup also raise err.
    """
    if CNXSESSIONID in flask_request_cookiedict:
        sessid = flask_request_cookiedict[CNXSESSIONID]
    else:
        raise Rhaptos2NoSessionCookieError("NO SESSION - REDIRECT TO LOGIN")
    userdata = lookup_session(sessid)
    return userdata
    

def lookup_session(sessid):
    """
    We would expect this to be redis-style cache in production

    returns python dict of ``user_dict`` format.
            or None if no session ID in cache
            or Error if lookup failed for other reason.
    
    """
    dolog("INFO", "begin look up sessid %s in cache" % sessid)
    try:
        userd = sessioncache.get_session(sessid)
        dolog("INFO", "we got this from session lookup %s" % str(userd))
        if userd:
            dolog("INFO", "We attempted to look up sessid %s in cache SUCCESS" % sessid)
            return userd
        else:
            dolog("INFO", "We attempted to look up sessid %s in cache FAILED" % sessid)
            return None
    except Exception, e:
        dolog("INFO", "We attempted to look up sessid %s in cache FAILED with Err %s" % (sessid, str(e)))        
        raise e
    
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
    discuss: do we expire this?
    do we limit domain?
    """
    sessionid = str(uuid.uuid4())
    def begin_session(resp):
        resp.set_cookie('cnxsessionid',sessionid,
                        httponly=True)
        return resp
        
    g.deferred_callbacks.append(begin_session)
    sessioncache.set_session(sessionid, userdata)
    
    ### Now at end of request we will call begin_session() and its closure will set sessionid correctly.
    
def set_temp_session():
    """
    Need to create_user in user service.
    - this functionality is stubbed for now
    """
    useruri = create_temp_user("temporary", "http:/openid.cnx.org/%s" % str(uuid.uuid4()))
    tempuserdict = {'fullname':"temporary user", 'user_id':useruri}
    create_session(tempuserdict)
    return tempuserdict

    
def create_temp_user(identifiertype, identifierstring):
    """
    We should ping to user service and create a temporary userid
    linked to a made up identifier.  This can then be linked to the
    unregistered user when they finally register.

    

    FIXME - needs to actually talk to userservice.
    THis is however a asynchronous problem, solve under session id
    """
    ### vist the user dbase, get back a user_uri
    stubbeduri = "cnxuser:" + str(uuid.uuid4())
    return stubbeduri
        
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
    if method not in ('openid', 'persona', 'temporary'):
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
