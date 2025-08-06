using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System.Collections.ObjectModel;
using WorkInstructionCreator.Models;
using WorkInstructionCreator.Services;

namespace WorkInstructionCreator.ViewModels;

public partial class FlowchartViewModel : ObservableObject
{
    private readonly IFlowchartService _flowchartService;

    [ObservableProperty]
    private ProcessFlowchart? _selectedFlowchart;

    [ObservableProperty]
    private ProcessFlowchart? _currentFlowchart;

    [ObservableProperty]
    private FlowchartNode? _selectedNode;

    [ObservableProperty]
    private bool _isLoading = false;

    [ObservableProperty]
    private bool _isEditMode = false;

    [ObservableProperty]
    private string _searchText = string.Empty;

    public ObservableCollection<ProcessFlowchart> Flowcharts { get; } = new();
    public ObservableCollection<ProcessFlowchart> FilteredFlowcharts { get; } = new();
    public ObservableCollection<FlowchartNode> Nodes { get; } = new();
    public ObservableCollection<FlowchartConnection> Connections { get; } = new();

    public event Action<ProcessFlowchart>? FlowchartSelected;

    public TemplateFlowchartNode[] NodeTemplates { get; } = new[]
    {
        new TemplateFlowchartNode { Type = FlowchartNodeType.Start, Name = "Start", Icon = "▶️" },
        new TemplateFlowchartNode { Type = FlowchartNodeType.End, Name = "End", Icon = "🛑" },
        new TemplateFlowchartNode { Type = FlowchartNodeType.Process, Name = "Process", Icon = "📋" },
        new TemplateFlowchartNode { Type = FlowchartNodeType.Decision, Name = "Decision", Icon = "❓" },
        new TemplateFlowchartNode { Type = FlowchartNodeType.Document, Name = "Document", Icon = "📄" },
        new TemplateFlowchartNode { Type = FlowchartNodeType.Data, Name = "Data", Icon = "💾" },
        new TemplateFlowchartNode { Type = FlowchartNodeType.Connector, Name = "Connector", Icon = "🔗" }
    };

    public FlowchartViewModel(IFlowchartService flowchartService)
    {
        _flowchartService = flowchartService;
    }

    public async Task InitializeAsync()
    {
        await LoadFlowchartsAsync();
    }

