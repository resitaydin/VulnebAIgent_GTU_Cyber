import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Card, Row, Col, Button, Badge } from 'react-bootstrap';

const Home = () => {
  // In a full application, we would fetch this data from the backend
  // For the sake of this demo, we'll use localStorage to store scans
  const [scans, setScans] = useState([]);

  useEffect(() => {
    // Get scans from localStorage
    const storedScans = JSON.parse(localStorage.getItem('scans') || '[]');
    setScans(storedScans);
  }, []);

  const getStatusBadge = (status) => {
    switch (status) {
      case 'running':
        return <Badge bg="info">Running</Badge>;
      case 'completed':
        return <Badge bg="success">Completed</Badge>;
      case 'error':
        return <Badge bg="danger">Error</Badge>;
      default:
        return <Badge bg="secondary">Unknown</Badge>;
    }
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>Recent Vulnerability Scans</h1>
        <Link to="/new-scan" className="btn btn-primary">
          Start New Scan
        </Link>
      </div>

      {scans.length === 0 ? (
        <div className="text-center p-5 bg-light rounded">
          <h3>No scans found</h3>
          <p>Start a new vulnerability scan to see results here.</p>
          <Link to="/new-scan" className="btn btn-primary">
            Start New Scan
          </Link>
        </div>
      ) : (
        <Row>
          {scans.map((scan) => (
            <Col md={4} key={scan.scanId}>
              <Card className={`scan-card status-${scan.status}`}>
                <Card.Body>
                  <Card.Title className="d-flex justify-content-between">
                    Scan ID: {scan.scanId.slice(-6)}
                    {getStatusBadge(scan.status)}
                  </Card.Title>
                  <Card.Text>
                    <strong>Target:</strong> {scan.targetIp}<br />
                    <strong>Started:</strong> {scan.startTime}<br />
                    <strong>Description:</strong> {scan.scanDescription.length > 50 
                      ? `${scan.scanDescription.slice(0, 50)}...` 
                      : scan.scanDescription}
                  </Card.Text>
                  <div className="d-flex justify-content-between">
                    <Link to={`/scan/${scan.scanId}`} className="btn btn-sm btn-primary">
                      View Details
                    </Link>
                    {scan.status === 'completed' && (
                      <Link to={`/report/${scan.scanId}`} className="btn btn-sm btn-success">
                        View Report
                      </Link>
                    )}
                  </div>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      )}
    </div>
  );
};

export default Home; 