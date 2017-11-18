
import json

import app
from .utils import load_properties
from .device_property_accessor import DevicePropertyAccessor
from .property_signal import PropertySignal


class Device(object):

    def __init__(self, device_id, json_file):
        self._id          = device_id
        self._name        = ""
        self._description = ""
        self._properties  = app.dotdict()
        self._events      = app.dotdict()

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
                    load_properties(self, self._properties, value)

                # events
                if key == "events":
                    self._load_events(value)
                # TODO: events, actions

    async def shutdown(self):
        pass

    def _load_events(self, definition):
        for event_name, event_definition in definition.items():
            self._events[event_name] = PropertySignal(self)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def events(self):
        return self._events

    @property
    def properties(self):
        return DevicePropertyAccessor(self)

    @property
    def link(self):
        return "/device/"+self._name.lower()

    def __getattr__(self, name):
        # check if this is a dynamic event
        if name in self._events:
            return self._events[name]

        # # check if this is a dynamic property
        if name in self._properties:
            # if this is an object, directly return it ...
            if self._properties[name].is_object or self._properties[name].is_list:
                return self._properties[name]

            # ... otherwise return the value
            return self._properties[name].get_value_async()

        raise AttributeError(__class__, "object has no attribute '%s" % name)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)

        elif name in self._properties:
            self._properties[name].value = value

        elif name in self._events:
            self._events[name] = value

        else:
            super().__setattr__(name, value)

    def __str__(self):
        return "<Device: %s>" % self._name
