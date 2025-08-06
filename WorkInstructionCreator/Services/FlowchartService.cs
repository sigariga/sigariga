using Newtonsoft.Json;
using WorkInstructionCreator.Models;

namespace WorkInstructionCreator.Services;

public class FlowchartService : IFlowchartService
{
    private readonly string _flowchartsPath;
    private List<ProcessFlowchart> _flowcharts = new();

    public FlowchartService()
    {
        _flowchartsPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "WorkInstructionCreator", "Flowcharts");
        Directory.CreateDirectory(_flowchartsPath);
        _ = InitializeBaseFlowchartsAsync();
    }

    public async Task<List<ProcessFlowchart>> GetAllFlowchartsAsync()
    {
        await LoadFlowchartsAsync();
        return _flowcharts.ToList();
    }

    public async Task<ProcessFlowchart?> GetFlowchartByIdAsync(string id)
    {
        await LoadFlowchartsAsync();
        return _flowcharts.FirstOrDefault(f => f.Id == id);
    }

    public async Task<ProcessFlowchart> CreateFlowchartAsync(ProcessFlowchart flowchart)
    {
        flowchart.Id = Guid.NewGuid().ToString();
        flowchart.CreatedDate = DateTime.Now;
        flowchart.LastModified = DateTime.Now;
        
        await LoadFlowchartsAsync();
        _flowcharts.Add(flowchart);
        await SaveFlowchartsAsync();
        
        return flowchart;
    }

    public async Task<ProcessFlowchart> UpdateFlowchartAsync(ProcessFlowchart flowchart)
    {
        await LoadFlowchartsAsync();
        var existingFlowchart = _flowcharts.FirstOrDefault(f => f.Id == flowchart.Id);
        if (existingFlowchart != null)
        {
            flowchart.LastModified = DateTime.Now;
            var index = _flowcharts.IndexOf(existingFlowchart);
            _flowcharts[index] = flowchart;
            await SaveFlowchartsAsync();
        }
        return flowchart;
    }

    public async Task<bool> DeleteFlowchartAsync(string id)
    {
        await LoadFlowchartsAsync();
        var flowchart = _flowcharts.FirstOrDefault(f => f.Id == id);
        if (flowchart != null)
        {
            _flowcharts.Remove(flowchart);
            await SaveFlowchartsAsync();
            return true;
        }
        return false;
    }

    public async Task<byte[]> ExportFlowchartToImageAsync(ProcessFlowchart flowchart)
    {
        // This would typically use a chart rendering library
        // For now, return empty byte array as placeholder
        await Task.CompletedTask;
        return Array.Empty<byte>();
    }

    public async Task<List<ProcessFlowchart>> GetBaseFlowchartsAsync()
    {
        await LoadFlowchartsAsync();
        return _flowcharts.Where(f => f.Name.Contains("Base") || f.Name.Contains("Template")).ToList();
    }

    private async Task LoadFlowchartsAsync()
    {
        var filePath = Path.Combine(_flowchartsPath, "flowcharts.json");
        if (File.Exists(filePath))
        {
            try
            {
                var json = await File.ReadAllTextAsync(filePath);
                var flowcharts = JsonConvert.DeserializeObject<List<ProcessFlowchart>>(json);
                if (flowcharts != null)
                    _flowcharts = flowcharts;
            }
            catch
            {
                _flowcharts = new List<ProcessFlowchart>();
            }
        }
    }

    private async Task SaveFlowchartsAsync()
    {
        var filePath = Path.Combine(_flowchartsPath, "flowcharts.json");
        var json = JsonConvert.SerializeObject(_flowcharts, Formatting.Indented);
        await File.WriteAllTextAsync(filePath, json);
    }

    private async Task InitializeBaseFlowchartsAsync()
    {
        await LoadFlowchartsAsync();
        
        if (!_flowcharts.Any())
        {
            var baseFlowcharts = CreateBaseFlowcharts();
            _flowcharts.AddRange(baseFlowcharts);
            await SaveFlowchartsAsync();
        }
    }

    private List<ProcessFlowchart> CreateBaseFlowcharts()
    {
        return new List<ProcessFlowchart>
        {
            new()
            {
                Id = "basic-process-template",
                Name = "Basic Process Template",
                Description = "Simple linear process flow template",
                Nodes = new List<FlowchartNode>
                {
                    new() { Id = "start", Text = "Start", Type = FlowchartNodeType.Start, X = 100, Y = 50 },
                    new() { Id = "process1", Text = "Process Step", Type = FlowchartNodeType.Process, X = 100, Y = 150 },
                    new() { Id = "decision1", Text = "Quality Check?", Type = FlowchartNodeType.Decision, X = 100, Y = 250 },
                    new() { Id = "process2", Text = "Corrective Action", Type = FlowchartNodeType.Process, X = 250, Y = 250 },
                    new() { Id = "end", Text = "End", Type = FlowchartNodeType.End, X = 100, Y = 350 }
                },
                Connections = new List<FlowchartConnection>
                {
                    new() { SourceNodeId = "start", TargetNodeId = "process1" },
                    new() { SourceNodeId = "process1", TargetNodeId = "decision1" },
                    new() { SourceNodeId = "decision1", TargetNodeId = "process2", Label = "No" },
                    new() { SourceNodeId = "process2", TargetNodeId = "decision1" },
                    new() { SourceNodeId = "decision1", TargetNodeId = "end", Label = "Yes" }
                }
            },
            new()
            {
                Id = "manufacturing-process-template",
                Name = "Manufacturing Process Template",
                Description = "Template for manufacturing work instructions",
                Nodes = new List<FlowchartNode>
                {
                    new() { Id = "start", Text = "Start", Type = FlowchartNodeType.Start, X = 100, Y = 50 },
                    new() { Id = "setup", Text = "Setup Equipment", Type = FlowchartNodeType.Process, X = 100, Y = 120 },
                    new() { Id = "check", Text = "Pre-Check", Type = FlowchartNodeType.Decision, X = 100, Y = 190 },
                    new() { Id = "process", Text = "Manufacturing", Type = FlowchartNodeType.Process, X = 100, Y = 260 },
                    new() { Id = "inspect", Text = "Quality Inspection", Type = FlowchartNodeType.Decision, X = 100, Y = 330 },
                    new() { Id = "rework", Text = "Rework", Type = FlowchartNodeType.Process, X = 250, Y = 330 },
                    new() { Id = "document", Text = "Document Results", Type = FlowchartNodeType.Document, X = 100, Y = 400 },
                    new() { Id = "end", Text = "End", Type = FlowchartNodeType.End, X = 100, Y = 470 }
                },
                Connections = new List<FlowchartConnection>
                {
                    new() { SourceNodeId = "start", TargetNodeId = "setup" },
                    new() { SourceNodeId = "setup", TargetNodeId = "check" },
                    new() { SourceNodeId = "check", TargetNodeId = "process", Label = "Pass" },
                    new() { SourceNodeId = "check", TargetNodeId = "setup", Label = "Fail" },
                    new() { SourceNodeId = "process", TargetNodeId = "inspect" },
                    new() { SourceNodeId = "inspect", TargetNodeId = "rework", Label = "Fail" },
                    new() { SourceNodeId = "rework", TargetNodeId = "inspect" },
                    new() { SourceNodeId = "inspect", TargetNodeId = "document", Label = "Pass" },
                    new() { SourceNodeId = "document", TargetNodeId = "end" }
                }
            }
        };
    }
}