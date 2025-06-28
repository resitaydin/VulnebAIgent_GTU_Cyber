import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, Button, Card, Alert } from 'react-bootstrap';
import { startScan } from '../services/api';

const NewScan = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    target_ip: '',
    scan_description: '',
    api_key: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Start the scan
      const response = await startScan(formData);
      const scanId = response.scan_id;

      // Add to localStorage for history
      const newScan = {
        scanId,
        targetIp: formData.target_ip,
        scanDescription: formData.scan_description,
        startTime: new Date().toLocaleString(),
        status: 'running'
      };
      
      const existingScans = JSON.parse(localStorage.getItem('scans') || '[]');
      localStorage.setItem('scans', JSON.stringify([newScan, ...existingScans]));

      // Navigate to the scan details page
      navigate(`/scan/${scanId}`);
    } catch (err) {
      console.error('Error starting scan:', err);
      setError(err.response?.data?.error || 'Failed to start scan. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="mb-4">Start New Vulnerability Scan</h1>

      <Card>
        <Card.Body>
          {error && <Alert variant="danger">{error}</Alert>}

          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="targetIp">
              <Form.Label>Target IP or Hostname</Form.Label>
              <Form.Control
                type="text"
                name="target_ip"
                value={formData.target_ip}
                onChange={handleChange}
                placeholder="Enter target IP or hostname"
                required
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="apiKey">
              <Form.Label>OpenAI API Key</Form.Label>
              <Form.Control
                type="password"
                name="api_key"
                value={formData.api_key}
                onChange={handleChange}
                placeholder="Enter your OpenAI API key"
                required
              />
              <Form.Text className="text-muted">
                Your API key is required for the AI agents to function and will be used securely.
              </Form.Text>
            </Form.Group>

            <Form.Group className="mb-3" controlId="scanDescription">
              <Form.Label>Scan Description</Form.Label>
              <Form.Control
                as="textarea"
                name="scan_description"
                value={formData.scan_description}
                onChange={handleChange}
                placeholder="Describe what you want to scan for (e.g., find if this target is vulnerable to any exploit on port 22, only using nmap)"
                rows={4}
                required
              />
              <Form.Text className="text-muted">
                Be as specific as possible to get the best results.
              </Form.Text>
            </Form.Group>

            <div className="d-grid gap-2">
              <Button variant="primary" type="submit" disabled={loading}>
                {loading ? 'Starting scan...' : 'Start Scan'}
              </Button>
            </div>
          </Form>
        </Card.Body>
      </Card>
    </div>
  );
};

export default NewScan; 