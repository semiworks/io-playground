
import app.web
import app.device
from aiohttp_json_rpc.auth import permission_required, user_passes_test, login_required


class ApiController(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.__rpc = app.web.JsonRpc()

        # register all API methods
        for func_name in dir(self):
            if func_name.startswith("_"):
                continue

            # get function
            func = getattr(self, func_name)
            if not callable(func):
                continue

            self.__rpc.add_methods(('', func))

    async def __call__(self, request):
        # forward to our json rpc handler
        return await self.__rpc.__call__(request)

    @login_required
    async def device_get_list(self, request):
        device_list = app.device.manager.get_devices()
        result = []
        async for device in device_list:
            result.append({
                "id"  : device.id,
                "name": device.name
            })
        return result

    async def ping(self, request):
        return 'pong'
