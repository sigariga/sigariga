const express = require('express');
const fs = require('fs-extra');
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const router = express.Router();

const FLOWCHARTS_DIR = path.join(__dirname, '../flowcharts');

// Base flowchart templates
const baseFlowchartTemplates = [
  {
    id: 'safety-inspection',
    name: 'Safety Inspection Flow',
    description: 'Standard safety inspection process flow',
    category: 'Safety',
    nodes: [
      { id: 'start', type: 'start', position: { x: 250, y: 50 }, data: { label: 'Start Inspection' } },
      { id: 'ppe-check', type: 'process', position: { x: 250, y: 150 }, data: { label: 'Check PPE Requirements' } },
      { id: 'area-secure', type: 'decision', position: { x: 250, y: 250 }, data: { label: 'Is Area Secure?' } },
      { id: 'secure-area', type: 'process', position: { x: 100, y: 350 }, data: { label: 'Secure Work Area' } },
      { id: 'conduct-inspection', type: 'process', position: { x: 400, y: 350 }, data: { label: 'Conduct Inspection' } },
      { id: 'issues-found', type: 'decision', position: { x: 400, y: 450 }, data: { label: 'Issues Found?' } },
      { id: 'document-issues', type: 'process', position: { x: 250, y: 550 }, data: { label: 'Document Issues' } },
      { id: 'complete', type: 'end', position: { x: 550, y: 550 }, data: { label: 'Inspection Complete' } }
    ],
    edges: [
      { id: 'e1', source: 'start', target: 'ppe-check' },
      { id: 'e2', source: 'ppe-check', target: 'area-secure' },
      { id: 'e3', source: 'area-secure', target: 'secure-area', label: 'No' },
      { id: 'e4', source: 'area-secure', target: 'conduct-inspection', label: 'Yes' },
      { id: 'e5', source: 'secure-area', target: 'conduct-inspection' },
      { id: 'e6', source: 'conduct-inspection', target: 'issues-found' },
      { id: 'e7', source: 'issues-found', target: 'document-issues', label: 'Yes' },
      { id: 'e8', source: 'issues-found', target: 'complete', label: 'No' },
      { id: 'e9', source: 'document-issues', target: 'complete' }
    ]
  },
  {
    id: 'maintenance-flow',
    name: 'Equipment Maintenance Flow',
    description: 'Standard equipment maintenance process',
    category: 'Maintenance',
    nodes: [
      { id: 'start', type: 'start', position: { x: 250, y: 50 }, data: { label: 'Start Maintenance' } },
      { id: 'lockout', type: 'process', position: { x: 250, y: 150 }, data: { label: 'Apply Lockout/Tagout' } },
      { id: 'verify-isolation', type: 'process', position: { x: 250, y: 250 }, data: { label: 'Verify Energy Isolation' } },
      { id: 'pre-maintenance', type: 'process', position: { x: 250, y: 350 }, data: { label: 'Pre-Maintenance Inspection' } },
      { id: 'maintenance-tasks', type: 'process', position: { x: 250, y: 450 }, data: { label: 'Perform Maintenance Tasks' } },
      { id: 'post-maintenance', type: 'process', position: { x: 250, y: 550 }, data: { label: 'Post-Maintenance Testing' } },
      { id: 'test-passed', type: 'decision', position: { x: 250, y: 650 }, data: { label: 'Test Passed?' } },
      { id: 'troubleshoot', type: 'process', position: { x: 100, y: 750 }, data: { label: 'Troubleshoot Issues' } },
      { id: 'remove-lockout', type: 'process', position: { x: 400, y: 750 }, data: { label: 'Remove Lockout/Tagout' } },
      { id: 'complete', type: 'end', position: { x: 400, y: 850 }, data: { label: 'Maintenance Complete' } }
    ],
    edges: [
      { id: 'e1', source: 'start', target: 'lockout' },
      { id: 'e2', source: 'lockout', target: 'verify-isolation' },
      { id: 'e3', source: 'verify-isolation', target: 'pre-maintenance' },
      { id: 'e4', source: 'pre-maintenance', target: 'maintenance-tasks' },
      { id: 'e5', source: 'maintenance-tasks', target: 'post-maintenance' },
      { id: 'e6', source: 'post-maintenance', target: 'test-passed' },
      { id: 'e7', source: 'test-passed', target: 'troubleshoot', label: 'No' },
      { id: 'e8', source: 'test-passed', target: 'remove-lockout', label: 'Yes' },
      { id: 'e9', source: 'troubleshoot', target: 'post-maintenance' },
      { id: 'e10', source: 'remove-lockout', target: 'complete' }
    ]
  }
];

// Initialize flowcharts
const initializeFlowcharts = async () => {
  try {
    await fs.ensureDir(FLOWCHARTS_DIR);
    
    for (const flowchart of baseFlowchartTemplates) {
      const flowchartPath = path.join(FLOWCHARTS_DIR, `${flowchart.id}.json`);
      if (!await fs.pathExists(flowchartPath)) {
        await fs.writeJson(flowchartPath, flowchart, { spaces: 2 });
      }
    }
  } catch (error) {
    console.error('Error initializing flowcharts:', error);
  }
};

