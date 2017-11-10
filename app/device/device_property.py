
import app
from .property_signal import PropertySignal


def load_properties(property_dict, property_definition):
    for key, value in property_definition.items():
        property_dict[key] = DeviceProperty(key, value)


class DeviceProperty(object):

    def __init__(self, name, config_dict):
        self.__properties = app.dotdict()
        self.__value = None

        self.__value_changed = PropertySignal(self)

        # check readonly
        self.__readonly = "readonly" in config_dict and config_dict["readonly"]

        # get type
        t = config_dict['type']
        if t == "string":
            self.__type = str
        elif t == "number":
            self.__type = float
        elif t == "object":
            self.__type = object
        else:
            self.__type = None  # is this allowed?
        # TODO: list
        # TODO: "enum": ["male", "female"]

        if self.__type == object:
            # an object is always readonly
            self.__readonly = True
            # load object properties
            if "properties" in config_dict:
                load_properties(self.__properties, config_dict["properties"])

        else:
            # try to get default value
            if "default" in config_dict:
                self.value = config_dict["default"]

    @property
    def value_changed(self):
        return self.__value_changed

    @value_changed.setter
    def value_changed(self, value):
        pass

    @property
    def readonly(self):
        return self.__readonly

    @property
    def is_object(self):
        return self.__type == object

    @property
    def value(self):
        # TODO: type conversion
        return self.__value

    @value.setter
    def value(self, value):
        if self.__value != value:
            self.__value = value
            self.__value_changed.emit()
        else:
            self.__value = value

    @property
    def type(self):
        return self.__type

    @property
    def properties(self):
        return self.__properties

    def __getattr__(self, name):
        # check if this is one of our dynamic properties
        if name in self.__properties:
            # if this is an object, directly return it, otherwise return the value
            if self.__properties[name].is_object:
                return self.__properties[name]
            return self.__properties[name].value

        raise AttributeError("%s object has no attribute '%s" % (__class__, name))

    def __setattr__(self, key, value):
        if not key.startswith("_") and key in self.__properties:
            self.__properties[key].value = value
        else:
            super().__setattr__(key, value)

    def __str__(self):
        return "<DeviceProperty: %s>" % self.__name
