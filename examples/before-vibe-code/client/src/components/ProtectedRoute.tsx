import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  const location = useLocation();

  if (!isAuthenticated) {
    // Redirect user to login with return state
    return (
      <Navigate
        to="/login"
        state={{
          from: location.pathname,
          notice: 'Please sign in to access Setup Prompt!'
        }}
        replace
      />
    );
  }

  return <>{children}</>;
};
