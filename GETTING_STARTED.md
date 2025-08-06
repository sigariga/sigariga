# Getting Started with Work Instruction Creator

## Quick Setup (5 minutes)

### 1. Prerequisites
- **Node.js 16+** and npm
- **Git** (for cloning the repository)
- (Optional) **OpenAI API key** for AI features

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd work-instruction-creator

# Run the automated installer
./install.sh

# OR install manually:
npm run install-all
```

### 3. Configuration (Optional)

```bash
# Add OpenAI API key for AI features
cd server
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your_key_here
```

### 4. Start the Application

```bash
# Start both frontend and backend
npm run dev
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## First Steps

### 1. Dashboard Overview
- View quick statistics and recent documents
- Access quick actions for creating new content

### 2. Create Your First Work Instruction

**Option A: From Template**
1. Click "Browse Templates" on dashboard
2. Select a template (Safety, Maintenance, Operations, Training)
3. Customize the content in the editor

**Option B: From Scratch**
1. Click "New Document" on dashboard
2. Start with a blank document
3. Add content using the rich text editor

### 3. Use the Content Library
1. Navigate to "Content Library"
2. Browse pre-written content by category:
   - Safety Items (PPE, procedures)
   - Quality Checks (inspections, testing)
   - Tools (equipment lists)
   - Common Steps (preparation, verification)
   - Troubleshooting (diagnostics)

### 4. Create Process Flowcharts
1. Go to "Flowcharts"
2. Use the drag-and-drop editor
3. Add nodes: Start/End, Process, Decision
4. Connect nodes with arrows
5. Include flowcharts in your documents

### 5. AI-Powered Error Checking
- Automatic content validation
- Safety requirement checking
- Style and clarity suggestions
- Interactive chat for guidance

### 6. Export Documents
1. Navigate to "Export Center"
2. Select your document
3. Choose format (Word .docx or PDF)
4. Download the professional document

## Key Features at a Glance

### 📝 Rich Text Editor
- Microsoft Word-like interface
- Formatting tools (bold, italic, lists, tables)
- Real-time spell checking
- Auto-save every 5 seconds

### 📋 Templates
- **Safety Procedures**: PPE, lockout/tagout, emergency
- **Maintenance**: Equipment maintenance, inspections
- **Operations**: SOPs, quality control, processes
- **Training**: Learning objectives, exercises, assessments

### 🔧 Content Library Categories
- **Safety Items**: 5+ pre-written safety procedures
- **Quality Checks**: Inspection and testing protocols
- **Tools**: Equipment specifications and requirements
- **Common Steps**: Reusable procedure steps
- **Troubleshooting**: Standard diagnostic procedures

### 📊 Process Flowcharts
- Drag-and-drop flowchart builder
- Pre-built process templates
- Custom node types with styling
- Export as images

### 🤖 AI Integration (Optional)
- Content analysis for completeness
- Safety requirement validation
- Style and grammar suggestions
- Interactive chat assistant

### 📄 Export Options
- Professional Word documents (.docx)
- Print-ready PDF files
- Maintains formatting and structure
- Batch export capabilities

## Common Workflows

### Creating a Safety Procedure
1. Dashboard → "Browse Templates" → "Safety Procedure"
2. Fill in title and purpose
3. Add PPE requirements from Content Library
4. Create step-by-step procedure
5. Include emergency procedures
6. Use AI checking for safety validation
7. Export to PDF for field use

### Creating a Maintenance Guide
1. Dashboard → "Browse Templates" → "Maintenance Procedure"
2. Specify equipment information
3. Add required tools from Content Library
4. Create maintenance flowchart
5. Add step-by-step instructions
6. Include quality inspection checklist
7. Export to Word for documentation

### Building Custom Content
1. Start with blank document
2. Use Content Library for standard sections
3. Create custom flowcharts for your process
4. Add organization-specific procedures
5. Use AI checking for consistency
6. Save as custom template for reuse

## Troubleshooting

### Application Won't Start
- Check Node.js version: `node -v` (need 16+)
- Verify all dependencies: `npm run install-all`
- Check port availability (3000, 5000)

### AI Features Not Working
- Add OpenAI API key to `server/.env`
- Check API key validity
- Ensure internet connection

### Export Not Working
- Check Puppeteer installation (for PDF)
- Verify file permissions in exports folder
- Try different export format

### Performance Issues
- Close other applications using ports 3000/5000
- Clear browser cache and cookies
- Restart the development server

## Next Steps

1. **Explore Templates**: Try each template type to understand the structure
2. **Build Content Library**: Add your organization's specific content
3. **Create Flowcharts**: Map your existing processes
4. **Setup AI**: Add OpenAI key for enhanced features
5. **Export Testing**: Test both Word and PDF exports
6. **Team Training**: Share with colleagues and gather feedback

## Support

- **Documentation**: See README.md for complete documentation
- **API Reference**: Check server/routes/ for API details
- **Issues**: Report bugs and feature requests on GitHub
- **Examples**: See /examples folder (if available)

## Quick Reference

### Keyboard Shortcuts (Editor)
- `Ctrl+S` / `Cmd+S`: Save document
- `Ctrl+B` / `Cmd+B`: Bold text
- `Ctrl+I` / `Cmd+I`: Italic text
- `Ctrl+Z` / `Cmd+Z`: Undo
- `Ctrl+Y` / `Cmd+Y`: Redo

### File Locations
- Templates: `server/templates/`
- Content Library: `server/content/`
- Flowcharts: `server/flowcharts/`
- Exports: `server/exports/` (temporary)

### Environment Variables
```bash
NODE_ENV=development          # Environment mode
PORT=5000                    # Server port
OPENAI_API_KEY=sk-...        # OpenAI API key (optional)
UPLOAD_LIMIT=50mb            # File upload limit
MAX_FILE_SIZE=52428800       # Max file size in bytes
```

Happy creating! 🎉