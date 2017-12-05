
class DeviceManager(object):

    def __init__(self):
        self._devices = []
        self._last_device_id = 0

    async def get_devices(self):
        for device in self._devices:
            yield device

    async def get_device_by_name(self, name):
        for device in self._devices:
            if device.name.lower() == name.lower():
                return device

        return None

    async def create_device(self, device_type):
        self._last_device_id += 1
        instance = device_type(self._last_device_id)
        self._devices.append(instance)
        return instance

    async def start(self):
        # TODO: read config from database and dynamically create devices

        #
        # 1) create devices with default value
        # 2) load values from db and override default values
        # 3) call init() on each device
        #

        from app.plugin.webcam import WebcamDevice
        webcam = await self.create_device(WebcamDevice)

        webcam.url = "http://www.erfurt.de/webcam/domplatz.jpg"

        # create a new device instance
        from app.plugin.yahoo_weather import YahooWeatherDevice
        yahoo_weather = await self.create_device(YahooWeatherDevice)

        from app.plugin.fritzbox import FritzboxDevice
        fritzbox = await self.create_device(FritzboxDevice)

        print("name       :", fritzbox.name)
        print(".model     :", await fritzbox.model)

        yahoo_weather.data_fetched += self.weather_update

        print("name       :", yahoo_weather.name)
        print("description:", yahoo_weather.description)

        print(".location  :", await yahoo_weather.location)

        yahoo_weather.location = "Berlin"

        print(".location  :", await yahoo_weather.location)

        # NOTE: we do not get the device, but a device property accessor here
        print(".location  :", yahoo_weather.properties.location)

    async def shutdown(self):
        for device in self._devices:
            await device.shutdown()

    async def weather_update(self, sender):
        print("weather_updated")
