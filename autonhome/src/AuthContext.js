import React, { createContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getMeasures } from './api';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const storedToken = localStorage.getItem('userToken');
  const [user, setUser] = useState(storedToken ? {token: storedToken} : null);
  const [token, setToken] = useState(storedToken || null);
  const [measures, setMeasures] = useState([]);
  const navigate = useNavigate();

  const logout = () => {
    setUser(null);
    localStorage.removeItem('userToken');
    setToken(null);
    setMeasures([]);
    navigate('/login');
  };

  useEffect(() => {
    const fetchData = async () => {
      if (token) {
        const measures = await getMeasures(token);
        setMeasures(measures);
      }
    };

    fetchData();
    const intervalId = setInterval(fetchData, 10000); // Fetch data every 10 seconds

    return () => clearInterval(intervalId); // This represents the unmount function, in which you need to clear your interval to prevent memory leaks.
  }, [token]);

  return (
    <AuthContext.Provider value={{ user, setUser, token, setToken, logout, measures, setMeasures }}>
      {children}
    </AuthContext.Provider>
  );
}
