// Custom JavaScript for Chainlit UI enhancements

document.addEventListener('DOMContentLoaded', function() {
  console.log('Chainlit UI enhancements loaded');
  
  // Add task list close button functionality
  function addTaskListCloseButtons() {
    console.log('Attempting to add task list close buttons');
    
    // Find all task lists using multiple possible selectors
    const taskLists = document.querySelectorAll('.cl-tasklist, .cl-task-list, [data-testid="task-list"]');
    console.log('Found task lists:', taskLists.length);
    
    taskLists.forEach((taskList, index) => {
      console.log(`Processing task list ${index + 1}`);
      
      // Check if this task list already has a close button
      if (!taskList.querySelector('.cl-tasklist-close')) {
        console.log(`Adding close button to task list ${index + 1}`);
        
        // Create close button
        const closeButton = document.createElement('div');
        closeButton.className = 'cl-tasklist-close';
        closeButton.title = 'Close task list';
        
        // Add click event to hide the task list
        closeButton.addEventListener('click', function() {
          console.log('Close button clicked');
          taskList.style.display = 'none';
          
          // Show a toast notification
          if (window.showToast) {
            window.showToast('Task list closed', 'info', 2000);
          }
        });
        
        // Add the close button to the task list
        taskList.appendChild(closeButton);
        console.log(`Close button added to task list ${index + 1}`);
      } else {
        console.log(`Task list ${index + 1} already has a close button`);
      }
    });
  }
  
  // Run initially with a longer delay to ensure DOM is fully loaded
  setTimeout(addTaskListCloseButtons, 2000);
  
  // Run again after a longer delay in case the first attempt missed any elements
  setTimeout(addTaskListCloseButtons, 5000);
  
  // Set up a mutation observer to add close buttons to new task lists
  const observer = new MutationObserver(function(mutations) {
    let taskListAdded = false;
    
    mutations.forEach(function(mutation) {
      if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
        // Check if any task lists were added
        Array.from(mutation.addedNodes).forEach(node => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            if (node.classList && (node.classList.contains('cl-tasklist') || node.classList.contains('cl-task-list'))) {
              taskListAdded = true;
            } else if (node.querySelector) {
              const nestedTaskLists = node.querySelectorAll('.cl-tasklist, .cl-task-list, [data-testid="task-list"]');
              if (nestedTaskLists.length > 0) {
                taskListAdded = true;
              }
            }
          }
        });
      }
    });
    
    if (taskListAdded) {
      console.log('Task list added to DOM, adding close buttons');
      // Add close buttons to new task lists with a slight delay
      setTimeout(addTaskListCloseButtons, 500);
    }
  });
  
  // Start observing the document body
  observer.observe(document.body, { childList: true, subtree: true });
  
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
  
  // Note: Toast notifications are handled by .chainlit/custom.js
  // Do not implement duplicate toast functionality here
  
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
      // Use the toast notification from .chainlit/custom.js
      if (window.showToast) {
        window.showToast('Error sending data to webhook', 'error', 3000);
      }
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

// Initialize Lucide icons
const initializeLucideIcons = () => {
  if (window.lucide && window.lucide.createIcons) {
    window.lucide.createIcons();
    console.log('Lucide icons initialized');
  } else {
    console.warn('Lucide library not found');
  }
};

// Initialize toast container
const initializeToastContainer = () => {
  // Check if toast container already exists
  let toastContainer = document.getElementById('toast-container');
  
  // If not, create it
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'toast-container';
    document.body.appendChild(toastContainer);
    console.log('Toast container initialized');
  }
};

