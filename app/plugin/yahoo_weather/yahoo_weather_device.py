
import os
import app.device


class YahooWeatherDevice(app.device.Device):

    def __init__(self):
        this_path = os.path.dirname(__file__)
        json_file = os.path.join(this_path, "yahoo_weather_device.json")
        super(YahooWeatherDevice, self).__init__(json_file=json_file)
