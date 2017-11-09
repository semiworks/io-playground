
from .plugin import Plugin

list_of_plugins = []

async def start():
    global list_of_plugins

    # TODO: find plugins dynamically
    from .yahoo_weather import YahooWeatherPlugin
    yahoo_weather = YahooWeatherPlugin()
    list_of_plugins.append(yahoo_weather)


async def shutdown():
    global list_of_plugins

    list_of_plugins.clear()


async def get_device_templates():
    global list_of_plugins

    l = []
    for pl in list_of_plugins:
        l += (await pl.get_device_templates())

    return l
