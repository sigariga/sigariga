using System.ComponentModel;

namespace WorkInstructionCreator.Models;

public class WorkInstructionTemplate : INotifyPropertyChanged
{
    private string _name = string.Empty;
    private string _description = string.Empty;
    private string _htmlTemplate = string.Empty;
    private string _category = string.Empty;

    public string Id { get; set; } = Guid.NewGuid().ToString();

    public string Name
    {
        get => _name;
        set
        {
            _name = value;
            OnPropertyChanged(nameof(Name));
        }
    }

    public string Description
    {
        get => _description;
        set
        {
            _description = value;
            OnPropertyChanged(nameof(Description));
        }
    }

    public string HtmlTemplate
    {
        get => _htmlTemplate;
        set
        {
            _htmlTemplate = value;
            OnPropertyChanged(nameof(HtmlTemplate));
        }
    }

    public string Category
    {
        get => _category;
        set
        {
            _category = value;
            OnPropertyChanged(nameof(Category));
        }
    }

    public DateTime CreatedDate { get; set; } = DateTime.Now;
    public string Author { get; set; } = Environment.UserName;
    public List<TemplateField> Fields { get; set; } = new();
    public string PreviewImagePath { get; set; } = string.Empty;
    public bool IsBuiltIn { get; set; } = false;

    public event PropertyChangedEventHandler? PropertyChanged;

    protected virtual void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}

public class TemplateField
{
    public string Name { get; set; } = string.Empty;
    public string Type { get; set; } = "Text"; // Text, RichText, Image, Table, List
    public string Placeholder { get; set; } = string.Empty;
    public bool IsRequired { get; set; } = false;
    public string DefaultValue { get; set; } = string.Empty;
    public Dictionary<string, object> Properties { get; set; } = new();
}