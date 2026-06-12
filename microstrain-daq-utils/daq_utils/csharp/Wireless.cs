using Daq.Core.OpenDAQ;

namespace Daq.Utils;

public static class WirelessUtils
{
    /// <summary>
    /// Prints a table of all wireless node channels discovered by a base station device.
    ///
    /// Example:
    ///   WirelessUtils.ListNodes(device);
    /// </summary>
    public static void ListNodes(Device baseStation)
    {
        var nodes = baseStation.GetChannels()
            .Where(ch => ch.LocalId.StartsWith("node_", StringComparison.Ordinal))
            .ToList();

        const string col0Header = "#";
        const string col1Header = "Model (Node ID)";
        var col0 = Math.Max(col0Header.Length, nodes.Count > 0 ? (nodes.Count - 1).ToString().Length : 1);
        var col1 = Math.Max(col1Header.Length, nodes.Count > 0 ? nodes.Max(n => n.Name.Length) : col1Header.Length);

        Console.WriteLine($"{col0Header.PadRight(col0)} | {col1Header.PadRight(col1)}");
        Console.WriteLine($"{new string('-', col0)}-+-{new string('-', col1)}");
        for (var i = 0; i < nodes.Count; i++)
            Console.WriteLine($"{i.ToString().PadRight(col0)} | {nodes[i].Name}");
    }
}
