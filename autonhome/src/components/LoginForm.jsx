import React, { useState } from 'react';
import axios from 'axios';
import { Button, TextField, Box } from '@mui/material';
import { postLogin } from '../api';

function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    const response = await postLogin(username, password);

    console.log(response.data);
  }

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{
        display: 'flex',
        flexDirection: 'column',
        maxWidth: 300,
        margin: 'auto',
      }}
    >
      <TextField
        label="Username"
        value={username}
        onChange={e => setUsername(e.target.value)}
        margin="normal"
        required
      />
      <TextField
        label="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        margin="normal"
        required
        type="password"
      />
      <Button type="submit" variant="contained" sx={{ mt: 3 }}>
        Login
      </Button>
    </Box>
  );
}

export default LoginForm;
