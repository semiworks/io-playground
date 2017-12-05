
import app.plugin
from .fritzbox_device import FritzboxDevice


class FritzboxPlugin(app.plugin.Plugin):

    @staticmethod
    async def get_device_infos():
        return [
            {
                'classname': FritzboxDevice.__class__
            }
        ]
