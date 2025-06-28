import React, { useState, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Card, Button, Alert, Spinner, Badge } from 'react-bootstrap';
import { getScanStatus, getScanLogs } from '../services/api';

const ScanDetails = () => {
  const { scanId } = useParams();
  const [scan, setScan] = useState(null);
  const [logs, setLogs] = useState([]);
  const [status, setStatus] = useState('loading'); // loading, running, completed, error
  const [error, setError] = useState('');
  const logEndRef = useRef(null);
  const pollingIntervalRef = useRef(null);
  
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
  
  // Poll for logs every few seconds
  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const logData = await getScanLogs(scanId);
        if (logData && logData.logs) {
          setLogs(logData.logs);
          
          // Check scan status
          if (logData.logs.some(log => {
            try {
              const logData = JSON.parse(log.text);
              return logData.status === 'completed' || logData.status === 'error';
            } catch (e) {
              return false;
            }
          })) {
            // Update scan status if completed or error is found
            const newStatus = logData.logs.find(log => {
              try {
                const logData = JSON.parse(log.text);
                return logData.status === 'completed' || logData.status === 'error';
              } catch (e) {
                return false;
              }
            }).text;
            
            try {
              const statusData = JSON.parse(newStatus);
              setStatus(statusData.status);
              
              // Update localStorage
              const storedScans = JSON.parse(localStorage.getItem('scans') || '[]');
              const updatedScans = storedScans.map(s => 
                s.scanId === scanId ? { ...s, status: statusData.status } : s
              );
              localStorage.setItem('scans', JSON.stringify(updatedScans));
              
              // If scan is completed or errored, stop polling
              if (statusData.status === 'completed' || statusData.status === 'error') {
                if (pollingIntervalRef.current) {
                  clearInterval(pollingIntervalRef.current);
                }
              }
            } catch (e) {
              // Not valid JSON status
            }
          }
        } else {
          // If logs property doesn't exist, check if there's an error message
          if (logData && logData.error) {
            console.warn("Error in logs response:", logData.error);
            
            // Check if the error indicates the scan has completed with an error
            if (logData.error.includes("not found")) {
              // Update scan status with error
              const storedScans = JSON.parse(localStorage.getItem('scans') || '[]');
              const updatedScans = storedScans.map(s => 
                s.scanId === scanId ? { ...s, status: 'error' } : s
              );
              localStorage.setItem('scans', JSON.stringify(updatedScans));
              setStatus('error');
              
              // Stop polling
              if (pollingIntervalRef.current) {
                clearInterval(pollingIntervalRef.current);
              }
            }
          }
        }
      } catch (err) {
        console.error('Error fetching logs:', err);
      }
    };
    
    // Initial fetch
    fetchLogs();
    
    // Set up polling (every 5 seconds)
    pollingIntervalRef.current = setInterval(fetchLogs, 5000);
    
    // Clean up on unmount
    return () => {
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
      }
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
                {status === 'running' ? 'Waiting for scan logs...' : 'No logs available'}
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
      
      <div className="mt-3 d-flex justify-content-between">
        <Link to="/" className="btn btn-primary">Back to Home</Link>
        <Button 
          variant="outline-primary"
          onClick={async () => {
            try {
              const logData = await getScanLogs(scanId);
              if (logData && logData.logs) {
                setLogs(logData.logs);
              }
            } catch (err) {
              console.error('Error refreshing logs:', err);
            }
          }}
        >
          Refresh Logs
        </Button>
      </div>
    </div>
  );
};

export default ScanDetails; 