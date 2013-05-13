#!/usr/bin/env python
#! -*- coding: utf-8 -*-

### Copyright Rice University

# This program is licensed under the terms of the
# GNU General Affero License version 3 (or later).  Please see
# LICENSE.txt for details

###

""":author:  paul@mikadosoftware.com <Paul Brian>


This is a temporary one module soltuon.
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
>>> print userd[0][0]
00000000-0000-0000-0000-000000000001
>>> delete_session(userd[0][0])


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


"""
import psycopg2
import json
import datetime
from err import Rhaptos2Error

#### I do not think this is suitable for configuring in usual channel.
#### (set to one hour for now)
FIXEDSESSIONDURATIONSECS = 3600
DT = datetime.timedelta(seconds=FIXEDSESSIONDURATIONSECS)


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
        conn = psycopg2.connect(host="www.frozone.mikadosoftware.com",
                            database="dbtest",
                            user="test1",
                            password="pass1")
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
    and a userdict 

    
    """
    if not validate_uuid_format(sessionid):
        raise Rhaptos2Error("Incorrect UUID format for sessionid %s" % sessionid)
        
    SQL = """INSERT INTO session_cache (sessionid
                                        , userdict
                                        , session_startutc
                                        , session_endutc)

             VALUES                    (%s
                                        , %s
                                        , %s
                                        , %s);"""

    try:
        tnow = datetime.datetime.utcnow()
        exec_stmt(SQL, [sessionid,
                        json.dumps(userd),
                        tnow,
                        tnow+DT                        
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
    Given a sessionid, if it exists, and is "in date" then return json.
    Otherwise return None
    """
    if not validate_uuid_format(sessionid):
        raise Rhaptos2Error("Incorrect UUID format for sessionid %s" % sessionid)

    SQL = """SELECT * FROM session_cache WHERE sessionid = %s
             AND CURRENT_TIMESTAMP BETWEEN session_startutc AND session_endutc;"""
    rs = run_query(SQL, [sessionid,])
    if len(rs) != 1:
        return None
    else:
        return rs

if __name__ == '__main__':
    import doctest
    val = doctest.ELLIPSIS+doctest.REPORT_ONLY_FIRST_FAILURE+doctest.IGNORE_EXCEPTION_DETAIL
    doctest.testmod(optionflags=val)