import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import Navbar from './components/Navbar';
import {CssBaseline } from '@mui/material';
import { AuthProvider } from './AuthContext';
import RoutesComponent from './components/RoutesComponent';

const theme = createTheme({});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <AuthProvider>
          <Navbar />
          <RoutesComponent />
        </AuthProvider>
      </Router>
    </ThemeProvider>
  );
}

export default App;
