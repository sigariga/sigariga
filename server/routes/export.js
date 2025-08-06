const express = require('express');
const fs = require('fs-extra');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType } = require('docx');
const puppeteer = require('puppeteer');
const { v4: uuidv4 } = require('uuid');
const router = express.Router();

const EXPORTS_DIR = path.join(__dirname, '../exports');

// Ensure exports directory exists
fs.ensureDirSync(EXPORTS_DIR);

// Export to Word document
router.post('/word', async (req, res) => {
  try {
    const { content, title, metadata = {} } = req.body;
    
    if (!content || !title) {
      return res.status(400).json({ error: 'Content and title are required' });
    }
    
    const doc = await createWordDocument(content, title, metadata);
    const buffer = await Packer.toBuffer(doc);
    
    const filename = `${sanitizeFilename(title)}_${Date.now()}.docx`;
    const filepath = path.join(EXPORTS_DIR, filename);
    
    await fs.writeFile(filepath, buffer);
    
    res.json({
      success: true,
      filename,
      downloadUrl: `/api/export/download/${filename}`,
      message: 'Word document generated successfully'
    });
  } catch (error) {
    console.error('Error generating Word document:', error);
    res.status(500).json({ error: 'Failed to generate Word document' });
  }
});

// Export to PDF
router.post('/pdf', async (req, res) => {
  try {
    const { content, title, metadata = {} } = req.body;
    
    if (!content || !title) {
      return res.status(400).json({ error: 'Content and title are required' });
    }
    
    const html = generateHTML(content, title, metadata);
    const pdfBuffer = await generatePDF(html);
    
    const filename = `${sanitizeFilename(title)}_${Date.now()}.pdf`;
    const filepath = path.join(EXPORTS_DIR, filename);
    
    await fs.writeFile(filepath, pdfBuffer);
    
    res.json({
      success: true,
      filename,
      downloadUrl: `/api/export/download/${filename}`,
      message: 'PDF document generated successfully'
    });
  } catch (error) {
    console.error('Error generating PDF:', error);
    res.status(500).json({ error: 'Failed to generate PDF' });
  }
});

// Download exported file
router.get('/download/:filename', async (req, res) => {
  try {
    const filename = req.params.filename;
    const filepath = path.join(EXPORTS_DIR, filename);
    
    if (!await fs.pathExists(filepath)) {
      return res.status(404).json({ error: 'File not found' });
    }
    
    const ext = path.extname(filename).toLowerCase();
    const mimeTypes = {
      '.pdf': 'application/pdf',
      '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    };
    
    const mimeType = mimeTypes[ext] || 'application/octet-stream';
    
    res.setHeader('Content-Type', mimeType);
    res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
    
    const fileStream = fs.createReadStream(filepath);
    fileStream.pipe(res);
    
    // Clean up file after download (optional)
    fileStream.on('end', () => {
      setTimeout(async () => {
        try {
          await fs.remove(filepath);
        } catch (error) {
          console.warn('Failed to clean up file:', error);
        }
      }, 5000); // Delete after 5 seconds
    });
    
  } catch (error) {
    console.error('Error downloading file:', error);
    res.status(500).json({ error: 'Failed to download file' });
  }
});

// Preview HTML (for testing)
router.post('/preview', async (req, res) => {
  try {
    const { content, title, metadata = {} } = req.body;
    
    if (!content || !title) {
      return res.status(400).json({ error: 'Content and title are required' });
    }
    
    const html = generateHTML(content, title, metadata);
    res.setHeader('Content-Type', 'text/html');
    res.send(html);
  } catch (error) {
    console.error('Error generating preview:', error);
    res.status(500).json({ error: 'Failed to generate preview' });
  }
});

// Helper functions
async function createWordDocument(content, title, metadata) {
  const sections = [];
  
  // Title
  sections.push(
    new Paragraph({
      text: title,
      heading: HeadingLevel.TITLE,
      spacing: { after: 400 }
    })
  );
  
  // Metadata table
  if (Object.keys(metadata).length > 0) {
    const metadataRows = Object.entries(metadata).map(([key, value]) => 
      new TableRow({
        children: [
          new TableCell({ children: [new Paragraph(formatLabel(key))] }),
          new TableCell({ children: [new Paragraph(String(value))] })
        ]
      })
    );
    
    sections.push(
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        rows: metadataRows,
        margins: { top: 200, bottom: 200, left: 200, right: 200 }
      }),
      new Paragraph({ text: '', spacing: { after: 400 } })
    );
  }
  
  // Process content sections
  if (Array.isArray(content)) {
    content.forEach(section => {
      sections.push(...processSection(section));
    });
  } else if (typeof content === 'string') {
    sections.push(...processTextContent(content));
  }
  
  return new Document({
    sections: [{
      properties: {},
      children: sections
    }]
  });
}

