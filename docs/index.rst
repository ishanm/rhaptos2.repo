Rhaptos2.Repo - Documentation 
=============================

Welcome to the docs for Rhaptos2.repo.

These docs will need filling out - however a number of the modules 
are internally documented and are laid out below


.. toctree::
   :maxdepth: 2

   testing
   config
   
API
---

.. toctree::
   :maxdepth: 2

   allmodules
   

Json Schema and examples
------------------------

.. toctree::
   :maxdepth: 1

   jsonflow



Session Cookies
===============

Please also see executableopinions docs.

There are two flows being considered here - the verify-existing-session flow, and login-then-set-up-session flow.  The first is simpler

Verify-existing-session
-----------------------

A browser supplies a cookie, for the domain, with k/v pair "cnxsessionid:[uuid]"
This uuid is mapped *on the server - not client side* to a cnxuser mediatype expressed as python dict or json object.  

This then returns the cached user object, and the user_uri is stored in REMOTE_USER_URI" in the environ, ready to be used for matching in the database etc.

If no session cookie exists, or is expired we redirect to login.



A neat trick
~~~~~~~~~~~~
Sometimes it is desireable to set a cookie in your browser - chrome enables us to do this as follows:

1. navigate to the domain & path desired (i.e. "/" in most cases)
2. enter ``javascript:document.cookie="name=value"`` in the address bar & return
3. you should then revisit the domain, and hey presto you have a cookie


Thanks to http://blog.nategood.com/quickly-add-and-edit-cookies-in-chrome



Misc.
=====

Here are misc notes that need to be better incorporated into the body of the
docs.






1. Concerns over use of <li> in storing data.
   
   We are using textual representations of HTML5 to store a module.
   This means we store the HTML5 of a module as part of a document
   that represents that doc and its associated metadata.

   THis seems to work well.

   We are also storing a collection using HTML5 in the body of the documnet
   - that is the tree structure of a collection is represented in one documnet
   as a seires of <li> nodes.

   Using <li> as nodes is of minor consequence, but there is consequence for
   storing the whole tree in one document.  Let us take for example a collection
   of three levels deep - lets choose the article on penguins in the
   Encycloipaedia Britiannica.  THe collection looks like::

     Britannica
     |
      - P-O
      | 
       - Penguin

    Now if Britannica is a collection (of all the volumes), and stores the whole
    tree within itself, and the P-O is another collection and stores the whole
    tree, we have two trees pointing to Penguion - and they need to be kept in
    synch.

    We basically cannot nest collections and store the whole tree within each
     
