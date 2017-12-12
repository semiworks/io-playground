
import datetime

from yarl import URL

from .device_property import DeviceProperty
from .property_signal import PropertySignal


class DeviceValueProperty(DeviceProperty):

    def __init__(self, parent, name, prop_def):
        self._value = None

        self._value_changed = PropertySignal(self)

        # check readonly
        readonly = "readonly" in prop_def and prop_def["readonly"]

        # get type
        typestr = prop_def['type']
        if typestr == "string":
            t = DeviceProperty.STRING_TYPE
        elif typestr == "number":
            t = DeviceProperty.NUMBER_TYPE
        elif typestr == "time":
            t = DeviceProperty.TIME_TYPE
        elif typestr == "date":
            t = DeviceProperty.DATE_TYPE
        elif typestr == "url":
            t = DeviceProperty.URL_TYPE
        else:
            t = None  # is this allowed?

        # call base class
        super().__init__(parent, name, type=t, readonly=readonly)

        # try to get default value
        if "default" in prop_def:
            self._value = prop_def["default"]

    @property
    def value_changed(self):
        return self._value_changed

    def set_value(self, value):
        self._value = value

    async def _get_async_value(self):
        # check if we have a value callback
        if self._get_callback is not None:
            return await self._get_callback()

        return self._value

    def get_value_async(self):
        return self._get_async_value()

    async def to_json_dict(self):
        d = await super().to_json_dict()
        if type(self._value) is datetime.time:
            d['value'] = self._value.isoformat(timespec='auto')
        elif type(self._value) is datetime.date:
            d['value'] = self._value.isoformat()
        else:
            d['value'] = self._value
        return d
