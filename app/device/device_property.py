

class DeviceProperty(object):

    def __init__(self, name, type, readonly=True):
        self._name = name
        self._type = type
        self._readonly = readonly

    @property
    def readonly(self):
        return self._readonly

    @property
    def is_object(self):
        return self._type == object

    @property
    def is_list(self):
        return self._type == list

    @property
    def type(self):
        return self._type

    def __str__(self):
        return "<DeviceProperty: %s>" % self._name
