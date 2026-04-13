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
    """Call an openDAQ function property and return its result.

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

instance = _create_instance()
