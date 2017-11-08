
from .manager import DbManager

# the manager instance
mngr = None


async def start():
    global mngr

    # create and initialize the DB manager
    mngr = DbManager()
    await mngr.start()


async def shutdown():
    global mngr

    # stop the manager
    if mngr is not None:
        await mngr.shutdown()
