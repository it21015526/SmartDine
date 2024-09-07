import logo from './logo.svg';
import './App.css';
import Home from './Screens/Home';
import { Route, Router, Routes } from 'react-router-dom';
import CustomerTurnaround from './component/CustomerTurnaround';
import CustomerInteraction from './component/CustomerInteraction';
import TableTurnover from './component/TableTurnover';
import DynamicRecource from './component/DynamicRecource';

function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/customerTurnaround" element={<CustomerTurnaround />} />
        <Route path="/customerInteraction" element={<CustomerInteraction />} />
        <Route path="/TableTurnover" element={<TableTurnover />} />
        <Route path="/dynamicresourceallocation" element={<DynamicRecource />} />
      </Routes>
    </div>
   
  );
}

export default App;
