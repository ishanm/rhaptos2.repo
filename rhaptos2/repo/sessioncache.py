#!/usr/bin/env python
#! -*- coding: utf-8 -*-

### Copyright Rice University

# This program is licensed under the terms of the
# GNU General Affero License version 3 (or later).  Please see
# LICENSE.txt for details

###

""":author:  paul@mikadosoftware.com <Paul Brian>

session-cache: This is a one module solution, proving ability for
               a web-app to get, set and delete a session marker on a client
               It is intended to be used by :mod:`auth.py` which controls the
               flow of authentication decisions made during request processing.

Why? Because I was getting confused with lack of fine control over sessions
and because the Flask implementation relied heavily on encryption which
seems to be the wrong direction.
So we needed a server-side session cookie impl. with fairly fine control.

I intend to replace the existing SqlAlchemy based services
with pure psycopg2 implementations, but for now I will be content
not adding another feature to SA

Session Cache
-------------

The session cache needs to be a fast, distributed lookup system for
matching a random ID to a dict of user details.

We shall store the user details in the tabl;e session_cache




Discussion on merits of cache architecture
------------------------------------------

Caches are hard.  They need to be very very fast, and in this case
distributable.  Distributed caches are very very hard because we need to ensure
they are synched.

I feel redis makes an excellent cache choice in many circumstances - it is
blazingly fast for key-value lookups, it is simple, it is threadsafe (as in
threads in the main app do not maintain any pooling or thread issues other than
opening a socket or keeping it open) and it has decent synching options.

However the synching is serious concern, and as such using a centralised, fast,
database will allow us to move to production with a secure solution, without the
immediate reliance on cache-invalidation strategies.


Overview
--------

We have one single table, ``session_cache``.  This stores a json string (as a string, not 9.3 JSON type)
as value in a key value pair.  The key is a UUID-formatted string, passed in from the application.
It is expected we will never see a collission.

We have three commands:

* :meth:`set_session`

* :meth:`get_session`

* :meth:`delete_session`

With this we can test the whole lifecyle as below



Example Usage
-------------

We firstly pass in a badly formed id.

>>> sid = "Dr. Evil"
>>> get_session(sid)
Traceback (most recent call last):
     ... 
Rhaptos2Error: Incorrect UUID format for sessionid...

OK, now lets use a properly formatted (but unlikely) UUID

>>> sid = "00000000-0000-0000-0000-000000000001"
>>> set_session(sid, {"name":"Paul"})
True
>>> userd = get_session(sid)
>>> print userd[0]
00000000-0000-0000-0000-000000000001
>>> delete_session(userd[0])


To do
-----

* greenlets & conn pooling
* wrap returned recordset in dict.
* pg's UUID type?




Error cases::
   * SessionID already exists
   * SessionID has been used before
   * Invalid format of sessionID

Create stmts
------------

CREATE TABLE session_cache(
   sessionid  character varying NOT NULL,
   userdict   character varying NOT NULL,
   session_startUTC timestamptz,
   session_endUTC timestamptz
);

ALTER TABLE ONLY session_cache
    ADD CONSTRAINT session_cache_pkey PRIMARY KEY (sessionid);


Standalone usage
----------------
d = {'host':'127.0.0.1', 'user':'repo', 'passwd':'repopass', 'dbase':'dbtest'}


"""
import psycopg2
import json
import datetime
from err import Rhaptos2Error,  Rhaptos2NoSessionCookieError
from rhaptos2.repo  import dolog

#### I do not think this is suitable for configuring in usual channel.
#### (set to one hour for now)
FIXEDSESSIONDURATIONSECS = 3600
DT = datetime.timedelta(seconds=FIXEDSESSIONDURATIONSECS)
CONFD = {}# module level global to be setup



def set_config(confd):
    """
    """
    global CONFD
    CONFD.update(confd)
    

