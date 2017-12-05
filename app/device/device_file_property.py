
from .device_property import DeviceProperty


class DeviceFileProperty(DeviceProperty):

    def __init__(self, parent, name):
        super().__init__(parent, name, DeviceProperty.FILE_TYPE, readonly=True)
