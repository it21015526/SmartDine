import React from 'react'
import task from '../Assets/task3.mp4'

function TableTurnover() {
  return (
    <div style={{padding  : 20}}>
        <div style={{fontSize : 30,fontWeight : 'bold',textAlign : 'center',marginBottom : 10}}>
        Table turnover and Layout information
        </div>
        <div style={{display : 'flex',justifyContent : 'space-between'}}>
            <div style={{ backgroundColor: 'white', height: '100%', width: '50%', display: 'block' }}>
              <video autoPlay loop muted style={{ width: '100%', height: '100%', objectFit: 'cover', zIndex: 10 }}>
                    <source src={task} type="video/mp4" />
                    Please use a browser that supports the video tag.
                  </video>
              </div>
            <div style={{backgroundColor : 'white',height : '100%',width : '40%',display : 'block'}}>
                  <div style={{backgroundColor : 'orange',borderRadius : 18,padding : 10,margin : 10,height : 150,display : 'flex',justifyContent : 'center'}}>
                    <div>
                        <div style={{textAlign : 'center',fontSize : 50,fontWeight : 'bold'}}>
                          16/25
                        </div>
                        <div style={{fontWeight : 'bold'}}>
                          Current tale turnover Rate
                        </div>
                    </div>
                  </div>
                  <div style={{backgroundColor : 'orange',borderRadius : 18,padding : 10,margin : 10,height : 150,display : 'flex',justifyContent : 'center'}}>
                    <div>
                        <div style={{textAlign : 'center',fontSize : 50,fontWeight : 'bold'}}>
                          0
                        </div>
                        <div style={{fontWeight : 'bold'}}>
                          Total Detected Layout Changes 
                        </div>
                    </div>
                  </div>
            </div>
        </div>
    </div>
  )
}

export default TableTurnover