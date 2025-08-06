using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System.Collections.ObjectModel;
using WorkInstructionCreator.Models;
using WorkInstructionCreator.Services;

namespace WorkInstructionCreator.ViewModels;

public partial class ContentLibraryViewModel : ObservableObject
{
    private readonly IContentLibraryService _contentLibraryService;

    [ObservableProperty]
    private WorkContentItem? _selectedContent;

    [ObservableProperty]
    private string _searchText = string.Empty;

    [ObservableProperty]
    private string _selectedCategory = "All";

    [ObservableProperty]
    private ContentType _selectedContentType = ContentType.Text;

    [ObservableProperty]
    private bool _isLoading = false;

    [ObservableProperty]
    private string _previewContent = string.Empty;

    public ObservableCollection<WorkContentItem> ContentItems { get; } = new();
    public ObservableCollection<WorkContentItem> FilteredContentItems { get; } = new();
    public ObservableCollection<string> Categories { get; } = new();

    public event Action<WorkContentItem>? ContentSelected;

    public ContentType[] ContentTypes { get; } = Enum.GetValues<ContentType>();

    public ContentLibraryViewModel(IContentLibraryService contentLibraryService)
    {
        _contentLibraryService = contentLibraryService;
    }

    public async Task InitializeAsync()
    {
        await LoadContentAsync();
        await LoadCategoriesAsync();
    }

    [RelayCommand]
    private async Task LoadContentAsync()
    {
        try
        {
            IsLoading = true;
            var content = await _contentLibraryService.GetAllContentAsync();
            
            ContentItems.Clear();
            foreach (var item in content)
            {
                ContentItems.Add(item);
            }
            
            ApplyFilters();
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"Error loading content: {ex.Message}");
        }
        finally
        {
            IsLoading = false;
        }
    }

    [RelayCommand]
    private async Task LoadCategoriesAsync()
    {
        try
        {
            var categories = await _contentLibraryService.GetCategoriesAsync();
            
            Categories.Clear();
            Categories.Add("All");
            foreach (var category in categories)
            {
                Categories.Add(category);
            }
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"Error loading categories: {ex.Message}");
        }
    }

    [RelayCommand]
    private void SelectContent(WorkContentItem content)
    {
        SelectedContent = content;
        PreviewContent = content.Content;
        ContentSelected?.Invoke(content);
    }

    [RelayCommand]
    private void ApplyFilters()
    {
        FilteredContentItems.Clear();
        
        var filtered = ContentItems.AsEnumerable();
        
        // Filter by category
        if (SelectedCategory != "All")
        {
            filtered = filtered.Where(c => c.Category.Equals(SelectedCategory, StringComparison.OrdinalIgnoreCase));
        }
        
        // Filter by content type
        if (SelectedContentType != ContentType.Text || FilteredContentItems.Count == 0)
        {
            // Show all types if Text is selected (default) and no specific filter is applied
            // Otherwise filter by selected type
            if (SelectedContentType != ContentType.Text)
            {
                filtered = filtered.Where(c => c.Type == SelectedContentType);
            }
        }
        
        // Filter by search text
        if (!string.IsNullOrWhiteSpace(SearchText))
        {
            filtered = filtered.Where(c => 
                c.Title.Contains(SearchText, StringComparison.OrdinalIgnoreCase) ||
                c.Description.Contains(SearchText, StringComparison.OrdinalIgnoreCase) ||
                c.Tags.Any(t => t.Contains(SearchText, StringComparison.OrdinalIgnoreCase)));
        }
        
        // Group by type for better organization
        var grouped = filtered.GroupBy(c => c.Type).OrderBy(g => g.Key);
        
        foreach (var group in grouped)
        {
            foreach (var item in group.OrderBy(i => i.Title))
            {
                FilteredContentItems.Add(item);
            }
        }
    }

    partial void OnSearchTextChanged(string value)
    {
        ApplyFilters();
    }

    partial void OnSelectedCategoryChanged(string value)
    {
        ApplyFilters();
    }

    partial void OnSelectedContentTypeChanged(ContentType value)
    {
        ApplyFilters();
    }

    [RelayCommand]
    private async Task CreateNewContentAsync()
    {
        var newContent = new WorkContentItem
        {
            Title = "New Content Item",
            Description = "Custom content item",
            Category = "Custom",
            Type = ContentType.Text,
            Content = "<p>Enter your content here...</p>"
        };

        try
        {
            IsLoading = true;
            await _contentLibraryService.CreateContentAsync(newContent);
            await LoadContentAsync();
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"Error creating content: {ex.Message}");
        }
        finally
        {
            IsLoading = false;
        }
    }

    [RelayCommand]
    private async Task DeleteContentAsync(WorkContentItem content)
    {
        try
        {
            IsLoading = true;
            await _contentLibraryService.DeleteContentAsync(content.Id);
            await LoadContentAsync();
            
            if (SelectedContent?.Id == content.Id)
            {
                SelectedContent = null;
                PreviewContent = string.Empty;
            }
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"Error deleting content: {ex.Message}");
        }
        finally
        {
            IsLoading = false;
        }
    }

    [RelayCommand]
    private async Task SearchContentAsync(string searchTerm)
    {
        if (string.IsNullOrWhiteSpace(searchTerm))
        {
            await LoadContentAsync();
            return;
        }

        try
        {
            IsLoading = true;
            var searchResults = await _contentLibraryService.SearchContentAsync(searchTerm);
            
            ContentItems.Clear();
            foreach (var item in searchResults)
            {
                ContentItems.Add(item);
            }
            
            ApplyFilters();
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"Error searching content: {ex.Message}");
        }
        finally
        {
            IsLoading = false;
        }
    }

    [RelayCommand]
    private async Task FilterByTypeAsync(ContentType contentType)
    {
        try
        {
            IsLoading = true;
            var filteredContent = await _contentLibraryService.GetContentByTypeAsync(contentType);
            
            ContentItems.Clear();
            foreach (var item in filteredContent)
            {
                ContentItems.Add(item);
            }
            
            ApplyFilters();
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"Error filtering content by type: {ex.Message}");
        }
        finally
        {
            IsLoading = false;
        }
    }

    [RelayCommand]
    private void ClearPreview()
    {
        SelectedContent = null;
        PreviewContent = string.Empty;
    }

    public string GetContentTypeIcon(ContentType type)
    {
        return type switch
        {
            ContentType.Text => "📝",
            ContentType.RichText => "📄",
            ContentType.Image => "🖼️",
            ContentType.Table => "📊",
            ContentType.List => "📋",
            ContentType.Checklist => "✅",
            ContentType.SafetyNote => "⚠️",
            ContentType.WarningNote => "🚨",
            ContentType.Procedure => "📋",
            ContentType.Equipment => "🔧",
            ContentType.Material => "📦",
            _ => "📄"
        };
    }

    public string GetContentTypeColor(ContentType type)
    {
        return type switch
        {
            ContentType.SafetyNote => "#FFF3CD",
            ContentType.WarningNote => "#F8D7DA",
            ContentType.Procedure => "#E3F2FD",
            ContentType.Equipment => "#F3E5F5",
            ContentType.Material => "#E8F5E8",
            ContentType.Checklist => "#FFF8E1",
            _ => "#F8F9FA"
        };
    }
}