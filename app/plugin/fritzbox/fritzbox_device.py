
import os
import asyncio

import app.device


class FritzboxDevice(app.device.Device):

    def __init__(self, device_id):
        this_path = os.path.dirname(__file__)
        json_file = os.path.join(this_path, "fritzbox_device.json")
        super().__init__(device_id, json_file=json_file)

        self.properties.model.set_get_callback(self._get_model)

    @asyncio.coroutine
    async def _get_model(self):
        return "testmodel"
