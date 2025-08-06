import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

function ExportCenter() {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Export Center
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            Document export interface for generating professional documents.
            Features include:
          </Typography>
          <ul>
            <li>Export to Word (.docx) format</li>
            <li>Export to PDF format</li>
            <li>Preview before export</li>
            <li>Batch export multiple documents</li>
          </ul>
        </CardContent>
      </Card>
    </Box>
  );
}

export default ExportCenter;