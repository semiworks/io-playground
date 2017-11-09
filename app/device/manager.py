
class DeviceManager(object):

    def __init__(self):
        self.__devices = []

    async def get_devices(self):
        for device in self.__devices:
            yield device

    async def start(self):
        # TODO: read config from database and dynamically create devices

        # create a new device instance
        from app.plugin.yahoo_weather import YahooWeatherDevice
        yahoo_weather = YahooWeatherDevice()
        self.__devices.append(yahoo_weather)

        print("name       :", yahoo_weather.name)
        print("description:", yahoo_weather.description)

        print(".location  :", yahoo_weather.location)
        print(".forecast.1d-ahead.temperature:", yahoo_weather.forecast.ahead_1d.temperature)

        yahoo_weather.location = "Berlin"
        yahoo_weather.forecast.ahead_1d.temperature = "42"

        print(".location  :", yahoo_weather.location)
        print(".forecast.1d-ahead.temperature:", yahoo_weather.forecast.ahead_1d.temperature)

        # TODO: cannot access last property object -> temperature
        print(".location  :", yahoo_weather.properties.forecast.ahead_1d.temperature)

    async def shutdown(self):
        pass
