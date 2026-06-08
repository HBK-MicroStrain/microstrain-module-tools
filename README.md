# MicroStrain Module Tools

Companion tools to enhance working with the MicroStrain Wireless OpenDAQ module:

| Tool                                                   | Supported Languages   |
| ------------------------------------------------------ | --------------------- |
| [Library](#library)                                    | C++, C#, Python |
| [JupyterLab](#interactive-prototyping-tool) | C#, Python        |

## Library

`daq_utils` is a library that simplifies working with openDAQ through extensions tailored for MicroStrain modules.

To import the library into your project:

```python
import daq_utils
```

See [Usage](#usage) for examples of how to use the library.

## JupyterLab
The [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/) environment comes with notebook templates for each supported language, all pre-configured with an openDAQ instance ready to use out of the box.

Ideal for exploration, prototyping, and testing.

### Setup

Run the setup script after cloning the repo. This will create a virtual environment and install all dependencies.

The Python notebook template is setup by default. Add `--csharp` to also set up the C# notebook template.

**Windows**
```
scripts\setup.bat
```

**Linux/Mac**
```
./scripts/setup.sh
```

### Running a Session

Run the startup script:

**Windows**
```
scripts\start.bat
```

**Linux/Mac**
```
./scripts/start.sh
```

This will open JupyterLab with the available notebook templates.

### Adding modules

Modules currently have to be copied over manually. Automatic module fetching is planned for a future update.

For now, copy any new modules into the `modules/` folder, then restart the kernel in JupyterLab to pick up the changes.


## Usage

See the openDAQ [documentation](https://docs.opendaq.com/manual/opendaq/3.30/introduction.html) for a full reference on the openDAQ API.

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

When you are ready to remove the device:

```python
instance.remove_device(device)
```

This will disconnect the device so you can use it in other applications, such as `SensorConnect`.

### Listing nodes

To see all wireless nodes currently discovered by the device:

```python
daq_utils.list_nodes(device)
```

This will print a table of each node's index and info, for example:

```
# | Model (Node ID)
--+------------------------
0 | G-Link-200-8g (33682)
1 | G-Link-200-8g (33683)
```

### Getting channels

Wireless nodes are represented as channels. See [Listing nodes](#listing-nodes) to find the index of the node you want, then retrieve its channel:

```python
channel = device.get_channels()[INDEX]
```

where:

* `INDEX` is the index of the node channel.

If that fails, try powering the node off and then back on again.

### Querying available property groups

Most properties are organized into `groups`. To get a list of all available property groups for a channel:

```python
daq_utils.print_property_groups(channel)
```

You can then get a reference to the group:

```python
prop_group = channel.get_property_value('Config')
```

### Querying available properties

To get a list of all available properties within a group:

```python
daq_utils.print_group_properties(channel, 'Config')
```

This will print the property name and its type:

```
Property          | Type
------------------+-------
LostBeaconTimeout | ctInt
Apply             | ctFunc
EnableChannel     | ctBool
```

To print all properties for a channel across every group at once:

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
daq_utils.find_property(channel, 'LostBeaconTimeout')
```

This will output:
```
'Config.LostBeaconTimeout'
```

### Accessing individual properties

Individual properties can be accessed in one of the following ways:
* using dot notation on the channel (*recommended*)
* via a group reference.

For example, to get and set the lost beacon timeout property using dot notation:

```python
# Get the current timeout
timeout = channel.get_property_value('Config.LostBeaconTimeout')

# Print the property value
print(f'Lost beacon timeout value: {timeout}')

# Set a new timeout
channel.set_property_value('Config.LostBeaconTimeout', 7)
```

### Querying function properties

To inspect a function property's description, arguments, and return type, read the `description` field directly from the property:

```python
print(channel.get_property('Features.MaxSweeps').description)
```

This will output:

```
Gets the maximum number of sweeps (or sweeps per burst) for the given sampling configuration.

Arguments:
    samplingMode: Enumeration<SamplingMode>
    dataMode: Enumeration<DataMode>
    dataFormat: Enumeration<DataFormat>
    channelMask: Int

Returns:
    Success: Bool,
    Result: Int
```

### Calling function properties

The easiest way to call function properties is using the wrapper:

```python
# Function with no arguments
result = daq_utils.call_function(channel, "Config.Apply")

# Function with arguments
result = daq_utils.call_function(channel, "Features.ChannelType", 1)
```

The result object can then be queried for any returned properties. For example:

```python
# Did the function execute properly?
success = result.get_property_value('Success')
print(success)
```

This will output:
```
'True'
```

### Inspecting types
To view what fields/values are available for openDAQ types such as enumerations and structs, create a `DaqTypeInspector`:

```python
inspector = daq_utils.DaqTypeInspector(instance)
```

#### Enums

To see all valid values for an enum:

```python
inspector.describe_enum('MSCL_Wireless_AutoCalCompletionFlag')
```

This will output:

```
Enumerator
----------
autocal_success
autocal_maybeInvalid_applied
autocal_maybeInvalid_notApplied
autocal_notComplete
```

#### Structs

To see the fields and their types for a struct:
```python
inspector.describe_struct('MSCL_Wireless_LinearEquation')
```

This will output:

```
Field  | Type
-------+------
Slope  | Float
Offset | Float
```

### Creating typed values

To create openDAQ typed values such as enumerations and structs, use `DaqTypeFactory`. It handles the type manager and string conversion automatically:

```python
types = daq_utils.DaqTypeFactory(instance)
```

#### Creating an enum value

Use `enumeration()`:

```python
voltage = types.enumeration("MSCL_Wireless_Voltage", "voltage_3000mV")
```

#### Creating a Struct value

Pass a Python dict with the struct's fields to `struct()`. Python primitives are converted automatically, and openDAQ types such as enumerations are passed through as-is:

```python
linear_eq = types.struct(
    "MSCL_Wireless_LinearEquation",
    {
        "Slope": 1.0,
        "Offset": 0.0
    }
)
```
