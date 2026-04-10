import pathlib

import opendaq as daq

MODULE_PATH = pathlib.Path(__file__).parent / "modules"
instance = daq.Instance(MODULE_PATH)
