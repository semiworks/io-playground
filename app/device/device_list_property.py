
from .device_property import DeviceProperty


class DeviceListProperty(DeviceProperty):

    def __init__(self, parent, name, prop_def):
        self._items = []
        # TODO: check 'items' exists
        self._item_def = prop_def["items"]

        # call base class
        super().__init__(parent, name, type=DeviceProperty.LIST_TYPE)

    async def clear(self):
        self._items.clear()

    async def append(self, item):
        if isinstance(item, DeviceProperty):
            # just add it to the list
            item.parent = self
            self._items.append(item)
        else:
            # TODO: only if item is a dict or dotdict

            # create a device property
            from .utils import create_property
            prop_inst = create_property(self, self._item_def)
            if prop_inst is not None:
                for name, value in item.items():
                    # TODO: exec is eval
                    exec("prop_inst.properties." + name + ".set_value(value)")
                self._items.append(prop_inst)

    def __iter__(self):
        return iter(self._items)

    def __next__(self):
        return next(self._items)

    async def to_json_dict(self):
        d = await super().to_json_dict()
        d['items'] = []
        for item in self._items:
            d['items'].append(await item.to_json_dict())
        return d