def validate_uuid_format(uuidstr):
    """
    Given a string, try to ensure it is of type UUID.
    
    
    >>> validate_uuid_format("75e06194-baee-4395-8e1a-566b656f6920")
    True
    >>> validate_uuid_format("FooBar")
    False
    
    """
    l =  uuidstr.split("-")
    res = [len(item) for item in l]
    if not res == [8,4,4,4,12]:
        return False
    else:
        return True

def getconn():
    """
    Connection pooling required, but want to use a greenlet-aware pool, but until finish testing
    not pooling at all will suffice.

    We do not want the ThreadedPool here, as it is designed for
    "real" threads, and listens to their states.
    
    http://initd.org/psycopg/docs/pool.html

    We want a pool that will relinquish control back using gevent calls
    https://bitbucket.org/denis/gevent/src/5f6169fc65c9/examples/psycopg2_pool.py - see surfly in github.
    """
    try:
        conn = psycopg2.connect(host=CONFD['pghost'],
                                database=CONFD['pgdbname'],
                                user=CONFD['pgusername'],
                                password=CONFD['pgpassword'])
    except psycopg2.Error, e:
        pass
        
    return conn
    

def run_query(insql, params):
    """
    Running a query, avoiding the idle transaction costs.


    run_query(conn, "SELECT * FROM tbl where id = %s;", (15,))
    todo: write the usual dict return stuff and object return stuff.

    issues: lots.  No fetch_iterator. connection per query(see above)
                   
    """
    conn = getconn()
    cur = conn.cursor()
    cur.execute(insql, params)
    rs = cur.fetchall()
    cur.close()
    #connection_refresh(conn)  #I can rollback here, its a SELECT
    return rs
    
def exec_stmt(insql, params):
    """
    Running a query, avoiding the idle transaction costs.


    run_query(conn, "SELECT * FROM tbl where id = %s;", (15,))
    todo: write the usual dict return stuff and object return stuff.

    FixMe: Write up all adge case handling here. 
    """
    conn = getconn()
    cur = conn.cursor()
    cur.execute(insql, params)
    conn.commit() 
    cur.close()
    #connection_refresh(conn)  #I can rollback here, its a SELECT
    conn.close()
    
def connection_refresh(conn):
    """
    As a default psycopg2 will wrap every sql stmt in a transaction,
    and so we can easily leave the system in idle-wait transactions.

    1. refresh by running commit / rollback
    2. refresh by replacing in pool using thread-approrpiate calls
    """
    conn.rollback()


def set_session(sessionid, userd):
    """
    Given a sessionid (generated according to ``cnxsessionid spec`` elsewhere)
    and a ``userdict`` store in session cache with appropriate timeouts.

    TIMESTAMPS.
    We are comparing the time now, with the expirytime of the cookie *in the database*
    This reduces the portability.

    This beats the previous solution of passing in python formatted UTC and then comparing
    on database.

    FIXME: bring comaprison into python.
    """
    if not validate_uuid_format(sessionid):
        raise Rhaptos2Error("Incorrect UUID format for sessionid %s" % sessionid)
        
    SQL = """INSERT INTO session_cache (sessionid
                                        , userdict
                                        , session_startutc
                                        , session_endutc)
             VALUES                    (%s
                                        , %s
                                        , CURRENT_TIMESTAMP
                                        , CURRENT_TIMESTAMP + INTERVAL '%s SECONDS');"""
    try:
        exec_stmt(SQL, [sessionid,
                        json.dumps(userd),
                        FIXEDSESSIONDURATIONSECS
                       ])
    except psycopg2.IntegrityError, e :
        ### This should never happen, but does in testing enough to trap.
        ### if it does, I guess the session is underattack, close it
        delete_session(sessionid)
        raise Rhaptos2Error(str(e))
    return True

def delete_session(sessionid):
    """
    Remve from session_cache an existing but no longer wanted session(id)
    
    for whatever reason we want to end a session.
    """
    if not validate_uuid_format(sessionid):
        raise Rhaptos2Error("Incorrect UUID format for sessionid %s" % sessionid)
    SQL = """DELETE FROM session_cache WHERE sessionid = %s;"""
    try:
        exec_stmt(SQL, [sessionid])
    except psycopg2.IntegrityError, e :
        ### Why did we try to close a non-existent session?
        raise Rhaptos2Error(str(e))
    
