
import asyncio
import sys
import os

# setup library lookup path before using it
this_path = os.path.dirname(__file__)
lib_path = os.path.join(this_path, 'libs')
for d in os.listdir(lib_path):
    # create absolute path
    abs_path = os.path.join(lib_path, d)
    if os.path.isdir(abs_path):
        sys.path.append(abs_path)

import web


packages = [
    web
]


if __name__ == "__main__":

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
