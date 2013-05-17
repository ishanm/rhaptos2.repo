#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###
# Copyright (c) Rice University 2012-13
# This software is subject to
# the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
###


'''                                                                                       
Configuration services to be used commonly across Rhaptos2
----------------------------------------------------------

This has been pared down to the simplest possible solution.  But this
means global file changes - moving from confd["rhaptos2repo_foobar" ]
to confd["rhaptos2repo"]["foobar"]

This should be acceptable (sed basically)

::

  from rhaptos2.common import conf
  confd = conf.get_config("/ini/file/path")

We now have a python dict, named confd, holding all the namesapced
configuration variables available in the "environment"

it would look like ::

  {
   'bamboo': 
       {'www_host_name':"www.cnx.org",},
   'rhaptos2repo':
       {'flag': "RedWhiteBlue"}
  }



>>> x = """[test]
... foo=1
...
... [test2]
... bar=1
... """
>>> open("/tmp/foo.ini", "w").write(x)
>>> d = get_config(ini_file_path="/tmp/foo.ini")
>>> expected = {'test': {'foo': '1'}, 'test2': {'bar': '1'}}
>>> assert d == expected

Possible enchancements: create and return a dict like object that
stores the last copy, and will compare on each change, so writing down
that the conf has changed in the application.


.. todo:: provide a validating .dat file holding a python dict to ensure we get right variables.


'''



import os
import ConfigParser
import types
from err import Rhaptos2Error


def get_config(ini_file_path=None):
    """
    Expect a .ini file at path location, parse and return dict

    """
    confd = {}
    if not os.path.isfile(ini_file_path):
        raise Rhaptos2Error("%s is not found" % ini_file_path)
    try:
        d = read_ini(ini_file_path)
        confd.update(d)    
    except Rhaptos2Error, e:
        pass
    return confd    

    

def read_ini(filepath):

    d = {}
    parser = ConfigParser.SafeConfigParser()
    parser.optionxform = str     #case sensitive
    try:
        parser.read(filepath)
    except Exception, e:
        raise Rhaptos2Error('Could not find or could not process: %s - %s' % (filepath, e) )

    ## convert ini file to a dict of dicts
    for sect in parser.sections():
        d[sect] = dict(parser.items(sect))
     
    return d
    



if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=False)

