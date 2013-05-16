#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###
# Copyright (c) Rice University 2012-13
# This software is subject to
# the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
###


"""Contains a common configuration parsing class and various utilities for
dealing with configuration.

Author: Michael Mulich
Copyright (c) 2012 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

from collections import Mapping
import ConfigParser


DEFAULT_APP_NAME = 'app'


class Configuration(Mapping):
    """A configuration settings object

    The Configuration class reads from a file, is *case-sensitive*
    and it transforms the [app] section into top-level dotted values
    (ie print conf.foo returns "bar")
    and stores all other sections under a key of the same name

    It looks and acts like a dict. And has

    >>> initxt = '''[app]
    ... appkey=appval
    ...
    ... [test]
    ... foo=1
    ...
    ... [test2]
    ... bar=1
    ... '''
    >>> f = "/tmp/foo.ini"
    >>> open(f, "w").write(initxt)
    >>> C = Configuration.from_file(f)
    >>> expected = {'test': {'foo': '1'},
    ...            'test2': {'bar': '1'},
    ...            "appkey":"appval"}
    >>> assert C == expected
    >>> assert C.test == {'foo': '1'}
    >>> assert C.appkey == "appval"
    >>> assert C.test["foo"] == '1'

    """

    def __init__(self, settings={}, **sections):
        self._settings = settings
        for k in sections:
            self._settings[k] = sections[k]

    @classmethod
    def from_file(cls, file, app_name=DEFAULT_APP_NAME):
        """Initialize the class from an INI file."""
        settings = {}
        global_settings = {}
        print file
        with open(file, 'r') as f:
            ### parser will be case-sensitive taking form config file.
            parser = ConfigParser.SafeConfigParser()
            parser.optionxform = str
            config = parser
            config.readfp(f)
            for section in config.sections():
                if section == app_name:
                    settings.update(config.items(section))
                else:
                    global_settings[section] = dict(config.items(section))
        return cls(settings, **global_settings)

    def __getattr__(self, i):
        return self._settings[i]

    def __getitem__(self, key):
        return self._settings[key]

    def __setitem__(self, key, val):
        self._settings.__setitem__(key, val)

    def __delitem__(self, key):
        self._settings.__delitem__(key)

    def __len__(self):
        return len(self._settings)

    def __iter__(self):
        return self._settings.__iter__()

    def __repr__(self):
        return repr(self._settings)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
