

class DevicePropertyAccessor(object):

    def __init__(self, parent):
        self._parent = parent

    def __getattr__(self, name):
        if "_properties" in dir(self._parent):
            # used to proxy item() function of dictionary
            if name in dir(self._parent._properties):
                return getattr(self._parent._properties, name)

            if name in self._parent._properties:
                return DevicePropertyAccessor(self._parent._properties[name])

        # default behaviour
        return getattr(self._parent, name)

    def __len__(self):
        if "_properties" in dir(self._parent):
            return len(self._parent._properties)

        # default behaviour
        return super().__len__()
