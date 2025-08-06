const express = require('express');
const fs = require('fs-extra');
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const router = express.Router();

const CONTENT_DIR = path.join(__dirname, '../content');

// Base content library
const baseContent = {
  safetyItems: [
    { id: 'ppe-basic', text: 'Wear appropriate Personal Protective Equipment (PPE)', category: 'PPE' },
    { id: 'lockout-tagout', text: 'Apply lockout/tagout procedures before maintenance', category: 'Lockout' },
    { id: 'hot-work', text: 'Obtain hot work permit for welding or cutting operations', category: 'Permits' },
    { id: 'confined-space', text: 'Follow confined space entry procedures', category: 'Confined Space' },
    { id: 'chemical-handling', text: 'Review Safety Data Sheet (SDS) before handling chemicals', category: 'Chemical Safety' }
  ],
  
  qualityChecks: [
    { id: 'visual-inspection', text: 'Perform visual inspection for defects', category: 'Inspection' },
    { id: 'dimensional-check', text: 'Verify dimensions against specifications', category: 'Measurement' },
    { id: 'functional-test', text: 'Conduct functional testing', category: 'Testing' },
    { id: 'documentation', text: 'Document all measurements and observations', category: 'Documentation' },
    { id: 'calibration-check', text: 'Verify equipment calibration status', category: 'Calibration' }
  ],
  
  tools: [
    { id: 'multimeter', text: 'Digital Multimeter', category: 'Electrical' },
    { id: 'torque-wrench', text: 'Torque Wrench (specify range)', category: 'Mechanical' },
    { id: 'calipers', text: 'Digital Calipers', category: 'Measurement' },
    { id: 'oscilloscope', text: 'Oscilloscope', category: 'Electrical' },
    { id: 'pressure-gauge', text: 'Pressure Gauge', category: 'Pneumatic/Hydraulic' },
    { id: 'socket-set', text: 'Socket Set', category: 'Mechanical' },
    { id: 'allen-keys', text: 'Allen Key Set', category: 'Mechanical' }
  ],
  
  commonSteps: [
    { id: 'power-off', text: 'Turn off main power supply', category: 'Preparation' },
    { id: 'cool-down', text: 'Allow equipment to cool down (specify time)', category: 'Preparation' },
    { id: 'clean-area', text: 'Clean work area and remove debris', category: 'Preparation' },
    { id: 'gather-tools', text: 'Gather all required tools and materials', category: 'Preparation' },
    { id: 'document-settings', text: 'Document current settings before changes', category: 'Documentation' },
    { id: 'test-operation', text: 'Test normal operation after completion', category: 'Verification' },
    { id: 'restore-guards', text: 'Replace all safety guards and covers', category: 'Safety' }
  ],
  
  emergencyProcedures: [
    { id: 'emergency-stop', text: 'Press emergency stop button if available', category: 'Immediate Action' },
    { id: 'evacuate-area', text: 'Evacuate immediate area if unsafe', category: 'Evacuation' },
    { id: 'call-emergency', text: 'Call emergency services (911) if required', category: 'Communication' },
    { id: 'notify-supervisor', text: 'Notify supervisor immediately', category: 'Communication' },
    { id: 'first-aid', text: 'Administer first aid if trained and safe to do so', category: 'Medical' },
    { id: 'secure-area', text: 'Secure area to prevent further incidents', category: 'Containment' }
  ],
  
  troubleshooting: [
    { id: 'check-power', text: 'Verify power supply is connected and functioning', category: 'Electrical' },
    { id: 'check-connections', text: 'Inspect all connections for looseness or corrosion', category: 'Connection' },
    { id: 'check-fuses', text: 'Check fuses and circuit breakers', category: 'Electrical' },
    { id: 'check-settings', text: 'Verify all settings match specifications', category: 'Configuration' },
    { id: 'check-pressure', text: 'Check pneumatic/hydraulic pressure levels', category: 'Pressure' },
    { id: 'check-temperature', text: 'Monitor operating temperatures', category: 'Temperature' }
  ]
};

// Initialize content library
const initializeContent = async () => {
  try {
    await fs.ensureDir(CONTENT_DIR);
    const contentPath = path.join(CONTENT_DIR, 'library.json');
    
    if (!await fs.pathExists(contentPath)) {
      await fs.writeJson(contentPath, baseContent, { spaces: 2 });
    }
  } catch (error) {
    console.error('Error initializing content:', error);
  }
};

