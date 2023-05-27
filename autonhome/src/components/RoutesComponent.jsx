import { useContext } from 'react';
import { Route, Routes, Navigate } from 'react-router-dom';
import Dashboard from './Dashboard';
import Calendar from './Calendar';
import LoginPage from '../pages/LoginPage';
import { AuthContext } from '../AuthContext';

function RoutesComponent() {
  const { token, measures } = useContext(AuthContext);

return (
  <Routes>
    <Route path="/login" element={<LoginPage />} />
    <Route path="/calendrier" element={token ? <Calendar /> : <Navigate to="/login" replace />} />
    <Route path="/" element={token ? <Dashboard measures={measures} /> : <Navigate to="/login" replace />} />
  </Routes>
);
}

export default RoutesComponent;
