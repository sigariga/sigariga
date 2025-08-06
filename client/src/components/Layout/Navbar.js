import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Box,
  Badge,
  Avatar,
  Tooltip,
  Menu,
  MenuItem
} from '@mui/material';
import {
  Menu as MenuIcon,
  Notifications as NotificationsIcon,
  Settings as SettingsIcon,
  Help as HelpIcon,
  AccountCircle as AccountIcon
} from '@mui/icons-material';
import { useWorkInstruction } from '../../context/WorkInstructionContext';

function Navbar({ onSidebarToggle }) {
  const { currentDocument, error } = useWorkInstruction();
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const getDocumentTitle = () => {
    if (currentDocument) {
      return currentDocument.title;
    }
    return 'Work Instruction Creator';
  };

  const getDocumentStatus = () => {
    if (currentDocument) {
      const status = currentDocument.metadata?.status || 'draft';
      return status.charAt(0).toUpperCase() + status.slice(1);
    }
    return null;
  };

  return (
    <AppBar 
      position="fixed" 
      sx={{ 
        zIndex: (theme) => theme.zIndex.drawer + 1,
        backgroundColor: '#1976d2'
      }}
    >
      <Toolbar>
        <IconButton
          color="inherit"
          aria-label="toggle sidebar"
          onClick={onSidebarToggle}
          edge="start"
          sx={{ mr: 2 }}
        >
          <MenuIcon />
        </IconButton>
        
        <Box sx={{ flexGrow: 1, display: 'flex', alignItems: 'center' }}>
          <Typography variant="h6" noWrap component="div" sx={{ mr: 2 }}>
            {getDocumentTitle()}
          </Typography>
          
          {getDocumentStatus() && (
            <Box
              sx={{
                px: 1,
                py: 0.5,
                borderRadius: 1,
                backgroundColor: 'rgba(255, 255, 255, 0.2)',
                fontSize: '0.75rem',
                fontWeight: 'medium'
              }}
            >
              {getDocumentStatus()}
            </Box>
          )}
          
          {currentDocument?.metadata?.lastSaved && (
            <Typography 
              variant="caption" 
              sx={{ 
                ml: 2, 
                opacity: 0.8,
                display: { xs: 'none', sm: 'block' }
              }}
            >
              Last saved: {new Date(currentDocument.metadata.lastSaved).toLocaleTimeString()}
            </Typography>
          )}
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          {error && (
            <Tooltip title={`Error: ${error}`}>
              <Badge color="error" variant="dot">
                <NotificationsIcon />
              </Badge>
            </Tooltip>
          )}
          
          <Tooltip title="Help">
            <IconButton color="inherit" size="small">
              <HelpIcon />
            </IconButton>
          </Tooltip>
          
          <Tooltip title="Settings">
            <IconButton color="inherit" size="small">
              <SettingsIcon />
            </IconButton>
          </Tooltip>
          
          <Tooltip title="Account">
            <IconButton
              color="inherit"
              onClick={handleMenuOpen}
              size="small"
            >
              <Avatar 
                sx={{ 
                  width: 32, 
                  height: 32, 
                  backgroundColor: 'rgba(255, 255, 255, 0.2)' 
                }}
              >
                <AccountIcon />
              </Avatar>
            </IconButton>
          </Tooltip>
        </Box>

        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
          onClick={handleMenuClose}
          PaperProps={{
            elevation: 0,
            sx: {
              overflow: 'visible',
              filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
              mt: 1.5,
              '& .MuiAvatar-root': {
                width: 24,
                height: 24,
                ml: -0.5,
                mr: 1,
              },
              '&:before': {
                content: '""',
                display: 'block',
                position: 'absolute',
                top: 0,
                right: 14,
                width: 10,
                height: 10,
                bgcolor: 'background.paper',
                transform: 'translateY(-50%) rotate(45deg)',
                zIndex: 0,
              },
            },
          }}
          transformOrigin={{ horizontal: 'right', vertical: 'top' }}
          anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
        >
          <MenuItem onClick={handleMenuClose}>
            <Avatar /> Profile
          </MenuItem>
          <MenuItem onClick={handleMenuClose}>
            <Avatar /> My Account
          </MenuItem>
          <MenuItem onClick={handleMenuClose}>
            <Avatar /> Settings
          </MenuItem>
          <MenuItem onClick={handleMenuClose}>
            <Avatar /> Logout
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;