// Get all content
router.get('/', async (req, res) => {
  try {
    await initializeContent();
    const contentPath = path.join(CONTENT_DIR, 'library.json');
    const content = await fs.readJson(contentPath);
    res.json(content);
  } catch (error) {
    console.error('Error fetching content:', error);
    res.status(500).json({ error: 'Failed to fetch content library' });
  }
});

// Get content by category
router.get('/:category', async (req, res) => {
  try {
    const contentPath = path.join(CONTENT_DIR, 'library.json');
    const content = await fs.readJson(contentPath);
    
    if (!content[req.params.category]) {
      return res.status(404).json({ error: 'Category not found' });
    }
    
    res.json(content[req.params.category]);
  } catch (error) {
    console.error('Error fetching category content:', error);
    res.status(500).json({ error: 'Failed to fetch category content' });
  }
});

// Add new content item
router.post('/:category', async (req, res) => {
  try {
    const { text, category } = req.body;
    
    if (!text) {
      return res.status(400).json({ error: 'Text is required' });
    }
    
    const contentPath = path.join(CONTENT_DIR, 'library.json');
    const content = await fs.readJson(contentPath);
    
    if (!content[req.params.category]) {
      content[req.params.category] = [];
    }
    
    const newItem = {
      id: uuidv4(),
      text,
      category: category || 'Custom',
      custom: true,
      created: new Date().toISOString()
    };
    
    content[req.params.category].push(newItem);
    await fs.writeJson(contentPath, content, { spaces: 2 });
    
    res.status(201).json(newItem);
  } catch (error) {
    console.error('Error adding content item:', error);
    res.status(500).json({ error: 'Failed to add content item' });
  }
});

// Update content item
router.put('/:category/:id', async (req, res) => {
  try {
    const contentPath = path.join(CONTENT_DIR, 'library.json');
    const content = await fs.readJson(contentPath);
    
    if (!content[req.params.category]) {
      return res.status(404).json({ error: 'Category not found' });
    }
    
    const itemIndex = content[req.params.category].findIndex(item => item.id === req.params.id);
    
    if (itemIndex === -1) {
      return res.status(404).json({ error: 'Content item not found' });
    }
    
    content[req.params.category][itemIndex] = {
      ...content[req.params.category][itemIndex],
      ...req.body,
      id: req.params.id,
      updated: new Date().toISOString()
    };
    
    await fs.writeJson(contentPath, content, { spaces: 2 });
    res.json(content[req.params.category][itemIndex]);
  } catch (error) {
    console.error('Error updating content item:', error);
    res.status(500).json({ error: 'Failed to update content item' });
  }
});

// Delete content item (only custom items)
router.delete('/:category/:id', async (req, res) => {
  try {
    const contentPath = path.join(CONTENT_DIR, 'library.json');
    const content = await fs.readJson(contentPath);
    
    if (!content[req.params.category]) {
      return res.status(404).json({ error: 'Category not found' });
    }
    
    const itemIndex = content[req.params.category].findIndex(item => item.id === req.params.id);
    
    if (itemIndex === -1) {
      return res.status(404).json({ error: 'Content item not found' });
    }
    
    const item = content[req.params.category][itemIndex];
    
    if (!item.custom) {
      return res.status(403).json({ error: 'Cannot delete base content items' });
    }
    
    content[req.params.category].splice(itemIndex, 1);
    await fs.writeJson(contentPath, content, { spaces: 2 });
    
    res.json({ message: 'Content item deleted successfully' });
  } catch (error) {
    console.error('Error deleting content item:', error);
    res.status(500).json({ error: 'Failed to delete content item' });
  }
});

// Search content
router.get('/search/:query', async (req, res) => {
  try {
    const contentPath = path.join(CONTENT_DIR, 'library.json');
    const content = await fs.readJson(contentPath);
    const query = req.params.query.toLowerCase();
    
    const results = {};
    
    Object.keys(content).forEach(category => {
      const filtered = content[category].filter(item => 
        item.text.toLowerCase().includes(query) ||
        item.category.toLowerCase().includes(query)
      );
      
      if (filtered.length > 0) {
        results[category] = filtered;
      }
    });
    
    res.json(results);
  } catch (error) {
    console.error('Error searching content:', error);
    res.status(500).json({ error: 'Failed to search content' });
  }
});

module.exports = router;