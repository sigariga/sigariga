using WorkInstructionCreator.Models;

namespace WorkInstructionCreator.Services;

public interface IFlowchartService
{
    Task<List<ProcessFlowchart>> GetAllFlowchartsAsync();
    Task<ProcessFlowchart?> GetFlowchartByIdAsync(string id);
    Task<ProcessFlowchart> CreateFlowchartAsync(ProcessFlowchart flowchart);
    Task<ProcessFlowchart> UpdateFlowchartAsync(ProcessFlowchart flowchart);
    Task<bool> DeleteFlowchartAsync(string id);
    Task<byte[]> ExportFlowchartToImageAsync(ProcessFlowchart flowchart);
    Task<List<ProcessFlowchart>> GetBaseFlowchartsAsync();
}