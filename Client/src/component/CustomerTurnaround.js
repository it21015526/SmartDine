import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Form, Button, Container, Row, Col, Card } from 'react-bootstrap';
import task from '../Assets/task1.mp4';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function CustomerTurnaround() {
  const [taskType, setTaskType] = useState('');
  const [videoFile, setVideoFile] = useState(null);
  const [modelPath, setModelPath] = useState('');
  const [CustomerCount,setCustomerCount] = useState([])

  const handleFileChange = (e) => {
    setVideoFile(e.target.files[0]);
  };

  useEffect(() => {
    const fetchCustomerCount = () => {
      axios.get("http://localhost:5000/currentCustomer")
        .then((res) => {
          console.log(res.data);
          setCustomerCount(res.data);
        })
        .catch((error) => {
          console.error("Error fetching customer count:", error);
        });
    };
    fetchCustomerCount();
    const intervalId = setInterval(fetchCustomerCount, 10000);
    return () => clearInterval(intervalId);
  }, []);

  
  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('task_type', 'task1');
    formData.append('video', videoFile);
    if (modelPath) {
      formData.append('model_path', modelPath);
    }

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
          <h2 className="text-center font-weight-bold">Customer Turnaround</h2>
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
            <Card.Body className="d-flex justify-content-center align-items-center">
              <div>
                <div className="text-center" style={{ fontSize: 50, fontWeight: 'bold' }}>{CustomerCount.customer_count}</div>
                <div className="text-center font-weight-bold">Current Customer Count</div>
              </div>
            </Card.Body>
          </Card>

          <Card className="mb-4" style={{ backgroundColor: 'cyan', borderRadius: 18 }}>
            <Card.Body className="d-flex justify-content-center align-items-center">
              <div>
                <div className="text-center" style={{ fontSize: 50, fontWeight: 'bold' }}>{CustomerCount.datetime}</div>
                <div className="text-center font-weight-bold">Last Updated</div>
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
