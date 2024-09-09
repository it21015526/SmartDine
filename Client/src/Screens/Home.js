import React from 'react';
import Grid from '@mui/material/Grid';
import { Button, Typography, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';

function Home() {
  const navigate = useNavigate();

  return (
    <Grid
      container
      style={{
        minHeight: '100vh',
        backgroundImage: 'url(https://source.unsplash.com/1600x900/?restaurant)',
        backgroundSize: 'cover',
        padding: '20px',
        zIndex: 0, // Ensure the content is visible above background elements
        position: 'relative',
      }}
    >
      {/* Header */}
      <Grid item xs={12} md={12}>
        <Box
          display="flex"
          justifyContent="center"
          alignItems="center"
          height="15vh"
        >
          <Typography
            variant="h2"
            component="div"
            style={{
              color: 'Black',
              fontWeight: 'bold',
              textShadow: '2px 2px 4px rgba(0, 0, 0, 0.7)',
            }}
          >
            Smart Dine
          </Typography>
        </Box>
      </Grid>

      {/* Image Section */}
      <Grid
        item
        xs={12}
        md={12}
        style={{
          display: 'flex',
          justifyContent: 'center',
          marginBottom: '40px',
        }}
      >
        <Box
          component="img"
          sx={{
            height: { xs: 250, md: 300 },
            width: { xs: 250, md: 300 },
            borderRadius: '50%',
            boxShadow: '0px 10px 20px rgba(0, 0, 0, 0.2)',
          }}
          alt="Smart Dine Image"
          src={require('../Assets/newIcn.jpeg')}
        />
      <a href="https://www.luckyelephanthotel.com/" target="_blank" rel="noopener noreferrer">
        <Box
          component="img"
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            marginTop: 15,
            height: { xs: 350, md: 100 },
          }}
          alt="Hotel Image"
          src={require('../Assets/le.png')}
        />
      </a>
      </Grid>

      {/* Button Section */}
      <Grid item xs={12} md={12}>
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'space-around',
            backgroundColor: 'rgba(255, 255, 255, 0.9)',
            borderRadius: '15px',
            padding: '20px',
            boxShadow: '0px 10px 20px rgba(0, 0, 0, 0.1)',
            zIndex: 1, // Ensure the buttons stay above the background and other elements
          }}
        >
          <Button
            variant="contained"
            color="primary"
            size="large"
            onClick={() => navigate('/customerTurnaround')}
            sx={{ fontSize: '1.2rem', padding: '10px 30px' }}
          >
            Customer Turnaround
          </Button>

          <Button
            variant="contained"
            color="primary"
            size="large"
            onClick={() => navigate('/customerInteraction')}
            sx={{ fontSize: '1.2rem', padding: '10px 30px' }}
          >
            Customer Interaction
          </Button>

          <Button
            variant="contained"
            color="primary"
            size="large"
            onClick={() => navigate('/TableTurnover')}
            sx={{ fontSize: '1.2rem', padding: '10px 30px' }}
          >
            Table Turnover
          </Button>

          <Button
            variant="contained"
            color="primary"
            size="large"
            onClick={() => navigate('/dynamicresourceallocation')}
            sx={{ fontSize: '1.2rem', padding: '10px 30px' }}
          >
            Dynamic Resource Allocation
          </Button>
        </Box>
      </Grid>
    </Grid>
  );
}

export default Home;
