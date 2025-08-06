using System.Text;
using WorkInstructionCreator.Models;
using iTextSharp.text;
using iTextSharp.text.pdf;
using iTextSharp.text.html.simpleparser;

namespace WorkInstructionCreator.Services;

public class DocumentExportService : IDocumentExportService
{
    public async Task<string> ExportToWordAsync(WorkInstruction workInstruction, string outputPath)
    {
        try
        {
            // Try to use Microsoft Word COM object if available
            if (await IsWordAvailableAsync())
            {
                return await ExportToWordWithComAsync(workInstruction, outputPath);
            }
            else
            {
                // Fallback to HTML-based export
                return await ExportToHtmlAsync(workInstruction, outputPath);
            }
        }
        catch (Exception ex)
        {
            throw new InvalidOperationException($"Failed to export to Word: {ex.Message}", ex);
        }
    }

    public async Task<string> ExportToPdfAsync(WorkInstruction workInstruction, string outputPath)
    {
        try
        {
            var pdfBytes = await GeneratePdfDocumentAsync(workInstruction);
            await File.WriteAllBytesAsync(outputPath, pdfBytes);
            return outputPath;
        }
        catch (Exception ex)
        {
            throw new InvalidOperationException($"Failed to export to PDF: {ex.Message}", ex);
        }
    }

    public async Task<byte[]> GenerateWordDocumentAsync(WorkInstruction workInstruction)
    {
        var html = await PreviewHtmlAsync(workInstruction);
        return Encoding.UTF8.GetBytes(html);
    }

    public async Task<byte[]> GeneratePdfDocumentAsync(WorkInstruction workInstruction)
    {
        using var memoryStream = new MemoryStream();
        var document = new Document(PageSize.A4, 50, 50, 50, 50);
        var writer = PdfWriter.GetInstance(document, memoryStream);
        
        document.Open();
        
        // Add title
        var titleFont = FontFactory.GetFont(FontFactory.HELVETICA_BOLD, 18, BaseColor.BLACK);
        var title = new Paragraph(workInstruction.Title, titleFont)
        {
            Alignment = Element.ALIGN_CENTER,
            SpacingAfter = 20
        };
        document.Add(title);
        
        // Add metadata
        var metadataFont = FontFactory.GetFont(FontFactory.HELVETICA, 10, BaseColor.GRAY);
        var metadata = new Paragraph($"Author: {workInstruction.Author} | Version: {workInstruction.Version} | Created: {workInstruction.CreatedDate:yyyy-MM-dd}", metadataFont)
        {
            Alignment = Element.ALIGN_CENTER,
            SpacingAfter = 20
        };
        document.Add(metadata);
        
        // Add description if available
        if (!string.IsNullOrWhiteSpace(workInstruction.Description))
        {
            var descriptionFont = FontFactory.GetFont(FontFactory.HELVETICA, 12, BaseColor.BLACK);
            var description = new Paragraph(workInstruction.Description, descriptionFont)
            {
                SpacingAfter = 15
            };
            document.Add(description);
        }
        
        // Add content
        if (!string.IsNullOrWhiteSpace(workInstruction.Content))
        {
            try
            {
                // Simple HTML to PDF conversion
                var htmlContent = workInstruction.Content;
                var styles = new StyleSheet();
                styles.LoadTagStyle("body", "font", "helvetica");
                styles.LoadTagStyle("body", "size", "12px");
                
                var htmlElements = HTMLWorker.ParseToList(new StringReader(htmlContent), styles);
                foreach (var element in htmlElements)
                {
                    document.Add(element);
                }
            }
            catch
            {
                // Fallback to plain text if HTML parsing fails
                var contentFont = FontFactory.GetFont(FontFactory.HELVETICA, 11, BaseColor.BLACK);
                var content = new Paragraph(StripHtml(workInstruction.Content), contentFont);
                document.Add(content);
            }
        }
        
        // Add flowchart info if available
        if (workInstruction.Flowchart != null)
        {
            document.NewPage();
            var flowchartTitle = new Paragraph("Process Flowchart", FontFactory.GetFont(FontFactory.HELVETICA_BOLD, 14, BaseColor.BLACK))
            {
                SpacingBefore = 20,
                SpacingAfter = 10
            };
            document.Add(flowchartTitle);
            
            var flowchartDesc = new Paragraph($"Flowchart: {workInstruction.Flowchart.Name}", FontFactory.GetFont(FontFactory.HELVETICA, 11, BaseColor.BLACK));
            document.Add(flowchartDesc);
            
            if (!string.IsNullOrWhiteSpace(workInstruction.Flowchart.Description))
            {
                var flowchartDescDetail = new Paragraph(workInstruction.Flowchart.Description, FontFactory.GetFont(FontFactory.HELVETICA, 10, BaseColor.BLACK));
                document.Add(flowchartDescDetail);
            }
        }
        
        document.Close();
        writer.Close();
        
        await Task.CompletedTask;
        return memoryStream.ToArray();
    }

    public async Task<bool> IsWordAvailableAsync()
    {
        try
        {
            // Check if Microsoft Word is available
            await Task.CompletedTask;
            return false; // For simplicity, returning false to use HTML export
        }
        catch
        {
            return false;
        }
    }

