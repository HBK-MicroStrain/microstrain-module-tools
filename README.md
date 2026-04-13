# Opendaq Module Validation

Interactive Python environment for validating openDAQ modules.

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
    print("Name:", device_info.name, "Connection string:", device_info.connection_string)
```

### Adding devices

Wireless base stations are represented as a device. Add one using it's connection string. For example:
```python
device = instance.add_device('microstrain-wireless://COM46:3000000')
```

Connection strings are in the format: `prefix://address`.

### Getting channels

Wireless nodes are represented as channels. Channels can be retrieved once there is a reference to a device. For example, to get the first channel for a device:

```python
channel = device.get_channels()[0]
```

### Querying available properties

Properties are organized into `groups`. To get a list of all available property groups for a channel, run:

```python
for propery in channel.visible_properties:
    print(propery.name)
```

You can then get a reference to the group:

```python
prop_group = channel.get_property_value("[GROUP]")
```

where, `[GROUP]` is a property group name from the query above.

### Accessing properties

Individual properties can be accessed once you have a reference to a their group. For example, to get the lost beacon timeout property:

```python
# Get the current timeout
timeout = prop_group.get_property_value("LostBeaconTimeout")

# Print the property value
print(f"Lost beacon timeout value: {timeout}")

# Set a new timeout
prop_group.set_property_value("LostBeaconTimeout", 7)
```
