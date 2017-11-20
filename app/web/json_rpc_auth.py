
import json

import aiohttp_json_rpc.auth


class JsonRpcAuthBackend(aiohttp_json_rpc.auth.AuthBackend):

    def __init__(self):
        pass

    def prepare_request(self, request):
        # todo: get user from request (per cookie? -> see web aiohttp_security)
        # todo: or http basic auth (unsecure)?

        if not hasattr(request, 'user'):
            request.user = None

        if not hasattr(request, 'permissions'):
            request.permissions = set()

        # methods
        request.methods = {}

        method_pool = dict(
            login=self.login, # TODO: really here, not in API controller?
            logout=self.logout,
            **request.rpc.methods
        )

        for name, method in method_pool.items():
            if self._is_authorized(request, method):
                request.methods[name] = method

        # topics
        request.topics = set()

        for name, method in request.rpc.topics.items():
            if self._is_authorized(request, method):
                request.topics.add(name)

        if not hasattr(request, 'subscriptions'):
            request.subscriptions = set()

        request.subscriptions = request.topics & request.subscriptions

    async def login(self, request):
        params = json.loads(request.params)
        username = params['username']
        password = params['password']

        verified = username == "bud" and password == "spencer"
        if verified:
            from aiohttp_session import get_session
            session = await get_session(request.http_request)
            session['AIOHTTP_SECURITY'] = username

        return dict()

    async def logout(self, request):
        pass

    def _is_authorized(self, request, method):
        if hasattr(method, 'login_required') and not request.user:
            return False

        if hasattr(method, 'permissions_required') and not (
              len(request.permissions & method.permissions_required) ==
              len(method.permissions_required)):
            return False

        return True
