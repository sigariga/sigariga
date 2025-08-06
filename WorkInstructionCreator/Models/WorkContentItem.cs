using System.ComponentModel;

namespace WorkInstructionCreator.Models;

public class WorkContentItem : INotifyPropertyChanged
{
    private string _title = string.Empty;
    private string _description = string.Empty;
    private string _content = string.Empty;
    private string _category = string.Empty;

    public string Id { get; set; } = Guid.NewGuid().ToString();

    public string Title
    {
        get => _title;
        set
        {
            _title = value;
            OnPropertyChanged(nameof(Title));
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

    public string Content
    {
        get => _content;
        set
        {
            _content = value;
            OnPropertyChanged(nameof(Content));
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

    public ContentType Type { get; set; } = ContentType.Text;
    public DateTime CreatedDate { get; set; } = DateTime.Now;
    public string Author { get; set; } = Environment.UserName;
    public List<string> Tags { get; set; } = new();
    public string IconPath { get; set; } = string.Empty;
    public Dictionary<string, object> Metadata { get; set; } = new();

    public event PropertyChangedEventHandler? PropertyChanged;

    protected virtual void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}

public enum ContentType
{
    Text,
    RichText,
    Image,
    Table,
    List,
    Checklist,
    SafetyNote,
    WarningNote,
    Procedure,
    Equipment,
    Material
}