
import os
import asyncio

import aiohttp
import aiohttp_jinja2
import jinja2
import aiohttp_session
import aiohttp_security

import app.web


class WebServer(object):

    def __init__(self):
        # get event loop
        loop = asyncio.get_event_loop()

        # create web application
        self.__web_app = aiohttp.web.Application()

        # setup sessions
        router = self.__web_app.router
        router.add_get ('/',          app.web.LoginController.show_login,     name='user.show_login')
        router.add_post('/login',     app.web.LoginController.login,          name='user.login')
        router.add_get ('/logout',    app.web.LoginController.logout,         name='user.logout')
        router.add_get ('/public',    app.web.LoginController.internal_page,  name='user.public')
        router.add_get ('/protected', app.web.LoginController.protected_page, name='user.protected')

        # initialize sessions
        storage = aiohttp_session.SimpleCookieStorage()
        aiohttp_session.setup(self.__web_app, storage)

        # initialize security
        policy = aiohttp_security.SessionIdentityPolicy()
        aiohttp_security.setup(self.__web_app, policy, app.web.AuthorizationPolicy())

        # initialize jinja2
        this_path = os.path.dirname(__file__)
        templates_path = os.path.join(this_path, 'templates')
        env = aiohttp_jinja2.setup(self.__web_app, loader=jinja2.FileSystemLoader(templates_path))
        # manipulate global context variables
        del env.globals['app']
        env.globals['route'] = self.route

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

    def route(self, name, **kwargs):
        return self.__web_app.router[name].url_for().with_query(kwargs)
