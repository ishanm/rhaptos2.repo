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
Provide common logging facilites for all rhaptos2 components.



We expect to create two log *handlers* in the application

1. to log audit messages to stderr
2. to fire off statsd events 

We combine both into one logger, I think that is the best approach.

See set_logger in rhaptos2.repo for useage

Changelog:

2012-09-13 : removed the get_logger facility, basically each app is
             responsible for setting up its own logger.  This merely
             supplies a custom Handler for statsd



'''

import os
import logging
from logging import StreamHandler
import statsd


class StatsdHandler(logging.Handler):
    """Logging Handler class that emits statsd calls to graphite, then stdout
    
    It *only* does incr logs, ie event counting.
    Thats probably appropriate for most all log related stats

    issues - we init with host and port, probably a bad idea.
    Just do not want to muck around with config mdule for logging yet.

    >>> lg = logging.getLogger("doctest") 
    >>> h = StatsdHandler("localhost", 2222, True)
    >>> lg.addHandler(h)
    >>> lg.warn("an error", extra={"statsd": ['a.b', 'e.f']})
    Firing a.b
    Firing e.f

    So we take it on trust that statsd fired.
    This is a unsolved problem with statsd.




    """
    def __init__(self, host, port, debug=False):
        logging.Handler.__init__(self)
        self.stats_client = statsd.StatsClient(
                                               host,
                                               port)
        self.debug = debug

    def emit(self, record):
        """given a LogRecord r, extract the dotted names if any and fire off
    
        Hmm, testing this in doctest (in anything) is hard....
        So A totally contrived test
        """
        if "statsd" not in record.__dict__.keys():
            pass # hmmm no logging in the logger?
        else:
            for s in record.statsd:
                self.stats_client.incr(s)
                if self.debug == True: 
                    print "Firing %s" % s
        

if __name__ == '__main__':
    import doctest
    doctest.testmod()

