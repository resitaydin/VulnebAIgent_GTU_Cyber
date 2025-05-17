import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Card, Alert, Spinner, Button } from 'react-bootstrap';
import ReactMarkdown from 'react-markdown';
import { getScanReport } from '../services/api';

const Report = () => {
  const { scanId } = useParams();
  const [report, setReport] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchReport = async () => {
      try {
        setLoading(true);
        const response = await getScanReport(scanId);
        if (response.report) {
          setReport(response.report);
        } else {
          setError('Report is empty or not available yet');
        }
      } catch (err) {
        console.error('Error fetching report:', err);
        setError('Failed to fetch report. The scan might still be in progress or encountered an error.');
      } finally {
        setLoading(false);
      }
    };

    fetchReport();
  }, [scanId]);

  const handleDownload = () => {
    const blob = new Blob([report], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `vulnerability-report-${scanId}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  if (loading) {
    return (
      <div className="text-center p-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading report...</span>
        </Spinner>
        <p className="mt-3">Loading vulnerability report...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div>
        <Alert variant="danger">
          {error}
        </Alert>
        <div className="mt-3">
          <Link to={`/scan/${scanId}`} className="btn btn-primary me-2">
            Back to Scan Details
          </Link>
          <Link to="/" className="btn btn-secondary">
            Back to Home
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>Vulnerability Scan Report</h1>
        <div>
          <Button variant="success" onClick={handleDownload} className="me-2">
            Download Report
          </Button>
          <Link to={`/scan/${scanId}`} className="btn btn-primary">
            Back to Scan Details
          </Link>
        </div>
      </div>

      <Card>
        <Card.Body>
          <div className="markdown-report">
            <ReactMarkdown>
              {report}
            </ReactMarkdown>
          </div>
        </Card.Body>
      </Card>
      
      <div className="mt-3 text-center">
        <Link to="/" className="btn btn-secondary">
          Back to Home
        </Link>
      </div>
    </div>
  );
};

export default Report; 