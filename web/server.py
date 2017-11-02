
import asyncio

import aiohttp
import aiohttp.web


class WebServer(object):

    def __init__(self):
        # get event loop
        loop = asyncio.get_event_loop()

        # create web application
        self.__web_app = aiohttp.web.Application()

        # add a route
        self.__web_app.router.add_get('/', self.serve_index)

        # create a socket handler
        self.__web_hndlr = self.__web_app.make_handler(loop=loop)

        # will be created when calling start
        self.__web_srv = None

    async def start(self):
        # get event loop
        loop = asyncio.get_event_loop()

        # start web application
        await self.__web_app.startup()

        # start serving
        try:
            self.__web_srv = await loop.create_server(self.__web_hndlr, host='0.0.0.0', port=8080)
        except asyncio.CancelledError:
            pass

    async def serve_index(self, request):
        txt = "Hello World"
        binary = txt.encode('utf8')

        resp = aiohttp.web.StreamResponse()
        resp.content_length = len(binary)
        resp.content_type = 'text/plain'

        await resp.prepare(request)
        resp.write(binary)

        return resp

    async def shutdown(self):
        if self.__web_srv is not None:
            # stop server
            self.__web_srv.close()

        # wait till the server shuts down
        await self.__web_srv.wait_closed()
        self.__web_srv = None

        # shutdown handler
        if self.__web_hndlr is not None:
            await self.__web_hndlr.shutdown()
            self.__web_hndlr = None

        # shutdown application
        if self.__web_app is not None:
            await self.__web_app.shutdown()
            await self.__web_app.cleanup()
            self.__web_app = None
