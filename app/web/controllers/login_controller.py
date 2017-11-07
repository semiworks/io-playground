
import aiohttp
import aiohttp_security

from .controller import Controller


class LoginController(Controller):

    async def show_login(self, request):
        # get logged in user
        username = await aiohttp_security.authorized_userid(request)

        context = {
            'title': 'io playground',
            'message': ''
        }

        if username:
            context['message'] = 'Hello, {username}!'.format(username=username)
        else:
            context['message'] = 'You need to login!'

        return await self.render('login.tmpl.html', request, context)

    async def login(self, request):
        response = aiohttp.web.HTTPFound('/')

        data = await request.post()
        username = data.get('username')
        password = data.get('password')

        verified = username == "bud" and password == "spencer"
        if verified:
            await aiohttp_security.remember(request, response, username)
            return response

        # TODO: redirect back with errors?
        return aiohttp.web.HTTPUnauthorized(body='Invalid username / password combination')

    @Controller.require()
    async def logout(self, request):
        response = aiohttp.web.HTTPFound(await request.app.route('show_index'))
        await aiohttp_security.forget(request, response)
        return response
