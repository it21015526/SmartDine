import React from 'react';
import { Route, Routes } from 'react-router-dom';
import Home from './Screens/Home';
import CustomerTurnaround from './component/CustomerTurnaround';
import CustomerInteraction from './component/CustomerInteraction';
import TableTurnover from './component/TableTurnover';
import DynamicRecource from './component/DynamicRecource';
import Layout from './component/Layout'; // Import Layout
import Login from './component/login';

function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/home" element={<Home />} />
        <Route path="/customerTurnaround" element={<Layout><CustomerTurnaround /></Layout>} />
        <Route path="/customerInteraction" element={<Layout><CustomerInteraction /></Layout>} />
        <Route path="/TableTurnover" element={<Layout><TableTurnover /></Layout>} />
        <Route path="/dynamicresourceallocation" element={<Layout><DynamicRecource /></Layout>} />
      </Routes>
    </div>
  );
}

export default App;
