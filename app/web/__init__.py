
from .server import WebServer
from .authorization_policy import AuthorizationPolicy
from .controllers import *
from .json_rpc import JsonRpc

# the server instance
srvr = None


async def start():
    global srvr

    # create and initialize the web server
    srvr = WebServer()
    await srvr.start()


async def shutdown():
    global srvr

    # stop the web server
    if srvr is not None:
        await srvr.shutdown()
