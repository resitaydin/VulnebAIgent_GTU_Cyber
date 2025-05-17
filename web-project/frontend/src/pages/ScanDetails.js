import React, { useState, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Card, Button, Alert, Spinner, Badge } from 'react-bootstrap';
import { getScanStatus } from '../services/api';
import { connectToSocket, disconnectFromSocket, subscribeToScanUpdates } from '../services/socket';

const ScanDetails = () => {
  const { scanId } = useParams();
  const [scan, setScan] = useState(null);
  const [logs, setLogs] = useState([]);
  const [status, setStatus] = useState('loading'); // loading, running, completed, error
  const [error, setError] = useState('');
  const logEndRef = useRef(null);
  
  // Get initial scan status
  useEffect(() => {
    const fetchScanStatus = async () => {
      try {
        const scanData = await getScanStatus(scanId);
        setScan(scanData);
        setStatus(scanData.status);
        
        // Update localStorage scan status
        const storedScans = JSON.parse(localStorage.getItem('scans') || '[]');
        const updatedScans = storedScans.map(s => 
          s.scanId === scanId ? { ...s, status: scanData.status } : s
        );
        localStorage.setItem('scans', JSON.stringify(updatedScans));
      } catch (err) {
        console.error('Error fetching scan status:', err);
        // Try to get scan info from localStorage
        const storedScans = JSON.parse(localStorage.getItem('scans') || '[]');
        const storedScan = storedScans.find(s => s.scanId === scanId);
        if (storedScan) {
          setScan(storedScan);
          setStatus(storedScan.status);
        } else {
          setError('Scan not found');
          setStatus('error');
        }
      }
    };
    
    fetchScanStatus();
  }, [scanId]);
  
  // Set up WebSocket connection
  useEffect(() => {
    connectToSocket();
    
    const unsubscribe = subscribeToScanUpdates(scanId, (newLog) => {
      setLogs(prevLogs => [...prevLogs, newLog]);
      
      // Check if scan completed or errored
      if (newLog.text && typeof newLog.text === 'string') {
        try {
          const logData = JSON.parse(newLog.text);
          if (logData.status === 'completed' || logData.status === 'error') {
            setStatus(logData.status);
            
            // Update localStorage
            const storedScans = JSON.parse(localStorage.getItem('scans') || '[]');
            const updatedScans = storedScans.map(s => 
              s.scanId === scanId ? { ...s, status: logData.status } : s
            );
            localStorage.setItem('scans', JSON.stringify(updatedScans));
          }
        } catch (e) {
          // Not JSON, ignore
        }
      }
    });
    
    return () => {
      unsubscribe();
      disconnectFromSocket();
    };
  }, [scanId]);
  
  // Auto-scroll to bottom when new logs arrive
  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);
  
  const formatLogText = (text) => {
    if (!text) return '';
    
    try {
      // Check if the text is JSON
      const jsonData = JSON.parse(text);
      return (
        <pre className="mb-0">
          {Object.entries(jsonData).map(([key, value]) => (
            <div key={key}>
              <strong>{key}:</strong> {typeof value === 'object' ? JSON.stringify(value, null, 2) : value.toString()}
            </div>
          ))}
        </pre>
      );
    } catch (e) {
      // Not JSON, return as is
      return <div>{text}</div>;
    }
  };
  
  const getStatusBadge = () => {
    switch (status) {
      case 'loading':
        return <Badge bg="secondary">Loading</Badge>;
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
  
  if (error) {
    return (
      <Alert variant="danger">
        {error}
        <div className="mt-3">
          <Link to="/" className="btn btn-primary">Back to Home</Link>
        </div>
      </Alert>
    );
  }
  
  if (!scan) {
    return (
      <div className="text-center p-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      </div>
    );
  }
  
  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1>Scan Details {getStatusBadge()}</h1>
          <p>
            <strong>Scan ID:</strong> {scanId}<br />
            <strong>Target:</strong> {scan.target_ip || scan.targetIp}<br />
            <strong>Started:</strong> {scan.start_time || scan.startTime}<br />
            <strong>Description:</strong> {scan.scan_description || scan.scanDescription}
          </p>
        </div>
        <div>
          {status === 'completed' && (
            <Link to={`/report/${scanId}`} className="btn btn-success">
              View Report
            </Link>
          )}
        </div>
      </div>

      <Card>
        <Card.Header>
          <div className="d-flex justify-content-between align-items-center">
            <h5 className="mb-0">Scan Logs</h5>
            {status === 'running' && (
              <Spinner animation="border" size="sm" role="status">
                <span className="visually-hidden">Running...</span>
              </Spinner>
            )}
          </div>
        </Card.Header>
        <Card.Body className="p-0">
          <div className="scan-log">
            {logs.length === 0 ? (
              <div className="p-3 text-center text-muted">
                Waiting for scan logs...
              </div>
            ) : (
              logs.map((log, index) => (
                <div key={index} className="log-entry p-2">
                  <div className="d-flex justify-content-between">
                    <span className={`agent-name agent-${log.agent_name}`}>{log.agent_name}</span>
                    <span className="timestamp">{log.timestamp}</span>
                  </div>
                  <div className="log-content mt-1">
                    {formatLogText(log.text)}
                  </div>
                </div>
              ))
            )}
            <div ref={logEndRef} />
          </div>
        </Card.Body>
      </Card>
      
      <div className="mt-3">
        <Link to="/" className="btn btn-primary">Back to Home</Link>
      </div>
    </div>
  );
};

export default ScanDetails; 