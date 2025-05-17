import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

// Import components
import Navbar from './components/Navbar';
import Home from './pages/Home';
import NewScan from './pages/NewScan';
import ScanDetails from './pages/ScanDetails';
import Report from './pages/Report';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <div className="container-fluid mt-3">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/new-scan" element={<NewScan />} />
            <Route path="/scan/:scanId" element={<ScanDetails />} />
            <Route path="/report/:scanId" element={<Report />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App; 