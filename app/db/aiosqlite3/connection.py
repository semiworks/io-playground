
import asyncio
import sqlite3
from functools import partial

from .cursor import Cursor
from .utils import _ContextManager


def connect(database):
    return _ContextManager(_connect(database))


async def _connect(database, executor=None):
    conn = Connection(database, executor=executor)
    await conn._connect()
    return conn


class Connection(object):

    def __init__(self, database, executor=None, loop=None):
        self._executor = executor
        self._loop = loop or asyncio.get_event_loop()
        self._conn = None

        self._database = database

    def _execute(self, func, *args, **kwargs):
        # execute function with args and kwargs in thread pool
        func = partial(func, *args, **kwargs)
        future = self._loop.run_in_executor(self._executor, func)
        return future

    async def _connect(self):
        # create sqlite connection
        f = self._execute(sqlite3.connect, self._database, check_same_thread=False)
        self._conn = await f

    @property
    def loop(self):
        return self._loop

    async def _cursor(self):
        c = await self._execute(self._conn.cursor)
        connection = self
        return Cursor(c, connection)

    def cursor(self):
        return _ContextManager(self._cursor())

    async def close(self):
        """Close sqlite3 connection"""
        if not self._conn:
            return
        c = await self._execute(self._conn.close)
        self._conn = None
        return c

    def commit(self):
        """Commit any pending transaction to the database."""
        fut = self._execute(self._conn.commit)
        return fut

    def rollback(self):
        """Causes the database to roll back to the start of any pending
        transaction.
        """
        fut = self._execute(self._conn.rollback)
        return fut

    async def execute(self, sql, *args):
        """Create a new Cursor object, call its execute method, and return it.
        See Cursor.execute for more details.This is a convenience method
        that is not part of the DB API.  Since a new Cursor is allocated
        by each call, this should not be used if more than one SQL
        statement needs to be executed.
        :param sql: str, formated sql statement
        :param args: tuple, arguments for construction of sql statement
        """
        _cursor = await self._execute(self._conn.execute, sql, *args)
        connection = self
        cursor = Cursor(_cursor, connection)
        return cursor

    def __del__(self):
        if self._conn:
            # This will block the loop, please use close
            # coroutine to close connection
            self._conn.close()
            self._conn = None
