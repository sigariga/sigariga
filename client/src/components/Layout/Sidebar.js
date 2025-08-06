import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  Box,
  Typography,
  Collapse
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Edit as EditIcon,
  Description as TemplateIcon,
  LibraryBooks as ContentIcon,
  AccountTree as FlowchartIcon,
  GetApp as ExportIcon,
  ExpandLess,
  ExpandMore,
  Add as AddIcon,
  Folder as FolderIcon
} from '@mui/icons-material';
import { useWorkInstruction } from '../../context/WorkInstructionContext';

const SIDEBAR_WIDTH = 280;
const SIDEBAR_COLLAPSED_WIDTH = 80;

function Sidebar({ open, onToggle }) {
  const navigate = useNavigate();
  const location = useLocation();
  const { documents, templates, currentDocument, actions } = useWorkInstruction();
  const [documentsOpen, setDocumentsOpen] = React.useState(true);
  const [templatesOpen, setTemplatesOpen] = React.useState(false);

  const navigationItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: <DashboardIcon />,
      path: '/',
    },
    {
      id: 'workspace',
      label: 'Workspace',
      icon: <EditIcon />,
      path: '/workspace',
    },
    {
      id: 'templates',
      label: 'Templates',
      icon: <TemplateIcon />,
      path: '/templates',
    },
    {
      id: 'content',
      label: 'Content Library',
      icon: <ContentIcon />,
      path: '/content',
    },
    {
      id: 'flowchart',
      label: 'Flowcharts',
      icon: <FlowchartIcon />,
      path: '/flowchart',
    },
    {
      id: 'export',
      label: 'Export Center',
      icon: <ExportIcon />,
      path: '/export',
    },
  ];

  const handleNavigation = (path) => {
    navigate(path);
  };

  const handleDocumentSelect = (document) => {
    actions.setCurrentDocument(document);
    navigate(`/workspace/${document.id}`);
  };

  const handleNewDocument = () => {
    actions.createDocument({
      title: 'New Work Instruction',
      author: 'Current User'
    });
    navigate('/workspace');
  };

  const isActive = (path) => {
    if (path === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(path);
  };

  const drawerContent = (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Logo/Header */}
      <Box
        sx={{
          p: 2,
          borderBottom: '1px solid rgba(0, 0, 0, 0.12)',
          minHeight: '64px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: open ? 'flex-start' : 'center'
        }}
      >
        {open ? (
          <Typography variant="h6" component="div" sx={{ fontWeight: 'bold', color: '#1976d2' }}>
            WI Creator
          </Typography>
        ) : (
          <Typography variant="h6" component="div" sx={{ fontWeight: 'bold', color: '#1976d2' }}>
            WI
          </Typography>
        )}
      </Box>

      {/* Main Navigation */}
      <List sx={{ flexGrow: 1, pt: 1 }}>
        {navigationItems.map((item) => (
          <ListItem key={item.id} disablePadding>
            <ListItemButton
              onClick={() => handleNavigation(item.path)}
              selected={isActive(item.path)}
              sx={{
                minHeight: 48,
                justifyContent: open ? 'initial' : 'center',
                px: 2.5,
                '&.Mui-selected': {
                  backgroundColor: 'rgba(25, 118, 210, 0.1)',
                  borderRight: '3px solid #1976d2',
                  '& .MuiListItemIcon-root': {
                    color: '#1976d2',
                  },
                  '& .MuiListItemText-primary': {
                    color: '#1976d2',
                    fontWeight: 'medium',
                  },
                },
              }}
            >
              <ListItemIcon
                sx={{
                  minWidth: 0,
                  mr: open ? 3 : 'auto',
                  justifyContent: 'center',
                }}
              >
                {item.icon}
              </ListItemIcon>
              <ListItemText 
                primary={item.label} 
                sx={{ 
                  opacity: open ? 1 : 0,
                  '& .MuiListItemText-primary': {
                    fontSize: '0.875rem',
                  }
                }} 
              />
            </ListItemButton>
          </ListItem>
        ))}

        <Divider sx={{ my: 1 }} />

        {/* Recent Documents Section */}
        {open && (
          <>
            <ListItemButton
              onClick={() => setDocumentsOpen(!documentsOpen)}
              sx={{ px: 2.5 }}
            >
              <ListItemIcon>
                <FolderIcon />
              </ListItemIcon>
              <ListItemText 
                primary="Recent Documents" 
                sx={{ '& .MuiListItemText-primary': { fontSize: '0.875rem' } }}
              />
              {documentsOpen ? <ExpandLess /> : <ExpandMore />}
            </ListItemButton>

            <Collapse in={documentsOpen} timeout="auto" unmountOnExit>
              <List component="div" disablePadding>
                <ListItem disablePadding>
                  <ListItemButton
                    onClick={handleNewDocument}
                    sx={{ pl: 4, py: 0.5 }}
                  >
                    <ListItemIcon sx={{ minWidth: 30 }}>
                      <AddIcon fontSize="small" />
                    </ListItemIcon>
                    <ListItemText 
                      primary="New Document" 
                      sx={{ 
                        '& .MuiListItemText-primary': { 
                          fontSize: '0.8rem',
                          fontStyle: 'italic'
                        } 
                      }}
                    />
                  </ListItemButton>
                </ListItem>

                {documents.slice(0, 5).map((doc) => (
                  <ListItem key={doc.id} disablePadding>
                    <ListItemButton
                      onClick={() => handleDocumentSelect(doc)}
                      selected={currentDocument?.id === doc.id}
                      sx={{ 
                        pl: 4, 
                        py: 0.5,
                        '&.Mui-selected': {
                          backgroundColor: 'rgba(25, 118, 210, 0.08)',
                        },
                      }}
                    >
                      <ListItemIcon sx={{ minWidth: 30 }}>
                        <EditIcon fontSize="small" />
                      </ListItemIcon>
                      <ListItemText 
                        primary={doc.title}
                        secondary={new Date(doc.metadata.updatedAt).toLocaleDateString()}
                        sx={{
                          '& .MuiListItemText-primary': {
                            fontSize: '0.8rem',
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap',
                          },
                          '& .MuiListItemText-secondary': {
                            fontSize: '0.7rem',
                          },
                        }}
                      />
                    </ListItemButton>
                  </ListItem>
                ))}

                {documents.length === 0 && (
                  <ListItem>
                    <ListItemText
                      primary="No documents yet"
                      sx={{
                        pl: 4,
                        '& .MuiListItemText-primary': {
                          fontSize: '0.8rem',
                          color: 'text.secondary',
                          fontStyle: 'italic',
                        },
                      }}
                    />
                  </ListItem>
                )}
              </List>
            </Collapse>

            {/* Templates Section */}
            <ListItemButton
              onClick={() => setTemplatesOpen(!templatesOpen)}
              sx={{ px: 2.5 }}
            >
              <ListItemIcon>
                <TemplateIcon />
              </ListItemIcon>
              <ListItemText 
                primary="Quick Templates" 
                sx={{ '& .MuiListItemText-primary': { fontSize: '0.875rem' } }}
              />
              {templatesOpen ? <ExpandLess /> : <ExpandMore />}
            </ListItemButton>

            <Collapse in={templatesOpen} timeout="auto" unmountOnExit>
              <List component="div" disablePadding>
                {templates.slice(0, 4).map((template) => (
                  <ListItem key={template.id} disablePadding>
                    <ListItemButton
                      onClick={() => {
                        actions.setActiveTemplate(template);
                        actions.createDocument({
                          title: `New ${template.name}`,
                          template: template.id,
                          content: template.sections || []
                        });
                        navigate('/workspace');
                      }}
                      sx={{ pl: 4, py: 0.5 }}
                    >
                      <ListItemIcon sx={{ minWidth: 30 }}>
                        <TemplateIcon fontSize="small" />
                      </ListItemIcon>
                      <ListItemText 
                        primary={template.name}
                        sx={{
                          '& .MuiListItemText-primary': {
                            fontSize: '0.8rem',
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap',
                          },
                        }}
                      />
                    </ListItemButton>
                  </ListItem>
                ))}
              </List>
            </Collapse>
          </>
        )}
      </List>

      {/* Footer */}
      {open && (
        <Box
          sx={{
            p: 2,
            borderTop: '1px solid rgba(0, 0, 0, 0.12)',
            backgroundColor: 'rgba(0, 0, 0, 0.02)',
          }}
        >
          <Typography variant="caption" color="text.secondary" align="center" display="block">
            Work Instruction Creator v1.0
          </Typography>
          <Typography variant="caption" color="text.secondary" align="center" display="block">
            © 2024 ahmad78
          </Typography>
        </Box>
      )}
    </Box>
  );

  return (
    <Drawer
      variant="permanent"
      open={open}
      sx={{
        width: open ? SIDEBAR_WIDTH : SIDEBAR_COLLAPSED_WIDTH,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: open ? SIDEBAR_WIDTH : SIDEBAR_COLLAPSED_WIDTH,
          boxSizing: 'border-box',
          transition: (theme) =>
            theme.transitions.create('width', {
              easing: theme.transitions.easing.sharp,
              duration: theme.transitions.duration.enteringScreen,
            }),
          overflowX: 'hidden',
        },
      }}
    >
      {drawerContent}
    </Drawer>
  );
}

export default Sidebar;