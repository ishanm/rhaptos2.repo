API for Views and models
========================

Summary
-------

We have a great deal of shared functionality for the models in 
the :mod:`rhaptos2.repo.cnxbase` which is inherited over *multiple* inheritence 
by each model class.  The model classes also inherit SqlAlchemy base class.

It is intended to remove sqlalchemy and move to pure psycopg2 approach.
If we move to greenlets as well we need to test that ability. As such 
I have not introduced a pool for psyocpg2 work yet. (see sessioncache)

API
---

:mod:`rhaptos2.repo.model`
--------------------------
.. automodule:: rhaptos2.repo.model
   :members: 

:mod:`rhaptos2.repo.views`
--------------------------
.. automodule:: rhaptos2.repo.views
   :members:

:mod:`rhaptos2.repo.cnxbase`
----------------------------
.. automodule:: rhaptos2.repo.cnxbase
   :members:

