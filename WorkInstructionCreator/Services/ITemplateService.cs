using WorkInstructionCreator.Models;

namespace WorkInstructionCreator.Services;

public interface ITemplateService
{
    Task<List<WorkInstructionTemplate>> GetAllTemplatesAsync();
    Task<WorkInstructionTemplate?> GetTemplateByIdAsync(string id);
    Task<List<WorkInstructionTemplate>> GetTemplatesByCategoryAsync(string category);
    Task<WorkInstructionTemplate> CreateTemplateAsync(WorkInstructionTemplate template);
    Task<WorkInstructionTemplate> UpdateTemplateAsync(WorkInstructionTemplate template);
    Task<bool> DeleteTemplateAsync(string id);
    Task<List<string>> GetCategoriesAsync();
    Task InitializeBuiltInTemplatesAsync();
}