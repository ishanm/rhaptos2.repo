Simple spec links
=================

This is a brief discussion and a linkage to more details of the 
``API spec`` for CNX rewrite.


URIs
----

I have made a mistake here and wish to correct it soon.
A URI is a URN, so I used the urh: format to define a URI.  
It also tried to avoid any unusual encoding around slashes and CGI escaping.
This is confusing and simply not simple.

current string that represents a pure single identifer for a resource::

   cnxuser:75e06194-baee-4395-8e1a-566b656f6920

THe new better format::

   /user/75e06194-baee-4395-8e1a-566b656f6920

or possibly ::

   /cnxuser/75e06194-baee-4395-8e1a-566b656f6920

If we are versioning the textual changes of say a module::

  /module/75e06194-baee-4395-8e1a-566b656f6920@aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d

  (sha1hash)


http://www.ietf.org/rfc/rfc4122.txt

User
----

The current dict-format for a user
::


    {u'affiliationinstitution': None,
     u'affiliationinstitution_url': None,
     u'biography': None,
     u'email': None,
     u'firstname': None,
     u'fullname': u'Paul Brian',
     u'homepage': None,
     u'identifiers': [{u'identifierstring': u'https://paulbrian.myopenid.com',
                       u'identifiertype': u'openid',
                       u'user_id': u'cnxuser:75e06194-baee-4395-8e1a-566b656f6920'},
                      {u'identifierstring': u'https://paulbrian.myopenid.com/',
                       u'identifiertype': u'openid',
                       u'user_id': u'cnxuser:75e06194-baee-4395-8e1a-566b656f6920'}],
     u'imageurl': None,
     u'interests': None,
     u'lastname': None,
     u'location': None,
     u'middlename': None,
     u'otherlangs': None,
     u'preferredlang': None,
     u'recommendations': None,
     u'suffix': None,
     u'title': None,
     u'user_id': u'cnxuser:75e06194-baee-4395-8e1a-566b656f6920',
     u'version': None}


Resources
---------

Module
------

Collection
----------

Folder
------

