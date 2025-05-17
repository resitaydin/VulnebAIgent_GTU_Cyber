import { io } from 'socket.io-client';

const SOCKET_URL = process.env.REACT_APP_SOCKET_URL || window.location.origin;

// Create a connection to the WebSocket server
const socket = io(SOCKET_URL, {
  autoConnect: false,
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 1000,
});

// Socket connection management
export const connectToSocket = () => {
  if (!socket.connected) {
    socket.connect();
  }
};

export const disconnectFromSocket = () => {
  if (socket.connected) {
    socket.disconnect();
  }
};

// Listen for scan updates
export const subscribeToScanUpdates = (scanId, callback) => {
  const eventName = `scan_update_${scanId}`;
  socket.on(eventName, callback);
  return () => {
    socket.off(eventName);
  };
};

// Error handling
socket.on('connect_error', (error) => {
  console.error('Socket connection error:', error);
});

socket.on('error', (error) => {
  console.error('Socket error:', error);
});

export default socket; 