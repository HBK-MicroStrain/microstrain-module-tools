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

instance = _create_instance()
