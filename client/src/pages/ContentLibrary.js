import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

function ContentLibrary() {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Content Library
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">
            Content library for managing reusable work instruction components.
            Features include:
          </Typography>
          <ul>
            <li>Browse content by category (Safety, Tools, Steps, etc.)</li>
            <li>Search and filter content items</li>
            <li>Add custom content items</li>
            <li>Drag-and-drop content into documents</li>
          </ul>
        </CardContent>
      </Card>
    </Box>
  );
}

export default ContentLibrary;