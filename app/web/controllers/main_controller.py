
import asyncio
import mimetypes

import aiohttp

import app.device
from .controller import Controller


class MainController(Controller):

    @Controller.require()
    async def show_index(self, request):

        devices = app.device.manager.get_devices()

        return await self.render('index.tmpl.html', request, {
            'devices': devices
        })

    async def device_property(self, request):
        device_name     = request.match_info.get('device_name')
        device_property = request.match_info.get('device_property')

        # get device by name
        device = await app.device.manager.get_device_by_name(device_name)
        if device is None:
            raise aiohttp.web.HTTPNotFound()

        prop = getattr(device.properties, device_property)
        if prop is None:
            raise aiohttp.web.HTTPNotFound()

        if prop.is_file:
            # create a stream response
            resp = aiohttp.web.StreamResponse(status=200, reason='OK')

            # TODO: get mime type & encodig
            (ct, encoding) = mimetypes.guess_type(await getattr(device, "url"))
            resp.content_type = ct
            if encoding:
                resp.headers[aiohttp.hdrs.CONTENT_ENCODING] = encoding
            # TODO: get filename
            resp.headers[aiohttp.hdrs.CONTENT_DISPOSITION] = "inline; filename=%s" % "test.jpg"

            # The StreamResponse is a FSM. Enter it with a call to prepare.
            await resp.prepare(request)

            coro = await prop.get_value_async()
            async for chunk in coro:
                resp._payload_writer.write(chunk)

            return resp

        else:
            raise aiohttp.web.HTTPNotFound()
