// Custom JavaScript for Chainlit UI enhancements

document.addEventListener('DOMContentLoaded', function() {
  console.log('Chainlit UI enhancements loaded');
  
  // ===== Progress Bar Functions =====
  
  // Create a progress bar element
  window.createProgressBar = function(containerId, initialValue = 0) {
    const container = document.getElementById(containerId);
    if (!container) return null;
    
    const progressBarContainer = document.createElement('div');
    progressBarContainer.className = 'cl-progress-bar';
    
    const progressBarFill = document.createElement('div');
    progressBarFill.className = 'cl-progress-bar-fill';
    progressBarFill.style.width = `${initialValue}%`;
    
    progressBarContainer.appendChild(progressBarFill);
    container.appendChild(progressBarContainer);
    
    return progressBarContainer;
  };
  
  // Update a progress bar value
  window.updateProgressBar = function(progressBar, value) {
    if (!progressBar) return;
    
    const fill = progressBar.querySelector('.cl-progress-bar-fill');
    if (fill) {
      fill.style.width = `${value}%`;
    }
  };
  
  // ===== Toast Notification Functions =====
  
  // Show a toast notification
  window.showToast = function(message, duration = 3000) {
    const toast = document.createElement('div');
    toast.className = 'cl-toast';
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(function() {
      toast.remove();
    }, duration);
    
    return toast;
  };
  
  // ===== Custom Button Functions =====
  
  // Create a custom action button
  window.createActionButton = function(containerId, options) {
    const container = document.getElementById(containerId);
    if (!container) return null;
    
    const button = document.createElement('button');
    button.className = 'cl-action-button';
    button.dataset.action = options.action || '';
    
    if (options.icon) {
      const icon = document.createElement('span');
      icon.className = 'cl-action-button-icon';
      icon.innerHTML = options.icon;
      button.appendChild(icon);
    }
    
    if (options.label) {
      const label = document.createTextNode(options.label);
      button.appendChild(label);
    }
    
    if (options.onClick) {
      button.addEventListener('click', options.onClick);
    }
    
    container.appendChild(button);
    return button;
  };
  
  // ===== Status Indicator Functions =====
  
  // Create a status indicator
  window.createStatusIndicator = function(containerId, status = 'idle') {
    const container = document.getElementById(containerId);
    if (!container) return null;
    
    const statusIndicator = document.createElement('div');
    statusIndicator.className = 'cl-status-indicator';
    
    updateStatusIndicator(statusIndicator, status);
    container.appendChild(statusIndicator);
    
    return statusIndicator;
  };
  
  // Update a status indicator
  window.updateStatusIndicator = function(indicator, status) {
    if (!indicator) return;
    
    // Remove all status classes
    indicator.classList.remove('cl-status-idle', 'cl-status-running', 'cl-status-success', 'cl-status-error');
    
    // Add the appropriate class
    indicator.classList.add(`cl-status-${status}`);
    
    // Update the text content
    let statusText = 'Idle';
    let statusIcon = '⚪';
    
    switch (status) {
      case 'running':
        statusText = 'Running';
        statusIcon = '🔄';
        break;
      case 'success':
        statusText = 'Success';
        statusIcon = '✅';
        break;
      case 'error':
        statusText = 'Error';
        statusIcon = '❌';
        break;
    }
    
    indicator.innerHTML = `${statusIcon} <span>${statusText}</span>`;
  };
  
  // ===== Webhook Data Handling =====
  
  // Setup webhook data listener
  window.setupWebhookListener = function(callback) {
    // Listen for messages from the parent window
    window.addEventListener('message', function(event) {
      // Check if the message is from a trusted source
      if (event.origin !== window.location.origin) {
        console.warn('Received message from untrusted origin:', event.origin);
        return;
      }
      
      // Check if this is a webhook data message
      if (event.data && event.data.type === 'webhook_data') {
        callback(event.data.payload);
      }
    });
  };
  
  // Send data to a webhook
  window.sendWebhookData = function(url, data) {
    return fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    .then(response => response.json())
    .catch(error => {
      console.error('Error sending webhook data:', error);
      window.showToast('Error sending data to webhook', 3000);
      throw error;
    });
  };
  
  // ===== Keyboard Shortcuts =====
  
  // Add keyboard shortcuts
  document.addEventListener('keydown', function(event) {
    // Ctrl+Enter or Cmd+Enter to send message
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
      const sendButton = document.querySelector('button[type="submit"]');
      if (sendButton) {
        sendButton.click();
      }
    }
    
    // Escape to close modals
    if (event.key === 'Escape') {
      const closeButtons = document.querySelectorAll('.cl-modal-close');
      if (closeButtons.length > 0) {
        closeButtons[0].click();
      }
    }
  });
  
  // ===== Initialization =====
  
  // Add custom CSS for status indicators
  const style = document.createElement('style');
  style.textContent = `
    .cl-status-indicator {
      display: inline-flex;
      align-items: center;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 14px;
      margin-right: 8px;
    }
    
    .cl-status-indicator span {
      margin-left: 6px;
    }
    
    .cl-status-idle {
      background-color: rgba(0, 0, 0, 0.05);
    }
    
    .cl-status-running {
      background-color: rgba(0, 102, 204, 0.1);
      animation: pulse 1.5s infinite;
    }
    
    .cl-status-success {
      background-color: rgba(40, 167, 69, 0.1);
    }
    
    .cl-status-error {
      background-color: rgba(220, 53, 69, 0.1);
    }
  `;
  document.head.appendChild(style);
  
  // Initialize any global UI enhancements here
  console.log('Chainlit UI enhancements initialized');
}); 