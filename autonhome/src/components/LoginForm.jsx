import React, { useState, useContext } from 'react';
import { AuthContext } from '../AuthContext';
import { Button, TextField, Box } from '@mui/material';
import { postLogin, getAccessToken, getMeasures } from '../api';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';

function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { user, setUser, setToken, setMeasures } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const token = await getAccessToken(username, password);
    
      if (token) {
        const data = await postLogin(token, username, password);
        if (data.key) {
          setUser({ token: data.key, username: username, password: password });
          setToken(data.key);

          // Fetch measures after successful login
          const measures = await getMeasures(data.key);
          setMeasures(measures);
          navigate('/'); // Navigates to the home page or any other page
        }
      }
    } catch (error) {
      console.error(`Login error: ${error}`);
    }
  };
  
  useEffect(() => {

  }, [user]);
  
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
