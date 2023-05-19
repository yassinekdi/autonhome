import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import Dashboard from './components/Dashboard';
import Calendar from './components/Calendar';
import Navbar from './components/Navbar';
import { getAccessToken, getMeasures } from './api';

const theme = createTheme();

function App() {
  const [measures, setMeasures] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const token = await getAccessToken('admin', 'admin123');
      console.log("Token : ", token); // Pour tester, on affiche le token dans la console

      const measures = await getMeasures(token);
      setMeasures(measures);
      console.log("Measures: ", measures);
    };
    fetchData();

    const intervalId = setInterval(fetchData, 10000); // Fetch data every 10 seconds

    return () => clearInterval(intervalId); // This represents the unmount function, in which you need to clear your interval to prevent memory leaks.
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/calendrier" element={<Calendar />} />
          <Route path="/" element={<Dashboard measures={measures} />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