function processSection(section) {
  const elements = [];
  
  if (section.title) {
    elements.push(
      new Paragraph({
        text: section.title,
        heading: HeadingLevel.HEADING_1,
        spacing: { before: 400, after: 200 }
      })
    );
  }
  
  if (section.content) {
    if (Array.isArray(section.content)) {
      section.content.forEach((item, index) => {
        if (section.type === 'numbered-list') {
          elements.push(
            new Paragraph({
              text: `${index + 1}. ${item}`,
              spacing: { after: 100 }
            })
          );
        } else if (section.type === 'list') {
          elements.push(
            new Paragraph({
              text: `• ${item}`,
              spacing: { after: 100 }
            })
          );
        } else {
          elements.push(
            new Paragraph({
              text: item,
              spacing: { after: 100 }
            })
          );
        }
      });
    } else {
      elements.push(...processTextContent(section.content));
    }
  }
  
  return elements;
}

function processTextContent(text) {
  const paragraphs = text.split('\n\n');
  return paragraphs.map(para => 
    new Paragraph({
      text: para.trim(),
      spacing: { after: 200 }
    })
  );
}

function generateHTML(content, title, metadata) {
  const metadataHtml = Object.keys(metadata).length > 0 ? `
    <div class="metadata">
      <table>
        ${Object.entries(metadata).map(([key, value]) => 
          `<tr><td><strong>${formatLabel(key)}:</strong></td><td>${value}</td></tr>`
        ).join('')}
      </table>
    </div>
  ` : '';
  
  const contentHtml = Array.isArray(content) 
    ? content.map(section => formatSectionHTML(section)).join('')
    : `<div class="content">${formatTextHTML(content)}</div>`;
  
  return `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>${title}</title>
      <style>
        body {
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          max-width: 800px;
          margin: 0 auto;
          padding: 40px 20px;
          line-height: 1.6;
          color: #333;
        }
        h1 {
          color: #2c3e50;
          border-bottom: 3px solid #3498db;
          padding-bottom: 10px;
          margin-bottom: 30px;
        }
        h2 {
          color: #34495e;
          margin-top: 30px;
          margin-bottom: 15px;
        }
        .metadata {
          background-color: #f8f9fa;
          padding: 20px;
          border-radius: 5px;
          margin-bottom: 30px;
        }
        .metadata table {
          width: 100%;
          border-collapse: collapse;
        }
        .metadata td {
          padding: 8px 0;
          border-bottom: 1px solid #dee2e6;
        }
        .metadata td:first-child {
          width: 200px;
          font-weight: bold;
        }
        .content {
          margin-bottom: 20px;
        }
        .section {
          margin-bottom: 25px;
        }
        ol, ul {
          padding-left: 25px;
        }
        li {
          margin-bottom: 5px;
        }
        .safety {
          background-color: #fff3cd;
          border-left: 4px solid #ffc107;
          padding: 15px;
          margin: 20px 0;
        }
        .warning {
          background-color: #f8d7da;
          border-left: 4px solid #dc3545;
          padding: 15px;
          margin: 20px 0;
        }
        @media print {
          body { padding: 20px; }
          .metadata { break-inside: avoid; }
        }
      </style>
    </head>
    <body>
      <h1>${title}</h1>
      ${metadataHtml}
      ${contentHtml}
    </body>
    </html>
  `;
}

function formatSectionHTML(section) {
  let html = '';
  
  if (section.title) {
    html += `<h2>${section.title}</h2>`;
  }
  
  if (section.content) {
    const cssClass = section.category === 'safety' ? 'safety' : 
                     section.category === 'warning' ? 'warning' : '';
    
    html += `<div class="section ${cssClass}">`;
    
    if (Array.isArray(section.content)) {
      if (section.type === 'numbered-list') {
        html += '<ol>' + section.content.map(item => `<li>${item}</li>`).join('') + '</ol>';
      } else if (section.type === 'list') {
        html += '<ul>' + section.content.map(item => `<li>${item}</li>`).join('') + '</ul>';
      } else {
        html += section.content.map(item => `<p>${item}</p>`).join('');
      }
    } else {
      html += formatTextHTML(section.content);
    }
    
    html += '</div>';
  }
  
  return html;
}

function formatTextHTML(text) {
  return text.split('\n\n').map(para => `<p>${para.trim()}</p>`).join('');
}

async function generatePDF(html) {
  let browser;
  try {
    browser = await puppeteer.launch({
      headless: 'new',
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    await page.setContent(html, { waitUntil: 'networkidle0' });
    
    const pdfBuffer = await page.pdf({
      format: 'A4',
      margin: {
        top: '20mm',
        right: '20mm',
        bottom: '20mm',
        left: '20mm'
      },
      printBackground: true
    });
    
    return pdfBuffer;
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}

function sanitizeFilename(filename) {
  return filename
    .replace(/[^a-z0-9]/gi, '_')
    .replace(/_+/g, '_')
    .replace(/^_|_$/g, '')
    .toLowerCase()
    .substring(0, 50);
}

function formatLabel(key) {
  return key
    .replace(/([A-Z])/g, ' $1')
    .replace(/^./, str => str.toUpperCase())
    .replace(/_/g, ' ');
}

module.exports = router;