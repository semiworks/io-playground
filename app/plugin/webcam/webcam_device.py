
import os
import asyncio

import aiohttp

import app.device


class WebcamDevice(app.device.Device):

    def __init__(self):
        this_path = os.path.dirname(__file__)
        json_file = os.path.join(this_path, "webcam_device.json")
        super(WebcamDevice, self).__init__(json_file=json_file)

        self.properties.snapshot.set_get_callback(self._get_snapshot)

    @asyncio.coroutine
    async def _get_snapshot(self):
        async with aiohttp.ClientSession() as session:
            # TODO: get url
            async with session.get('http://www.erfurt.de/webcam/domplatz.jpg') as resp:
                while True:
                    chunk = await resp.content.read(1024)
                    if not chunk:
                        break
                    yield chunk
