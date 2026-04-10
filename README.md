# Opendaq Module Validation
Interactive Python environment for validating openDAQ modules.

## Setup

Run the setup script after cloning the repo. This will create a virtual environment and install all dependencies automatically.

#### Windows
```
scripts/setup.bat
```

## Running a Session

Modules currently have to be copied over manually. Hoping to change this to be automatic in the future.

For now, copy the latest model over and run the start script.

#### Windows

1. Get the module `.dll` from the ticket and copy it into the `modules/` directory
2. Run: `scripts/start.bat`

This will start an interactive Python session with the openDAQ instance already initialized and ready to use.

## Usage

The following variables are available in the session:

- `daq` — the openDAQ python module
- `instance` — the openDAQ Instance with the loaded openDAQ module(s)

See the [example code](https://docs.opendaq.com/manual/opendaq/3.30/tutorials/quick_start_setting_up_python.html) for reference.
