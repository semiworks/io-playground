
from .aiosqlite3 import connect
from .migration import Migration

SQLITE_FILENAME = 'config.db'


class DbManager(object):

    def __init__(self):
        self.__conn = None
        self.__migration = Migration()

    async def start(self):
        # create a connection to the database
        # TODO: place database file in proper location
        self.__conn = await connect(SQLITE_FILENAME)

        # now apply all missing migrations
        await self.__migration.apply(self.__conn)

    async def shutdown(self):
        if self.__conn is not None:
            await self.__conn.close()
            self.__conn = None
