import React from 'react'
import Grid from '@mui/material/Grid';
import { Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

function Home({navigaion}) {

    const navigate = useNavigate()

   




  return (
    <Grid container style={{height : '100vh',justifyContent : 'space-between',padding : 20}}>
        <Grid xs = {12} md = {12}>
            <div style={{fontSize : 40,textAlign : 'center',fontWeight : 'bold'}}>
                Smart Dine 
            </div>
        </Grid>
        <Grid style={{display : 'flex',justifyContent :'center'}} md = {12} xs = {12}>
                <img src={require('../Assets/homeImg.png')}/>
        </Grid>
        <Grid md = {12} xs= {12} >
            <div style={{justifyContent :'space-between',width : '100%',backgroundColor : 'white',display : 'flex'}}>
                <Button variant='contained' onClick={() => {navigate('/customerTurnaround')}}>Customer Turnaround</Button>
                <Button variant='contained' onClick={() => {navigate('/customerInteraction')}}>Customer Interaction</Button>
                <Button variant='contained' onClick={() => {navigate('/TableTurnover')}}>Table turnover</Button>
                <Button variant='contained' onClick={() => {navigate('/dynamicresourceallocation')}}>Dynamic recourse allocation</Button>
            </div>
        </Grid>

    </Grid>

  )
}

export default Home