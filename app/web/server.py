
import os
import asyncio

import aiohttp
import jinja2
import aiohttp_session
import aiohttp_security

import app.web


class WebServer(aiohttp.web.Application):

    def __init__(self):
        # get event loop
        loop = asyncio.get_event_loop()

        # call base class
        super(WebServer, self).__init__()

        # setup sessions
        router = self.router
        public_folder = os.path.join(os.path.dirname(__file__), "public")
        router.add_static('/css',    os.path.join(public_folder, "css"))
        router.add_static('/images', os.path.join(public_folder, "images"))
        router.add_static('/js',     os.path.join(public_folder, "js"))

        router.add_get ('/new',       app.web.MainController().show_new_index)
        router.add_get ('/',          app.web.MainController().show_index,      name='show_index')
        router.add_get ('/login',     app.web.LoginController().show_login,     name='user.show_login')
        router.add_post('/login',     app.web.LoginController().login,          name='user.login')
        router.add_get ('/logout',    app.web.LoginController().logout,         name='user.logout')

        router.add_route('*', '/api', app.web.ApiController())
        router.add_get ('/device/{device_name}/{device_property}', app.web.MainController().device_property)

        # initialize sessions
        storage = aiohttp_session.SimpleCookieStorage()
        aiohttp_session.setup(self, storage)

        # initialize security
        self.__policy = aiohttp_security.SessionIdentityPolicy()
        aiohttp_security.setup(self, self.__policy, app.web.AuthorizationPolicy())

        # initialize jinja2
        this_path = os.path.dirname(__file__)
        templates_path = os.path.join(this_path, 'templates')
        self.__jinja2 = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_path), enable_async=True,
                                           autoescape=True)
        self.__jinja2.globals['route'] = self.route
        self.__jinja2.globals['user']  = self.user
        self.__jinja2.globals['url']   = self.url
        self.__jinja2.globals['str']   = str
        self.__jinja2.globals['len']   = len

        # create a socket handler
        self.__web_hndlr = self.make_handler(loop=loop)

        # will be created when calling start
        self.__web_srv = None

    async def start(self):
        # get event loop
        loop = asyncio.get_event_loop()

        # start web application
        await self.startup()

        # start serving
        try:
            self.__web_srv = await loop.create_server(self.__web_hndlr, host='0.0.0.0', port=8080)
        except asyncio.CancelledError:
            pass

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
        await super(WebServer, self).shutdown()
        await self.cleanup()

    async def user(self, request):
        return await self.__policy.identify(request)

    async def route(self, name, **kwargs):
        return self.router[name].url_for(**kwargs)

    async def render(self, template_name, request, context=None, *args, encoding='utf-8', status=200, **kwargs):
        response = aiohttp.web.Response(status=status)
        if context is None:
            context = {}

        # add request to context
        context['request'] = request

        # Load the template from file
        template = self.__jinja2.get_template(template_name)
        rendered_template = await template.render_async(context)
        response.content_type = 'text/html'
        response.charset = encoding
        response.text = rendered_template
        return response

    async def url(self, request, tail):
        # TODO: take base_url in account
        if tail.startswith("/"):
            return tail
        return "/"+tail
