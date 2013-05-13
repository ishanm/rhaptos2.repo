Session Management
==================

Summary
=======

Session management in the repo has been poor for a long time, and it 
has made testing of the various functionalities more awkward and 
requiring more brain use by developer and test suite than needed.

THere are two main phases

* validate already set-up sessions and proceed correctly

* Create and destroy sessions, existing or none (ie login and out)


What is wrong with current setup?
---------------------------------

1. NO session cache, which was to be redis but never came in.  We are storing
   the users OpenID identifier.  This is a massive security hole.

2. reliance on Flask security session implementation.  THere are a number of
   reasons to be disatissfied with this, the first is the secret key is a single
   phrase, in config.

3. No clear migration away from Flask.

4. The awful temptation to put more and more stuff in session cookies for "ease" and "scalbility".

Primarily I am frustrated in testing ACLs, and in creating /resources/ - whoch would be again reliant on a broken session implementation.


validate already set-up sessions and proceed correctly
------------------------------------------------------

Starting from Master #c296332b2fc35c10f46f7decaa6483221f9b0ebe

1. SessionID as random number stored in cookie.  Actual details of user
   kept server-side in cache.

2. Use of deferred callbacks to handle response setting

3. use of cache session store - database?

4. 

What about API Tokens?
----------------------

Did we not discuss these at the Sprint?

Yes, and there is, to all intents and purposes, zero difference between
a random string stored as cookie that allows the next request sent to 
have users privileges, and 



Testing issues
--------------

* Creation of a "fake-login-API". During testing *only* (ie a flag set)
  we can visit a API page, and get a valid session cookie for one of a
  number of pre-defined users.

  

Why do you not encrypt the session ID in the cookie?
----------------------------------------------------

Mostly because I know bupkiss about encryption.  No really I can do AES
with OpenSSH just fine, but did I do it right? Did I rotate my encryption keys 
with each user? Did I use cyclic or block level encryption? Am I handing out 
an oracle? (The last one is yes)

Here is a simple argument - to correctly and securely encrypt anything sent 
client side one should have a salt/key unique to each user.

This simple and reasonable request destroys the main argument for sticking session details like isAdmin and UserName into a encrypted cookie - that it simplifies distributed architecture (I can let client connect to any web server, and I will still have the session state in the cookie, *no need for a database lookup*)

Well the minute we need to get a unique salt for a user, we are back to database lookups, and even more frequently than just plain session lookups.  

Anyway, enough round the houses, I don;t know enough about securing encrypted
services with part of the service under complete control of the attacker, to be 
sure I have not screwed it up.  So I wont do it till I do, and even then *all we should store* is the session ID.



A neat trick
~~~~~~~~~~~~
Sometimes it is desireable to set a cookie in your browser - chrome enables us to do this as follows:

1. navigate to the domain & path desired (i.e. "/" in most cases)
2. enter ``javascript:document.cookie="name=value"`` in the address bar & return
3. you should then revisit the domain, and hey presto you have a cookie


Thanks to http://blog.nategood.com/quickly-add-and-edit-cookies-in-chrome


