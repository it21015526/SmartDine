import React, { useEffect, useState } from 'react';
import { Form, Button, Container, Row, Col, Card } from 'react-bootstrap';
import task from '../Assets/task2.mp4'; // Import the video file
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';

function CustomerInteraction() {
  const [taskType, setTaskType] = useState('');
  const [videoFile, setVideoFile] = useState(null);
  const [interInfo,setInterInfo] = useState([])

  const handleFileChange = (e) => {
    setVideoFile(e.target.files[0]);
  };


  useEffect(() => {
    const fetchInteractionInfo = () => {
      axios.get("http://localhost:5000/interactionInfo")
        .then((res) => {
          console.log(res.data);
          setInterInfo(res.data);
        })
        .catch((error) => {
          console.error("Error fetching customer count:", error);
        });
    };
    fetchInteractionInfo();
    const intervalId = setInterval(fetchInteractionInfo, 10000);
    return () => clearInterval(intervalId);
  }, []);



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
          <h6 className="text-center font-weight-bold">Last Updated : {interInfo.datetime}</h6>
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
              <Card className="mb-4" style={{ backgroundColor: 'yellow', borderRadius: 18,height : 130 }}>
                <Card.Body style={{textAlign : 'center'}}>
                  <p style={{fontWeight : 'bold',fontSize : 20}}>{interInfo.nonEmpty}</p>
                  <h6 >Dining Completed Non-Empty plates</h6>
                </Card.Body>
              </Card>
            </Col>
            <Col>
              <Card className="mb-4" style={{ backgroundColor: 'yellow', borderRadius: 18,height : 130 }}>
                <Card.Body style={{textAlign : 'center'}}>
                  <p style={{fontWeight : 'bold',fontSize : 20}}>{interInfo.waitingTime} min.</p>
                  <h5>Avg Assistance seeking Time </h5>
                </Card.Body>
              </Card>
            </Col>
            <Col>
              <Card className="mb-4" style={{ backgroundColor: 'yellow', borderRadius: 18,height : 130 }}>
                <Card.Body style={{textAlign : 'center'}}>
                  <p style={{fontWeight : 'bold',fontSize : 20}}>{interInfo.nonEating} min.</p>
                  <h5>Non Eating Dining time </h5>
                </Card.Body>
              </Card>
            </Col>
          </Row>

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
