// Task List Close Button Implementation

(function() {
  console.log('Task List Close Button script loaded');
  
  // Function to add close buttons to task lists
  function addTaskListCloseButtons() {
    console.log('Adding task list close buttons');
    
    // Find all task lists using multiple possible selectors
    const taskLists = document.querySelectorAll('[data-testid="task-list"], .cl-tasklist, .cl-task-list');
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
        closeButton.style.cssText = `
          position: absolute;
          top: 10px;
          right: 10px;
          width: 24px;
          height: 24px;
          border-radius: 50%;
          background-color: rgba(0, 0, 0, 0.3);
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          z-index: 100;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        `;
        
        // Add click event to hide the task list
        closeButton.addEventListener('click', function(event) {
          console.log('Close button clicked');
          event.stopPropagation();
          taskList.style.display = 'none';
          
          // Show a toast notification if the function exists
          if (typeof window.showToast === 'function') {
            window.showToast('Task list closed', 'info', 2000);
          }
        });
        
        // Create X icon with inline styles
        const beforeElement = document.createElement('div');
        beforeElement.style.cssText = `
          position: absolute;
          width: 14px;
          height: 2px;
          background-color: white;
          transform: rotate(45deg);
        `;
        
        const afterElement = document.createElement('div');
        afterElement.style.cssText = `
          position: absolute;
          width: 14px;
          height: 2px;
          background-color: white;
          transform: rotate(-45deg);
        `;
        
        closeButton.appendChild(beforeElement);
        closeButton.appendChild(afterElement);
        
        // Make sure the task list has position relative
        if (window.getComputedStyle(taskList).position === 'static') {
          taskList.style.position = 'relative';
        }
        
        // Add the close button to the task list
        taskList.appendChild(closeButton);
        console.log(`Close button added to task list ${index + 1}`);
      } else {
        console.log(`Task list ${index + 1} already has a close button`);
      }
    });
  }
  
  // Function to initialize the task list close buttons
  function initialize() {
    console.log('Initializing task list close buttons');
    
    // Run initially with a delay to ensure DOM is loaded
    setTimeout(addTaskListCloseButtons, 1000);
    
    // Run again after a longer delay in case the first attempt missed any elements
    setTimeout(addTaskListCloseButtons, 3000);
    
    // Set up a mutation observer to add close buttons to new task lists
    const observer = new MutationObserver(function(mutations) {
      let taskListAdded = false;
      
      mutations.forEach(function(mutation) {
        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
          // Check if any task lists were added
          Array.from(mutation.addedNodes).forEach(node => {
            if (node.nodeType === Node.ELEMENT_NODE) {
              if (node.matches && (
                  node.matches('[data-testid="task-list"]') || 
                  node.matches('.cl-tasklist') || 
                  node.matches('.cl-task-list')
              )) {
                taskListAdded = true;
              } else if (node.querySelectorAll) {
                const nestedTaskLists = node.querySelectorAll('[data-testid="task-list"], .cl-tasklist, .cl-task-list');
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
        setTimeout(addTaskListCloseButtons, 300);
      }
    });
    
    // Start observing the document body
    observer.observe(document.body, { childList: true, subtree: true });
  }
  
  // Initialize when the DOM is fully loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
  } else {
    initialize();
  }
})(); 