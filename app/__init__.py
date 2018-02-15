
import asyncio

import app.db
import app.device
import app.plugin
import app.web

from .utils import *


packages = [
    #
    # setup database connection
    #
    app.db,

    #
    #
    #

#    app.device,
#    app.plugin,

    #
    # start internal webserver
    #
    app.web
]


def run():
    # get event loop
    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    # initialize all packages
    for package in packages:
        loop.run_until_complete(package.start())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # shutdown packages
    for package in reversed(packages):
        loop.run_until_complete(package.shutdown())

    # close the loop
    loop.close()
