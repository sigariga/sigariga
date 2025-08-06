namespace WorkInstructionCreator.Services;

public interface IChatbotService
{
    Task<string> CheckWorkInstructionAsync(string content);
    Task<string> SuggestImprovementsAsync(string content);
    Task<string> ValidateTemplateAsync(string templateContent);
    Task<string> GetHelpAsync(string query);
    Task<List<string>> GetSuggestionsAsync(string partialContent);
    Task<bool> IsServiceAvailableAsync();
}

public class ChatbotResponse
{
    public string Message { get; set; } = string.Empty;
    public ChatbotResponseType Type { get; set; } = ChatbotResponseType.Information;
    public List<string> Suggestions { get; set; } = new();
    public Dictionary<string, object> Metadata { get; set; } = new();
}

public enum ChatbotResponseType
{
    Information,
    Warning,
    Error,
    Suggestion,
    Validation
}