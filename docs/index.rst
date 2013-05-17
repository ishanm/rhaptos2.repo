Rhaptos2.Repo - Documentation 
=============================

Welcome to the docs for Rhaptos2.repo.

Some documentation is hand-written as below, and some is API further below

.. toctree::
   :maxdepth: 1

   testing
   config
   session-mgmt   
   jsonflow
   specindex



API
===

These documents come directly from source code as API docs (ala epydoc), 
but are divided up and commented in reasonable order below.

.. toctree::
   :maxdepth: 1

   viewmodelAPI
   authenticationAPI
   commonAPI
   runAPI
   


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
     
