# Wireless Usage Guide

Overview of how wireless devices are represented in the openDAQ module and the wireless-specific utilities available in the library.

## Setup

Import the wireless submodule to access wireless-specific utilities:

**Python**
```python
import daq_utils.wireless as wireless
```

**C#**
```csharp
using Daq.Utils;
```

## Usage

See the main [README](../README.md) for general usage.

### Devices

Wireless base stations are represented as devices. See [Adding devices](../README.md#adding-devices) for how to connect to one.

### Channels

For wireless base stations, each connected node is represented as a channel. See [Getting channels](../README.md#getting-channels) for how to retrieve one.

To see all nodes currently discovered by the device:

**Python**
```python
wireless.list_nodes(device)
```

**C#**
```csharp
WirelessUtils.ListNodes(device);
```

This will print a table of each node's index and info, for example:

```
# | Model (Node ID)
--+------------------------
0 | G-Link-200-8g (33682)
1 | G-Link-200-8g (33683)
```

If a node channel is missing, try powering the node off and back on again.
