
import app
from .device_list_property import DeviceListProperty
from .device_object_property import DeviceObjectProperty
from .device_value_property import DeviceValueProperty


def create_property(prop_def, prop_name="anonymous"):
    if "type" not in prop_def:
        # skip this
        return None

    if prop_def["type"] == "list":
        return DeviceListProperty(prop_name, prop_def)

    elif prop_def["type"] == "object":
        # get properties of object
        # -> recursive call
        properties = app.dotdict()
        load_properties(properties, prop_def["properties"])
        return DeviceObjectProperty(prop_name, prop_def, properties=properties)

    else:
        return DeviceValueProperty(prop_name, prop_def)


def load_properties(property_dict, property_definition):
    for prop_name, prop_def in property_definition.items():
        prop_inst = create_property(prop_def)
        if prop_inst is not None:
            property_dict[prop_name] = prop_inst

