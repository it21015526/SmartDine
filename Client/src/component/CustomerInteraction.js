import React, { useState } from 'react';
import { Form, Button, Container, Row, Col, Card } from 'react-bootstrap';
import task from '../Assets/task2.mp4'; // Import the video file
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';

function CustomerInteraction() {
  const [taskType, setTaskType] = useState('');
  const [videoFile, setVideoFile] = useState(null);

  const handleFileChange = (e) => {
    setVideoFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('task_type', 'task2');
    formData.append('video', videoFile);

    try {
      const response = await axios.post('http://localhost:5000/process_video', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('Response:', response.data);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <Container style={{ padding: 20 }}>
      <Row className="mb-4">
        <Col>
          <h2 className="text-center font-weight-bold">Customer Interaction</h2>
        </Col>
      </Row>
      <Row>
        <Col md={6}>
          <video autoPlay loop muted style={{ width: '100%', height: '100%', objectFit: 'cover' }}>
            <source src={task} type="video/mp4" />
            Please use a browser that supports the video tag.
          </video>
        </Col>
        <Col md={6}>
          <Card className="mb-4" style={{ backgroundColor: 'cyan', borderRadius: 18 }}>
            <Card.Body>
              <div className="d-flex justify-content-between">
                <div>
                  <h5>Incidents:</h5>
                  <p>0</p>
                </div>
                <div>
                  <h5>Other Value:</h5>
                  <p>0</p>
                </div>
              </div>
            </Card.Body>
          </Card>

          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="videoFile">
              <Form.Label>Video File</Form.Label>
              <Form.Control type="file" onChange={handleFileChange} required />
            </Form.Group>

            <Button variant="primary" type="submit" className="mt-3">
              Submit
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
}

export default CustomerInteraction;