// Create a toast notification
const createToast = (message, description = '', type = 'info', duration = 3000) => {
  const toastContainer = document.getElementById('toast-container');
  if (!toastContainer) {
    console.error('Toast container not found');
    return;
  }
  
  // Create toast element
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  // Get icon based on type
  let iconName = 'info';
  switch (type) {
    case 'success':
      iconName = 'check-circle';
      break;
    case 'warning':
      iconName = 'alert-triangle';
      break;
    case 'error':
      iconName = 'alert-circle';
      break;
    default:
      iconName = 'info';
  }
  
  // Set toast content
  toast.innerHTML = `
    <div class="toast-icon">
      <i data-lucide="${iconName}"></i>
    </div>
    <div class="toast-content">
      <div class="toast-title">${message}</div>
    </div>
    <button class="toast-close" aria-label="Close">
      <i data-lucide="x"></i>
    </button>
  `;
  
  // Add to container
  toastContainer.appendChild(toast);
  
  // Initialize icons in the toast
  if (window.lucide && window.lucide.createIcons) {
    window.lucide.createIcons({
      icons: ['check-circle', 'alert-triangle', 'alert-circle', 'info', 'x'],
      attrs: {
        class: ['toast-icon-svg']
      },
      elements: [toast]
    });
  }
  
  // Show toast
  setTimeout(() => {
    toast.classList.add('show');
  }, 10);
  
  // Set up close button
  const closeButton = toast.querySelector('.toast-close');
  if (closeButton) {
    closeButton.addEventListener('click', () => {
      toast.classList.remove('show');
      setTimeout(() => {
        toast.remove();
      }, 300);
    });
  }
  
  // Auto-dismiss
  if (duration > 0) {
    setTimeout(() => {
      if (toast.parentNode) {
        toast.classList.remove('show');
        setTimeout(() => {
          if (toast.parentNode) {
            toast.remove();
          }
        }, 300);
      }
    }, duration);
  }
  
  return toast;
};

// Listen for toast events from Chainlit
const listenForToastEvents = () => {
  // Create a MutationObserver to watch for toast events
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.type === 'childList') {
        // Look for toast elements added by Chainlit
        const toasts = document.querySelectorAll('.cl-toast');
        toasts.forEach((toast) => {
          // Extract data from Chainlit toast
          const message = toast.textContent || '';
          const type = toast.getAttribute('data-type') || 'info';
          
          // Create our custom toast
          createToast(message, '', type);
          
          // Remove the original toast
          toast.remove();
        });
      }
    });
  });
  
  // Start observing the document body
  observer.observe(document.body, { childList: true, subtree: true });
  console.log('Toast event listener initialized');
};

// Initialize when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM loaded, initializing custom components');
  initializeLucideIcons();
  initializeToastContainer();
  listenForToastEvents();
  
  // Set up a MutationObserver to detect dynamically added content
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
        initializeLucideIcons();
      }
    });
  });
  
  // Start observing the document body
  observer.observe(document.body, { childList: true, subtree: true });
});

// Expose functions to window for debugging
window.chainlitHelpers = {
  createToast,
  initializeLucideIcons
};

// Add support for custom status updates
document.addEventListener('chainlit:update', () => {
  // Find all status update elements
  const statusUpdates = document.querySelectorAll('.status-update');
  
  statusUpdates.forEach(statusUpdate => {
    // Find icon container
    const iconContainer = statusUpdate.querySelector('.status-update-icon');
    if (iconContainer) {
      // Find icon element
      const iconElement = iconContainer.querySelector('i[data-lucide]');
      if (iconElement && !iconElement.querySelector('svg')) {
        // If icon element exists but doesn't have SVG, initialize it
        if (window.lucide && window.lucide.createIcons) {
          window.lucide.createIcons({
            attrs: {
              class: ['status-icon'],
              stroke: 'currentColor',
              'stroke-width': 2
            }
          });
        }
      }
    }
  });
});

// Custom JavaScript to add persistent mode buttons below the chat input

function createModeButton(id, label, isActive = false) {
  console.log(`Creating mode button: ${id}, label: ${label}, isActive: ${isActive}`);
  
  const button = document.createElement('button');
  button.id = id;
  button.className = `mode-button ${isActive ? 'active' : ''}`;
  button.innerHTML = label;
  
  // Add click event listener
  button.addEventListener('click', () => {
    console.log(`Mode button clicked: ${id}`);
    
    // Toggle active state
    button.classList.toggle('active');
    const isNowActive = button.classList.contains('active');
    console.log(`Button ${id} is now ${isNowActive ? 'active' : 'inactive'}`);
    
    // Send message to backend
    console.log(`Sending action message for ${id}`);
    window.chainlitClient.sendMessage({
      type: 'action',
      name: id,
      payload: {}
    });
  });
  
  console.log(`Mode button created: ${id}`);
  return button;
}

function updateModeButton(id, isActive) {
  console.log(`Updating mode button: ${id}, isActive: ${isActive}`);
  
  const button = document.getElementById(id);
  if (button) {
    console.log(`Found button ${id}, updating state to ${isActive ? 'active' : 'inactive'}`);
    if (isActive) {
      button.classList.add('active');
    } else {
      button.classList.remove('active');
    }
  } else {
    console.error(`Button with id ${id} not found`);
  }
}

