import React, { useEffect, useState } from 'react';
import { Form, Button, Container, Row, Col, Card } from 'react-bootstrap';
import task from '../Assets/task3.mp4'; // Import the video file
import 'bootstrap/dist/css/bootstrap.min.css';

import axios from 'axios';

function TableTurnover() {
  const [taskType, setTaskType] = useState('');
  const [videoFile, setVideoFile] = useState(null);
  const [TableTurnover,setTableTurnover] = useState([])




  useEffect(() => {
    const fetchCustomerCount = () => {
      axios.get("http://localhost:5000/tableInfo")
        .then((res) => {
          console.log(res.data);
          setTableTurnover(res.data);
        })
        .catch((error) => {
          console.error("Error fetching table info:", error);
        });
    };
    fetchCustomerCount();
    const intervalId = setInterval(fetchCustomerCount, 10000);
    return () => clearInterval(intervalId);
  }, []);

  const handleFileChange = (e) => {
    setVideoFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('task_type', 'task3');
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
          <h2 className="text-center font-weight-bold">Table Turnover and Layout Information</h2>
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
          <Card className="mb-4" style={{ backgroundColor: 'orange', borderRadius: 18 }}>
            <Card.Body>
              <div className="d-flex justify-content-between">
                <div>
                  <h5>Current Table Turnover Rate:</h5>
                  <p>{TableTurnover.currentturnover}</p>
                </div>
              </div>
            </Card.Body>
          </Card>

          <Card className="mb-4" style={{ backgroundColor: 'orange', borderRadius: 18 }}>
            <Card.Body>
              <div className="d-flex justify-content-between">
                <div>
                  <h5>Total Detected Layout Changes:</h5>
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

export default TableTurnover;
