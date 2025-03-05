// Custom JavaScript for the Chainlit UI

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  console.log('Personal Assistant UI loaded');
  
  // Add a custom keyboard shortcut (Ctrl+Enter) to send messages
  document.addEventListener('keydown', function(event) {
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
      const sendButton = document.querySelector('button[type="submit"]');
      if (sendButton) {
        sendButton.click();
      }
    }
  });
  
  // Add a custom function to scroll to the bottom of the chat
  window.scrollToBottom = function() {
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  };
  
  // Add a custom function to clear the input field
  window.clearInput = function() {
    const inputField = document.querySelector('textarea');
    if (inputField) {
      inputField.value = '';
    }
  };
  
  // Add a custom function to copy the last message
  window.copyLastMessage = function() {
    const messages = document.querySelectorAll('.assistant-message');
    if (messages.length > 0) {
      const lastMessage = messages[messages.length - 1];
      const text = lastMessage.textContent;
      
      navigator.clipboard.writeText(text).then(function() {
        console.log('Message copied to clipboard');
        // Show a toast notification
        showToast('Message copied to clipboard', 'info');
      });
    }
  };
  
  // Add a custom function to show toast notifications
  window.showToast = function(message, type = 'info', duration = 3000) {
    console.log(`Showing toast: ${message} (${type})`);
    
    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
      toastContainer = document.createElement('div');
      toastContainer.id = 'toast-container';
      document.body.appendChild(toastContainer);
    }
    
    // Check if there's already a toast with the same message to prevent duplicates
    const existingToasts = Array.from(toastContainer.querySelectorAll('.toast'));
    for (const existingToast of existingToasts) {
      const existingMessage = existingToast.querySelector('.toast-message');
      if (existingMessage && existingMessage.textContent === message) {
        console.log('Duplicate toast message detected, not showing:', message);
        return;
      }
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    // Add icon based on type
    let icon = '';
    switch (type) {
      case 'success':
        icon = '✅';
        break;
      case 'warning':
        icon = '⚠️';
        break;
      case 'error':
        icon = '❌';
        break;
      case 'info':
      default:
        icon = 'ℹ️';
        break;
    }
    
    toast.innerHTML = `<span class="toast-icon">${icon}</span><span class="toast-message">${message}</span>`;
    toastContainer.appendChild(toast);
    
    // Set custom animation duration based on toast duration
    const progressDuration = duration / 1000; // Convert to seconds
    toast.style.setProperty('--progress-duration', `${progressDuration}s`);
    
    // Animate the toast
    setTimeout(() => {
      toast.classList.add('show');
    }, 10);
    
    // Remove the toast after duration
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => {
        toast.remove();
      }, 400); // Match the transition duration
    }, duration);
    
    return toast;
  };
  
  // Register custom element for toast notifications
  class ToastElement extends HTMLElement {
    constructor() {
      super();
      this.attachShadow({ mode: 'open' });
      
      // Create styles
      const style = document.createElement('style');
      style.textContent = `
        :host {
          display: none;
        }
      `;
      
      this.shadowRoot.appendChild(style);
    }
    
    connectedCallback() {
      // Get attributes
      const message = this.getAttribute('message') || '';
      const type = this.getAttribute('type') || 'info';
      const duration = parseInt(this.getAttribute('duration') || '3000', 10);
      
      // Show toast
      if (message) {
        window.showToast(message, type, duration);
      }
    }
  }
  
  // Register the custom element
  if (!customElements.get('chainlit-toast')) {
    customElements.define('chainlit-toast', ToastElement);
  }
  
  // Listen for custom toast events
  document.addEventListener('chainlit:toast', function(event) {
    const { message, type, duration } = event.detail;
    window.showToast(message, type, duration);
  });
  
  // Add a custom event listener for new messages
  const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
        // Check if a new message was added
        const newMessages = Array.from(mutation.addedNodes).filter(node => 
          node.nodeType === Node.ELEMENT_NODE && 
          (node.classList.contains('user-message') || node.classList.contains('assistant-message'))
        );
        
        if (newMessages.length > 0) {
          // Scroll to the bottom when a new message is added
          window.scrollToBottom();
          
          // Check for custom elements in the new messages
          newMessages.forEach(message => {
            const customElements = message.querySelectorAll('[data-testid="custom-element"]');
            customElements.forEach(element => {
              // Check if this is a Toast element
              if (element.getAttribute('name') === 'Toast') {
                try {
                  const props = JSON.parse(element.getAttribute('props'));
                  if (props.message) {
                    window.showToast(props.message, props.type || 'info', props.duration || 3000);
                  }
                } catch (error) {
                  console.error('Error parsing Toast props:', error);
                }
              }
            });
          });
        }
      }
    });
  });
  
  // Start observing the chat container
  const chatContainer = document.querySelector('.chat-container');
  if (chatContainer) {
    observer.observe(chatContainer, { childList: true, subtree: true });
  }
  
  // Handle chat profile changes without restarting the chat
  function setupProfileChangeHandler() {
    // Find the profile selector dropdown
    const profileSelector = document.querySelector('[data-testid="chat-profile-selector"]');
    
    if (profileSelector) {
      console.log('Found profile selector, setting up change handler');
      
      // Add event listener for profile changes
      profileSelector.addEventListener('change', function(event) {
        const selectedProfile = event.target.value;
        console.log('Profile changed to:', selectedProfile);
        
        // Send a special command to update the model
        const textarea = document.querySelector('textarea');
        const sendButton = document.querySelector('button[type="submit"]');
        
        if (textarea && sendButton) {
          // Get the profile data from the selected option
          const selectedOption = Array.from(event.target.options).find(option => option.value === selectedProfile);
          
          if (selectedOption && selectedOption.dataset.profile) {
            try {
              // Parse the profile data
              const profileData = JSON.parse(selectedOption.dataset.profile);
              console.log('Profile data:', profileData);
              
              // Extract provider and model ID
              if (profileData.on_select_data) {
                const provider = profileData.on_select_data.provider;
                const modelId = profileData.on_select_data.model_id;
                
                if (provider && modelId) {
                  // Set the command to update the model
                  textarea.value = `/model ${provider}:${modelId}`;
                  
                  // Send the command
                  sendButton.click();
                  
                  // Prevent the default behavior (restarting the chat)
                  event.preventDefault();
                  event.stopPropagation();
                  return false;
                }
              }
            } catch (error) {
              console.error('Error parsing profile data:', error);
            }
          }
        }
      }, true);
    } else {
      // If the profile selector isn't available yet, try again later
      setTimeout(setupProfileChangeHandler, 1000);
    }
  }
  
  // Start setting up the profile change handler
  setupProfileChangeHandler();
}); 