function createModeButtonsContainer() {
  // Create container for mode buttons
  const container = document.createElement('div');
  container.id = 'mode-buttons-container';
  container.style.display = 'flex';
  container.style.justifyContent = 'center';
  container.style.gap = '10px';
  container.style.padding = '10px';
  container.style.borderTop = '1px solid rgba(0, 0, 0, 0.1)';
  
  return container;
}

function addModeButtons() {
  console.log('Attempting to add mode buttons');
  
  // Try different selectors for the chat input container
  const selectors = [
    '.cl-chat-input-container',
    '.cl-chat-container',
    '.cl-input-container',
    '[data-testid="chat-input-container"]',
    '.cl-chat-input',
    '.cl-input-box'
  ];
  
  let chatInput = null;
  
  // Try each selector
  for (const selector of selectors) {
    const element = document.querySelector(selector);
    if (element) {
      console.log(`Found element with selector: ${selector}`, element);
      chatInput = element;
      break;
    }
  }
  
  if (!chatInput) {
    console.log('Chat input container not found with any selector, retrying in 1000ms');
    setTimeout(addModeButtons, 1000);
    return;
  }
  
  console.log('Found chat input container:', chatInput);
  
  // Check if we've already added the buttons
  if (document.getElementById('mode-buttons-container')) {
    console.log('Mode buttons container already exists, skipping');
    return;
  }
  
  console.log('Creating mode buttons container');
  
  // Create container
  const container = createModeButtonsContainer();
  
  // Create buttons
  console.log('Creating mode buttons');
  const thinkButton = createModeButton('toggle_reasoning', '🧠 Think');
  const privacyButton = createModeButton('toggle_privacy', '🛡️ Privacy');
  const deepResearchButton = createModeButton('toggle_deep_research', '🔍 Deep Research');
  const webSearchButton = createModeButton('toggle_web_search', '🌐 Web Search');
  
  // Add buttons to container
  container.appendChild(thinkButton);
  container.appendChild(privacyButton);
  container.appendChild(deepResearchButton);
  container.appendChild(webSearchButton);
  
  // Try different insertion methods
  try {
    console.log('Trying to insert before chat input');
    chatInput.parentNode.insertBefore(container, chatInput);
    console.log('Successfully inserted before chat input');
  } catch (e) {
    console.error('Error inserting before chat input:', e);
    
    try {
      console.log('Trying to append to chat input parent');
      chatInput.parentNode.appendChild(container);
      console.log('Successfully appended to chat input parent');
    } catch (e) {
      console.error('Error appending to chat input parent:', e);
      
      try {
        console.log('Trying to append to body');
        document.body.appendChild(container);
        console.log('Successfully appended to body');
        
        // Position at the bottom of the screen
        container.style.position = 'fixed';
        container.style.bottom = '80px';
        container.style.left = '0';
        container.style.right = '0';
        container.style.zIndex = '1000';
      } catch (e) {
        console.error('Error appending to body:', e);
      }
    }
  }
  
  console.log('Mode buttons added successfully');
  
  // Add CSS for the buttons
  console.log('Adding CSS for mode buttons');
  const style = document.createElement('style');
  style.textContent = `
    #mode-buttons-container {
      display: flex;
      justify-content: center;
      gap: 10px;
      padding: 10px;
      border-top: 1px solid rgba(0, 0, 0, 0.1);
      background-color: var(--cl-background);
    }
    
    .mode-button {
      padding: 8px 16px;
      border-radius: 20px;
      border: 1px solid rgba(0, 0, 0, 0.1);
      background-color: var(--cl-background);
      color: var(--cl-text);
      cursor: pointer;
      transition: all 0.2s ease;
      font-size: 14px;
    }
    
    .mode-button:hover {
      background-color: rgba(0, 0, 0, 0.05);
    }
    
    .mode-button.active {
      background-color: var(--cl-primary);
      color: white;
      border-color: var(--cl-primary);
    }
  `;
  document.head.appendChild(style);
  console.log('CSS added for mode buttons');
}

