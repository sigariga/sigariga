using Newtonsoft.Json;
using WorkInstructionCreator.Models;

namespace WorkInstructionCreator.Services;

public class TemplateService : ITemplateService
{
    private readonly string _templatesPath;
    private List<WorkInstructionTemplate> _templates = new();

    public TemplateService()
    {
        _templatesPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "WorkInstructionCreator", "Templates");
        Directory.CreateDirectory(_templatesPath);
        _ = InitializeBuiltInTemplatesAsync();
    }

    public async Task<List<WorkInstructionTemplate>> GetAllTemplatesAsync()
    {
        await LoadTemplatesAsync();
        return _templates.ToList();
    }

    public async Task<WorkInstructionTemplate?> GetTemplateByIdAsync(string id)
    {
        await LoadTemplatesAsync();
        return _templates.FirstOrDefault(t => t.Id == id);
    }

    public async Task<List<WorkInstructionTemplate>> GetTemplatesByCategoryAsync(string category)
    {
        await LoadTemplatesAsync();
        return _templates.Where(t => t.Category.Equals(category, StringComparison.OrdinalIgnoreCase)).ToList();
    }

    public async Task<WorkInstructionTemplate> CreateTemplateAsync(WorkInstructionTemplate template)
    {
        template.Id = Guid.NewGuid().ToString();
        template.CreatedDate = DateTime.Now;
        
        await LoadTemplatesAsync();
        _templates.Add(template);
        await SaveTemplatesAsync();
        
        return template;
    }

    public async Task<WorkInstructionTemplate> UpdateTemplateAsync(WorkInstructionTemplate template)
    {
        await LoadTemplatesAsync();
        var existingTemplate = _templates.FirstOrDefault(t => t.Id == template.Id);
        if (existingTemplate != null)
        {
            var index = _templates.IndexOf(existingTemplate);
            _templates[index] = template;
            await SaveTemplatesAsync();
        }
        return template;
    }

    public async Task<bool> DeleteTemplateAsync(string id)
    {
        await LoadTemplatesAsync();
        var template = _templates.FirstOrDefault(t => t.Id == id);
        if (template != null && !template.IsBuiltIn)
        {
            _templates.Remove(template);
            await SaveTemplatesAsync();
            return true;
        }
        return false;
    }

    public async Task<List<string>> GetCategoriesAsync()
    {
        await LoadTemplatesAsync();
        return _templates.Select(t => t.Category).Distinct().OrderBy(c => c).ToList();
    }

    public async Task InitializeBuiltInTemplatesAsync()
    {
        await LoadTemplatesAsync();
        
        if (!_templates.Any(t => t.IsBuiltIn))
        {
            var builtInTemplates = CreateBuiltInTemplates();
            _templates.AddRange(builtInTemplates);
            await SaveTemplatesAsync();
        }
    }

    private async Task LoadTemplatesAsync()
    {
        var filePath = Path.Combine(_templatesPath, "templates.json");
        if (File.Exists(filePath))
        {
            try
            {
                var json = await File.ReadAllTextAsync(filePath);
                var templates = JsonConvert.DeserializeObject<List<WorkInstructionTemplate>>(json);
                if (templates != null)
                    _templates = templates;
            }
            catch
            {
                _templates = new List<WorkInstructionTemplate>();
            }
        }
    }

    private async Task SaveTemplatesAsync()
    {
        var filePath = Path.Combine(_templatesPath, "templates.json");
        var json = JsonConvert.SerializeObject(_templates, Formatting.Indented);
        await File.WriteAllTextAsync(filePath, json);
    }

    private List<WorkInstructionTemplate> CreateBuiltInTemplates()
    {
        return new List<WorkInstructionTemplate>
        {
            new()
            {
                Id = "standard-procedure",
                Name = "Standard Operating Procedure",
                Description = "Basic template for standard operating procedures",
                Category = "Manufacturing",
                IsBuiltIn = true,
                HtmlTemplate = @"
                    <h1>{{Title}}</h1>
                    <h2>Purpose</h2>
                    <p>{{Purpose}}</p>
                    <h2>Scope</h2>
                    <p>{{Scope}}</p>
                    <h2>Materials Required</h2>
                    <ul>{{Materials}}</ul>
                    <h2>Safety Precautions</h2>
                    <div class='safety-note'>{{Safety}}</div>
                    <h2>Procedure Steps</h2>
                    <ol>{{Steps}}</ol>
                    <h2>Quality Checks</h2>
                    <ul>{{QualityChecks}}</ul>
                ",
                Fields = new List<TemplateField>
                {
                    new() { Name = "Title", Type = "Text", IsRequired = true, Placeholder = "Enter procedure title" },
                    new() { Name = "Purpose", Type = "RichText", IsRequired = true, Placeholder = "Describe the purpose of this procedure" },
                    new() { Name = "Scope", Type = "RichText", IsRequired = true, Placeholder = "Define the scope and applicability" },
                    new() { Name = "Materials", Type = "List", IsRequired = false, Placeholder = "List required materials and tools" },
                    new() { Name = "Safety", Type = "RichText", IsRequired = true, Placeholder = "Important safety considerations" },
                    new() { Name = "Steps", Type = "List", IsRequired = true, Placeholder = "Detailed procedure steps" },
                    new() { Name = "QualityChecks", Type = "List", IsRequired = false, Placeholder = "Quality control checkpoints" }
                }
            },
            new()
            {
                Id = "maintenance-checklist",
                Name = "Maintenance Checklist",
                Description = "Template for equipment maintenance procedures",
                Category = "Maintenance",
                IsBuiltIn = true,
                HtmlTemplate = @"
                    <h1>{{Title}}</h1>
                    <h2>Equipment Information</h2>
                    <table>
                        <tr><td><strong>Equipment ID:</strong></td><td>{{EquipmentID}}</td></tr>
                        <tr><td><strong>Model:</strong></td><td>{{Model}}</td></tr>
                        <tr><td><strong>Location:</strong></td><td>{{Location}}</td></tr>
                    </table>
                    <h2>Maintenance Tasks</h2>
                    <div class='checklist'>{{MaintenanceTasks}}</div>
                    <h2>Safety Requirements</h2>
                    <div class='safety-note'>{{SafetyRequirements}}</div>
                    <h2>Completion Sign-off</h2>
                    <p>Technician: _________________ Date: _________________</p>
                ",
                Fields = new List<TemplateField>
                {
                    new() { Name = "Title", Type = "Text", IsRequired = true, Placeholder = "Maintenance procedure title" },
                    new() { Name = "EquipmentID", Type = "Text", IsRequired = true, Placeholder = "Equipment identification number" },
                    new() { Name = "Model", Type = "Text", IsRequired = true, Placeholder = "Equipment model number" },
                    new() { Name = "Location", Type = "Text", IsRequired = true, Placeholder = "Equipment location" },
                    new() { Name = "MaintenanceTasks", Type = "Checklist", IsRequired = true, Placeholder = "List of maintenance tasks" },
                    new() { Name = "SafetyRequirements", Type = "RichText", IsRequired = true, Placeholder = "Safety requirements and PPE" }
                }
            },
            new()
            {
                Id = "quality-inspection",
                Name = "Quality Inspection Guide",
                Description = "Template for quality control and inspection procedures",
                Category = "Quality",
                IsBuiltIn = true,
                HtmlTemplate = @"
                    <h1>{{Title}}</h1>
                    <h2>Inspection Overview</h2>
                    <p>{{Overview}}</p>
                    <h2>Inspection Points</h2>
                    <table class='inspection-table'>
                        {{InspectionPoints}}
                    </table>
                    <h2>Acceptance Criteria</h2>
                    <div>{{AcceptanceCriteria}}</div>
                    <h2>Non-Conformance Actions</h2>
                    <div class='warning-note'>{{NonConformanceActions}}</div>
                    <h2>Documentation</h2>
                    <p>{{Documentation}}</p>
                ",
                Fields = new List<TemplateField>
                {
                    new() { Name = "Title", Type = "Text", IsRequired = true, Placeholder = "Inspection procedure title" },
                    new() { Name = "Overview", Type = "RichText", IsRequired = true, Placeholder = "Brief overview of the inspection" },
                    new() { Name = "InspectionPoints", Type = "Table", IsRequired = true, Placeholder = "Define inspection points and methods" },
                    new() { Name = "AcceptanceCriteria", Type = "RichText", IsRequired = true, Placeholder = "Define acceptance criteria" },
                    new() { Name = "NonConformanceActions", Type = "RichText", IsRequired = true, Placeholder = "Actions for non-conforming items" },
                    new() { Name = "Documentation", Type = "RichText", IsRequired = false, Placeholder = "Required documentation and records" }
                }
            }
        };
    }
}