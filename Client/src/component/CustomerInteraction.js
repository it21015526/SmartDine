import React from 'react';
import task from '../Assets/task2.mp4'; // Import the video file

function CustomerInteraction() {
  return (
    <div style={{ padding: 20 }}>
      <div style={{ fontSize: 30, fontWeight: 'bold', textAlign: 'center', marginBottom: 10 }}>
        Customer Interaction
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
        <div style={{ backgroundColor: 'white', height: '100%', width: '50%', border: '1px solid black', display: 'block' }}>

          <video autoPlay loop muted style={{ width: '100%', height: '100%', objectFit: 'cover', zIndex: -1 }}>
                <source src={task} type="video/mp4" />
                Please use a browser that supports the video tag.
              </video>
        </div>
        <div style={{ backgroundColor: 'white', height: '100%', width: '50%', border: '1px solid black', display: 'block' }}>
          <div>
            <div>
              Incidents : 0
            </div>
            <div>
              Other value : 0
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CustomerInteraction;
