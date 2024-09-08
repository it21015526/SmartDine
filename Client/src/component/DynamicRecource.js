import React from 'react'

function DynamicRecource() {
  return (
    <div style={{padding  : 20}}>
        <div style={{fontSize : 30,fontWeight : 'bold',textAlign : 'center',marginBottom : 10}}>
        Dynamic Recouce Allocation
        </div>
            
            <div style={{backgroundColor : 'white',display : 'block'}}>
                <iframe title="Dynamic Resource Allocation" width="100%" height="600" src="https://app.powerbi.com/reportEmbed?reportId=4a0d0199-f05c-4e1a-bacf-808362a28125&autoAuth=true&ctid=44e3cf94-19c9-4e32-96c3-14f5bf01391a" frameborder="0" allowFullScreen="true"></iframe>
            </div>
    </div>
  )
}

export default DynamicRecource