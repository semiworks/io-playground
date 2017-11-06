
import functools

import aiohttp
import aiohttp_security
import aiohttp_jinja2


def configure_handlers(app):
    router = app.router
    router.add_get('/', index, name='index')

    # TODO: move to login controller

    router.add_post('/login', login, name='login')
    router.add_get('/logout', logout, name='logout')
    router.add_get('/public', internal_page, name='public')
    router.add_get('/protected', protected_page, name='protected')


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


async def index(request):
    username = await aiohttp_security.authorized_userid(request)

    context = {
        'title'  : 'io playground',
        'message': ''
    }

    if username:
        context['message'] = 'Hello, {username}!'.format(username=username)
    else:
        context['message'] = 'You need to login!'

    return aiohttp_jinja2.render_template('index.tmpl.html', request, context)


async def login(request):
    response = aiohttp.web.HTTPFound('/')
    form = await request.post()
    username = form.get('username')
    password = form.get('password')

    verified = username == "bud" and password == "spencer"
    if verified:
        await aiohttp_security.remember(request, response, username)
        return response

    return aiohttp.web.HTTPUnauthorized(body='Invalid username / password combination')


@require('public')
async def internal_page(request):
    # pylint: disable=unused-argument
    response = aiohttp.web.Response(
        text='This page is visible for all registered users',
        content_type='text/html',
    )
    return response


@require('protected')
async def protected_page(request):
    # pylint: disable=unused-argument
    response = aiohttp.web.Response(
        text='You are on protected page',
        content_type='text/html',
    )
    return response


@require('public')
async def logout(request):
    response = aiohttp.web.Response(text='You have been logged out', content_type='text/html')
    await aiohttp_security.forget(request, response)
    return response
