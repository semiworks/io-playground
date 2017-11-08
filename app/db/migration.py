

class Migration(object):

    def __init__(self):
        pass

    async def apply(self, conn):
        # get a database cursor
        cur = await conn.cursor()

        # check if a 'config' table exists
        await cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='config'")

        db_version = None
        if await cur.fetchone() is not None:
            # config table exists
            # -> fetch database version
            await cur.execute("SELECT value from config WHERE key='db_version'")
            (db_version,) = await cur.fetchone()

        # close cursor
        await cur.close()

        # now execute all available migrations
        nr = 1
        while True:
            method_name = "migration_%d" % nr

            # check if such a method exists
            if method_name not in dir(self):
                # stop here
                break

            # check if the migration with 'nr' was already applied
            if db_version is not None and nr >= db_version:
                # stop here
                break

            # now apply the migration
            method = getattr(self, method_name)
            await method(conn)

            # update db version
            cur = await conn.cursor()
            await cur.execute("INSERT OR REPLACE INTO config(key, value) VALUES (?, ?)", ("db_version", nr,))
            await conn.commit()

            # go to the next migration
            nr += 1

    async def migration_1(self, conn):
        # create config table
        cur = await conn.cursor()
        await cur.execute("""CREATE TABLE IF NOT EXISTS config(id INTEGER PRIMARY KEY ASC, key UNIQUE, value)""")
        await conn.commit()
