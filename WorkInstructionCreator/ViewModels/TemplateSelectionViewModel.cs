using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System.Collections.ObjectModel;
using WorkInstructionCreator.Models;
using WorkInstructionCreator.Services;

namespace WorkInstructionCreator.ViewModels;

public partial class TemplateSelectionViewModel : ObservableObject
{
    private readonly ITemplateService _templateService;

    [ObservableProperty]
    private WorkInstructionTemplate? _selectedTemplate;

    [ObservableProperty]
    private string _searchText = string.Empty;

    [ObservableProperty]
    private string _selectedCategory = "All";

    [ObservableProperty]
    private bool _isLoading = false;

    public ObservableCollection<WorkInstructionTemplate> Templates { get; } = new();
    public ObservableCollection<WorkInstructionTemplate> FilteredTemplates { get; } = new();
    public ObservableCollection<string> Categories { get; } = new();

    public event Action<WorkInstructionTemplate>? TemplateSelected;

    public TemplateSelectionViewModel(ITemplateService templateService)
    {
        _templateService = templateService;
    }

    public async Task InitializeAsync()
    {
        await LoadTemplatesAsync();
        await LoadCategoriesAsync();
    }

    [RelayCommand]
    private async Task LoadTemplatesAsync()
    {
        try
        {
            IsLoading = true;
            var templates = await _templateService.GetAllTemplatesAsync();
            
            Templates.Clear();
            foreach (var template in templates)
            {
                Templates.Add(template);
            }
            
            ApplyFilters();
        }
        catch (Exception ex)
        {
            // Handle error - in a real app, you'd show this to the user
            System.Diagnostics.Debug.WriteLine($"Error loading templates: {ex.Message}");
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
            var categories = await _templateService.GetCategoriesAsync();
            
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
    private void SelectTemplate(WorkInstructionTemplate template)
    {
        SelectedTemplate = template;
        TemplateSelected?.Invoke(template);
    }

    [RelayCommand]
    private void ApplyFilters()
    {
        FilteredTemplates.Clear();
        
        var filtered = Templates.AsEnumerable();
        
        // Filter by category
        if (SelectedCategory != "All")
        {
            filtered = filtered.Where(t => t.Category.Equals(SelectedCategory, StringComparison.OrdinalIgnoreCase));
        }
        
        // Filter by search text
        if (!string.IsNullOrWhiteSpace(SearchText))
        {
            filtered = filtered.Where(t => 
                t.Name.Contains(SearchText, StringComparison.OrdinalIgnoreCase) ||
                t.Description.Contains(SearchText, StringComparison.OrdinalIgnoreCase));
        }
        
        foreach (var template in filtered)
        {
            FilteredTemplates.Add(template);
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

    [RelayCommand]
    private async Task CreateNewTemplateAsync()
    {
        var newTemplate = new WorkInstructionTemplate
        {
            Name = "New Template",
            Description = "Custom template",
            Category = "Custom",
            HtmlTemplate = "<h1>{{Title}}</h1><p>{{Content}}</p>"
        };

        try
        {
            IsLoading = true;
            await _templateService.CreateTemplateAsync(newTemplate);
            await LoadTemplatesAsync();
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"Error creating template: {ex.Message}");
        }
        finally
        {
            IsLoading = false;
        }
    }

    [RelayCommand]
    private async Task DeleteTemplateAsync(WorkInstructionTemplate template)
    {
        if (template.IsBuiltIn)
            return; // Can't delete built-in templates

        try
        {
            IsLoading = true;
            await _templateService.DeleteTemplateAsync(template.Id);
            await LoadTemplatesAsync();
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"Error deleting template: {ex.Message}");
        }
        finally
        {
            IsLoading = false;
        }
    }
}