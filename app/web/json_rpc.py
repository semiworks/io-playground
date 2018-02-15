
import json

import aiohttp
import aiohttp_session
import aiohttp_json_rpc

from .json_rpc_auth import JsonRpcAuthBackend


class JsonRpc(aiohttp_json_rpc.JsonRpc):

    def __init__(self):
        super().__init__(auth_backend=JsonRpcAuthBackend())

    async def __call__(self, request):
        # get identy from cookie
        session = await aiohttp_session.get_session(request)
        request.user = session.get('AIOHTTP_SECURITY') # TODO: session ID

        # call base class
        result = await super().__call__(request)
        if type(result) == aiohttp.web.Response and result.status == 405:
            # the base class does not yet support GET/POST requests (only websockets)
            # -> implement it here

            if request.method == 'GET':

                # get query parameters and create a json object
                query_data = dict(request.query.items())
                json_data = json.dumps(query_data)

                # decode the message
                try:
                    msg = aiohttp_json_rpc.protocol.decode_msg(json_data)
                except aiohttp_json_rpc.exceptions.RpcError as error:
                    return aiohttp.web.Response(text=aiohttp_json_rpc.protocol.encode_error(error))

                # handle requests
                if msg.type == aiohttp_json_rpc.protocol.JsonRpcMsgTyp.REQUEST:

                    # in python we declare a method with underscore 'this_is_a_message()', but in javascript we call it
                    # with a dit 'call.this.method'
                    method_name = msg.data['method'].replace('.', '_');

                    # check if method is available
                    if method_name not in request.methods:
                        # method is unknown or restricted
                        if method_name in self.methods:
                            # the method does exist, but the user has no privileges to access it
                            return aiohttp.web.Response(status=403) # FORBIDDEN
                        return aiohttp.web.Response(status=404) # NOT FOUND

                    # call method
                    try:
                        json_rpc_request = aiohttp_json_rpc.communicaton.JsonRpcRequest(
                            http_request=request,
                            rpc=self,
                            msg=msg,
                        )

                        result = await request.methods[method_name](json_rpc_request)
                        return aiohttp.web.Response(text=aiohttp_json_rpc.protocol.encode_result(msg.data['id'], result))

                    except (aiohttp_json_rpc.RpcInvalidParamsError, aiohttp_json_rpc.RpcInvalidRequestError) as error:
                        return aiohttp.web.Response(text=aiohttp_json_rpc.protocol.encode_error(error), status=500)

                    except Exception as error:
                        return aiohttp.web.Response(text=aiohttp_json_rpc.protocol.encode_error(
                            aiohttp_json_rpc.exceptions.RpcInternalError(msg_id=msg.data.get('id', None))), status=500)

                # handle result
                elif msg.type == aiohttp_json_rpc.protocol.JsonRpcMsgTyp.RESULT:
                    # TODO: handle message as result
                    return aiohttp.web.Response(status=405)

                else:
                    # TODO: unsupported message type
                    return aiohttp.web.Response(status=405)

            else:
                # TODO: handle POST requests
                return result

        return result
