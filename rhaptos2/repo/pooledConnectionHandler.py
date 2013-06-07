import sys
import contextlib

import gevent
from gevent.queue import Queue
from gevent.socket import wait_read, wait_write
from psycopg2 import OperationalError, connect

class DatabaseConnectionPool(object):

    def __init__(self, maxsize):
        if not isinstance(maxsize, (int, long)):
            raise TypeError('Expected integer, got %r' % (maxsize, ))
        self.maxsize = maxsize
        self.pool = Queue()
        self.size = 0

    def get(self):
        pool = self.pool
        if self.size >= self.maxsize or pool.qsize():
            return pool.get()
        else:
            self.size += 1
            try:
                new_item = self.create_connection()
            except:
                self.size -= 1
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
        self.connect = kwargs.pop('connect', connect)
        maxsize = kwargs.pop('maxsize', None)
        self.confSettings = {}
        DatabaseConnectionPool.__init__(self, maxsize)

    def set_conf_settings(self, **confSettings):
        self.confSettings['host'] = confSettings.get('pghost')
        self.confSettings['database'] = confSettings.get('pgdbname')
        self.confSettings['user'] = confSettings.get('pgusername')
        self.confSettings['password'] = confSettings.get('pgpassword')
        
    def create_connection(self):
        return self.connect(**self.confSettings)


if __name__ == '__main__':
    import time
    pool = PostgresConnectionPool("dbname=postgres", maxsize=3)
    start = time.time()
    threads = [gevent.spawn(pool.execute, 'select pg_sleep(1);') for _ in xrange(4)]
    gevent.joinall(threads)
    delay = time.time() - start
    print 'Running "select pg_sleep(1);" 4 times with 3 connections. Should take about 2 seconds: %.2fs' % delay