import React from 'react';
import { AppBar, Toolbar,Typography, Button } from '@mui/material';
import { styled } from '@mui/system';
import { Link } from 'react-router-dom';

import EventNoteIcon from '@mui/icons-material/EventNote';
import NotificationsIcon from '@mui/icons-material/Notifications';
import SettingsIcon from '@mui/icons-material/Settings';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';

const StyledAppBar = styled(AppBar)(({ theme }) => ({
  marginBottom: theme.spacing(2),
  // backgroundColor: '#CBEAED', // insérer votre couleur ici
}));

function Navbar() {
  const fsize = "16px";

  return (
    <StyledAppBar position="static">
      <Toolbar>
        <Typography variant="h6" component={Link} sx={{ flexGrow: 1, color: 'inherit', textDecoration: 'none' }} to="/">
          AutonHome
        </Typography>
        <Button
          color="inherit"
          component={Link}
          to="/calendrier"
          startIcon={<EventNoteIcon />}
          sx={{ textTransform: 'capitalize', fontSize: fsize, fontWeight: 'bold' }}
        >
          Calendrier
        </Button>
        <Button
          color="inherit"
          startIcon={<NotificationsIcon />}
          sx={{ textTransform: 'capitalize', fontSize: fsize, fontWeight: 'bold' }}
        >
          Notifications
        </Button>
        <Button
          color="inherit"
          startIcon={<SettingsIcon />}
          sx={{ textTransform: 'capitalize', fontSize: fsize, fontWeight: 'bold' }}
        >
          Paramètres
        </Button>
        <Button
          color="inherit"
          startIcon={<ExitToAppIcon />}
          sx={{ textTransform: 'capitalize', fontSize: fsize, fontWeight: 'bold' }}
        >
          Déconnexion
        </Button>
      </Toolbar>
    </StyledAppBar>
  );
}

export default Navbar;
