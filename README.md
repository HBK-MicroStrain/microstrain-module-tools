# MicroStrain Module Tools

A library and interactive prototyping tool that extends openDAQ for MicroStrain modules.

Currently supports the *Python* bindings, with *C++* and *C#* planned.

## Overview
These tools are for working with openDAQ programmatically. For interfacing through GUI, see [AdvantageConnect](https://github.com/HBK-OneHBK/basic-recorder/actions/workflows/release.yml).

### Library

`daq_utils` is a library that simplifies working with openDAQ through extensions tailored for MicroStrain modules.

To use the library, import it into your project:

```python
import daq_utils

# Example usage
daq_utils.print_channel_properties(channel)
```

See [Usage](#usage) for more examples.

### Interactive Prototyping Tool
This tool provides a pre-configured Python session with an openDAQ instance ready to use out of the box — ideal for exploration, prototyping, and testing.

#### Setup

Run the setup script after cloning the repo. This will create a virtual environment and install all dependencies automatically.

**Windows**
```
scripts\setup.bat
```

**Linux/Mac**
```
./scripts/setup.sh
```

#### Running a Session

Run the startup script:

**Windows**
```
scripts\start.bat
```

**Linux/Mac**
```
./scripts/start.sh
```

This will open an interactive Python session with the openDAQ instance and library initialized and ready for use. The following variables are available in the session:

- `daq` — the openDAQ python module
- `daq_utils` — utility functions for working with openDAQ properties
- `instance` — the openDAQ Instance with the loaded openDAQ module(s)

See the [example code](https://docs.opendaq.com/manual/opendaq/3.30/tutorials/quick_start_setting_up_python.html#_testing_the_installation) for an example of these variables.

#### Adding modules

Modules currently have to be copied over manually. Automatic module fetching is planned for a future update.

For now, copy any new modules into the `modules/` folder and reload the session:

```python
reload_session()
```

This reloads the openDAQ instance and picks up any newly added modules.

#### Updating the library

If you update the library while a session is running, make the new features available immediately:

```python
reload_utils()
```

This will preserve the existing openDAQ instance and any connected devices, so you can continue working without interruption.

## Usage

See the openDAQ [documentation](https://docs.opendaq.com/manual/opendaq/3.30/introduction.html) for more info.

### Discovering devices

This code snippet will display a list of all currently available devices:

```python
for device_info in instance.available_devices:
    print('Name:', device_info.name, 'Connection string:', device_info.connection_string)
```

### Adding devices

Wireless base stations are represented as a device. Add one using it's connection string. For example:
```python
device = instance.add_device('microstrain-wireless://COM46:3000000')
```

Connection strings are in the format: `prefix://address`.

### Removing devices

When you are ready to remove the device, run:

```python
instance.remove_device(device)
```

This will disconnect the device so you can use it in other applications, such as `SensorConnect`.

### Getting channels

Wireless nodes are represented as channels. Channels can be retrieved once there is a reference to a device. For example, to get the first channel for a device:

```python
channel = device.get_channels()[0]
```

If that fails, try powering the node off and then back on again. This should fix the issue. If commands can no longer be entered in the interactive terminal, press `Enter` one or two times.

### Querying available property groups

Most properties are organized into `groups`. To get a list of all available property groups for a channel, run:

```python
daq_utils.print_property_groups(channel)
```

You can then get a reference to the group:

```python
prop_group = channel.get_property_value('[GROUP]')
```

where:
 * `[GROUP]` is a property group name from the query above.

### Querying available properties

To get a list of all available properties within a group, run:

```python
daq_utils.print_group_properties(channel, '[GROUP]')
```

This will print the property name and its type. For example:

```
Property          | Type
------------------+-------
LostBeaconTimeout | ctInt
Apply             | ctFunc
EnableChannel     | ctBool
```

To print all properties for a channel across every group at once, run:

```python
daq_utils.print_channel_properties(channel)
```

This will print the group, property name, and type for every property. For example:

```
Group  | Property          | Type
-------+-------------------+--------
Config | LostBeaconTimeout | ctInt
Config | Apply             | ctFunc
Config | EnableChannel     | ctBool
```

### Finding a property path

If you know a property name but not which group it belongs to, use `find_property` to get its full dot-notation path:

```python
daq_utils.find_property(channel, '[PROPERTY]')
```

For example:

```python
daq_utils.find_property(channel, 'LostBeaconTimeout')
# => 'Config.LostBeaconTimeout'
```

### Accessing individual properties

Individual properties can be accessed from their group. This can be done in two ways:

```python
# Recommended: using the dot notation on the channel
channel.get_property_value('[GROUP].[PROPERTY]')

# Using a reference to the property group
prop_group.get_property_value('[PROPERTY]')
```

where:
 * `[PROPERTY]` is the name of the individual property to be accessed.

**NOTE:** Dot notation is the recommended approach, and will be used for the rest of this document.

For example, to get and set the lost beacon timeout property:

```python
# Get the current timeout
timeout = channel.get_property_value('Config.LostBeaconTimeout')

# Print the property value
print(f'Lost beacon timeout value: {timeout}')

# Set a new timeout
channel.set_property_value('Config.LostBeaconTimeout', 7)
```

### Calling function properties

The easiest way to call function properties is using the wrapper:

```python
result = daq_utils.call_function([ROOT], '[PATH]')
```

where:
*  `[ROOT]` is a reference to the property object containing the property
*  `[PATH]` is the name or dot notation path from root to the function property to call.

For example:

```python
result = daq_utils.call_function(channel, "Config.Apply")
```

The result object can then be queried for any returned properties. For example:

```python
# Did the function execute properly?
result.get_property_value('Success')
```
