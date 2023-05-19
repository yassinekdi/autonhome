import React from 'react';
import { Box, Typography } from '@mui/material';

function Calendar() {
  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4" component="div" sx={{ fontWeight: 'bold', textAlign: 'center' }}>
        Calendrier
      </Typography>
      {/* Le composant de calendrier ira ici */}
    </Box>
  );
}

export default Calendar;
