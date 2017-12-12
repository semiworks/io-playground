

class DeviceProperty(object):

    OBJECT_TYPE="<object>"
    URL_TYPE="<url>"
    DATE_TYPE="<date>"
    TIME_TYPE="<time>"
    LIST_TYPE="<list>"
    NUMBER_TYPE="<number>"
    STRING_TYPE="<string>"
    FILE_TYPE="<file>"

    def __init__(self, parent, name, type, readonly=True):
        self._parent = parent
        self._name = name
        self._type = type
        self._readonly = readonly

        self._get_callback = None

    @property
    def readonly(self):
        return self._readonly

    @property
    def is_object(self):
        return self._type == self.OBJECT_TYPE

    @property
    def is_list(self):
        return self._type == self.LIST_TYPE

    @property
    def is_url(self):
        return self._type == self.URL_TYPE

    @property
    def is_file(self):
        return self._type == self.FILE_TYPE

    @property
    def type(self):
        return self._type

    @property
    def link(self):
        return self._parent.link + "/" + self._name.lower()

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    def set_get_callback(self, cb):
        self._get_callback = cb

    def _async_value(self):
        return self._get_callback()

    def get_value_async(self):
        return self._async_value()

    async def to_json_dict(self):
        d = dict()
        d['type']     = self._type
        d['readonly'] = self._readonly
        return d

    def __str__(self):
        return "<DeviceProperty: %s>" % self._name
