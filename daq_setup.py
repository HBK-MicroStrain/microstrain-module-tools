import pathlib

import opendaq as daq


MODULE_PATH = str(pathlib.Path(__file__).parent / "modules")

def _create_instance():
    builder = daq.InstanceBuilder()
    builder.module_path = MODULE_PATH
    return builder.build()

def reload():
    """Reloads the openDAQ instance, picking up any new modules in the modules/ directory.

    Call this after copying a new .dll into modules/ without restarting the session.
    """
    global instance
    instance = _create_instance()
    print("Session reloaded.")

def call_function(root, path):
    """Calls an openDAQ function property and return its result.

    This function handles casting to a callable automatically.

    Args:
        root: The root openDAQ property object to start from.
        path: The name or dot-notation path from the root to the function property.

    Returns:
        The result returned by the function property, typically a PropertyObject.

    Raises:
        RuntimeError: If the property does not exist or cannot be cast properly.

    Example:
        # Recommended: using dot notation from the channel
        result = call_function(channel, "Config.Apply")

        # Using a reference to the property group
        result = call_function(config_group, "Apply")

        # Query the result
        print(result.get_property_value("Success"))
    """
    return daq.IFunction.cast_from(root.get_property_value(path))()

def print_channel_properties(channel):
    """Prints all available properties for a channel, regardless of group.

    Outputs in the following format:
        Group Name | Property Name | Property Type

    Args:
        channel: The openDAQ channel to query properties from.
    """
    # Builds a list of tuples in the format: (group name, property name, property type)
    rows = []
    for prop in channel.visible_properties:
        # Properties within a group
        if prop.value_type == daq.CoreType.ctObject:
            for child in channel.get_property_value(prop.name).visible_properties:
                rows.append((prop.name, child.name, str(child.value_type).split('CoreType.')[-1]))
        # Top-level properties that are not in a group, which we want to include as well
        else:
            rows.append(('No group', prop.name, str(prop.value_type).split('CoreType.')[-1]))

    # Computes the width of the widest entry in each of the columns, at least as wide as the header
    headers = ('Group', 'Property', 'Type')
    col_widths = [max(len(r[i]) for r in rows + [headers]) for i in range(3)]

    # Display header row
    print(f'{headers[0]:<{col_widths[0]}} | {headers[1]:<{col_widths[1]}} | {headers[2]:<{col_widths[2]}}')
    print(f'{"-" * col_widths[0]}-+-{"-" * col_widths[1]}-+-{"-" * col_widths[2]}')

    # Display rows
    for row in rows:
        print(f'{row[0]:<{col_widths[0]}} | {row[1]:<{col_widths[1]}} | {row[2]:<{col_widths[2]}}')

instance = _create_instance()
