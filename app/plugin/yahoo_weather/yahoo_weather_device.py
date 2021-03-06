
import os
import json
import datetime
import time
import asyncio

import aiohttp

import app.device

# keys
WIND_DIRECTION = "wind_direction"
WIND_SPEED     = "wind_speed"
WIND_CHILL     = "wind_chill"
HUMIDITY       = "humidity"
VISIBILITY     = "visibility"
PRESSURE       = "pressure"
SUNRISE        = "sunrise"
SUNSET         = "sunset"
TEMPERATURE    = "temperature"
TEXT           = "text"


class YahooWeatherDevice(app.device.Device):

    def __init__(self, device_id):
        this_path = os.path.dirname(__file__)
        json_file = os.path.join(this_path, "yahoo_weather_device.json")
        super().__init__(device_id, json_file=json_file)

        self._fetch_task = None
        self._last_fetched = None

        self.properties.interval.value_changed += self.on_interval_changed
        self.properties.location.value_changed += self.on_location_changed

    async def start(self):
        await self.trigger_fetch()

    async def shutdown(self):
        if self._fetch_task is not None:
            self._fetch_task.cancel()

    async def on_location_changed(self, sender):
        await self.trigger_fetch()

    async def on_interval_changed(self, sender):
        await self.trigger_fetch()

    async def trigger_fetch(self):
        interval = await self.interval
        location = await self.location
        if interval is None or location is None:
            # not properly configured
            return

        if self._fetch_task is not None:
            self._fetch_task.cancel()

        self._fetch_task = asyncio.ensure_future(self._fetch_task_func())

    async def _fetch_task_func(self):
        try:
            if self._last_fetched is not None:
                # wait some time
                time_to_wait = max(0, await self.interval - (time.time() - self._last_fetched))
                await asyncio.sleep(time_to_wait)

            await self._fetch_data()
            self._last_fetched = time.time()

            self._fetch_task=None
            await self.trigger_fetch()

            self.data_fetched.emit()

        except asyncio.CancelledError:
            pass
        except Exception as e:
            pass

    async def _fetch_data(self):
        print("_fetch_data")
        baseurl = "http://query.yahooapis.com/v1/public/yql?"
        yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='%s')" % await self.location
        params = {
            'q': yql_query,
            'format': 'json'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(baseurl, params=params) as resp:
                t = await resp.text()
                data = json.loads(t)

                if "query" not in data or "results" not in data["query"] or "channel" not in data["query"]["results"]:
                    return

                channel = data["query"]["results"]["channel"]

                # get units (TODO: check units exists)
                units = await self.__get_units(channel["units"])

                # get wind data
                wind_data = await self.__get_wind(channel["wind"], units)
                if WIND_CHILL in wind_data:
                    self.wind.chill = wind_data[WIND_CHILL]
                if WIND_SPEED in wind_data:
                    self.wind.speed = wind_data[WIND_SPEED]
                if WIND_DIRECTION in wind_data:
                    self.wind.direction = wind_data[WIND_DIRECTION]

                # get atmosphere data
                atmosphere_data = await self.__get_atmosphere(channel["atmosphere"], units)
                if HUMIDITY in atmosphere_data:
                    self.humidity = atmosphere_data[HUMIDITY]
                if VISIBILITY in atmosphere_data:
                    self.visibility = atmosphere_data[VISIBILITY]
                if PRESSURE in atmosphere_data:
                    self.pressure = atmosphere_data[PRESSURE]

                # get astronomy data
                astronomy_data = await self.__get_astronomy(channel["astronomy"], units)
                if SUNRISE in astronomy_data:
                    self.sunrise = astronomy_data[SUNRISE]
                if SUNSET in astronomy_data:
                    self.sunset = astronomy_data[SUNSET]

                # get condition data
                condition_data = await self.__get_condition(channel["item"]["condition"], units)
                if TEMPERATURE in condition_data:
                    self.temperature = condition_data[TEMPERATURE]
                if TEXT in condition_data:
                    self.text = condition_data[TEXT]

                # get forecast
                await self.forecast.clear()
                for i in range(10):
                    data = await self.__get_forecast(channel["item"]["forecast"][i], units)
                    await self.forecast.append({
                        "high": data["high"],
                        "low" : data["low"],
                        "date": data["date"],
                        "text": data["text"]
                    })

    @staticmethod
    async def __get_forecast(forecast_data, units):
        data = dict()

        if "date" in forecast_data:
            try:
                dt = datetime.datetime.strptime(forecast_data["date"], "%d %b %Y").date()
                data["date"] = dt
            except ValueError:
                pass

        if "high" in forecast_data:
            try:
                high = float(forecast_data["high"])
                if "temperature" in units and units["temperature"] == "F":
                    # convert from "F" to "°C"
                    high = (high - 32) * 5 / 9
                data["high"] = high
            except ValueError:
                pass

        if "low" in forecast_data:
            try:
                low = float(forecast_data["low"])
                if "temperature" in units and units["temperature"] == "F":
                    # convert from "F" to "°C"
                    low = (low - 32) * 5 / 9
                data["low"] = low
            except ValueError:
                pass

        # get text
        if "text" in forecast_data:
            try:
                text = forecast_data["text"]
                data["text"] = text
            except ValueError:
                pass

        return data

    @staticmethod
    async def __get_units(units_data):
        units = dict()

        for attrib_name in ['distance', 'pressure', 'speed', 'temperature']:
            if attrib_name in units_data:
                units[attrib_name] = units_data[attrib_name]
        return units

    @staticmethod
    async def __get_atmosphere(atmo_data, units):
        data = dict()

        # get humidity
        if "humidity" in atmo_data:
            try:
                humidity = int(atmo_data["humidity"])
                data[HUMIDITY] = humidity
            except ValueError:
                pass

        # get visibility
        if "visibility" in atmo_data:
            try:
                visibility = float(atmo_data["visibility"])
                if "distance" in units and units["distance"] == "mi":
                    # convert from "m" to "km"
                    visibility *= 1.60934
                data[VISIBILITY] = visibility
            except ValueError:
                pass

        # get pressure
        if "pressure" in atmo_data:
            try:
                pressure = float(atmo_data["pressure"])
                data[PRESSURE] = pressure
            except ValueError:
                pass

        return data

    @staticmethod
    async def __get_wind(wind_data, units):
        data = dict()

        # get direction
        if "direction" in wind_data:
            try:
                direction = int(wind_data["direction"])
                data[WIND_DIRECTION] = direction
            except ValueError:
                pass

        # get speed
        if "speed" in wind_data:
            try:
                speed = int(wind_data["speed"])
                if "speed" in units and units["speed"] == "mph":
                    # convert from "m/h" to "km/h"
                    speed *= 1.60934
                data[WIND_SPEED] = speed
            except ValueError:
                pass

        # get wind chill
        if "chill" in wind_data:
            try:
                chill = float(wind_data["chill"])
                if "temperature" in units and units["temperature"] == "F":
                    # convert from "F" to "°C"
                    chill = (chill - 32) * 5 / 9
                data[WIND_CHILL] = chill
            except ValueError:
                pass

        return data

    @staticmethod
    async def __get_astronomy(astro_data, units):
        data = dict()

        # get sunrise
        if "sunrise" in astro_data:
            try:
                dt = datetime.datetime.strptime(astro_data["sunrise"], "%I:%M %p").time()
                data[SUNRISE] = dt
            except ValueError:
                pass

        # get sunset
        if "sunset" in astro_data:
            try:
                dt = datetime.datetime.strptime(astro_data["sunset"], "%I:%M %p").time()
                data[SUNSET] = dt
            except ValueError:
                pass

        return data

    @staticmethod
    async def __get_condition(cond_data, units):
        data = dict()

        # get temperature
        if "temp" in cond_data:
            try:
                temperature = float(cond_data["temp"])
                if "temperature" in units and units["temperature"] == "F":
                    # convert from "F" to "°C"
                    temperature = (temperature - 32) * 5/9
                data[TEMPERATURE] = temperature
            except ValueError:
                pass

        # get text
        if "text" in cond_data:
            try:
                text = cond_data["text"]
                data[TEXT] = text
            except ValueError:
                pass

        return data
