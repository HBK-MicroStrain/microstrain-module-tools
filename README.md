# Opendaq Module Validation

Interactive Python environment for validating openDAQ modules.

## Setup

Run the setup script after cloning the repo. This will create a virtual environment and install all dependencies automatically.

**Windows**
```
scripts/setup.bat
```

## Running a Session

Run the start script. This will open an interactive Python session with the openDAQ instance already initialized and ready to use.

**Windows**
```
scripts/start.bat
```

## Usage

The following variables are available in the session:

- `daq` — the openDAQ python module
- `instance` — the openDAQ Instance with the loaded openDAQ module(s)

See the openDAQ [documentation](https://docs.opendaq.com/manual/opendaq/3.30/introduction.html) for more info.

### Adding modules

Modules currently have to be copied over manually. Automatic module fetching is planned for a future update.

For now, copy any new modules into the `modules/` folder and reload the session:

```python
>>> reload()
```

This reloads the openDAQ instance and picks up any newly added modules.

### Discovering devices

```python
>>> for device_info in instance.available_devices:
...     print("Name:", device_info.name, "Connection string:", device_info.connection_string)
```