def get_session(sessionid):
    """
    Given a sessionid, if it exists, and is "in date" then
       return userdict (oppostie of set_session)
    
    Otherwise return None
    (We do not error out on id not found)

    NB this depends heavily on co-ordinating the incoming TZ of 
    """
    if not validate_uuid_format(sessionid):
        raise Rhaptos2Error("Incorrect UUID format for sessionid %s" % sessionid)
    dolog("INFO", "lookup %s type %s" % (sessionid, type(sessionid)))
          
    SQL = """SELECT userdict FROM session_cache WHERE sessionid = %s
             AND CURRENT_TIMESTAMP BETWEEN
                  session_startutc AND session_endutc;"""
    rs = run_query(SQL, [sessionid,])
    if len(rs) != 1:
        return None
    else:
        return json.loads(rs[0][0])
    

def _fakesessionusers(sessiontype='fixed'):
    """a mechainsims to help with testing.
    :param:`sessiontype` can be either ``floating`` or ``fixed``
    
    ``fixed`` will set three sessionids of type all zeros + 1 / 2 and assign
    them three test users as below

    ``floating`` will randomly choose a "normal" uuid, and will always set
    edwoodward and will then have ed as a "real logged in user".  THis is
    expected to be for testing without faking openid logins.


    usage:
>> import sessioncache, json
>> userd = sessioncache.get_session("00000000-0000-0000-0000-000000000002")
>>> userd.keys()
[u'interests', u'user_id', u'suffix', u'firstname', u'title', u'middlename', u'lastname', u'imageurl', u'identifiers', u'affiliationinstitution_url', u'email', u'version', u'location', u'recommendations', u'preferredlang', u'affiliationinstitution', u'otherlangs', u'homepage', u'fullname', u'biography']

    """
    developertmpl = """{"interests": null,
                        "identifiers": [{"identifierstring":  "https://%(name)s.myopenid.com",
                                         "user_id": "%(uri)s",
                                         "identifiertype": "openid"}],
                        "user_id": "%(uri)s",
                        "suffix": null, "firstname": null, "title": null,
                        "middlename": null, "lastname": null, "imageurl": null,
                        "otherlangs": null, "affiliationinstitution_url": null,
                        "email": null, "version": null, "location": null,
                        "recommendations": null, "preferredlang": null,
                        "fullname": "%(name)s", "homepage": null,
                        "affiliationinstitution": null, "biography": null}"""

    developers = [{"name":"pbrian",
                   "uri":"cnxuser:75e06194-baee-4395-8e1a-566b656f6920",
                   "fakesessionid":"00000000-0000-0000-0000-000000000000"
                  },
                  {"name":"rossreedstrm",
                   "uri":"cnxuser:75e06194-baee-4395-8e1a-566b656f6921",
                   "fakesessionid":"00000000-0000-0000-0000-000000000001"
                  },
                  {"name":"edwoodward",
                   "uri":"cnxuser:75e06194-baee-4395-8e1a-566b656f6922",
                   "fakesessionid":"00000000-0000-0000-0000-000000000002"
                  }
    ]
    
    if sessiontype == 'fixed':
        #clear down the cache - only use this in testing anyway
        exec_stmt("DELETE from session_cache;", {})
        for dev in developers:
            js = developertmpl % dev
            tmpdict = json.loads(js)
            sid = dev['fakesessionid']
            set_session(sid, tmpdict)
    elif sessiontype == 'floating':
        js = developertmpl % developers[2]
        sid = uuid.uuid4()
        set_session(sid, js)
    else:
        raise Rhaptos2Error("sessiontype Must be 'floating' or 'fixed'")
        
        

        
if __name__ == '__main__':
    import doctest
    val = doctest.ELLIPSIS+doctest.REPORT_ONLY_FIRST_FAILURE+doctest.IGNORE_EXCEPTION_DETAIL
    doctest.testmod(optionflags=val)