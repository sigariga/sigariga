using System.ComponentModel;

namespace WorkInstructionCreator.Models;

public class WorkInstruction : INotifyPropertyChanged
{
    private string _title = string.Empty;
    private string _description = string.Empty;
    private string _content = string.Empty;
    private DateTime _createdDate = DateTime.Now;
    private DateTime _lastModified = DateTime.Now;
    private string _author = Environment.UserName;
    private string _version = "1.0";
    private WorkInstructionTemplate? _template;
    private ProcessFlowchart? _flowchart;

    public string Id { get; set; } = Guid.NewGuid().ToString();

    public string Title
    {
        get => _title;
        set
        {
            _title = value;
            OnPropertyChanged(nameof(Title));
            UpdateLastModified();
        }
    }

    public string Description
    {
        get => _description;
        set
        {
            _description = value;
            OnPropertyChanged(nameof(Description));
            UpdateLastModified();
        }
    }

    public string Content
    {
        get => _content;
        set
        {
            _content = value;
            OnPropertyChanged(nameof(Content));
            UpdateLastModified();
        }
    }

    public DateTime CreatedDate
    {
        get => _createdDate;
        set
        {
            _createdDate = value;
            OnPropertyChanged(nameof(CreatedDate));
        }
    }

    public DateTime LastModified
    {
        get => _lastModified;
        set
        {
            _lastModified = value;
            OnPropertyChanged(nameof(LastModified));
        }
    }

    public string Author
    {
        get => _author;
        set
        {
            _author = value;
            OnPropertyChanged(nameof(Author));
            UpdateLastModified();
        }
    }

    public string Version
    {
        get => _version;
        set
        {
            _version = value;
            OnPropertyChanged(nameof(Version));
            UpdateLastModified();
        }
    }

    public WorkInstructionTemplate? Template
    {
        get => _template;
        set
        {
            _template = value;
            OnPropertyChanged(nameof(Template));
            UpdateLastModified();
        }
    }

    public ProcessFlowchart? Flowchart
    {
        get => _flowchart;
        set
        {
            _flowchart = value;
            OnPropertyChanged(nameof(Flowchart));
            UpdateLastModified();
        }
    }

    public List<WorkContentItem> ContentItems { get; set; } = new();
    public List<string> Tags { get; set; } = new();
    public Dictionary<string, object> Metadata { get; set; } = new();

    private void UpdateLastModified()
    {
        LastModified = DateTime.Now;
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    protected virtual void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}