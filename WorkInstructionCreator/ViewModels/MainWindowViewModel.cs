using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System.Collections.ObjectModel;
using WorkInstructionCreator.Models;
using WorkInstructionCreator.Services;

namespace WorkInstructionCreator.ViewModels;

public partial class MainWindowViewModel : ObservableObject
{
    private readonly ITemplateService _templateService;
    private readonly IFlowchartService _flowchartService;
    private readonly IContentLibraryService _contentLibraryService;
    private readonly IChatbotService _chatbotService;
    private readonly IDocumentExportService _documentExportService;

    [ObservableProperty]
    private WorkInstruction _currentWorkInstruction = new();

    [ObservableProperty]
    private string _selectedTabIndex = "0";

    [ObservableProperty]
    private bool _isLoading = false;

    [ObservableProperty]
    private string _statusMessage = "Ready";

    [ObservableProperty]
    private string _chatbotResponse = string.Empty;

    [ObservableProperty]
    private bool _isChatbotVisible = false;

    public ObservableCollection<WorkInstructionTemplate> Templates { get; } = new();
    public ObservableCollection<ProcessFlowchart> Flowcharts { get; } = new();
    public ObservableCollection<WorkContentItem> ContentItems { get; } = new();
    public ObservableCollection<WorkInstruction> RecentDocuments { get; } = new();

    public EditorViewModel EditorViewModel { get; }
    public TemplateSelectionViewModel TemplateSelectionViewModel { get; }
    public FlowchartViewModel FlowchartViewModel { get; }
    public ContentLibraryViewModel ContentLibraryViewModel { get; }

    public MainWindowViewModel(
        ITemplateService templateService,
        IFlowchartService flowchartService,
        IContentLibraryService contentLibraryService,
        IChatbotService chatbotService,
        IDocumentExportService documentExportService)
    {
        _templateService = templateService;
        _flowchartService = flowchartService;
        _contentLibraryService = contentLibraryService;
        _chatbotService = chatbotService;
        _documentExportService = documentExportService;

        // Initialize child view models
        EditorViewModel = new EditorViewModel();
        TemplateSelectionViewModel = new TemplateSelectionViewModel(_templateService);
        FlowchartViewModel = new FlowchartViewModel(_flowchartService);
        ContentLibraryViewModel = new ContentLibraryViewModel(_contentLibraryService);

        // Subscribe to events
        TemplateSelectionViewModel.TemplateSelected += OnTemplateSelected;
        FlowchartViewModel.FlowchartSelected += OnFlowchartSelected;
        ContentLibraryViewModel.ContentSelected += OnContentSelected;
        EditorViewModel.ContentChanged += OnEditorContentChanged;

        _ = InitializeAsync();
    }

    [RelayCommand]
    private async Task NewDocumentAsync()
    {
        CurrentWorkInstruction = new WorkInstruction();
        EditorViewModel.Content = string.Empty;
        StatusMessage = "New document created";
    }

    [RelayCommand]
    private async Task OpenDocumentAsync()
    {
        // In a real application, this would show a file dialog
        StatusMessage = "Open functionality would be implemented here";
        await Task.CompletedTask;
    }

    [RelayCommand]
    private async Task SaveDocumentAsync()
    {
        try
        {
            IsLoading = true;
            CurrentWorkInstruction.Content = EditorViewModel.Content;
            // In a real application, this would save to a file or database
            StatusMessage = "Document saved successfully";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error saving document: {ex.Message}";
        }
        finally
        {
            IsLoading = false;
        }
    }

    [RelayCommand]
    private async Task ExportToPdfAsync()
    {
        try
        {
            IsLoading = true;
            StatusMessage = "Exporting to PDF...";
            
            CurrentWorkInstruction.Content = EditorViewModel.Content;
            var documentsPath = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
            var fileName = $"{CurrentWorkInstruction.Title}_{DateTime.Now:yyyyMMdd_HHmmss}.pdf";
            var filePath = Path.Combine(documentsPath, fileName);
            
            await _documentExportService.ExportToPdfAsync(CurrentWorkInstruction, filePath);
            StatusMessage = $"PDF exported to: {filePath}";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error exporting PDF: {ex.Message}";
        }
        finally
        {
            IsLoading = false;
        }
    }

