import axios from 'axios';
import React, { useEffect, useState } from 'react'
import task from '../Assets/task1.mp4'

export default function CustomerTurnaround() {


    const [taskType, setTaskType] = useState('');
    const [videoFile, setVideoFile] = useState(null);
    const [modelPath, setModelPath] = useState('');
  
    const handleFileChange = (e) => {
      setVideoFile(e.target.files[0]);
    };
  

    useEffect(() => {


    }, [])


    const handleSubmit = async (e) => {
        e.preventDefault();
    
        const formData = new FormData();
        formData.append('task_type', taskType);
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
          console.log('Response::', response.data);
        } catch (error) {
          console.error('Error uploading file:', error);
        }
      };
    





  return (
    <>
     <div style={{padding  : 20}}>
        <div style={{fontSize : 30,fontWeight : 'bold',textAlign : 'center',marginBottom : 10}}>
        Customer turnaround 
        </div>
        <div style={{display : 'flex',justifyContent : 'space-between'}}>
            <div style={{ backgroundColor: 'white', height: '100%', width: '50%', display: 'block' }}>
              <video autoPlay loop muted style={{ width: '100%', height: '100%', objectFit: 'cover', zIndex: 10 }}>
                    <source src={task} type="video/mp4" />
                    Please use a browser that supports the video tag.
                  </video>
              </div>
            <div style={{backgroundColor : 'white',height : '100%',width : '40%',display : 'block'}}>
                  <div style={{backgroundColor : 'cyan',borderRadius : 18,padding : 10,margin : 10,height : 150,display : 'flex',justifyContent : 'center'}}>
                    <div>
                        <div style={{textAlign : 'center',fontSize : 50,fontWeight : 'bold'}}>
                          6
                        </div>
                        <div style={{fontWeight : 'bold'}}>
                          Current customer count 
                        </div>
                    </div>
                  </div>
                  <div style={{backgroundColor : 'cyan',borderRadius : 18,padding : 10,margin : 10,height : 150,display : 'flex',justifyContent : 'center'}}>
                    <div>
                        <div style={{textAlign : 'center',fontSize : 50,fontWeight : 'bold'}}>
                          0
                        </div>
                        <div style={{fontWeight : 'bold'}}>
                          Annomalies detected
                        </div>
                    </div>
                  </div>
            </div>
        </div>
    </div>    </>
  )
}
