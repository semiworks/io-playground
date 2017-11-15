
import app
from .device_list_property import DeviceListProperty
from .device_object_property import DeviceObjectProperty
from .device_value_property import DeviceValueProperty
from .device_file_property import DeviceFileProperty


def create_property(parent, prop_def, prop_name="anonymous"):
    if "type" not in prop_def:
        # skip this
        return None

    if prop_def["type"] == "file":
        return DeviceFileProperty(parent, prop_name)

    elif prop_def["type"] == "list":
        return DeviceListProperty(parent, prop_name, prop_def)

    elif prop_def["type"] == "object":
        # get properties of object
        # -> recursive call
        return DeviceObjectProperty(parent, prop_name, prop_def)

    else:
        return DeviceValueProperty(parent, prop_name, prop_def)


def load_properties(parent, property_dict, property_definition):
    for prop_name, prop_def in property_definition.items():
        prop_inst = create_property(parent, prop_def, prop_name)
        if prop_inst is not None:
            property_dict[prop_name] = prop_inst

