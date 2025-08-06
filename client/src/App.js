import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import Navbar from './components/Layout/Navbar';
import Sidebar from './components/Layout/Sidebar';
import Dashboard from './pages/Dashboard';
import WorkspaceEditor from './pages/WorkspaceEditor';
import TemplateManager from './pages/TemplateManager';
import ContentLibrary from './pages/ContentLibrary';
import FlowchartEditor from './pages/FlowchartEditor';
import ExportCenter from './pages/ExportCenter';
import { WorkInstructionProvider } from './context/WorkInstructionContext';
import './App.css';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Segoe UI", "Roboto", "Arial", sans-serif',
  },
  components: {
    MuiDrawer: {
      styleOverrides: {
        paper: {
          borderRight: '1px solid rgba(0, 0, 0, 0.12)',
        },
      },
    },
  },
});

function App() {
  const [sidebarOpen, setSidebarOpen] = React.useState(true);

  const handleSidebarToggle = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <WorkInstructionProvider>
        <Router>
          <Box sx={{ display: 'flex', minHeight: '100vh' }}>
            <Navbar onSidebarToggle={handleSidebarToggle} />
            <Sidebar open={sidebarOpen} onToggle={handleSidebarToggle} />
            <Box
              component="main"
              sx={{
                flexGrow: 1,
                ml: sidebarOpen ? '280px' : '80px',
                mt: '64px',
                transition: theme.transitions.create(['margin'], {
                  easing: theme.transitions.easing.sharp,
                  duration: theme.transitions.duration.leavingScreen,
                }),
                minHeight: 'calc(100vh - 64px)',
                backgroundColor: theme.palette.background.default,
              }}
            >
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/workspace" element={<WorkspaceEditor />} />
                <Route path="/workspace/:id" element={<WorkspaceEditor />} />
                <Route path="/templates" element={<TemplateManager />} />
                <Route path="/content" element={<ContentLibrary />} />
                <Route path="/flowchart" element={<FlowchartEditor />} />
                <Route path="/flowchart/:id" element={<FlowchartEditor />} />
                <Route path="/export" element={<ExportCenter />} />
              </Routes>
            </Box>
          </Box>
        </Router>
      </WorkInstructionProvider>
    </ThemeProvider>
  );
}

export default App;