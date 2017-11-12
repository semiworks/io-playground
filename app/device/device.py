
import json

import app
from .utils import load_properties
from .device_property_accessor import DevicePropertyAccessor


class Device(object):

    def __init__(self, json_file):
        self._name        = ""
        self._description = ""
        self._properties  = app.dotdict()

        with open(json_file) as fp:
            data = json.load(fp)

            for key, value in data.items():
                # name
                if key == "name":
                    self._name = str(value)

                # description
                if key == "description":
                    self._description = str(value)

                # properties
                if key == "properties":
                    load_properties(self._properties, value)

                # TODO: events, actions

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def properties(self):
        return DevicePropertyAccessor(self)

    def __getattr__(self, name):
        # # check if this is a dynamic property
        if name in self._properties:
            # if this is an object, directly return it ...
            if self._properties[name].is_object or self._properties[name].is_list:
                return self._properties[name]

            # ... otherwise return the value
            return self._properties[name].value

        raise AttributeError(__class__, "object has no attribute '%s" % name)

    def __setattr__(self, name, value):
        if not name.startswith("_") and name in self._properties:
            self._properties[name].value = value

        else:
            super().__setattr__(name, value)

    def __str__(self):
        return "<Device: %s>" % self._name
