
import asyncio

import app.web


packages = [
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