    public async Task<string> PreviewHtmlAsync(WorkInstruction workInstruction)
    {
        var html = new StringBuilder();
        
        html.AppendLine("<!DOCTYPE html>");
        html.AppendLine("<html>");
        html.AppendLine("<head>");
        html.AppendLine("    <meta charset='utf-8'>");
        html.AppendLine($"    <title>{workInstruction.Title}</title>");
        html.AppendLine("    <style>");
        html.AppendLine(GetDefaultCss());
        html.AppendLine("    </style>");
        html.AppendLine("</head>");
        html.AppendLine("<body>");
        
        // Header
        html.AppendLine("    <div class='header'>");
        html.AppendLine($"        <h1>{workInstruction.Title}</h1>");
        html.AppendLine("        <div class='metadata'>");
        html.AppendLine($"            <span>Author: {workInstruction.Author}</span> | ");
        html.AppendLine($"            <span>Version: {workInstruction.Version}</span> | ");
        html.AppendLine($"            <span>Created: {workInstruction.CreatedDate:yyyy-MM-dd}</span>");
        if (workInstruction.LastModified != workInstruction.CreatedDate)
        {
            html.AppendLine($" | <span>Modified: {workInstruction.LastModified:yyyy-MM-dd}</span>");
        }
        html.AppendLine("        </div>");
        html.AppendLine("    </div>");
        
        // Description
        if (!string.IsNullOrWhiteSpace(workInstruction.Description))
        {
            html.AppendLine("    <div class='section'>");
            html.AppendLine("        <h2>Description</h2>");
            html.AppendLine($"        <p>{workInstruction.Description}</p>");
            html.AppendLine("    </div>");
        }
        
        // Main content
        if (!string.IsNullOrWhiteSpace(workInstruction.Content))
        {
            html.AppendLine("    <div class='section'>");
            html.AppendLine("        <h2>Work Instruction</h2>");
            html.AppendLine($"        <div class='content'>{workInstruction.Content}</div>");
            html.AppendLine("    </div>");
        }
        
        // Flowchart information
        if (workInstruction.Flowchart != null)
        {
            html.AppendLine("    <div class='section'>");
            html.AppendLine("        <h2>Process Flow</h2>");
            html.AppendLine($"        <h3>{workInstruction.Flowchart.Name}</h3>");
            if (!string.IsNullOrWhiteSpace(workInstruction.Flowchart.Description))
            {
                html.AppendLine($"        <p>{workInstruction.Flowchart.Description}</p>");
            }
            html.AppendLine("        <p><em>Flowchart visualization would be rendered here in the application.</em></p>");
            html.AppendLine("    </div>");
        }
        
        // Content items
        if (workInstruction.ContentItems.Any())
        {
            html.AppendLine("    <div class='section'>");
            html.AppendLine("        <h2>Additional Content</h2>");
            foreach (var item in workInstruction.ContentItems)
            {
                html.AppendLine("        <div class='content-item'>");
                html.AppendLine($"            <h4>{item.Title}</h4>");
                if (!string.IsNullOrWhiteSpace(item.Description))
                {
                    html.AppendLine($"            <p class='item-description'>{item.Description}</p>");
                }
                html.AppendLine($"            <div class='item-content'>{item.Content}</div>");
                html.AppendLine("        </div>");
            }
            html.AppendLine("    </div>");
        }
        
        // Footer
        html.AppendLine("    <div class='footer'>");
        html.AppendLine($"        <p>Generated by Work Instruction Creator on {DateTime.Now:yyyy-MM-dd HH:mm}</p>");
        html.AppendLine("    </div>");
        
        html.AppendLine("</body>");
        html.AppendLine("</html>");
        
        await Task.CompletedTask;
        return html.ToString();
    }

    private async Task<string> ExportToWordWithComAsync(WorkInstruction workInstruction, string outputPath)
    {
        // This would implement Microsoft Word COM automation
        // For now, fall back to HTML export
        return await ExportToHtmlAsync(workInstruction, outputPath);
    }

    private async Task<string> ExportToHtmlAsync(WorkInstruction workInstruction, string outputPath)
    {
        var html = await PreviewHtmlAsync(workInstruction);
        var htmlPath = Path.ChangeExtension(outputPath, ".html");
        await File.WriteAllTextAsync(htmlPath, html);
        return htmlPath;
    }

    private string GetDefaultCss()
    {
        return @"
            body { font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; color: #333; }
            .header { border-bottom: 2px solid #007ACC; padding-bottom: 20px; margin-bottom: 30px; }
            .header h1 { color: #007ACC; margin: 0; font-size: 28px; }
            .metadata { color: #666; font-size: 12px; margin-top: 10px; }
            .section { margin-bottom: 30px; }
            .section h2 { color: #007ACC; border-bottom: 1px solid #ddd; padding-bottom: 5px; }
            .content { margin: 15px 0; }
            .content-item { border: 1px solid #eee; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .item-description { font-style: italic; color: #666; }
            .safety-note { background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; }
            .warning-note { background-color: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; border-radius: 5px; }
            .checklist ul { list-style-type: none; padding-left: 0; }
            .checklist li { margin: 5px 0; }
            .footer { border-top: 1px solid #ddd; padding-top: 20px; margin-top: 40px; text-align: center; color: #666; font-size: 12px; }
            table { border-collapse: collapse; width: 100%; margin: 10px 0; }
            table th, table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            table th { background-color: #f2f2f2; font-weight: bold; }
        ";
    }

    private string StripHtml(string html)
    {
        return System.Text.RegularExpressions.Regex.Replace(html, "<.*?>", string.Empty);
    }
}