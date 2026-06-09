import opendaq as daq


class DaqTypeFactory:
    """Creates openDAQ typed values (enumerations, structs) without requiring explicit type manager or string wrapping.

    Args:
        instance: The openDAQ Instance to retrieve the type manager from.

    Example:
        types = daq_utils.DaqTypeFactory(instance)
        voltage = types.enumeration("MSCL_Wireless_Voltage", "voltage_3000mV")
    """

    def __init__(self, instance):
        self._instance = instance
        self._type_manager = instance.context.type_manager

    def enumeration(self, type_name, value_name):
        """Creates an openDAQ Enumeration value.

        Args:
            type_name: The openDAQ enum type name.
            value_name: The enum value name.

        Example:
            voltage = types.enumeration("MSCL_Wireless_Voltage", "voltage_3000mV")
        """
        return daq.Enumeration(daq.String(type_name), daq.String(value_name), self._type_manager)

    def struct(self, type_name, fields):
        """Creates an openDAQ Struct value.

        Args:
            type_name: The openDAQ struct type name.
            fields: A dict containing the struct's field names and values. Python primitives
                (bool, int, float) are converted to their openDAQ equivalents automatically.
                openDAQ types (e.g. Enumeration) are passed through as-is.

        Example:
            linear_eq = types.struct("MSCL_Wireless_LinearEquation", {"Slope": 1.0, "Offset": 0.0})
        """
        daq_fields = daq.Dict()

        for key, value in fields.items():
            if isinstance(value, bool):
                daq_fields[key] = daq.Boolean(value)
            elif isinstance(value, int):
                daq_fields[key] = daq.Integer(value)
            elif isinstance(value, float):
                daq_fields[key] = daq.Float(value)
            else:
                daq_fields[key] = value

        return daq.Struct(daq.String(type_name), daq_fields, self._type_manager)


class DaqTypeInspector:
    """Inspects openDAQ registered types without requiring an explicit instance argument on each call.

    Args:
        instance: The openDAQ Instance to retrieve the type manager from.

    Example:
        inspector = daq_utils.DaqTypeInspector(instance)
        inspector.describe_struct("MSCL_Wireless_ShuntCalCmdInfo")
        inspector.describe_enum("MSCL_Wireless_Voltage")
    """

    def __init__(self, instance):
        self._instance = instance
        # Releasing an IEnumerationType Python wrapper corrupts the underlying C++ object in the
        # openDAQ Python binding, causing a segfault on any subsequent call for the same type. Caching
        # the names as plain Python strings after the first call avoids touching the C++ object again.
        #
        # NOTE: Temporary workaround — remove once the openDAQ version is updated with a fix.
        self._enum_name_cache: dict[str, list[str]] = {}

    def describe_enum(self, type_name):
        """Prints the enumerator names for a registered enum type.

        Args:
            type_name: The full registered enum type name.

        Example:
            inspector.describe_enum("MSCL_Wireless_AutoCalCompletionFlag")
        """
        if type_name not in self._enum_name_cache:
            type_obj = self._instance.context.type_manager.get_type(type_name)
            enum_type = daq.IEnumerationType.cast_from(type_obj)
            self._enum_name_cache[type_name] = [str(k) for k in enum_type.as_dictionary]

        names = self._enum_name_cache[type_name]
        header = 'Enumerator'
        width = max(len(header), max(len(str(n)) for n in names))

        print()
        print(f'{header:<{width}}')
        print('-' * width)

        for name in names:
            print(str(name))

        print()

    def describe_struct(self, type_name):
        """Prints the fields and their types for a registered struct type.

        Args:
            type_name: The full registered struct type name.

        Example:
            inspector.describe_struct("MSCL_Wireless_LinearEquation")
        """
        type_obj = self._instance.context.type_manager.get_type(type_name)
        struct_type = daq.IStructType.cast_from(type_obj)
        builder = daq.StructBuilder(daq.String(type_name), self._instance.context.type_manager)

        rows = [
            (str(name), _field_type_label(value))
            for name, value in zip(struct_type.field_names, builder.field_values)
        ]
        headers = ('Field', 'Type')
        col_widths = [max(len(r[i]) for r in rows + [headers]) for i in range(2)]

        print()
        print(f'{headers[0]:<{col_widths[0]}} | {headers[1]:<{col_widths[1]}}')
        print(f'{"-" * col_widths[0]}-+-{"-" * col_widths[1]}')

        for name, type_str in rows:
            print(f'{name:<{col_widths[0]}} | {type_str:<{col_widths[1]}}')

        print()


def _field_type_label(value):
    if value is None:
        return '?'
    if isinstance(value, bool):
        return 'Bool'
    if isinstance(value, int):
        return 'Int'
    if isinstance(value, float):
        return 'Float'
    if isinstance(value, str):
        return 'String'
    if daq.IEnumeration.can_cast_from(value):
        return f'Enum<{daq.IEnumeration.cast_from(value).enumeration_type.name}>'
    return type(value).__name__


