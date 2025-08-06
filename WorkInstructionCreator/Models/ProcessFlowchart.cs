using System.ComponentModel;

namespace WorkInstructionCreator.Models;

public class ProcessFlowchart : INotifyPropertyChanged
{
    private string _name = string.Empty;
    private string _description = string.Empty;

    public string Id { get; set; } = Guid.NewGuid().ToString();

    public string Name
    {
        get => _name;
        set
        {
            _name = value;
            OnPropertyChanged(nameof(Name));
        }
    }

    public string Description
    {
        get => _description;
        set
        {
            _description = value;
            OnPropertyChanged(nameof(Description));
        }
    }

    public List<FlowchartNode> Nodes { get; set; } = new();
    public List<FlowchartConnection> Connections { get; set; } = new();
    public DateTime CreatedDate { get; set; } = DateTime.Now;
    public DateTime LastModified { get; set; } = DateTime.Now;
    public string Author { get; set; } = Environment.UserName;

    public event PropertyChangedEventHandler? PropertyChanged;

    protected virtual void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}

public class FlowchartNode
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string Text { get; set; } = string.Empty;
    public FlowchartNodeType Type { get; set; } = FlowchartNodeType.Process;
    public double X { get; set; }
    public double Y { get; set; }
    public double Width { get; set; } = 120;
    public double Height { get; set; } = 60;
    public string BackgroundColor { get; set; } = "#E3F2FD";
    public string BorderColor { get; set; } = "#1976D2";
    public Dictionary<string, object> Properties { get; set; } = new();
}

public class FlowchartConnection
{
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string SourceNodeId { get; set; } = string.Empty;
    public string TargetNodeId { get; set; } = string.Empty;
    public string Label { get; set; } = string.Empty;
    public ConnectionType Type { get; set; } = ConnectionType.Arrow;
    public string Color { get; set; } = "#666666";
}

public enum FlowchartNodeType
{
    Start,
    End,
    Process,
    Decision,
    Document,
    Data,
    Connector
}

public enum ConnectionType
{
    Arrow,
    Line,
    DottedLine
}