
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

import aiohttp
import aiohttp.web


async def serve_index(request):
    txt = "Hello World"
    binary = txt.encode('utf8')

    resp = aiohttp.web.StreamResponse()
    resp.content_length = len(binary)
    resp.content_type = 'text/plain'

    await resp.prepare(request)
    resp.write(binary)

    return resp


async def init_web():
    # create an aiohttp application
    app = aiohttp.web.Application()
    app.router.add_get('/', serve_index)
    return app


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_web())
    aiohttp.web.run_app(app)
