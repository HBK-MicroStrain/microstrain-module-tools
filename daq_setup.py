import pathlib

import opendaq as daq

instance_builder = daq.InstanceBuilder()
instance_builder.module_path = str(pathlib.Path(__file__).parent / "modules")
instance = instance_builder.build()
