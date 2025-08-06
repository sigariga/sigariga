using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

namespace WorkInstructionCreator.ViewModels;

public partial class EditorViewModel : ObservableObject
{
    [ObservableProperty]
    private string _content = string.Empty;

    [ObservableProperty]
    private bool _isBold = false;

    [ObservableProperty]
    private bool _isItalic = false;

    [ObservableProperty]
    private bool _isUnderline = false;

    [ObservableProperty]
    private string _selectedFontFamily = "Arial";

    [ObservableProperty]
    private double _selectedFontSize = 12;

    [ObservableProperty]
    private int _cursorPosition = 0;

    public event Action<string>? ContentChanged;

    public string[] FontFamilies { get; } = new[]
    {
        "Arial", "Times New Roman", "Calibri", "Verdana", "Helvetica", "Georgia", "Tahoma"
    };

    public double[] FontSizes { get; } = new[]
    {
        8.0, 9.0, 10.0, 11.0, 12.0, 14.0, 16.0, 18.0, 20.0, 24.0, 28.0, 32.0, 36.0, 48.0
    };

    partial void OnContentChanged(string value)
    {
        ContentChanged?.Invoke(value);
    }

    [RelayCommand]
    private void ToggleBold()
    {
        IsBold = !IsBold;
        ApplyFormatting("bold");
    }

    [RelayCommand]
    private void ToggleItalic()
    {
        IsItalic = !IsItalic;
        ApplyFormatting("italic");
    }

    [RelayCommand]
    private void ToggleUnderline()
    {
        IsUnderline = !IsUnderline;
        ApplyFormatting("underline");
    }

    [RelayCommand]
    private void InsertBulletList()
    {
        InsertContent("<ul><li>List item 1</li><li>List item 2</li><li>List item 3</li></ul>");
    }

    [RelayCommand]
    private void InsertNumberedList()
    {
        InsertContent("<ol><li>Step 1</li><li>Step 2</li><li>Step 3</li></ol>");
    }

    [RelayCommand]
    private void InsertTable()
    {
        var tableHtml = @"
<table border='1' style='border-collapse: collapse; width: 100%;'>
    <tr>
        <th>Header 1</th>
        <th>Header 2</th>
        <th>Header 3</th>
    </tr>
    <tr>
        <td>Cell 1</td>
        <td>Cell 2</td>
        <td>Cell 3</td>
    </tr>
    <tr>
        <td>Cell 4</td>
        <td>Cell 5</td>
        <td>Cell 6</td>
    </tr>
</table>";
        InsertContent(tableHtml);
    }

    [RelayCommand]
    private void InsertSafetyNote()
    {
        var safetyHtml = @"
<div class='safety-note' style='background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 10px 0;'>
    <h4>⚠️ Safety Notice</h4>
    <p>Enter important safety information here...</p>
</div>";
        InsertContent(safetyHtml);
    }

    [RelayCommand]
    private void InsertWarningNote()
    {
        var warningHtml = @"
<div class='warning-note' style='background-color: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; border-radius: 5px; margin: 10px 0;'>
    <h4>🔴 Warning</h4>
    <p>Enter warning information here...</p>
</div>";
        InsertContent(warningHtml);
    }

    [RelayCommand]
    private void InsertProcedureStep()
    {
        var stepHtml = @"
<div class='procedure-step' style='border-left: 4px solid #007ACC; padding-left: 15px; margin: 10px 0;'>
    <h4>Step X: [Step Title]</h4>
    <p>Detailed step description...</p>
    <ul>
        <li>Sub-step or requirement</li>
        <li>Additional notes</li>
    </ul>
</div>";
        InsertContent(stepHtml);
    }

    [RelayCommand]
    private void InsertChecklist()
    {
        var checklistHtml = @"
<div class='checklist' style='background-color: #f8f9fa; border: 1px solid #dee2e6; padding: 15px; border-radius: 5px; margin: 10px 0;'>
    <h4>✓ Checklist</h4>
    <ul style='list-style-type: none; padding-left: 0;'>
        <li>☐ Item 1</li>
        <li>☐ Item 2</li>
        <li>☐ Item 3</li>
        <li>☐ Item 4</li>
    </ul>
</div>";
        InsertContent(checklistHtml);
    }

    [RelayCommand]
    private void Undo()
    {
        // Implement undo functionality
        // This would typically interact with the rich text editor control
    }

    [RelayCommand]
    private void Redo()
    {
        // Implement redo functionality
        // This would typically interact with the rich text editor control
    }

    [RelayCommand]
    private void FindReplace()
    {
        // Show find/replace dialog
        // This would typically open a dialog window
    }

    [RelayCommand]
    private void ChangeFontFamily(string fontFamily)
    {
        SelectedFontFamily = fontFamily;
        ApplyFormatting("fontFamily", fontFamily);
    }

    [RelayCommand]
    private void ChangeFontSize(double fontSize)
    {
        SelectedFontSize = fontSize;
        ApplyFormatting("fontSize", fontSize.ToString());
    }

    public void InsertContent(string htmlContent)
    {
        if (CursorPosition >= 0 && CursorPosition <= Content.Length)
        {
            Content = Content.Insert(CursorPosition, htmlContent);
            CursorPosition += htmlContent.Length;
        }
        else
        {
            Content += htmlContent;
        }
    }

    public void ReplaceSelectedText(string newText)
    {
        // In a real implementation, this would replace currently selected text
        InsertContent(newText);
    }

    public void SetSelection(int start, int length)
    {
        // In a real implementation, this would set the selection in the editor
        CursorPosition = start;
    }

    public string GetSelectedText()
    {
        // In a real implementation, this would return the currently selected text
        return string.Empty;
    }

    private void ApplyFormatting(string formatType, string? value = null)
    {
        // In a real implementation, this would apply formatting to selected text
        // This is where you would interact with the actual rich text editor control
        
        switch (formatType)
        {
            case "bold":
                // Apply bold formatting
                break;
            case "italic":
                // Apply italic formatting
                break;
            case "underline":
                // Apply underline formatting
                break;
            case "fontFamily":
                // Apply font family
                break;
            case "fontSize":
                // Apply font size
                break;
        }
    }

    public void ClearFormatting()
    {
        IsBold = false;
        IsItalic = false;
        IsUnderline = false;
    }

    public void LoadContent(string htmlContent)
    {
        Content = htmlContent;
        CursorPosition = 0;
        ClearFormatting();
    }
}