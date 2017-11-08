
import sqlite3


class Cursor(object):

    def __init__(self, sqlite3_cursor, connection):
        self._conn = connection
        self._impl = sqlite3_cursor
        self._loop = connection.loop

    def _run_operation(self, func, *args, **kwargs):
        # execute func in thread pool of attached to cursor connection
        if not self._conn:
            raise sqlite3.DatabaseError('Cursor is closed.')
        future = self._conn._execute(func, *args, **kwargs)
        return future

    @property
    def connection(self):
        """Cursors database connection"""
        return self._conn

    @property
    def lastrowid(self):
        return self._impl.lastrowid

    @property
    def rowcount(self):
        """The number of rows modified by the previous DDL statement.
        This is -1 if no SQL has been executed or if the number of rows is
        unknown. Note that it is not uncommon for databases to report -1
        after a select statement for performance reasons. (The exact number
        may not be known before the first records are returned to the
        application.)
        """
        return self._impl.rowcount

    @property
    def description(self):
        """This read-only attribute is a list of 7-item tuples, each
        containing (name, type_code, display_size, internal_size, precision,
        scale, null_ok).
        pyodbc only provides values for name, type_code, internal_size,
        and null_ok. The other values are set to None.
        This attribute will be None for operations that do not return rows
        or if one of the execute methods has not been called.
        The type_code member is the class type used to create the Python
        objects when reading rows. For example, a varchar column's type will
        be str.
        """
        return self._impl.description

    @property
    def closed(self):
        """Read only property indicates if cursor has been closed"""
        return self._conn is None

    @property
    def arraysize(self):
        """This read/write attribute specifies the number of rows to fetch
        at a time with .fetchmany() . It defaults to 1 meaning to fetch a
        single row at a time.
        """
        return self._impl.arraysize

    @arraysize.setter
    def arraysize(self, size):
        self._impl.arraysize = size

    async def close(self):
        """Close the cursor now (rather than whenever __del__ is called).
        The cursor will be unusable from this point forward; an Error
        (or subclass) exception will be raised if any operation is attempted
        with the cursor.
        """
        if self._conn is None:
            return
        await self._run_operation(self._impl.close)
        self._conn = None

    async def execute(self, sql, *params):
        """Executes the given operation substituting any markers with
        the given parameters.
        :param sql: the SQL statement to execute with optional ? parameter
            markers. Note that pyodbc never modifies the SQL statement.
        :param params: optional parameters for the markers in the SQL. They
            can be passed in a single sequence as defined by the DB API.
            For convenience, however, they can also be passed individually
        """
        await self._run_operation(self._impl.execute, sql, *params)
        return self

    def executemany(self, sql, *params):
        """Prepare a database query or command and then execute it against
        all parameter sequences  found in the sequence seq_of_params.
        :param sql: the SQL statement to execute with optional ? parameters
        :param params: sequence parameters for the markers in the SQL.
        """
        fut = self._run_operation(self._impl.executemany, sql, *params)
        return fut

    def fetchone(self):
        """Returns the next row or None when no more data is available.
        A ProgrammingError exception is raised if no SQL has been executed
        or if it did not return a result set (e.g. was not a SELECT
        statement).
        """
        fut = self._run_operation(self._impl.fetchone)
        return fut

    def fetchall(self):
        """Returns a list of all remaining rows.
        Since this reads all rows into memory, it should not be used if
        there are a lot of rows. Consider iterating over the rows instead.
        However, it is useful for freeing up a Cursor so you can perform a
        second query before processing the resulting rows.
        A ProgrammingError exception is raised if no SQL has been executed
        or if it did not return a result set (e.g. was not a SELECT statement)
        """
        fut = self._run_operation(self._impl.fetchall)
        return fut

    def fetchmany(self, size):
        """Returns a list of remaining rows, containing no more than size
        rows, used to process results in chunks. The list will be empty when
        there are no more rows.
        The default for cursor.arraysize is 1 which is no different than
        calling fetchone().
        A ProgrammingError exception is raised if no SQL has been executed
        or if it did not return a result set (e.g. was not a SELECT
        statement).
        :param size: int, max number of rows to return
        """
        fut = self._run_operation(self._impl.fetchmany, size)
        return fut
