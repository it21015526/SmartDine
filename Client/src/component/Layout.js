import React from 'react';
import { Box, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';  // Import useNavigate
import DrawerMenu from './DrawerMenu'; // Import the DrawerMenu

function Layout({ children }) {
  const navigate = useNavigate();  // Initialize navigate

  return (
    <div>
      <Box display="flex" justifyContent="space-between" alignItems="center" padding="16px" bgcolor="primary.main" color="white">
        {/* Clickable Typography for navigation to Home */}
        <Typography 
          variant="h5" 
          fontWeight="bold" 
          style={{ cursor: 'pointer' }} 
          onClick={() => navigate('/')} // Navigate to home page when clicked
        >
          Smart Dine
        </Typography>
        <DrawerMenu />
      </Box>
      <Box padding={4}>
        {children}
      </Box>
    </div>
  );
}

export default Layout;