// Listen for messages from the backend to update button states
function setupMessageListener() {
  console.log('Setting up message listener for mode updates');
  
  // Check if chainlitClient exists
  if (!window.chainlitClient || !window.chainlitClient.socket) {
    console.error('chainlitClient or socket not found, retrying in 1s');
    setTimeout(setupMessageListener, 1000);
    return;
  }
  
  // Add CSS to hide system_hidden messages
  const style = document.createElement('style');
  style.textContent = `
    .cl-message-author[data-author="system_hidden"],
    .cl-message-container[data-author="system_hidden"] {
      display: none !important;
    }
  `;
  document.head.appendChild(style);
  console.log('Added CSS to hide system_hidden messages');
  
  const originalOnMessage = window.chainlitClient.socket.onmessage;
  
  window.chainlitClient.socket.onmessage = function(event) {
    // Call the original handler
    originalOnMessage.call(this, event);
    
    try {
      // Parse the message
      const data = JSON.parse(event.data);
      console.log('Received message:', data);
      
      // Check if it's a message with content
      if (data.message && data.message.author === 'system_hidden' && data.message.language === 'json') {
        console.log('Found system_hidden JSON message:', data.message);
        
        try {
          // Try to parse the content as JSON
          const contentData = JSON.parse(data.message.content);
          console.log('Parsed content data:', contentData);
          
          // Check if it's a mode update message
          if (contentData.type === 'mode_update') {
            console.log('Processing mode update:', contentData);
            updateModeButton('toggle_reasoning', contentData.reasoning_mode);
            updateModeButton('toggle_privacy', contentData.privacy_mode);
            updateModeButton('toggle_deep_research', contentData.deep_research_mode);
            updateModeButton('toggle_web_search', contentData.web_search_mode);
            
            // Hide the message element if it's visible
            setTimeout(() => {
              const messages = document.querySelectorAll('.cl-message-container');
              messages.forEach(msg => {
                const authorEl = msg.querySelector('.cl-message-author');
                if (authorEl && authorEl.textContent.includes('system_hidden')) {
                  msg.style.display = 'none';
                }
              });
            }, 100);
          }
        } catch (e) {
          console.error('Error parsing message content as JSON:', e);
        }
      }
    } catch (e) {
      console.error('Error processing message:', e);
    }
  };
}

// Function to hide system_hidden messages
function hideSystemHiddenMessages() {
  console.log('Checking for system_hidden messages to hide');
  
  // Find all message containers
  const messages = document.querySelectorAll('.cl-message-container');
  let hiddenCount = 0;
  
  messages.forEach(msg => {
    // Check if the message is from system_hidden
    const authorEl = msg.querySelector('.cl-message-author');
    if (authorEl && authorEl.textContent.includes('system_hidden')) {
      msg.style.display = 'none';
      hiddenCount++;
    }
    
    // Also check if the message content is a mode update JSON
    const contentEl = msg.querySelector('.cl-message-content');
    if (contentEl && contentEl.textContent.includes('"type":"mode_update"')) {
      msg.style.display = 'none';
      hiddenCount++;
    }
  });
  
  if (hiddenCount > 0) {
    console.log(`Hidden ${hiddenCount} system_hidden messages`);
  }
}

// Initialize when the page is loaded
function init() {
  console.log('Initializing custom UI components');
  
  // Function to check if chainlit is ready
  const checkChainlit = () => {
    console.log('Checking if chainlit is ready...');
    
    // Check if chainlitClient is available
    if (window.chainlitClient) {
      console.log('chainlitClient found, adding mode buttons and setting up listeners');
      
      // Setup message listener first
      setupMessageListener();
      
      // Then add mode buttons
      setTimeout(() => {
        addModeButtons();
        
        // Hide any system_hidden messages
        hideSystemHiddenMessages();
        
        // Set up a periodic check to hide system_hidden messages
        setInterval(hideSystemHiddenMessages, 2000);
        
        console.log('Initialization complete');
      }, 1000);
    } else {
      // Try again in 1000ms
      console.log('chainlitClient not found, retrying in 1000ms');
      setTimeout(checkChainlit, 1000);
    }
  };
  
  // Start checking if document is ready
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    console.log('Document is ready, starting chainlit check');
    checkChainlit();
  } else {
    // Wait for the page to load
    console.log('Document not ready, waiting for DOMContentLoaded');
    window.addEventListener('DOMContentLoaded', () => {
      console.log('DOMContentLoaded fired, starting chainlit check');
      checkChainlit();
    });
  }
}

// Start initialization with a delay to ensure the page is fully loaded
console.log('Starting initialization with delay');
setTimeout(() => {
  init();
}, 2000); 