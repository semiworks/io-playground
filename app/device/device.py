
import json

import app
from .device_property import load_properties


class Device(object):

    def __init__(self, json_file):
        self.__name        = ""
        self.__description = ""
        self.__properties  = app.dotdict()

        with open(json_file) as fp:
            data = json.load(fp)

            for key, value in data.items():
                # name
                if key == "name":
                    self.__name = str(value)

                # description
                if key == "description":
                    self.__description = str(value)

                # properties
                if key == "properties":
                    load_properties(self.__properties, value)

                # TODO: events, actions

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def properties(self):
        return self.__properties

    def __getattr__(self, name):
        # check if this is one of our dynamic properties
        if name in self.__properties:
            # if this is an obect, directly return it, otherwise return the value
            if self.__properties[name].is_object:
                return self.__properties[name]
            return self.__properties[name].value

        else:
            # Default behaviour
            return super(Device, self).__getattr__(name)