    [RelayCommand]
    private async Task ExportToWordAsync()
    {
        try
        {
            IsLoading = true;
            StatusMessage = "Exporting to Word...";
            
            CurrentWorkInstruction.Content = EditorViewModel.Content;
            var documentsPath = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
            var fileName = $"{CurrentWorkInstruction.Title}_{DateTime.Now:yyyyMMdd_HHmmss}.docx";
            var filePath = Path.Combine(documentsPath, fileName);
            
            await _documentExportService.ExportToWordAsync(CurrentWorkInstruction, filePath);
            StatusMessage = $"Word document exported to: {filePath}";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error exporting Word document: {ex.Message}";
        }
        finally
        {
            IsLoading = false;
        }
    }

    [RelayCommand]
    private async Task CheckWithChatbotAsync()
    {
        try
        {
            IsLoading = true;
            IsChatbotVisible = true;
            ChatbotResponse = "Analyzing content...";
            
            var response = await _chatbotService.CheckWorkInstructionAsync(EditorViewModel.Content);
            ChatbotResponse = response;
        }
        catch (Exception ex)
        {
            ChatbotResponse = $"Error checking content: {ex.Message}";
        }
        finally
        {
            IsLoading = false;
        }
    }

    [RelayCommand]
    private async Task GetChatbotSuggestionsAsync()
    {
        try
        {
            IsLoading = true;
            IsChatbotVisible = true;
            ChatbotResponse = "Generating suggestions...";
            
            var response = await _chatbotService.SuggestImprovementsAsync(EditorViewModel.Content);
            ChatbotResponse = response;
        }
        catch (Exception ex)
        {
            ChatbotResponse = $"Error getting suggestions: {ex.Message}";
        }
        finally
        {
            IsLoading = false;
        }
    }

    [RelayCommand]
    private void ToggleChatbot()
    {
        IsChatbotVisible = !IsChatbotVisible;
    }

    [RelayCommand]
    private async Task PreviewDocumentAsync()
    {
        try
        {
            CurrentWorkInstruction.Content = EditorViewModel.Content;
            var html = await _documentExportService.PreviewHtmlAsync(CurrentWorkInstruction);
            
            // In a real application, this would show the preview in a dialog or separate window
            StatusMessage = "Preview generated (would display in preview window)";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error generating preview: {ex.Message}";
        }
    }

    private async Task InitializeAsync()
    {
        try
        {
            IsLoading = true;
            StatusMessage = "Loading application data...";

            // Load templates
            var templates = await _templateService.GetAllTemplatesAsync();
            Templates.Clear();
            foreach (var template in templates)
            {
                Templates.Add(template);
            }

            // Load flowcharts
            var flowcharts = await _flowchartService.GetAllFlowchartsAsync();
            Flowcharts.Clear();
            foreach (var flowchart in flowcharts)
            {
                Flowcharts.Add(flowchart);
            }

            // Load content items
            var contentItems = await _contentLibraryService.GetAllContentAsync();
            ContentItems.Clear();
            foreach (var item in contentItems)
            {
                ContentItems.Add(item);
            }

            // Initialize child view models
            await TemplateSelectionViewModel.InitializeAsync();
            await FlowchartViewModel.InitializeAsync();
            await ContentLibraryViewModel.InitializeAsync();

            StatusMessage = "Ready";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error initializing application: {ex.Message}";
        }
        finally
        {
            IsLoading = false;
        }
    }

    private void OnTemplateSelected(WorkInstructionTemplate template)
    {
        CurrentWorkInstruction.Template = template;
        
        // Apply template to editor
        if (!string.IsNullOrWhiteSpace(template.HtmlTemplate))
        {
            EditorViewModel.Content = template.HtmlTemplate;
            StatusMessage = $"Template '{template.Name}' applied";
        }
    }

    private void OnFlowchartSelected(ProcessFlowchart flowchart)
    {
        CurrentWorkInstruction.Flowchart = flowchart;
        StatusMessage = $"Flowchart '{flowchart.Name}' selected";
    }

    private void OnContentSelected(WorkContentItem content)
    {
        // Insert content into editor at cursor position
        EditorViewModel.InsertContent(content.Content);
        StatusMessage = $"Content '{content.Title}' inserted";
    }

    private void OnEditorContentChanged(string content)
    {
        CurrentWorkInstruction.Content = content;
    }
}