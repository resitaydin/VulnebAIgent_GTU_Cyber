import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || '';

// Create and configure axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API functions
export const startScan = async (data) => {
  try {
    const response = await api.post('/api/scan', data);
    return response.data;
  } catch (error) {
    console.error('Error starting scan:', error);
    throw error;
  }
};

export const getScanStatus = async (scanId) => {
  try {
    const response = await api.get(`/api/scan/${scanId}`);
    return response.data;
  } catch (error) {
    console.error(`Error getting scan status for ${scanId}:`, error);
    throw error;
  }
};

export const getScanLogs = async (scanId) => {
  try {
    const response = await api.get(`/api/scan/${scanId}/logs`);
    return response.data;
  } catch (error) {
    console.error(`Error getting logs for ${scanId}:`, error);
    throw error;
  }
};

export const getScanReport = async (scanId) => {
  try {
    const response = await api.get(`/api/scan/${scanId}/report`);
    return response.data;
  } catch (error) {
    console.error(`Error getting report for ${scanId}:`, error);
    throw error;
  }
};

export default api; 