def call_function(root, path, *args):
    """Calls an openDAQ function property and return its result.

    This function handles casting to a callable automatically.

    Args:
        root: The root openDAQ property object to start from.
        path: The name or dot-notation path from the root to the function property.
        *args: Optional arguments to pass to the function property.

    Returns:
        The result returned by the function property, typically a PropertyObject.

    Raises:
        RuntimeError: If the property does not exist or cannot be cast properly.

    Example:
        # Function with no arguments
        result = call_function(channel, "Setup.Configure.Apply")

        # Function with arguments
        result = call_function(channel, "Capabilities.ChannelType", 1)

        # Query the result
        print(result.get_property_value("Success"))
    """
    return daq.IFunction.cast_from(root.get_property_value(path))(*args)


def find_property(channel, name):
    """Returns the full dot-notation path of a property given its name.

    Searches all groups and top-level properties on the channel.
    Returns 'Property not found' if no matching property is found.

    Args:
        channel: The openDAQ channel to search.
        name: The property name to search for.

    Example:
        find_property(channel, 'LostBeaconTimeout')
        # => 'Setup.Configure.Sampling.LostBeaconTimeout'
    """
    for prop in channel.visible_properties:
        if prop.value_type == daq.CoreType.ctObject:
            for child in channel.get_property_value(prop.name).visible_properties:
                if child.name == name:
                    return f'{prop.name}.{name}'
        elif prop.name == name:
            return name
    return 'Property not found'


def groups(root):
    """Returns all property groups and subgroups as dot-notation path strings.

    Args:
        root: The openDAQ object to query property groups from (channel, device, group, etc.).
    """
    # DFS keeps related subgroups adjacent in output, which is more readable than BFS for a hierarchy.
    # Otherwise, it would be like this: [Setup, Capabilities, ..., Setup.Configure, ...]

    result = []
    stack = [
        (root.get_property_value(prop.name), prop.name)
        for prop in root.visible_properties
        if prop.value_type == daq.CoreType.ctObject
    ]
    stack.reverse()

    while stack:
        obj, path = stack.pop()
        result.append(path)

        subgroups = [
            (obj.get_property_value(prop.name), f'{path}.{prop.name}')
            for prop in obj.visible_properties
            if prop.value_type == daq.CoreType.ctObject
        ]
        subgroups.reverse()
        stack.extend(subgroups)

    return result


def print_groups(root):
    """Prints all property groups and subgroups using dot-notation paths, sorted alphabetically.

    Args:
        root: The openDAQ object to query property groups from (channel, device, group, etc.).
    """
    print('\n'.join(sorted(groups(root))))


def print_group_properties(channel, group):
    """Prints all properties within a group for a channel as an aligned table.

    Args:
        channel: The openDAQ channel to query properties from.
        group: The name of the property group to query.

    Example:
        print_group_properties(channel, 'Setup.Configure.Sampling')
    """
    rows = [
        (prop.name, str(prop.value_type).split('CoreType.')[-1])
        for prop in channel.get_property_value(group).visible_properties
    ]

    headers = ('Property', 'Type')
    col_widths = [max(len(r[i]) for r in rows + [headers]) for i in range(2)]

    print(f'{headers[0]:<{col_widths[0]}} | {headers[1]:<{col_widths[1]}}')
    print(f'{"-" * col_widths[0]}-+-{"-" * col_widths[1]}')

    for row in rows:
        print(f'{row[0]:<{col_widths[0]}} | {row[1]:<{col_widths[1]}}')


def print_channel_properties(channel):
    """Prints all properties available on a channel, regardless of group.

    Outputs in the following format:
        Group Name | Property Name | Property Type

    Args:
        channel: The openDAQ channel to query properties from.
    """
    rows = []
    for prop in channel.visible_properties:
        # Properties within a group
        if prop.value_type == daq.CoreType.ctObject:
            for child in channel.get_property_value(prop.name).visible_properties:
                rows.append((prop.name, child.name, str(child.value_type).split('CoreType.')[-1]))
        # Top-level properties that are not in a group, which we want to include as well
        else:
            rows.append(('No group', prop.name, str(prop.value_type).split('CoreType.')[-1]))

    headers = ('Group', 'Property', 'Type')
    col_widths = [max(len(r[i]) for r in rows + [headers]) for i in range(3)]

    print(f'{headers[0]:<{col_widths[0]}} | {headers[1]:<{col_widths[1]}} | {headers[2]:<{col_widths[2]}}')
    print(f'{"-" * col_widths[0]}-+-{"-" * col_widths[1]}-+-{"-" * col_widths[2]}')

    for row in rows:
        print(f'{row[0]:<{col_widths[0]}} | {row[1]:<{col_widths[1]}} | {row[2]:<{col_widths[2]}}')