    [RelayCommand]
    private async Task LoadFlowchartsAsync()
    {
        try
        {
            IsLoading = true;
            var flowcharts = await _flowchartService.GetAllFlowchartsAsync();
            
            Flowcharts.Clear();
            foreach (var flowchart in flowcharts)
            {
                Flowcharts.Add(flowchart);
            }
            
            ApplyFilters();
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"Error loading flowcharts: {ex.Message}");
        }
        finally
        {
            IsLoading = false;
        }
    }

    [RelayCommand]
    private void SelectFlowchart(ProcessFlowchart flowchart)
    {
        SelectedFlowchart = flowchart;
        CurrentFlowchart = flowchart;
        LoadFlowchartData(flowchart);
        FlowchartSelected?.Invoke(flowchart);
    }

    [RelayCommand]
    private void CreateNewFlowchart()
    {
        CurrentFlowchart = new ProcessFlowchart
        {
            Name = "New Flowchart",
            Description = "Custom process flowchart"
        };
        
        Nodes.Clear();
        Connections.Clear();
        IsEditMode = true;
    }

    [RelayCommand]
    private async Task SaveFlowchartAsync()
    {
        if (CurrentFlowchart == null) return;

        try
        {
            IsLoading = true;
            
            // Update current flowchart with nodes and connections
            CurrentFlowchart.Nodes = Nodes.ToList();
            CurrentFlowchart.Connections = Connections.ToList();
            
            if (string.IsNullOrEmpty(CurrentFlowchart.Id) || CurrentFlowchart.Id == Guid.Empty.ToString())
            {
                await _flowchartService.CreateFlowchartAsync(CurrentFlowchart);
            }
            else
            {
                await _flowchartService.UpdateFlowchartAsync(CurrentFlowchart);
            }
            
            await LoadFlowchartsAsync();
            IsEditMode = false;
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"Error saving flowchart: {ex.Message}");
        }
        finally
        {
            IsLoading = false;
        }
    }

    [RelayCommand]
    private void CancelEdit()
    {
        IsEditMode = false;
        if (SelectedFlowchart != null)
        {
            LoadFlowchartData(SelectedFlowchart);
        }
        else
        {
            CurrentFlowchart = null;
            Nodes.Clear();
            Connections.Clear();
        }
    }

    [RelayCommand]
    private void AddNode(FlowchartNodeType nodeType)
    {
        var newNode = new FlowchartNode
        {
            Type = nodeType,
            Text = GetDefaultNodeText(nodeType),
            X = 100 + (Nodes.Count * 150) % 600,
            Y = 100 + (Nodes.Count / 4) * 120
        };
        
        Nodes.Add(newNode);
    }

    [RelayCommand]
    private void DeleteNode(FlowchartNode node)
    {
        // Remove connections to/from this node
        var connectionsToRemove = Connections.Where(c => 
            c.SourceNodeId == node.Id || c.TargetNodeId == node.Id).ToList();
        
        foreach (var connection in connectionsToRemove)
        {
            Connections.Remove(connection);
        }
        
        Nodes.Remove(node);
        
        if (SelectedNode == node)
        {
            SelectedNode = null;
        }
    }

    [RelayCommand]
    private void SelectNode(FlowchartNode node)
    {
        SelectedNode = node;
    }

    [RelayCommand]
    private void ConnectNodes(string sourceNodeId, string targetNodeId)
    {
        // Check if connection already exists
        if (Connections.Any(c => c.SourceNodeId == sourceNodeId && c.TargetNodeId == targetNodeId))
            return;

        var connection = new FlowchartConnection
        {
            SourceNodeId = sourceNodeId,
            TargetNodeId = targetNodeId
        };
        
        Connections.Add(connection);
    }

    [RelayCommand]
    private void DeleteConnection(FlowchartConnection connection)
    {
        Connections.Remove(connection);
    }

    [RelayCommand]
    private void ApplyFilters()
    {
        FilteredFlowcharts.Clear();
        
        var filtered = Flowcharts.AsEnumerable();
        
        if (!string.IsNullOrWhiteSpace(SearchText))
        {
            filtered = filtered.Where(f => 
                f.Name.Contains(SearchText, StringComparison.OrdinalIgnoreCase) ||
                f.Description.Contains(SearchText, StringComparison.OrdinalIgnoreCase));
        }
        
        foreach (var flowchart in filtered)
        {
            FilteredFlowcharts.Add(flowchart);
        }
    }

    partial void OnSearchTextChanged(string value)
    {
        ApplyFilters();
    }

    [RelayCommand]
    private async Task DeleteFlowchartAsync(ProcessFlowchart flowchart)
    {
        try
        {
            IsLoading = true;
            await _flowchartService.DeleteFlowchartAsync(flowchart.Id);
            await LoadFlowchartsAsync();
            
            if (CurrentFlowchart?.Id == flowchart.Id)
            {
                CurrentFlowchart = null;
                Nodes.Clear();
                Connections.Clear();
            }
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"Error deleting flowchart: {ex.Message}");
        }
        finally
        {
            IsLoading = false;
        }
    }

    private void LoadFlowchartData(ProcessFlowchart flowchart)
    {
        Nodes.Clear();
        Connections.Clear();
        
        foreach (var node in flowchart.Nodes)
        {
            Nodes.Add(node);
        }
        
        foreach (var connection in flowchart.Connections)
        {
            Connections.Add(connection);
        }
    }

    private string GetDefaultNodeText(FlowchartNodeType nodeType)
    {
        return nodeType switch
        {
            FlowchartNodeType.Start => "Start",
            FlowchartNodeType.End => "End",
            FlowchartNodeType.Process => "Process Step",
            FlowchartNodeType.Decision => "Decision?",
            FlowchartNodeType.Document => "Document",
            FlowchartNodeType.Data => "Data",
            FlowchartNodeType.Connector => "Connector",
            _ => "Node"
        };
    }
}

public class TemplateFlowchartNode
{
    public FlowchartNodeType Type { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Icon { get; set; } = string.Empty;
}