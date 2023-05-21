import { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from './AuthContext';

const PrivateRoute = ({ component: Component, ...rest }) => {
  const { user } = useContext(AuthContext);

  return user 
    ? <Component {...rest} /> 
    : <Navigate to="/login" replace />;
};

export default PrivateRoute;
