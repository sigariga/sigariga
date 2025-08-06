# Work Instruction Creator

A comprehensive web application for creating professional work instructions with base templates, process flowcharts, rich text editing, AI-powered error checking, and export capabilities to Word and PDF formats.

## Features

### 🎯 Core Functionality
- **Template-based Creation**: Pre-built templates for safety procedures, maintenance, operations, and training
- **Rich Text Editor**: Microsoft Word-like editing experience with formatting tools
- **Process Flowcharts**: Drag-and-drop flowchart editor with predefined process templates
- **Content Library**: Reusable content blocks for safety items, tools, procedures, and more
- **AI Error Checking**: Intelligent content validation and improvement suggestions
- **Export Options**: Professional Word and PDF document generation

### 🛠 Technical Features
- **Modern React Frontend**: Built with React 18, Material-UI, and modern hooks
- **Node.js Backend**: Express server with comprehensive API endpoints
- **Real-time Collaboration**: WebSocket support for team editing (planned)
- **Auto-save**: Automatic document saving every 5 seconds
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Project Structure

```
work-instruction-creator/
├── client/                    # React frontend
│   ├── src/
│   │   ├── components/        # Reusable React components
│   │   ├── pages/            # Main application pages
│   │   ├── context/          # React context for state management
│   │   └── App.js            # Main application component
│   └── package.json
├── server/                   # Node.js backend
│   ├── routes/              # API route handlers
│   │   ├── templates.js     # Template management
│   │   ├── content.js       # Content library
│   │   ├── flowchart.js     # Flowchart management
│   │   ├── chatbot.js       # AI error checking
│   │   └── export.js        # Document export
│   ├── templates/           # Stored templates
│   ├── content/             # Content library data
│   └── index.js             # Main server file
└── package.json             # Root package file
```

## Installation

### Prerequisites
- Node.js 16+ and npm
- (Optional) OpenAI API key for AI features

### Quick Start

1. **Clone and Install**
   ```bash
   git clone <repository-url>
   cd work-instruction-creator
   npm run install-all
   ```

2. **Environment Setup**
   ```bash
   cd server
   cp .env.example .env
   # Edit .env and add your OpenAI API key (optional)
   ```

3. **Start Development**
   ```bash
   npm run dev
   ```

4. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## Usage Guide

### Creating Work Instructions

1. **Start from Template**
   - Choose from pre-built templates (Safety, Maintenance, Operations, Training)
   - Templates include structured sections with field types

2. **Use Rich Text Editor**
   - Microsoft Word-like interface with formatting tools
   - Insert images, tables, lists, and styled text
   - Real-time spell checking and grammar assistance

3. **Add Process Flowcharts**
   - Drag-and-drop flowchart builder
   - Pre-built process templates for common workflows
   - Custom node types: Start/End, Process, Decision, etc.

4. **Select from Content Library**
   - Pre-written safety procedures
   - Standard tool lists and requirements
   - Common troubleshooting steps
   - Quality control checkpoints

5. **AI Error Checking**
   - Automatic content analysis for clarity and completeness
   - Safety requirement validation
   - Style and grammar suggestions
   - Interactive chat assistant for guidance

6. **Export Documents**
   - Professional Word (.docx) format
   - Print-ready PDF format
   - Maintains formatting and structure

### Template Categories

- **Safety Procedures**: PPE requirements, lockout/tagout, emergency procedures
- **Maintenance**: Equipment maintenance, inspection checklists, troubleshooting
- **Operations**: Standard operating procedures, quality control, process flows
- **Training**: Learning objectives, practical exercises, assessment criteria

### Content Library Categories

- **Safety Items**: PPE requirements, safety protocols, emergency procedures
- **Quality Checks**: Inspection procedures, testing protocols, documentation
- **Tools**: Equipment lists with specifications and requirements
- **Common Steps**: Reusable procedure steps for preparation, verification, cleanup
- **Troubleshooting**: Standard diagnostic and resolution procedures

## API Documentation

### Templates API
- `GET /api/templates` - List all templates
- `GET /api/templates/:id` - Get specific template
- `POST /api/templates` - Create new template
- `PUT /api/templates/:id` - Update template
- `DELETE /api/templates/:id` - Delete template

### Content API
- `GET /api/content` - Get all content categories
- `GET /api/content/:category` - Get specific category
- `POST /api/content/:category` - Add content item
- `PUT /api/content/:category/:id` - Update content item
- `DELETE /api/content/:category/:id` - Delete content item

### Flowchart API
- `GET /api/flowchart` - List all flowcharts
- `GET /api/flowchart/:id` - Get specific flowchart
- `POST /api/flowchart` - Create new flowchart
- `PUT /api/flowchart/:id` - Update flowchart
- `DELETE /api/flowchart/:id` - Delete flowchart

### AI Chatbot API
- `POST /api/chatbot/check` - Check content for errors
- `POST /api/chatbot/suggestions` - Get improvement suggestions
- `POST /api/chatbot/chat` - Interactive chat assistance

### Export API
- `POST /api/export/word` - Generate Word document
- `POST /api/export/pdf` - Generate PDF document
- `GET /api/export/download/:filename` - Download generated file

## Configuration

### Environment Variables (.env)
```bash
NODE_ENV=development
PORT=5000
OPENAI_API_KEY=your_openai_api_key_here  # Optional for AI features
UPLOAD_LIMIT=50mb
MAX_FILE_SIZE=52428800
```

### Features Configuration
- **Auto-save**: Configurable interval (default: 5 seconds)
- **AI Integration**: Optional OpenAI integration for advanced features
- **Export Options**: Word and PDF format support
- **Content Validation**: Rule-based and AI-powered checking

## Development

### Available Scripts
- `npm run dev` - Start both frontend and backend in development mode
- `npm run client` - Start only React frontend
- `npm run server` - Start only Node.js backend
- `npm run build` - Build production frontend
- `npm run install-all` - Install dependencies for both frontend and backend

### Technology Stack

**Frontend:**
- React 18 with hooks and context
- Material-UI for modern component library
- React Quill for rich text editing
- React Flow for flowchart editing
- Axios for API communication

**Backend:**
- Express.js web framework
- Puppeteer for PDF generation
- DOCX library for Word document creation
- OpenAI integration for AI features
- File system storage for templates and content

### Adding New Features

1. **New Template Types**: Add to `server/routes/templates.js`
2. **Content Categories**: Extend `server/routes/content.js`
3. **Export Formats**: Modify `server/routes/export.js`
4. **AI Capabilities**: Enhance `server/routes/chatbot.js`

## Deployment

### Production Build
```bash
npm run build
npm start
```

### Docker Deployment (Optional)
```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 5000
CMD ["npm", "start"]
```

### Environment Setup
- Set NODE_ENV=production
- Configure proper CORS settings
- Set up SSL certificates for HTTPS
- Configure database if persistent storage needed

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions, issues, or feature requests:
- Create an issue on GitHub
- Check the documentation in `/docs`
- Review API examples in `/examples`

## Future Enhancements

- [ ] Real-time collaborative editing
- [ ] Version control and document history
- [ ] Advanced template builder
- [ ] Integration with external systems
- [ ] Mobile app for field use
- [ ] Advanced analytics and reporting
- [ ] Multi-language support
- [ ] Custom branding options
