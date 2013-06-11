import sys
import contextlib

import gevent
from gevent.queue import Queue
from gevent.socket import wait_read, wait_write
from psycopg2 import OperationalError, connect

class DatabaseConnectionPool(object):

    def __init__(self):
        self.pool = Queue()

    def get(self):
        pool = self.pool
        if pool.qsize():
            return pool.get()
        else:
            try:
                new_item = self.create_connection()
            except:
                raise
            return new_item

    def put(self, item):
        self.pool.put(item)

    def closeall(self):
        while not self.pool.empty():
            conn = self.pool.get_nowait()
            try:
                conn.close()
            except Exception:
                pass

    @contextlib.contextmanager
    def cursor(self, *args, **kwargs):
        conn = self.get()
        try:
            yield conn.cursor(*args, **kwargs)
        except:
            if conn.closed:
                conn = None
                self.closeall()
            else:
                conn = self._rollback(conn)
            raise
        else:
            if conn.closed:
                raise OperationalError("Cannot commit because connection was closed: %r" % (conn, ))
            conn.commit()
        finally:
            if conn is not None and not conn.closed:
                self.put(conn)

    def _rollback(self, conn):
        try:
            conn.rollback()
        except:
            gevent.get_hub().handle_error(conn, *sys.exc_info())
            return
        return conn

    def execute(self, *args, **kwargs):
        with self.cursor() as cursor:
            cursor.execute(*args, **kwargs)
            return cursor.rowcount

    def fetchall(self, *args, **kwargs):
        with self.cursor() as cursor:
            cursor.execute(*args, **kwargs)
            return cursor.fetchall()

class PostgresConnectionPool(DatabaseConnectionPool):

    def __init__(self, *args, **kwargs):
        self.connect = kwargs.get('connect', connect)
        self.confSettings = kwargs.get('confSettings', {})
        DatabaseConnectionPool.__init__(self)

    def set_conf_settings(self, confSettings):
        self.confSettings['host'] = confSettings.get('pghost')
        self.confSettings['database'] = confSettings.get('pgdbname')
        self.confSettings['user'] = confSettings.get('pgusername')
        self.confSettings['password'] = confSettings.get('pgpassword')
        
    def create_connection(self):
        connection = self.connect(**self.confSettings)
        return connection