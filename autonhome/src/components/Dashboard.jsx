import React from 'react';
import DashboardSection from './DashboardSection';
import { Container, Box } from '@mui/material';

const Dashboard = ({ measures }) => {
  if (!measures) {
    return null; // ou retourner un loader, un message, etc.
  }

  const measuresBySection = measures.reduce((groups, measure) => {
    const group = (groups[measure.section] || []);
    group.push(measure);
    groups[measure.section] = group;
    return groups;
  }, {});

  return (
    <Box>
      <Container>
        {Object.entries(measuresBySection).map(([section, sectionMeasures]) => (
          <DashboardSection key={section} title={section} measures={sectionMeasures}/>
        ))}
      </Container>
    </Box>
  );
}

export default Dashboard;
