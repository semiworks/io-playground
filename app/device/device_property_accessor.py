

class DevicePropertyAccessor(object):

    def __init__(self, parent, prop_dict):
        self.__parent    = parent
        self.__prop_dict = prop_dict

    def items(self):
        return self.__prop_dict.items()

    def __getattr__(self, name):
        if name in self.__prop_dict:
            return DevicePropertyAccessor(self.__prop_dict[name], self.__prop_dict[name].properties)

        # default behaviour
        return getattr(self.__parent, name)

    def __len__(self):
        return len(self.__prop_dict)
