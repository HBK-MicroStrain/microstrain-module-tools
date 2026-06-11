import opendaq as daq


def list_nodes(device):
    """Prints a table of all wireless nodes discovered by the device.

    Displays each node's index, ID, and model name.

    Args:
        device: The openDAQ device (wireless base station).
    """
    channels = device.get_channels()

    if not channels:
        print('No nodes found.')
        return

    rows = [(str(i), channel.name) for i, channel in enumerate(channels)]

    headers = ('#', 'Model (Node ID)')
    col_widths = [max(len(r[i]) for r in rows + [headers]) for i in range(2)]

    print()

    print(f'{headers[0]:<{col_widths[0]}} | {headers[1]:<{col_widths[1]}}')
    print(f'{"-" * col_widths[0]}-+-{"-" * col_widths[1]}')

    for row in rows:
        print(f'{row[0]:<{col_widths[0]}} | {row[1]:<{col_widths[1]}}')

    print()
