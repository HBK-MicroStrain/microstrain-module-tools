# Opendaq Module Validation

Interactive Python environment for validating openDAQ modules.

This tool exposes the programmatic interface for working with openDAQ modules. For interfacing through GUI, see [AdvantageConnect](https://github.com/HBK-OneHBK/basic-recorder/actions/workflows/release.yml).

## Setup

Run the setup script after cloning the repo. This will create a virtual environment and install all dependencies automatically.

**Windows**
```
scripts\setup.bat
```

**Linux/Mac**
```
./scripts/setup.sh
```

## Running a Session

Run the start script. This will open an interactive Python session with the openDAQ instance already initialized and ready to use.

**Windows**
```
scripts\start.bat
```

**Linux/Mac**
```
./scripts/start.sh
```

## Usage

See the openDAQ [documentation](https://docs.opendaq.com/manual/opendaq/3.30/introduction.html) for more info.

The following variables are available in the session:

- `daq` — the openDAQ python module
- `instance` — the openDAQ Instance with the loaded openDAQ module(s)

See the [example code](https://docs.opendaq.com/manual/opendaq/3.30/tutorials/quick_start_setting_up_python.html#_testing_the_installation) for an example of these variables.

### Adding modules

Modules currently have to be copied over manually. Automatic module fetching is planned for a future update.

For now, copy any new modules into the `modules/` folder and reload the session:

```python
reload()
```

This reloads the openDAQ instance and picks up any newly added modules.

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
print_property_groups(channel)
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
for prop in channel.get_property_value('[GROUP]').visible_properties:
    print(prop.name, '|', prop.value_type)
```

This will print the property name and its type. For example:

```
LostBeaconTimeout | CoreType.ctInt
Apply | CoreType.ctFunc
EnableChannel | CoreType.ctBool
```

To print all properties for a channel across every group at once, run:

```python
print_channel_properties(channel)
```

This will print the group, property name, and type for every property. For example:

```
Group  | Property          | Type
-------+-------------------+--------
Config | LostBeaconTimeout | ctInt
Config | Apply             | ctFunc
Config | EnableChannel     | ctBool
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

Dot notation is the recommended approach, and will be used for the rest of this document.

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
result = call_function([ROOT], '[PATH]')
```

where:
*  `[ROOT]` is a reference to the property object containing the property
*  `[PATH]` is the name or dot notation path from root to the function property to call.

For example:

```python
result = call_function(channel, "Config.Apply")
```

The result object can then be queried for any returned properties. For example:

```python
# Did the function execute properly?
result.get_property_value('Success')
```
