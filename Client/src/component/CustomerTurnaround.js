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
          <h6 className="text-center font-weight-bold">Last Updated : {CustomerCount.datetime}</h6>
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
        <Row xs={1} sm={2} md={3} lg={3} className="g-4">
            <Col>
              <Card className="mb-4" style={{ backgroundColor: 'cyan', borderRadius: 18,height : 130 }}>
                <Card.Body style={{textAlign : 'center'}}>
                  <h5 >Total Customer Count</h5>
                  <p style={{fontWeight : 'bold',fontSize : 20}}>{CustomerCount.customer_count}</p>
                </Card.Body>
              </Card>
            </Col>
            <Col>
              <Card className="mb-4" style={{ backgroundColor: 'cyan', borderRadius: 18,height : 130 }}>
                <Card.Body style={{textAlign : 'center'}}>
                  <h5>Average Seating Time exceeded </h5>
                  <p style={{fontWeight : 'bold',fontSize : 20}}>{CustomerCount.seting_exceed}</p>
                </Card.Body>
              </Card>
            </Col>
            <Col>
              <Card className="mb-4" style={{ backgroundColor: 'cyan', borderRadius: 18,height : 130 }}>
                <Card.Body style={{textAlign : 'center'}}>
                  <h5>Food Delivary Time Exceeded</h5>
                  <p style={{fontWeight : 'bold',fontSize : 20}}>{CustomerCount.food_exceed}</p>
                </Card.Body>
              </Card>
            </Col>
         
          </Row>

          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="videoFile">
              <Form.Label>Video File</Form.Label>
              <Form.Control type="file" onChange={handleFileChange} required />
            </Form.Group>

            <Button variant="primary" type="submit" className="mt-2">
              Submit
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
}
