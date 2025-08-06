using Newtonsoft.Json;
using WorkInstructionCreator.Models;

namespace WorkInstructionCreator.Services;

public class ContentLibraryService : IContentLibraryService
{
    private readonly string _contentPath;
    private List<WorkContentItem> _contentItems = new();

    public ContentLibraryService()
    {
        _contentPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "WorkInstructionCreator", "Content");
        Directory.CreateDirectory(_contentPath);
        _ = InitializeBuiltInContentAsync();
    }

    public async Task<List<WorkContentItem>> GetAllContentAsync()
    {
        await LoadContentAsync();
        return _contentItems.ToList();
    }

    public async Task<WorkContentItem?> GetContentByIdAsync(string id)
    {
        await LoadContentAsync();
        return _contentItems.FirstOrDefault(c => c.Id == id);
    }

    public async Task<List<WorkContentItem>> GetContentByCategoryAsync(string category)
    {
        await LoadContentAsync();
        return _contentItems.Where(c => c.Category.Equals(category, StringComparison.OrdinalIgnoreCase)).ToList();
    }

    public async Task<List<WorkContentItem>> GetContentByTypeAsync(ContentType type)
    {
        await LoadContentAsync();
        return _contentItems.Where(c => c.Type == type).ToList();
    }

    public async Task<List<WorkContentItem>> SearchContentAsync(string searchTerm)
    {
        await LoadContentAsync();
        return _contentItems.Where(c => 
            c.Title.Contains(searchTerm, StringComparison.OrdinalIgnoreCase) ||
            c.Description.Contains(searchTerm, StringComparison.OrdinalIgnoreCase) ||
            c.Content.Contains(searchTerm, StringComparison.OrdinalIgnoreCase) ||
            c.Tags.Any(t => t.Contains(searchTerm, StringComparison.OrdinalIgnoreCase))
        ).ToList();
    }

    public async Task<WorkContentItem> CreateContentAsync(WorkContentItem content)
    {
        content.Id = Guid.NewGuid().ToString();
        content.CreatedDate = DateTime.Now;
        
        await LoadContentAsync();
        _contentItems.Add(content);
        await SaveContentAsync();
        
        return content;
    }

    public async Task<WorkContentItem> UpdateContentAsync(WorkContentItem content)
    {
        await LoadContentAsync();
        var existingContent = _contentItems.FirstOrDefault(c => c.Id == content.Id);
        if (existingContent != null)
        {
            var index = _contentItems.IndexOf(existingContent);
            _contentItems[index] = content;
            await SaveContentAsync();
        }
        return content;
    }

    public async Task<bool> DeleteContentAsync(string id)
    {
        await LoadContentAsync();
        var content = _contentItems.FirstOrDefault(c => c.Id == id);
        if (content != null)
        {
            _contentItems.Remove(content);
            await SaveContentAsync();
            return true;
        }
        return false;
    }

    public async Task<List<string>> GetCategoriesAsync()
    {
        await LoadContentAsync();
        return _contentItems.Select(c => c.Category).Distinct().OrderBy(c => c).ToList();
    }

    public async Task InitializeBuiltInContentAsync()
    {
        await LoadContentAsync();
        
        if (!_contentItems.Any())
        {
            var builtInContent = CreateBuiltInContent();
            _contentItems.AddRange(builtInContent);
            await SaveContentAsync();
        }
    }

    private async Task LoadContentAsync()
    {
        var filePath = Path.Combine(_contentPath, "content.json");
        if (File.Exists(filePath))
        {
            try
            {
                var json = await File.ReadAllTextAsync(filePath);
                var content = JsonConvert.DeserializeObject<List<WorkContentItem>>(json);
                if (content != null)
                    _contentItems = content;
            }
            catch
            {
                _contentItems = new List<WorkContentItem>();
            }
        }
    }

    private async Task SaveContentAsync()
    {
        var filePath = Path.Combine(_contentPath, "content.json");
        var json = JsonConvert.SerializeObject(_contentItems, Formatting.Indented);
        await File.WriteAllTextAsync(filePath, json);
    }

    private List<WorkContentItem> CreateBuiltInContent()
    {
        return new List<WorkContentItem>
        {
            new()
            {
                Title = "Personal Protective Equipment (PPE)",
                Description = "Standard PPE requirements for manufacturing operations",
                Category = "Safety",
                Type = ContentType.SafetyNote,
                Content = @"<div class='safety-note'>
                    <h3>Required PPE:</h3>
                    <ul>
                        <li>Safety glasses with side shields</li>
                        <li>Hard hat (Class C minimum)</li>
                        <li>Steel-toed safety boots</li>
                        <li>High-visibility vest</li>
                        <li>Cut-resistant gloves (Level 3 minimum)</li>
                    </ul>
                    <p><strong>Note:</strong> Additional PPE may be required based on specific task hazards.</p>
                </div>",
                Tags = new List<string> { "PPE", "Safety", "Protection", "Equipment" }
            },
            new()
            {
                Title = "Lockout/Tagout Procedure",
                Description = "Standard LOTO procedure for equipment maintenance",
                Category = "Safety",
                Type = ContentType.Procedure,
                Content = @"<div class='procedure'>
                    <h3>Lockout/Tagout Steps:</h3>
                    <ol>
                        <li>Notify all affected personnel</li>
                        <li>Identify all energy sources</li>
                        <li>Shut down equipment properly</li>
                        <li>Isolate energy sources</li>
                        <li>Apply lockout devices</li>
                        <li>Verify zero energy state</li>
                        <li>Test equipment controls</li>
                    </ol>
                </div>",
                Tags = new List<string> { "LOTO", "Safety", "Maintenance", "Procedure" }
            },
            new()
            {
                Title = "Quality Inspection Checklist",
                Description = "Standard quality checkpoints for manufactured parts",
                Category = "Quality",
                Type = ContentType.Checklist,
                Content = @"<div class='checklist'>
                    <h3>Quality Inspection Points:</h3>
                    <ul>
                        <li>☐ Dimensional accuracy within tolerance</li>
                        <li>☐ Surface finish meets specification</li>
                        <li>☐ No visible defects or damage</li>
                        <li>☐ Material certification verified</li>
                        <li>☐ Part markings clearly visible</li>
                        <li>☐ Documentation complete</li>
                    </ul>
                </div>",
                Tags = new List<string> { "Quality", "Inspection", "Checklist", "Manufacturing" }
            },
            new()
            {
                Title = "Standard Tools and Equipment",
                Description = "Common tools required for assembly operations",
                Category = "Equipment",
                Type = ContentType.Equipment,
                Content = @"<div class='equipment-list'>
                    <h3>Required Tools:</h3>
                    <table>
                        <tr><th>Tool</th><th>Size/Type</th><th>Purpose</th></tr>
                        <tr><td>Torque Wrench</td><td>10-100 Nm</td><td>Bolt tightening</td></tr>
                        <tr><td>Digital Caliper</td><td>0-150mm</td><td>Dimension measurement</td></tr>
                        <tr><td>Multimeter</td><td>Digital</td><td>Electrical testing</td></tr>
                        <tr><td>Allen Key Set</td><td>Metric</td><td>Fastener adjustment</td></tr>
                    </table>
                </div>",
                Tags = new List<string> { "Tools", "Equipment", "Assembly", "Manufacturing" }
            },
            new()
            {
                Title = "Environmental Conditions",
                Description = "Standard environmental requirements for operations",
                Category = "Environment",
                Type = ContentType.Text,
                Content = @"<div class='environment-conditions'>
                    <h3>Required Conditions:</h3>
                    <ul>
                        <li>Temperature: 18-24°C (64-75°F)</li>
                        <li>Humidity: 40-60% RH</li>
                        <li>Lighting: Minimum 500 lux at work surface</li>
                        <li>Ventilation: 6-8 air changes per hour</li>
                        <li>Noise Level: <85 dB(A) TWA</li>
                    </ul>
                </div>",
                Tags = new List<string> { "Environment", "Conditions", "Temperature", "Humidity" }
            },
            new()
            {
                Title = "Emergency Procedures",
                Description = "Standard emergency response procedures",
                Category = "Safety",
                Type = ContentType.WarningNote,
                Content = @"<div class='warning-note'>
                    <h3>Emergency Contacts:</h3>
                    <ul>
                        <li>Emergency Services: 911</li>
                        <li>Plant Security: Ext. 2000</li>
                        <li>First Aid: Ext. 2001</li>
                        <li>Maintenance: Ext. 2002</li>
                    </ul>
                    <h3>In Case of Emergency:</h3>
                    <ol>
                        <li>Ensure personal safety first</li>
                        <li>Alert others in the area</li>
                        <li>Call appropriate emergency number</li>
                        <li>Provide first aid if qualified</li>
                        <li>Report to supervisor immediately</li>
                    </ol>
                </div>",
                Tags = new List<string> { "Emergency", "Safety", "Procedures", "Response" }
            }
        };
    }
}