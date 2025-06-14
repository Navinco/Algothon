// Simple demo app for Pera Wallet connection

// This is a demo version that simulates wallet connection
// In a real app, you would use the Pera Wallet SDK

document.addEventListener('DOMContentLoaded', function() {
  const loading = document.getElementById('loading');
  const connectBtn = document.getElementById('connect-wallet');
  const qrCodeContainer = document.getElementById('qr-code-container');
  const qrCodeElement = document.getElementById('qr-code');
  const walletAddress = document.getElementById('wallet-address');
  
  // Hide loading indicator
  if (loading) loading.style.display = 'none';
  
  // Show connection status
  const connectionStatus = document.getElementById('connection-status');
  if (connectionStatus) connectionStatus.style.display = 'block';
  
  // Handle connect button click
  if (connectBtn) {
    connectBtn.onclick = function() {
      // For demo purposes, we'll just show a QR code with test data
      if (qrCodeElement) {
        qrCodeElement.innerHTML = '';
        new QRCode(qrCodeElement, {
          text: 'https://perawallet.app/connect-demo',
          width: 200,
          height: 200,
          colorDark: '#000000',
          colorLight: '#ffffff',
          correctLevel: QRCode.CorrectLevel.H
        });
        
        // Show the QR code container
        if (qrCodeContainer) qrCodeContainer.style.display = 'block';
        
        // For demo purposes, simulate a connection after 2 seconds
        setTimeout(() => {
          // This is just for demo - in a real app, this would be set when the wallet connects
          if (walletAddress) walletAddress.textContent = 'Connected (Demo Mode)';
          if (connectBtn) {
            connectBtn.textContent = 'Disconnect';
            connectBtn.style.backgroundColor = '#e74c3c';
            connectBtn.onclick = disconnectWallet;
          }
        }, 2000);
      }
    };
  }
  
  // Handle disconnect
  function disconnectWallet() {
    if (walletAddress) walletAddress.textContent = 'Not connected';
    if (connectBtn) {
      connectBtn.textContent = 'Connect Wallet';
      connectBtn.style.backgroundColor = '#00b894';
      connectBtn.onclick = function() { window.location.reload(); };
    }
    if (qrCodeContainer) qrCodeContainer.style.display = 'none';
  }
});
