
class DeviceManager(object):

    def __init__(self):
        self._devices = []

    async def get_devices(self):
        for device in self._devices:
            yield device

    async def start(self):
        # TODO: read config from database and dynamically create devices

        #
        # 1) create devices with default value
        # 2) load values from db and override default values
        # 3) call init() on each device
        #

        from app.plugin.webcam import WebcamDevice
        webcam = WebcamDevice()
        self._devices.append(webcam)

        webcam.url = "http://www.erfurt.de/webcam/domplatz.jpg"

        # create a new device instance
        from app.plugin.yahoo_weather import YahooWeatherDevice
        yahoo_weather = YahooWeatherDevice()
        self._devices.append(yahoo_weather)

        print("name       :", yahoo_weather.name)
        print("description:", yahoo_weather.description)

        print(".location  :", yahoo_weather.location)

        yahoo_weather.location = "Berlin"

        print(".location  :", yahoo_weather.location)

        # NOTE: we do not get the device, but a device property accessor here
        print(".location  :", yahoo_weather.properties.location)

    async def shutdown(self):
        for device in self._devices:
            await device.shutdown()
