
import functools

import aiohttp
import aiohttp_security
import aiohttp_jinja2


def require(permission):
    def wrapper(f):
        @functools.wraps(f)
        async def wrapped(request):
            # NOTE: always fails if no user logged in
            has_perm = await aiohttp_security.permits(request, permission)
            if not has_perm:
                message = 'User has no permission {}'.format(permission)
                raise aiohttp.web.HTTPForbidden(body=message.encode())
            return await f(request)
        return wrapped
    return wrapper


class LoginController(object):

    def __init__(self):
        pass

    @staticmethod
    async def show_login(request):
        username = await aiohttp_security.authorized_userid(request)

        context = {
            'title': 'io playground',
            'message': ''
        }

        if username:
            context['message'] = 'Hello, {username}!'.format(username=username)
        else:
            context['message'] = 'You need to login!'

        return aiohttp_jinja2.render_template('index.tmpl.html', request, context)

    @staticmethod
    async def login(request):
        response = aiohttp.web.HTTPFound('/')

        data = await request.post()
        username = data.get('username')
        password = data.get('password')

        verified = username == "bud" and password == "spencer"
        if verified:
            await aiohttp_security.remember(request, response, username)
            return response

        return aiohttp.web.HTTPUnauthorized(body='Invalid username / password combination')

    @staticmethod
    @require('public')
    async def logout(request):
        response = aiohttp.web.Response(text='You have been logged out', content_type='text/html')
        await aiohttp_security.forget(request, response)
        return response

    @staticmethod
    @require('public')
    async def internal_page(request):
        # pylint: disable=unused-argument
        response = aiohttp.web.Response(
            text='This page is visible for all registered users',
            content_type='text/html',
        )
        return response

    @staticmethod
    @require('protected')
    async def protected_page(request):
        # pylint: disable=unused-argument
        response = aiohttp.web.Response(
            text='You are on protected page',
            content_type='text/html',
        )
        return response
