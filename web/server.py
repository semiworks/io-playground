
import os
import asyncio

import aiohttp
import aiohttp.web
import aiohttp_jinja2
import jinja2
import aiohttp_session
import aiohttp_security

import web
from .handlers import configure_handlers


class WebServer(object):

    def __init__(self):
        # get event loop
        loop = asyncio.get_event_loop()

        # create web application
        self.__web_app = aiohttp.web.Application()

        # initialize sessions
        storage = aiohttp_session.SimpleCookieStorage()
        aiohttp_session.setup(self.__web_app, storage)

        # initialize security
        policy = aiohttp_security.SessionIdentityPolicy()
        aiohttp_security.setup(self.__web_app, policy, web.AuthorizationPolicy())

        # initialize jinja2
        this_path = os.path.dirname(__file__)
        templates_path = os.path.join(this_path, 'templates')
        aiohttp_jinja2.setup(self.__web_app, loader=jinja2.FileSystemLoader(templates_path))

        # add a route
        configure_handlers(self.__web_app)

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
        context = {'title': 'io playground', 'body': 'Hello <strong>World!</strong>'}
        response = aiohttp_jinja2.render_template('index.tmpl.html', request, context)
        return response

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
