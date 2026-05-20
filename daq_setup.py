import importlib
import inspect
import pathlib

import opendaq as daq

import daq_utils


if '_SETUP_FILE' not in globals():
    _SETUP_FILE = pathlib.Path(__file__).resolve()
MODULE_PATH = str(_SETUP_FILE.parent / "modules")


def _create_instance():
    builder = daq.InstanceBuilder()
    builder.module_path = MODULE_PATH
    return builder.build()


def reload_session():
    """Reloads the openDAQ instance and utility library.

    Call this after copying a new .dll into `modules/` or after updating
    daq_utils.py.

    Note: this will drop any existing device connections.
    """
    importlib.reload(daq_utils)
    exec(open(_SETUP_FILE).read(), globals())
    print("Session reloaded.")


def reload_utils():
    """Reloads the utility library, picking up any changes from an updated installation.

    Call this after updating the library to make new utilities available immediately.

    This allows you to update in-place in an active session. Preserves the existing openDAQ
    instance and any connected devices, so you can continue working without interruption.
    """
    caller_globals = inspect.currentframe().f_back.f_globals

    # Capture any daq_utils instances before reload so they can be re-instantiated
    # with the new class definitions afterward, preventing stale method references.
    stale = {
        name: value
        for name, value in caller_globals.items()
        if type(value).__module__ == 'daq_utils'
    }

    importlib.reload(daq_utils)

    for name, value in stale.items():
        new_cls = getattr(daq_utils, type(value).__name__)
        caller_globals[name] = new_cls(value._instance)

    print("Utility library reloaded.")


if __name__ == '__main__':
    instance = _create_instance()
