=======
Testing
=======

We have a WSGI app to be tested. 

I am using 3 approaches, which more or less marry up.

1. Doctests, and examples.

2. nosetesting for webtest

3. config passing for testing...


* standalone - should run with just python/rhaptos packages 
* with network
* with selenium

To test locally
---------------

1. We do not have sqllite working [#]_ as a backend so *we must have netowrked postgres* working,

2. apart from that run the tests as follows

3. doctests:  each file individually should support testmod
   doctests can run in their own suite - they should not require netowrk access.
   This is not always true.

4. functional testing of wsgi app::

   nosetests --tc-file=../../testing.ini runtests.py

This will use webtest to send requests *in-process* to the app - *no http calls
are made*.  The app however does not know this and proceeds as if runing in a
wsgi server.

5. functional HTTP testing of wsgi app::

    nosetests --tc-file=../../pbrian.ini  --tc=HTTPPROXY:http://localhost:8000/ runtests.py
    python run.py --config=../../pbrian.in

5. example.txt - a demo / example of how the various bits fir together.  it is a
   doctest suite but needs integrated system


config passing
--------------

nose











Also
----

Use `interlude <http://bluedynamics.com/articles/jens/interlude-write-python-doctests-interactive>`_ During development, copy the below into a doctest::

 >>> import interlude; interlude.interact(locals())

now run the doctest, and it drops you into a shell at that line
Just use the shell to develop, check, test etc.  Its using locals() *in* the doctest.  Its really helpful.




:biblio:
http://ivory.idyll.org/articles/nose-intro.html



footnotes
---------

.. [#]:: sqllite does not support the postgres ARRAY feature.
         I would like to intoriduce a SQLALchemy custom convertor so that we can store ARRAY in sqllite as probably just TEXT and do a exec/eval. THis way we divocre local testing from network connected postgres.
