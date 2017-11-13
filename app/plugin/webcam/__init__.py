
import app.plugin
from .webcam_device import WebcamDevice


class WebcamPlugin(app.plugin.Plugin):

    @staticmethod
    async def get_device_infos():
        return [
            {
                'classname': WebcamDevice.__class__
            }
        ]
