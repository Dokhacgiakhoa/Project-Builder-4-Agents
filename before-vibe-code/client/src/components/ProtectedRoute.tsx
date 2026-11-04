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
    // Chuyển hướng người dùng về trang đăng nhập kèm trạng thái để sau khi đăng nhập có thể quay lại
    return (
      <Navigate
        to="/login"
        state={{
          from: location.pathname,
          notice: 'Vui lòng đăng nhập để sử dụng tính năng Setup Prompt!'
        }}
        replace
      />
    );
  }

  return <>{children}</>;
};
