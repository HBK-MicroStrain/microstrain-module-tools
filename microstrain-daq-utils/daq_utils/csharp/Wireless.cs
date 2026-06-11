using Daq.Core.OpenDAQ;

namespace Daq.Utils;

public static class WirelessUtils
{
    /// <summary>
    /// Returns all wireless node channels from a base station device.
    ///
    /// Example:
    ///   var nodes = WirelessUtils.ListNodes(device);
    ///   foreach (var node in nodes) Console.WriteLine(node.Name);
    /// </summary>
    public static IList<Channel> ListNodes(Device baseStation) =>
        baseStation.GetChannels()
            .Where(ch => ch.LocalId.StartsWith("node_", StringComparison.Ordinal))
            .ToList();
}
