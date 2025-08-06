# Work Instruction Creator

A modern Windows desktop application for creating professional work instructions with templates, flowcharts, content libraries, AI assistance, and export capabilities.

## Features

### 🎨 Modern User Interface
- Material Design-inspired interface using MaterialDesignInXaml
- Responsive layout with collapsible panels
- Dark/Light theme support
- Professional typography and iconography

### 📝 Rich Text Editor
- Word-like editing experience with formatting toolbar
- Support for tables, lists, and structured content
- Quick insertion of safety notes, warnings, and procedure steps
- Built-in templates for common work instruction elements

### 📋 Template System
- Pre-built templates for:
  - Standard Operating Procedures (SOP)
  - Maintenance Checklists
  - Quality Inspection Guides
- Custom template creation with placeholder fields
- Template categorization and search functionality
- Template preview and validation

### 🔄 Process Flowcharts
- Visual process flow creation and editing
- Multiple node types (Start, End, Process, Decision, Document, Data, Connector)
- Drag-and-drop flowchart builder
- Base flowchart templates for common processes
- Export flowcharts as images

### 📚 Content Library
- Reusable content blocks organized by category and type:
  - Safety Notes (PPE requirements, emergency procedures)
  - Equipment Lists (tools, materials, specifications)
  - Quality Checklists (inspection points, acceptance criteria)
  - Procedure Steps (standardized process elements)
- Smart search and filtering
- Content tagging system
- Content type indicators with visual styling

### 🤖 AI Assistant Integration
- Real-time content analysis and error checking
- Intelligent suggestions for improvement
- Content validation and completeness checking
- Context-aware help and guidance
- Offline fallback with rule-based validation

### 📄 Export Capabilities
- **PDF Export**: Professional document generation with styling
- **Word Export**: Microsoft Word-compatible format (.docx)
- **HTML Preview**: Web-ready format with embedded styling
- Customizable export settings and templates
- Metadata inclusion (author, version, dates)

### 🔧 Additional Features
- Document versioning and metadata tracking
- Recent documents list
- Auto-save functionality
- Multi-language support foundation
- Extensible architecture for custom integrations

## Technology Stack

- **Framework**: .NET 8 WPF (Windows Presentation Foundation)
- **UI Library**: Material Design In XAML Toolkit
- **Architecture**: MVVM with CommunityToolkit.Mvvm
- **Dependency Injection**: Microsoft.Extensions.DependencyInjection
- **Document Export**: iTextSharp (PDF), Microsoft Office Interop (Word)
- **Data Storage**: JSON-based local storage with extensible backend support

## System Requirements

- **Operating System**: Windows 10 version 1809 or later / Windows 11
- **Framework**: .NET 8 Runtime
- **Memory**: 4 GB RAM (8 GB recommended)
- **Storage**: 500 MB available space
- **Optional**: Microsoft Office (for enhanced Word export features)

## Installation

### From Release
1. Download the latest release from the releases page
2. Run the installer (`WorkInstructionCreator-Setup.exe`)
3. Follow the installation wizard
4. Launch from Start Menu or Desktop shortcut

### From Source
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/WorkInstructionCreator.git
   cd WorkInstructionCreator
   ```

2. Restore dependencies:
   ```bash
   dotnet restore
   ```

3. Build the application:
   ```bash
   dotnet build --configuration Release
   ```

4. Run the application:
   ```bash
   dotnet run --project WorkInstructionCreator
   ```

## Usage Guide

### Getting Started
1. **Launch** the application
2. **Choose a template** from the left panel or start with a blank document
3. **Edit your content** using the rich text editor in the center panel
4. **Add flowcharts** or **insert content** from the library as needed
5. **Use AI assistance** to check and improve your work instruction
6. **Export** to PDF or Word when complete

### Creating Templates
1. Navigate to the Templates tab
2. Click the "+" button to create a new template
3. Define template fields and structure using HTML with placeholders
4. Save and categorize your template
5. Use `{{FieldName}}` syntax for dynamic content areas

### Building Flowcharts
1. Go to the Flowcharts tab
2. Create a new flowchart or select a base template
3. Drag nodes from the toolbar to the canvas
4. Connect nodes to show process flow
5. Edit node text and properties
6. Save your flowchart for reuse

### Content Management
1. Browse the Content Library tab
2. Filter by category or content type
3. Click any content item to insert it into your document
4. Create custom content items for your organization
5. Use tags to organize and find content quickly

### AI Assistant
1. Click the AI Assistant button in the toolbar
2. Get real-time feedback on your content
3. Request suggestions for improvement
4. Ask for help with specific topics
5. Validate template structure and completeness

## Configuration

### Application Settings
Settings are stored in `%APPDATA%\WorkInstructionCreator\settings.json`:

```json
{
  "Theme": "Light",
  "AutoSave": true,
  "AutoSaveInterval": 300,
  "DefaultExportFormat": "PDF",
  "AIAssistantEnabled": true,
  "CompanyName": "Your Organization",
  "CompanyLogo": ""
}
```

### Data Storage
- **Templates**: `%APPDATA%\WorkInstructionCreator\Templates\`
- **Flowcharts**: `%APPDATA%\WorkInstructionCreator\Flowcharts\`
- **Content Library**: `%APPDATA%\WorkInstructionCreator\Content\`
- **Documents**: User's Documents folder by default

## Customization

### Custom Templates
Create HTML templates with placeholder syntax:
```html
<h1>{{Title}}</h1>
<h2>Purpose</h2>
<p>{{Purpose}}</p>
<h2>Safety Requirements</h2>
<div class="safety-note">{{SafetyRequirements}}</div>
```

### Content Styling
Built-in CSS classes for consistent styling:
- `.safety-note` - Yellow background for safety information
- `.warning-note` - Red background for warnings
- `.procedure-step` - Blue left border for procedure steps
- `.checklist` - Gray background for checklists

### AI Integration
Configure AI services in `Services\ChatbotService.cs`:
- OpenAI GPT integration
- Azure Cognitive Services
- Custom API endpoints
- Offline rule-based validation

## Troubleshooting

### Common Issues

**Application won't start**
- Ensure .NET 8 Runtime is installed
- Check Windows Event Viewer for error details
- Run as Administrator if needed

**Export functionality not working**
- For PDF: Verify iTextSharp libraries are present
- For Word: Install Microsoft Office or Office runtime
- Check file permissions in output directory

**Templates not loading**
- Verify JSON syntax in template files
- Check `%APPDATA%\WorkInstructionCreator\Templates\` permissions
- Reset to default templates via Settings

**AI Assistant not responding**
- Check internet connection for online services
- Verify API keys in configuration
- Fallback to offline validation should work automatically

### Support
- Create an issue on GitHub for bug reports
- Check the Wiki for detailed documentation
- Contact support at support@workinstruction.app

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
1. Install Visual Studio 2022 or VS Code with C# extension
2. Install .NET 8 SDK
3. Clone the repository
4. Open the solution file in your IDE
5. Restore NuGet packages
6. Build and run

### Architecture Overview
```
WorkInstructionCreator/
├── Models/          # Data models and entities
├── ViewModels/      # MVVM view models
├── Views/           # WPF user controls and windows  
├── Services/        # Business logic and data access
├── Resources/       # Images, styles, and localization
└── Converters/      # Value converters for data binding
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Material Design In XAML Toolkit for the beautiful UI components
- iTextSharp for PDF generation capabilities
- CommunityToolkit.Mvvm for MVVM infrastructure
- All contributors and users who provide feedback and improvements

---

**Work Instruction Creator** - Making professional work instructions accessible to everyone.
