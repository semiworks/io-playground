
from .device_property import DeviceProperty


class DeviceFileProperty(DeviceProperty):

    def __init__(self, parent, name):
        super().__init__(parent, name, DeviceProperty.FILE_TYPE, readonly=True)

        self._callback = None

    def set_get_callback(self, cb):
        self._callback = cb

    def _async_value(self):
        return self._callback()

    def get_value_async(self):
        return self._async_value()
