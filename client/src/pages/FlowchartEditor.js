import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

function FlowchartEditor() {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Flowchart Editor
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            Interactive flowchart editor for creating process flow diagrams.
            Features include:
          </Typography>
          <ul>
            <li>Drag-and-drop flowchart builder</li>
            <li>Pre-built process templates</li>
            <li>Custom node types (Start/End, Process, Decision)</li>
            <li>Export flowcharts as images</li>
          </ul>
        </CardContent>
      </Card>
    </Box>
  );
}

export default FlowchartEditor;