import React, { useState } from 'react';
import './Disclaimer.css';

function Disclaimer() {
  const [dismissed, setDismissed] = useState(
    localStorage.getItem('disclaimerDismissed') === 'true'
  );

  const handleDismiss = () => {
    setDismissed(true);
    localStorage.setItem('disclaimerDismissed', 'true');
  };

  if (dismissed) {
    return null;
  }

  return (
    <div className="disclaimer-banner">
      <div className="disclaimer-content">
        <div className="disclaimer-icon">⚠️</div>
        <div className="disclaimer-text">
          <strong>Important Notice:</strong> This AI-powered system is designed
          to provide emotional support and monitoring. It is <strong>not a
          substitute for professional therapy, medical advice, or mental health
          treatment</strong>. If you are experiencing a mental health emergency,
          please contact your local emergency services or a mental health
          professional immediately.
        </div>
        <button className="dismiss-button" onClick={handleDismiss}>
          I Understand
        </button>
      </div>
    </div>
  );
}

export default Disclaimer;

