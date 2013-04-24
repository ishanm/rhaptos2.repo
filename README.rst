=============
rhaptos2.repo
=============

A content repository for storing unpublished works or works in
progress. The purpose of this application is to provide
individuals with a web interface to their content before. This
includes capabilities for creating, editing, mixing and publication of
content into a Connexions Archive (where publish works are stored).

See the `Connexions development documentation
<http://connexions.github.com/>`_ for more information.

Install 
-------

The following will setup a development install. For instructions about
a production deployment, go to http://connexions.github.com/ .

Pre-requisites::

     Python 2.7 (with header files)
     Postgres >=8.4
     npm >= 1.2.0

.. note:: There are various ways to install Postgres. Here are a few
   recommendations:

   - For Debian distributions use the following command
     and see followup instructions for system specific configuration::

         $ apt-get install postgresql

   - Fedora/CentOS distributions use the command below::

         $ yum install postgresql

   - On the Mac, it is recommended you use the `Postgres App at
     postgresapp.com <http://postgresapp.com/>`_.

To initialize your database to work with the default database
settings (do not use these same instructions for a production install)::

    $ su - postgres
    $ createuser -W -s rhaptos2repo
    Password: rhaptos2repo
    $ createdb -O rhaptos2repo rhaptos2repo
    $ createdb -O rhaptos2repo rhaptos2users

These commands setup a Postgres user named ``rhaptos2repo`` and made
it the owner of the newly created ``rhaptos2repo`` database.

Quick
~~~~~

This will install the repsository, with simple defaults, ready for developer use.
Download the Bash script
`quickdownload.sh
<https://raw.github.com/Connexions/rhaptos2.repo/master/quickdownload.sh>`_. 
Run that with an argument of an *empty* dir you want to use for the
source and repos.
Then this will download the application code, dependancies and set up
a Python virtual environment (an isolated Python environment).

::

    $ curl -O https://raw.github.com/Connexions/rhaptos2.repo/master/quickdownload.sh
    $ bash quickdownload.sh /tmp/testrepo1 # <- replace with any empty dir you like

.. If you need to make changes to quickdownload.sh, you will need to
   stop the script just before the buildvenv.sh script is run. This is
   a chicken and egg issue.
   After you have stopped the script--by commenting probably--you need
   to swap your local copy of the package in place of the cloned one
   before continuing the script--again, probably through commenting.

You'll need to launch the user server::

    cd /tmp/testrepo1/venvs/vrepo; source bin/activate
    cd /tmp/testrepo1/src/rhaptos2.user; python rhaptos2/user/run.py --config local.ini --port 8001

Then running these below to start the content repository instance::

    cd /tmp/testrepo1/venvs/vrepo;
    rhaptos2repo-run --debug --config=develop.ini

At this point you should see a running instance

Complete
~~~~~~~~

.. note:: It's recommended that you use a virtual environment to
   install this application. The installation and usage of virtualenv
   is out of scope for this document, but you can follow the
   instructions at `virtualenv.org <http://www.virtualenv.org>`_.

.. note:: If you are working on a Debian distribution, it is probably
   a good idea to use the native system packages for some of the
   dependencies. Here are our recommendations::
   
       apt-get install libxml2-dev
       apt-get install libxslt1-dev
       apt-get install python-psycopg2

To install the package mananually, checkout this package,
`rhaptos2.common <https://github.com/connexions/rhaptos2.common>`_,
and
`atc (authoring tools client) <https://github.com/connexions/atc>`_.

::

    git clone https://github.com/connexions/rhaptos2.repo.git
    git clone https://github.com/connexions/rhaptos2.common.git
    git clone https://github.com/connexions/atc.git

The ``atc`` project is a ``node.js`` project that will need installed
using ``npm`` as follows ::

    cd atc
    npm install .

(For more information and detailed instructions see the
`ATC project's readme file <https://github.com/connexions/atc>`_.)

Install these development packages into your Python environment::

    cd rhatpos2.common
    python setup.py develop
    cd rhaptos2.repo
    python setup.py develop

The installation will have supplied two scripts:

  * ``rhaptos2repo-run`` - a stand-alone server instance that
    can be used to bring up the application without a production
    worthy webserver.
  * ``rhaptos2repo-initdb`` - a script used to initialize the
    database tables.

To install the database schema, setup the database and note the
host, database name, user name and password in the applications
configuration file. (An example configuration file can be found in in
the root of the rhaptos2.repo project as ``develop.ini``.)

::

    [app]
    pghost = localhost
    pgdbname = rhaptos2repo
    pgusername = rhaptos2repo
    pgpassword = rhaptos2repo
    ...

After the database settings have been updated, you can call the
``rhaptos2repo-initdb`` utility to initialize the database. The
following command illustrates its usage. Make sure to swap in your
configuration file in place of the develop.ini mentioned here.

::

    $ rhaptos2repo-initdb --config=develop.ini

You will also need to tell the configuration where the copy of ``atc``
has been installed::

    [app]
    atc_directory = <location you cloned to>

Usage
-----

For general usage, you can use the stand-alone server
implementation. This requires that you have cloned and configured a
copy of the ``atc`` project (see the install instructions for more
information). You will need to supply the command with a configuration
file. An example configuration file can be found in the root of this
project as the file named ``develop.ini``.

::

   rhaptos2repo-run --debug --config=develop.ini --port=8000
   * Running on http://127.0.0.1:8000/

Deployment
----------

This is designed to be deployed into environments as follows::

   cd ~/src  
   git clone https://github.com/Connexions/bamboo.recipies.git

   cd ~/venvs/dev
   . bin/activate
   (dev) cd ~/src/bamboo.scaffold/bamboo/scaffold/scripts/
   (dev) . ./repo_config.sh && python controller.py --recipie rhaptos2repo stage build test deploy

The above will stage (move files, apply patches), build, create a
venv, run unit tests, and deploy into the web servers set in config,
using sshkeys set in config etc.

Third Party code
----------------

We rely on third party code.  
Eventually we shall pull all dependancies out into a stageing process.
For now pretty much all dependnacies (ie bootstrap.css) is in the static folder of Flask.  However, we are developing in parallel with Aloha, 
so we track the cnx-master branch of that - to do so clone Aloha into
a directory and point Flask at it (Flask will serve that cloned dir from 
localhost) ::

  In local.ini set: rhaptos2repo_aloha_staging_dir=/my/path
  cd /my/path
  git clone https://github.com/wysiwhat/Aloha-Editor.git
  git checkout cnx-master



running Tests
-------------

Functional tests have been written in runtests.py and 
are able to both run as tests of the output of an inprocess wsgi app 
(ie we call the app callable with our made up environ and start_repsonse)
It is also able to "reverse the flow through the gate" and generate HTTP 
requests which are pushed against a live server


$ nosetests --tc-file=../../testing.ini runtests.py

$ python run.py --config=../../testing.ini --host=0.0.0.0 --port=8000
$ nosetests --tc-file=../../testing.ini --tc=HTTPPROXY:http://localhost:8000

License
-------

This software is subject to the provisions of the GNU Affero General Public License Version 3.0 (AGPL). See license.txt for details. Copyright (c) 2012 Rice University

