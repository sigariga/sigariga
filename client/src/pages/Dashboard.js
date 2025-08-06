import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Grid,
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  IconButton,
  Chip,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Paper,
  Avatar,
  Stack
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Description as TemplateIcon,
  LibraryBooks as ContentIcon,
  AccountTree as FlowchartIcon,
  GetApp as ExportIcon,
  TrendingUp as TrendingUpIcon,
  AccessTime as RecentIcon,
  Star as StarIcon,
  ArrowForward as ArrowForwardIcon
} from '@mui/icons-material';
import { useWorkInstruction } from '../context/WorkInstructionContext';

function Dashboard() {
  const navigate = useNavigate();
  const { 
    documents, 
    templates, 
    contentLibrary, 
    flowcharts, 
    actions,
    isLoading 
  } = useWorkInstruction();

  const handleCreateDocument = () => {
    actions.createDocument({
      title: 'New Work Instruction',
      author: 'Current User'
    });
    navigate('/workspace');
  };

  const handleCreateFromTemplate = (template) => {
    actions.setActiveTemplate(template);
    actions.createDocument({
      title: `New ${template.name}`,
      template: template.id,
      content: template.sections || [],
      author: 'Current User'
    });
    navigate('/workspace');
  };

  const handleEditDocument = (document) => {
    actions.setCurrentDocument(document);
    navigate(`/workspace/${document.id}`);
  };

  const getRecentDocuments = () => {
    return documents
      .sort((a, b) => new Date(b.metadata.updatedAt) - new Date(a.metadata.updatedAt))
      .slice(0, 5);
  };

  const getDocumentStats = () => {
    const total = documents.length;
    const draft = documents.filter(d => d.metadata.status === 'draft').length;
    const published = documents.filter(d => d.metadata.status === 'published').length;
    const inReview = documents.filter(d => d.metadata.status === 'review').length;

    return { total, draft, published, inReview };
  };

  const getContentStats = () => {
    const totalContent = Object.values(contentLibrary).reduce((acc, items) => acc + items.length, 0);
    const categories = Object.keys(contentLibrary).length;
    return { totalContent, categories };
  };

  const stats = getDocumentStats();
  const contentStats = getContentStats();

  if (isLoading) {
    return (
      <Box sx={{ p: 3 }}>
        <LinearProgress />
        <Typography sx={{ mt: 2 }}>Loading dashboard...</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Dashboard
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Welcome back! Here's an overview of your work instructions.
        </Typography>
      </Box>

      {/* Quick Actions */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quick Actions
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6} md={3}>
                  <Button
                    fullWidth
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={handleCreateDocument}
                    sx={{ mb: 1 }}
                  >
                    New Document
                  </Button>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<TemplateIcon />}
                    onClick={() => navigate('/templates')}
                    sx={{ mb: 1 }}
                  >
                    Browse Templates
                  </Button>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<FlowchartIcon />}
                    onClick={() => navigate('/flowchart')}
                    sx={{ mb: 1 }}
                  >
                    Create Flowchart
                  </Button>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<ContentIcon />}
                    onClick={() => navigate('/content')}
                    sx={{ mb: 1 }}
                  >
                    Content Library
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quick Stats
              </Typography>
              <Stack spacing={2}>
                <Box display="flex" justifyContent="space-between" alignItems="center">
                  <Typography variant="body2">Total Documents</Typography>
                  <Chip label={stats.total} color="primary" size="small" />
                </Box>
                <Box display="flex" justifyContent="space-between" alignItems="center">
                  <Typography variant="body2">Templates Available</Typography>
                  <Chip label={templates.length} color="secondary" size="small" />
                </Box>
                <Box display="flex" justifyContent="space-between" alignItems="center">
                  <Typography variant="body2">Content Items</Typography>
                  <Chip label={contentStats.totalContent} color="info" size="small" />
                </Box>
                <Box display="flex" justifyContent="space-between" alignItems="center">
                  <Typography variant="body2">Flowcharts</Typography>
                  <Chip label={flowcharts.length} color="success" size="small" />
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Main Content Grid */}
      <Grid container spacing={3}>
        {/* Recent Documents */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                <Typography variant="h6">
                  <RecentIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Recent Documents
                </Typography>
                <Button 
                  size="small" 
                  endIcon={<ArrowForwardIcon />}
                  onClick={() => navigate('/workspace')}
                >
                  View All
                </Button>
              </Box>
              
              {getRecentDocuments().length > 0 ? (
                <List>
                  {getRecentDocuments().map((doc, index) => (
                    <React.Fragment key={doc.id}>
                      <ListItem
                        button
                        onClick={() => handleEditDocument(doc)}
                        sx={{ pl: 0 }}
                      >
                        <ListItemIcon>
                          <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}>
                            <EditIcon fontSize="small" />
                          </Avatar>
                        </ListItemIcon>
                        <ListItemText
                          primary={doc.title}
                          secondary={`Updated ${new Date(doc.metadata.updatedAt).toLocaleDateString()}`}
                        />
                        <Chip 
                          label={doc.metadata.status} 
                          size="small" 
                          variant="outlined"
                          color={
                            doc.metadata.status === 'published' ? 'success' :
                            doc.metadata.status === 'review' ? 'warning' : 'default'
                          }
                        />
                      </ListItem>
                      {index < getRecentDocuments().length - 1 && <Divider />}
                    </React.Fragment>
                  ))}
                </List>
              ) : (
                <Box textAlign="center" py={4}>
                  <Typography variant="body2" color="text.secondary">
                    No documents yet. Create your first work instruction!
                  </Typography>
                  <Button 
                    variant="contained" 
                    startIcon={<AddIcon />}
                    onClick={handleCreateDocument}
                    sx={{ mt: 2 }}
                  >
                    Create Document
                  </Button>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Popular Templates */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                <Typography variant="h6">
                  <StarIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Popular Templates
                </Typography>
                <Button 
                  size="small" 
                  endIcon={<ArrowForwardIcon />}
                  onClick={() => navigate('/templates')}
                >
                  View All
                </Button>
              </Box>
              
              {templates.slice(0, 4).map((template, index) => (
                <React.Fragment key={template.id}>
                  <ListItem
                    button
                    onClick={() => handleCreateFromTemplate(template)}
                    sx={{ pl: 0 }}
                  >
                    <ListItemIcon>
                      <Avatar sx={{ width: 32, height: 32, bgcolor: 'secondary.main' }}>
                        <TemplateIcon fontSize="small" />
                      </Avatar>
                    </ListItemIcon>
                    <ListItemText
                      primary={template.name}
                      secondary={template.description}
                    />
                    <Chip 
                      label={template.category} 
                      size="small" 
                      variant="outlined"
                    />
                  </ListItem>
                  {index < Math.min(templates.length, 4) - 1 && <Divider />}
                </React.Fragment>
              ))}
            </CardContent>
          </Card>
        </Grid>

        {/* Document Status Overview */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <TrendingUpIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Document Status Overview
              </Typography>
              
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'primary.light', color: 'white' }}>
                    <Typography variant="h4">{stats.draft}</Typography>
                    <Typography variant="body2">Draft</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={6}>
                  <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'warning.light', color: 'white' }}>
                    <Typography variant="h4">{stats.inReview}</Typography>
                    <Typography variant="body2">In Review</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={6}>
                  <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'success.light', color: 'white' }}>
                    <Typography variant="h4">{stats.published}</Typography>
                    <Typography variant="body2">Published</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={6}>
                  <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'info.light', color: 'white' }}>
                    <Typography variant="h4">{stats.total}</Typography>
                    <Typography variant="body2">Total</Typography>
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Content Library Overview */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                <Typography variant="h6">
                  <ContentIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Content Library
                </Typography>
                <Button 
                  size="small" 
                  endIcon={<ArrowForwardIcon />}
                  onClick={() => navigate('/content')}
                >
                  Browse
                </Button>
              </Box>
              
              <Grid container spacing={1}>
                {Object.entries(contentLibrary).map(([category, items]) => (
                  <Grid item xs={6} key={category}>
                    <Box
                      sx={{
                        p: 1.5,
                        borderRadius: 1,
                        bgcolor: 'grey.100',
                        textAlign: 'center',
                        cursor: 'pointer',
                        '&:hover': { bgcolor: 'grey.200' }
                      }}
                      onClick={() => navigate('/content')}
                    >
                      <Typography variant="h6" color="primary">
                        {items.length}
                      </Typography>
                      <Typography variant="caption" display="block">
                        {category.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
                      </Typography>
                    </Box>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard;