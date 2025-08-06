using WorkInstructionCreator.Models;

namespace WorkInstructionCreator.Services;

public interface IDocumentExportService
{
    Task<string> ExportToWordAsync(WorkInstruction workInstruction, string outputPath);
    Task<string> ExportToPdfAsync(WorkInstruction workInstruction, string outputPath);
    Task<byte[]> GenerateWordDocumentAsync(WorkInstruction workInstruction);
    Task<byte[]> GeneratePdfDocumentAsync(WorkInstruction workInstruction);
    Task<bool> IsWordAvailableAsync();
    Task<string> PreviewHtmlAsync(WorkInstruction workInstruction);
}

public class ExportSettings
{
    public bool IncludeFlowchart { get; set; } = true;
    public bool IncludeMetadata { get; set; } = true;
    public bool IncludeTableOfContents { get; set; } = false;
    public string CompanyLogo { get; set; } = string.Empty;
    public string CompanyName { get; set; } = string.Empty;
    public string DocumentTemplate { get; set; } = "Standard";
    public Dictionary<string, object> CustomSettings { get; set; } = new();
}