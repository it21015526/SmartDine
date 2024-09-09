import React, { useState } from 'react';
import { Form, Button, Container, Row, Col } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box'; // Import Material UI Box if you're using it

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Username:', username);
    console.log('Password:', password);

    if (username === 'admin' && password === 'admin') {
      navigate('/home');
    }
  };

  return (
    <Container>
      <Row className="justify-content-md-center align-items-center" style={{ minHeight: '100vh' }}>
        {/* Column for the Image */}
        <Col xs={12} md={6} className="text-center">
          <Box
            component="img"
            sx={{
              height: { xs: 250, md: 300 },
              width: { xs: 250, md: 300 },
              borderRadius: '50%',
              boxShadow: '0px 10px 20px rgba(0, 0, 0, 0.2)',
            }}
            alt="Smart Dine Image"
            src={require('../Assets/newIcn.jpeg')} // Make sure the path is correct
          />
        </Col>

        {/* Column for the Login Form */}
        <Col xs={12} md={6}>
          <h2 className="text-center">Login</h2>
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="formBasicUsername" className="mb-3">
              <Form.Label>Username</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group controlId="formBasicPassword" className="mb-3">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </Form.Group>

            <Button variant="primary" type="submit" className="w-100">
              Login
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default Login;
