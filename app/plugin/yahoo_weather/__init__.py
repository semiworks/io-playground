
import app.plugin
from .yahoo_weather_device import YahooWeatherDevice


class YahooWeatherPlugin(app.plugin.Plugin):

    @staticmethod
    async def get_device_infos():
        return [
            {
                'classname': YahooWeatherDevice.__class__
            }
        ]
