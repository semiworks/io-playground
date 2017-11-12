
import datetime

from .device_property import DeviceProperty
from .property_signal import PropertySignal


class DeviceValueProperty(DeviceProperty):

    def __init__(self, name, prop_def):
        self._value = None

        self._value_changed = PropertySignal(self)

        # check readonly
        readonly = "readonly" in prop_def and prop_def["readonly"]

        # get type
        typestr = prop_def['type']
        if typestr == "string":
            t = str
        elif typestr == "number":
            t = float
        elif typestr == "time":
            t = datetime.time
        elif typestr == "date":
            t = datetime.date
        else:
            t = None  # is this allowed?

        # call base class
        super().__init__(name, type=t, readonly=readonly)

        # try to get default value
        if "default" in prop_def:
            self.value = prop_def["default"]

    @property
    def value_changed(self):
        return self._value_changed

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self._value != value:
            self._value = value
            self._value_changed.emit()
        else:
            self._value = value
