
import json

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

    async def editor_blocklist(self, request):
        blocks = []
        blocks.append({
            'name': 'static value',
            'id'  : 'static.value'
        })
        blocks.append({
            'name': 'addition',
            'id'  : 'addition'
        })
        blocks.append({
            'name': 'export',
            'id'  : 'export'
        })

        return {
            'blocks': blocks
        }

    async def editor_blockinfo(self, request):
        params = json.loads(request.params)
        block_id = params['id']
        if block_id == 'static.value':
            return {
                'id'      : 'static.value',
                'name'    : 'static value',
                'template': 'simple',
                'ports'   : [
                    {
                        'id'     : 'output',
                        'name'   : 'Wert',
                        'type'   : 'out'
                    }
                ]
            }

        # TODO: produce HTML 500 error
        return {
        }
