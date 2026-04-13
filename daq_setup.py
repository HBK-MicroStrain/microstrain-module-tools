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

def call_function(group, name):
    """Call an openDAQ function property and return its result.

    This function handles casting to a callable automatically.

    Args:
        group: The openDAQ property object (group) containing the function property.
        name: The name of the function property to call.

    Returns:
        The result returned by the function property, typically a PropertyObject.

    Raises:
        RuntimeError: If the property does not exist or cannot be cast to IFunction.

    Example:
        result = call_function(prop_group, "Apply")
        print(result.get_property_value("Success"))
    """
    return daq.IFunction.cast_from(group.get_property_value(name))()

instance = _create_instance()
