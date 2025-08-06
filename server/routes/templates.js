const express = require('express');
const fs = require('fs-extra');
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const router = express.Router();

const TEMPLATES_DIR = path.join(__dirname, '../templates');

// Base templates data
const baseTemplates = [
  {
    id: 'safety-procedure',
    name: 'Safety Procedure',
    description: 'Standard template for safety procedures',
    category: 'Safety',
    sections: [
      { id: 'title', name: 'Title', type: 'text', required: true },
      { id: 'purpose', name: 'Purpose', type: 'richtext', required: true },
      { id: 'scope', name: 'Scope', type: 'richtext', required: false },
      { id: 'responsibilities', name: 'Responsibilities', type: 'list', required: true },
      { id: 'procedure', name: 'Procedure Steps', type: 'numbered-list', required: true },
      { id: 'safety-notes', name: 'Safety Notes', type: 'richtext', required: true },
      { id: 'emergency', name: 'Emergency Procedures', type: 'richtext', required: false }
    ]
  },
  {
    id: 'maintenance-procedure',
    name: 'Maintenance Procedure',
    description: 'Template for equipment maintenance procedures',
    category: 'Maintenance',
    sections: [
      { id: 'title', name: 'Title', type: 'text', required: true },
      { id: 'equipment', name: 'Equipment Information', type: 'richtext', required: true },
      { id: 'tools', name: 'Required Tools', type: 'list', required: true },
      { id: 'safety', name: 'Safety Precautions', type: 'richtext', required: true },
      { id: 'steps', name: 'Maintenance Steps', type: 'numbered-list', required: true },
      { id: 'inspection', name: 'Quality Inspection', type: 'checklist', required: true },
      { id: 'documentation', name: 'Documentation Requirements', type: 'richtext', required: false }
    ]
  },
  {
    id: 'operational-procedure',
    name: 'Operational Procedure',
    description: 'Template for standard operating procedures',
    category: 'Operations',
    sections: [
      { id: 'title', name: 'Title', type: 'text', required: true },
      { id: 'objective', name: 'Objective', type: 'richtext', required: true },
      { id: 'prerequisites', name: 'Prerequisites', type: 'list', required: false },
      { id: 'materials', name: 'Materials/Equipment', type: 'list', required: true },
      { id: 'procedure', name: 'Operating Procedure', type: 'numbered-list', required: true },
      { id: 'quality-control', name: 'Quality Control Points', type: 'checklist', required: true },
      { id: 'troubleshooting', name: 'Troubleshooting', type: 'richtext', required: false }
    ]
  },
  {
    id: 'training-procedure',
    name: 'Training Procedure',
    description: 'Template for training and onboarding procedures',
    category: 'Training',
    sections: [
      { id: 'title', name: 'Title', type: 'text', required: true },
      { id: 'learning-objectives', name: 'Learning Objectives', type: 'list', required: true },
      { id: 'prerequisites', name: 'Prerequisites', type: 'list', required: false },
      { id: 'training-content', name: 'Training Content', type: 'richtext', required: true },
      { id: 'practical-exercises', name: 'Practical Exercises', type: 'numbered-list', required: true },
      { id: 'assessment', name: 'Assessment Criteria', type: 'checklist', required: true },
      { id: 'resources', name: 'Additional Resources', type: 'list', required: false }
    ]
  }
];

// Initialize templates if they don't exist
const initializeTemplates = async () => {
  try {
    await fs.ensureDir(TEMPLATES_DIR);
    
    for (const template of baseTemplates) {
      const templatePath = path.join(TEMPLATES_DIR, `${template.id}.json`);
      if (!await fs.pathExists(templatePath)) {
        await fs.writeJson(templatePath, template, { spaces: 2 });
      }
    }
  } catch (error) {
    console.error('Error initializing templates:', error);
  }
};

// Get all templates
router.get('/', async (req, res) => {
  try {
    await initializeTemplates();
    const templates = [];
    
    const files = await fs.readdir(TEMPLATES_DIR);
    for (const file of files) {
      if (file.endsWith('.json')) {
        const templateData = await fs.readJson(path.join(TEMPLATES_DIR, file));
        templates.push(templateData);
      }
    }
    
    res.json(templates);
  } catch (error) {
    console.error('Error fetching templates:', error);
    res.status(500).json({ error: 'Failed to fetch templates' });
  }
});

// Get specific template
router.get('/:id', async (req, res) => {
  try {
    const templatePath = path.join(TEMPLATES_DIR, `${req.params.id}.json`);
    
    if (!await fs.pathExists(templatePath)) {
      return res.status(404).json({ error: 'Template not found' });
    }
    
    const template = await fs.readJson(templatePath);
    res.json(template);
  } catch (error) {
    console.error('Error fetching template:', error);
    res.status(500).json({ error: 'Failed to fetch template' });
  }
});

// Create new template
router.post('/', async (req, res) => {
  try {
    const { name, description, category, sections } = req.body;
    
    if (!name || !sections || !Array.isArray(sections)) {
      return res.status(400).json({ error: 'Invalid template data' });
    }
    
    const template = {
      id: uuidv4(),
      name,
      description: description || '',
      category: category || 'Custom',
      sections,
      created: new Date().toISOString(),
      custom: true
    };
    
    const templatePath = path.join(TEMPLATES_DIR, `${template.id}.json`);
    await fs.writeJson(templatePath, template, { spaces: 2 });
    
    res.status(201).json(template);
  } catch (error) {
    console.error('Error creating template:', error);
    res.status(500).json({ error: 'Failed to create template' });
  }
});

// Update template
router.put('/:id', async (req, res) => {
  try {
    const templatePath = path.join(TEMPLATES_DIR, `${req.params.id}.json`);
    
    if (!await fs.pathExists(templatePath)) {
      return res.status(404).json({ error: 'Template not found' });
    }
    
    const existingTemplate = await fs.readJson(templatePath);
    const updatedTemplate = {
      ...existingTemplate,
      ...req.body,
      id: req.params.id, // Preserve ID
      updated: new Date().toISOString()
    };
    
    await fs.writeJson(templatePath, updatedTemplate, { spaces: 2 });
    res.json(updatedTemplate);
  } catch (error) {
    console.error('Error updating template:', error);
    res.status(500).json({ error: 'Failed to update template' });
  }
});

// Delete template (only custom templates)
router.delete('/:id', async (req, res) => {
  try {
    const templatePath = path.join(TEMPLATES_DIR, `${req.params.id}.json`);
    
    if (!await fs.pathExists(templatePath)) {
      return res.status(404).json({ error: 'Template not found' });
    }
    
    const template = await fs.readJson(templatePath);
    
    if (!template.custom) {
      return res.status(403).json({ error: 'Cannot delete base templates' });
    }
    
    await fs.remove(templatePath);
    res.json({ message: 'Template deleted successfully' });
  } catch (error) {
    console.error('Error deleting template:', error);
    res.status(500).json({ error: 'Failed to delete template' });
  }
});

module.exports = router;