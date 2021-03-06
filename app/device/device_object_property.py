
import app
from .device_property import DeviceProperty


class DeviceObjectProperty(DeviceProperty):

    def __init__(self, parent, name, prop_def):
        # load property
        from .utils import load_properties
        properties = app.dotdict()
        load_properties(self, properties, prop_def["properties"])

        self._properties = properties
        # call base class
        super().__init__(parent, name, type=DeviceProperty.OBJECT_TYPE)

    @property
    def properties(self):
        return self._properties

    def __setattr__(self, name, value):
        if not name.startswith("_") and name in self._properties:
            self._properties[name].set_value(value)
        else:
            super().__setattr__(name, value)

    async def to_json_dict(self):
        d = await super().to_json_dict()
        d['properties'] = dict()

        for key,value in self._properties.items():
            d['properties'][key] = await value.to_json_dict()

        return d
