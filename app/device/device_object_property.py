
from .device_property import DeviceProperty


class DeviceObjectProperty(DeviceProperty):

    def __init__(self, name, prop_def, properties):
        self._properties = properties
        # call base class
        super().__init__(name, type=object)

    @property
    def properties(self):
        return self._properties

    def __setattr__(self, name, value):
        if not name.startswith("_") and name in self._properties:
            self._properties[name].value = value
        else:
            super().__setattr__(name, value)