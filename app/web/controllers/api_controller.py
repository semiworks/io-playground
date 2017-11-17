
import app.web
from .controller import Controller


class ApiController(Controller):

    def __init__(self):
        self.__rpc = app.web.JsonRpc()

        # register all API methods
        self.__rpc.add_methods(('', self.ping))

    async def __call__(self, request):
        # forward to our json rpc handler
        return await self.__rpc.__call__(request)

    async def ping(self, request):
        return 'pong'
