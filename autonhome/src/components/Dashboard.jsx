import React from 'react';
import DashboardSection from './DashboardSection';
import { Container, Box } from '@mui/material';

const Dashboard = ({ measures }) => {
  const airMeasures = measures.filter(measure => measure.section === 'Air');
  const soilMeasures = measures.filter(measure => measure.section === 'Soil');
  const waterMeasures = measures.filter(measure => measure.section === 'Water');

  return (
    <Box>
      <Container>
        <DashboardSection title="Air" measures={airMeasures}/>
        <DashboardSection title="Sol" measures={soilMeasures}/>
        <DashboardSection title="Eau" measures={waterMeasures}/>
      </Container>
    </Box>
  );
}

export default Dashboard;
