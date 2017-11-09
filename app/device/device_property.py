
import app


def load_properties(property_dict, property_definition):
    for key, value in property_definition.items():
        property_dict[key] = DeviceProperty(value)


class DeviceProperty(object):

    def __init__(self, config_dict):
        self.__properties = app.dotdict()
        self.__value = None

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
    def is_object(self):
        return self.__type == object

    @property
    def value(self, value):
        # TODO: type conversion
        self.__value = value

    @value.setter
    def set_value(self):
        return self.__value

    def __getattr__(self, name):
        # check if this is one of our dynamic properties
        if name in self.__properties:
            # if this is an obect, directly return it, otherwise return the value
            if self.__properties[name].is_object:
                return self.__properties[name]
            return self.__properties[name].get_value()

        else:
            # Default behaviour
            return super(DeviceProperty, self).__getattr__(name)

    def __setattr__(self, name, value):
        if not name.startswith("_") and name in self.__properties:
            self.__properties[name].value = value
        else:
            super().__setattr__(name, value)
