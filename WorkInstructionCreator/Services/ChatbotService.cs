using System.Text.RegularExpressions;

namespace WorkInstructionCreator.Services;

public class ChatbotService : IChatbotService
{
    private readonly HttpClient _httpClient;
    private const string DefaultErrorMessage = "Unable to connect to chatbot service. Using offline validation.";

    public ChatbotService(HttpClient? httpClient = null)
    {
        _httpClient = httpClient ?? new HttpClient();
    }

    public async Task<string> CheckWorkInstructionAsync(string content)
    {
        // Simulate chatbot analysis with basic rule-based checking
        var issues = new List<string>();
        
        await Task.Delay(500); // Simulate API call
        
        // Check for common issues
        if (string.IsNullOrWhiteSpace(content))
        {
            issues.Add("Content is empty or contains only whitespace.");
        }
        
        if (content.Length < 50)
        {
            issues.Add("Content appears to be too short for a complete work instruction.");
        }
        
        if (!content.Contains("safety", StringComparison.OrdinalIgnoreCase))
        {
            issues.Add("Consider adding safety information to your work instruction.");
        }
        
        if (!Regex.IsMatch(content, @"\b(step|procedure|process)\b", RegexOptions.IgnoreCase))
        {
            issues.Add("Work instruction should include clear steps or procedures.");
        }
        
        if (!Regex.IsMatch(content, @"\b(tools?|equipment|materials?)\b", RegexOptions.IgnoreCase))
        {
            issues.Add("Consider listing required tools, equipment, or materials.");
        }
        
        if (content.Split('.').Length < 3)
        {
            issues.Add("Work instruction may need more detailed explanations.");
        }
        
        if (issues.Any())
        {
            return $"⚠️ Found {issues.Count} potential issue(s):\n\n" + string.Join("\n• ", issues.Select(i => "• " + i));
        }
        
        return "✅ Work instruction looks good! No major issues detected.";
    }

    public async Task<string> SuggestImprovementsAsync(string content)
    {
        await Task.Delay(300); // Simulate API call
        
        var suggestions = new List<string>();
        
        if (!content.Contains("PPE", StringComparison.OrdinalIgnoreCase) && 
            !content.Contains("protective equipment", StringComparison.OrdinalIgnoreCase))
        {
            suggestions.Add("Add personal protective equipment (PPE) requirements");
        }
        
        if (!content.Contains("quality", StringComparison.OrdinalIgnoreCase))
        {
            suggestions.Add("Include quality control checkpoints");
        }
        
        if (!Regex.IsMatch(content, @"\b(warning|caution|danger|notice)\b", RegexOptions.IgnoreCase))
        {
            suggestions.Add("Add safety warnings or cautions where appropriate");
        }
        
        if (!content.Contains("completion", StringComparison.OrdinalIgnoreCase) && 
            !content.Contains("sign-off", StringComparison.OrdinalIgnoreCase))
        {
            suggestions.Add("Include completion verification or sign-off section");
        }
        
        if (suggestions.Any())
        {
            return "💡 Suggestions for improvement:\n\n" + string.Join("\n", suggestions.Select(s => "• " + s));
        }
        
        return "✨ Your work instruction is comprehensive!";
    }

    public async Task<string> ValidateTemplateAsync(string templateContent)
    {
        await Task.Delay(200); // Simulate API call
        
        var validationIssues = new List<string>();
        
        // Check for template placeholders
        var placeholders = Regex.Matches(templateContent, @"\{\{(\w+)\}\}");
        if (placeholders.Count == 0)
        {
            validationIssues.Add("No template placeholders found. Templates should contain {{FieldName}} placeholders.");
        }
        
        // Check for proper HTML structure
        if (templateContent.Contains("<") && !templateContent.Contains("</"))
        {
            validationIssues.Add("Possible unclosed HTML tags detected.");
        }
        
        // Check for required sections
        if (!templateContent.Contains("title", StringComparison.OrdinalIgnoreCase))
        {
            validationIssues.Add("Template should include a title section.");
        }
        
        if (validationIssues.Any())
        {
            return "❌ Template validation issues:\n\n" + string.Join("\n", validationIssues.Select(i => "• " + i));
        }
        
        return "✅ Template structure is valid.";
    }

    public async Task<string> GetHelpAsync(string query)
    {
        await Task.Delay(100); // Simulate API call
        
        var helpResponses = new Dictionary<string, string>
        {
            ["template"] = "Templates provide a structured format for your work instructions. Choose from built-in templates or create your own with placeholders like {{Title}} and {{Steps}}.",
            ["flowchart"] = "Flowcharts help visualize your process flow. Use different shapes for different types of steps: ovals for start/end, rectangles for processes, diamonds for decisions.",
            ["content"] = "The content library contains reusable elements like safety notes, equipment lists, and procedures that you can insert into your work instructions.",
            ["export"] = "You can export your completed work instructions to Word (.docx) or PDF formats using the export buttons in the toolbar.",
            ["safety"] = "Always include relevant safety information in your work instructions, including PPE requirements, hazard warnings, and emergency procedures.",
            ["quality"] = "Quality checkpoints help ensure consistency. Include inspection points, acceptance criteria, and what to do if standards aren't met.",
            ["steps"] = "Break down procedures into clear, numbered steps. Each step should be actionable and specific."
        };
        
        var lowerQuery = query.ToLowerInvariant();
        var matchingKey = helpResponses.Keys.FirstOrDefault(key => lowerQuery.Contains(key));
        
        if (matchingKey != null)
        {
            return $"ℹ️ Help with {matchingKey}:\n\n{helpResponses[matchingKey]}";
        }
        
        return "ℹ️ I can help with:\n• Templates and template creation\n• Flowcharts and process visualization\n• Content library usage\n• Export options\n• Safety considerations\n• Quality control\n• Writing effective procedures\n\nTry asking about any of these topics!";
    }

    public async Task<List<string>> GetSuggestionsAsync(string partialContent)
    {
        await Task.Delay(50); // Simulate API call
        
        var suggestions = new List<string>();
        var lowerContent = partialContent.ToLowerInvariant();
        
        if (lowerContent.Contains("step") || lowerContent.Contains("procedure"))
        {
            suggestions.AddRange(new[]
            {
                "Ensure personal safety first",
                "Verify all equipment is properly calibrated",
                "Check that all required materials are available",
                "Follow lockout/tagout procedures if applicable"
            });
        }
        
        if (lowerContent.Contains("safety") || lowerContent.Contains("ppe"))
        {
            suggestions.AddRange(new[]
            {
                "Safety glasses with side shields",
                "Cut-resistant gloves (Level 3 minimum)",
                "Steel-toed safety boots",
                "Hard hat (Class C minimum)"
            });
        }
        
        if (lowerContent.Contains("quality") || lowerContent.Contains("inspection"))
        {
            suggestions.AddRange(new[]
            {
                "Dimensional accuracy within tolerance",
                "Surface finish meets specification",
                "No visible defects or damage",
                "Documentation complete and accurate"
            });
        }
        
        if (lowerContent.Contains("tool") || lowerContent.Contains("equipment"))
        {
            suggestions.AddRange(new[]
            {
                "Torque wrench (10-100 Nm)",
                "Digital caliper (0-150mm)",
                "Multimeter (digital)",
                "Allen key set (metric)"
            });
        }
        
        return suggestions.Take(10).ToList();
    }

    public async Task<bool> IsServiceAvailableAsync()
    {
        try
        {
            // Simulate checking external service availability
            await Task.Delay(100);
            return true; // For demo purposes, always return true
        }
        catch
        {
            return false;
        }
    }
}