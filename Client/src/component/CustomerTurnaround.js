import axios from 'axios';
import React, { useEffect, useState } from 'react'

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
            Customer Turnaround
        </div>
        <div style={{display : 'flex',justifyContent : 'space-between'}}>
            <div style={{backgroundColor  : 'white',height : '100%',width : '50%',border : '1px solid black',display : 'block'}}>
                <div>Video frame</div>
            
                <iframe src="URL" title="description"></iframe>
            </div>
            <div style={{backgroundColor : 'white',height : '100%',width : '50%',border : '1px solid black',display : 'block'}}>
                <div>Dashboard</div>
                <iframe src="URL" title="description"></iframe>
            </div>
        </div>
<div>
<form onSubmit={handleSubmit}>
      <div>
        <label>Task Type:</label>
        <input
          type="text"
          value={taskType}
          onChange={(e) => setTaskType(e.target.value)}
          required
        />
      </div>
      <div>
        <label>Video File:</label>
        <input
          type="file"
          onChange={handleFileChange}
          required
        />
      </div>
      <div>
        <label>Model Path (optional):</label>
        <input
          type="text"
          value={modelPath}
          onChange={(e) => setModelPath(e.target.value)}
        />
      </div>
      <button type="submit">Submit</button>
    </form>
</div>
    </div>
    </>
  )
}
