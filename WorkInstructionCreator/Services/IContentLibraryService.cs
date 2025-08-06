using WorkInstructionCreator.Models;

namespace WorkInstructionCreator.Services;

public interface IContentLibraryService
{
    Task<List<WorkContentItem>> GetAllContentAsync();
    Task<WorkContentItem?> GetContentByIdAsync(string id);
    Task<List<WorkContentItem>> GetContentByCategoryAsync(string category);
    Task<List<WorkContentItem>> GetContentByTypeAsync(ContentType type);
    Task<List<WorkContentItem>> SearchContentAsync(string searchTerm);
    Task<WorkContentItem> CreateContentAsync(WorkContentItem content);
    Task<WorkContentItem> UpdateContentAsync(WorkContentItem content);
    Task<bool> DeleteContentAsync(string id);
    Task<List<string>> GetCategoriesAsync();
    Task InitializeBuiltInContentAsync();
}