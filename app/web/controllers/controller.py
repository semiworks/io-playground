
import aiohttp
import aiohttp_security


class Controller(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    # TODO: rename to 'protect' or 'permission' or 'privilege' ?
    @classmethod
    def require(cls, permission=None):
        # if permission is None, we need at least a logged in user

        def wrapper(f):

            async def wrapped(instance, request):
                # determine user
                identity = await request.app.user(request)
                if identity is None:
                    # no logged in user
                    # -> redirect to '/login'
                    raise aiohttp.web.HTTPFound( await request.app.route('user.show_login') )

                # we have an user -> check permission

                if permission is not None:
                    has_perm = await aiohttp_security.permits(request, permission)
                    if not has_perm:
                        message = 'User has no permission {}'.format(permission)
                        raise aiohttp.web.HTTPForbidden(body=message.encode())

                return await f(instance, request)

            return wrapped

        return wrapper

    async def render(self, template_name, request, context={}):
        return await request.app.render(template_name, request, context=context)
