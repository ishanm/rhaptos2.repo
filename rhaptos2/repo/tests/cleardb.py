
import os, json
import pprint
from rhaptos2.repo import backend, model, sessioncache
from rhaptos2.repo.backend import db_session
from rhaptos2.common import conf



CONFD_PATH = os.path.join(".", "../../../testing.ini")
confd = conf.get_config(CONFD_PATH)
#backend.clean_dbase(confd['app'])
backend.initdb(confd['app'])
backend.clean_dbase(confd['app'])

sessioncache._fakesessionusers()