// Get all flowcharts
router.get('/', async (req, res) => {
  try {
    await initializeFlowcharts();
    const flowcharts = [];
    
    const files = await fs.readdir(FLOWCHARTS_DIR);
    for (const file of files) {
      if (file.endsWith('.json')) {
        const flowchartData = await fs.readJson(path.join(FLOWCHARTS_DIR, file));
        // Remove nodes and edges for list view (only metadata)
        const { nodes, edges, ...metadata } = flowchartData;
        flowcharts.push(metadata);
      }
    }
    
    res.json(flowcharts);
  } catch (error) {
    console.error('Error fetching flowcharts:', error);
    res.status(500).json({ error: 'Failed to fetch flowcharts' });
  }
});

// Get specific flowchart
router.get('/:id', async (req, res) => {
  try {
    const flowchartPath = path.join(FLOWCHARTS_DIR, `${req.params.id}.json`);
    
    if (!await fs.pathExists(flowchartPath)) {
      return res.status(404).json({ error: 'Flowchart not found' });
    }
    
    const flowchart = await fs.readJson(flowchartPath);
    res.json(flowchart);
  } catch (error) {
    console.error('Error fetching flowchart:', error);
    res.status(500).json({ error: 'Failed to fetch flowchart' });
  }
});

// Create new flowchart
router.post('/', async (req, res) => {
  try {
    const { name, description, category, nodes, edges } = req.body;
    
    if (!name || !nodes || !Array.isArray(nodes)) {
      return res.status(400).json({ error: 'Invalid flowchart data' });
    }
    
    const flowchart = {
      id: uuidv4(),
      name,
      description: description || '',
      category: category || 'Custom',
      nodes: nodes || [],
      edges: edges || [],
      created: new Date().toISOString(),
      custom: true
    };
    
    const flowchartPath = path.join(FLOWCHARTS_DIR, `${flowchart.id}.json`);
    await fs.writeJson(flowchartPath, flowchart, { spaces: 2 });
    
    res.status(201).json(flowchart);
  } catch (error) {
    console.error('Error creating flowchart:', error);
    res.status(500).json({ error: 'Failed to create flowchart' });
  }
});

// Update flowchart
router.put('/:id', async (req, res) => {
  try {
    const flowchartPath = path.join(FLOWCHARTS_DIR, `${req.params.id}.json`);
    
    if (!await fs.pathExists(flowchartPath)) {
      return res.status(404).json({ error: 'Flowchart not found' });
    }
    
    const existingFlowchart = await fs.readJson(flowchartPath);
    const updatedFlowchart = {
      ...existingFlowchart,
      ...req.body,
      id: req.params.id, // Preserve ID
      updated: new Date().toISOString()
    };
    
    await fs.writeJson(flowchartPath, updatedFlowchart, { spaces: 2 });
    res.json(updatedFlowchart);
  } catch (error) {
    console.error('Error updating flowchart:', error);
    res.status(500).json({ error: 'Failed to update flowchart' });
  }
});

// Delete flowchart (only custom flowcharts)
router.delete('/:id', async (req, res) => {
  try {
    const flowchartPath = path.join(FLOWCHARTS_DIR, `${req.params.id}.json`);
    
    if (!await fs.pathExists(flowchartPath)) {
      return res.status(404).json({ error: 'Flowchart not found' });
    }
    
    const flowchart = await fs.readJson(flowchartPath);
    
    if (!flowchart.custom) {
      return res.status(403).json({ error: 'Cannot delete base flowcharts' });
    }
    
    await fs.remove(flowchartPath);
    res.json({ message: 'Flowchart deleted successfully' });
  } catch (error) {
    console.error('Error deleting flowchart:', error);
    res.status(500).json({ error: 'Failed to delete flowchart' });
  }
});

// Duplicate flowchart
router.post('/:id/duplicate', async (req, res) => {
  try {
    const flowchartPath = path.join(FLOWCHARTS_DIR, `${req.params.id}.json`);
    
    if (!await fs.pathExists(flowchartPath)) {
      return res.status(404).json({ error: 'Flowchart not found' });
    }
    
    const originalFlowchart = await fs.readJson(flowchartPath);
    const duplicatedFlowchart = {
      ...originalFlowchart,
      id: uuidv4(),
      name: `${originalFlowchart.name} (Copy)`,
      created: new Date().toISOString(),
      custom: true
    };
    
    const newFlowchartPath = path.join(FLOWCHARTS_DIR, `${duplicatedFlowchart.id}.json`);
    await fs.writeJson(newFlowchartPath, duplicatedFlowchart, { spaces: 2 });
    
    res.status(201).json(duplicatedFlowchart);
  } catch (error) {
    console.error('Error duplicating flowchart:', error);
    res.status(500).json({ error: 'Failed to duplicate flowchart' });
  }
});

module.exports = router;