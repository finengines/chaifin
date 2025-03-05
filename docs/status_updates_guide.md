# Chainlit Status Updates Guide

This guide explains how to use the custom status updates, progress indicators, and alerts provided in the `status_updates.py` module.

## Table of Contents

1. [Installation](#installation)
2. [Agent Action Status Updates](#agent-action-status-updates)
3. [Progress Status Updates](#progress-status-updates)
4. [Alert Status Updates](#alert-status-updates)
5. [Animated Progress Indicators](#animated-progress-indicators)
6. [Styled Task Lists](#styled-task-lists)
7. [Toast Notifications](#toast-notifications)
8. [Customization](#customization)

## Installation

To use these status updates in your Chainlit application:

1. Copy the `status_updates.py` file to your project directory
2. Add the CSS styles from `public/custom.css` to your project's CSS file
3. Import the required functions from the module

```python
from status_updates import email_status, progress_status, important_alert
```

## Agent Action Status Updates

Agent action status updates are used to display the status of different agent actions, such as email processing, calendar operations, web searches, etc.

### Email Status

```python
await email_status(
    "Email Processing", 
    "Checking inbox for new messages..."
)
```

### Calendar Status

```python
await calendar_status(
    "Calendar Update", 
    "Scheduling meeting with John Doe for tomorrow at 2:00 PM"
)
```

### Web Search Status

```python
await web_search_status(
    "Web Search", 
    "Searching for information about 'machine learning frameworks'"
)
```

### File System Status

```python
await file_system_status(
    "File System Operation", 
    "Scanning documents folder for PDF files"
)
```

### Database Status

```python
await database_status(
    "Database Query", 
    "Executing query to retrieve user data"
)
```

### API Status

```python
await api_status(
    "API Request", 
    "Sending POST request to /api/users endpoint"
)
```

## Progress Status Updates

Progress status updates are used to display the progress of operations, success/failure messages, warnings, and information.

### Progress Status with Progress Bar

```python
await progress_status(
    "Data Processing", 
    "Processing large dataset...",
    progress=45  # Percentage (0-100)
)
```

### Success Status

```python
await success_status(
    "Operation Complete", 
    "Successfully processed all files"
)
```

### Warning Status

```python
await warning_status(
    "Warning", 
    "Some files could not be processed due to permission issues"
)
```

### Error Status

```python
await error_status(
    "Error", 
    "Failed to connect to the database server"
)
```

### Info Status

```python
await info_status(
    "Information", 
    "The system will be undergoing maintenance in 30 minutes"
)
```

## Alert Status Updates

Alert status updates are used to display important notifications, alerts, and system messages.

### Important Alert

```python
await important_alert(
    "Critical Alert", 
    "System resources are running low. Please take action immediately."
)
```

### Notification Alert

```python
await notification_alert(
    "New Notification", 
    "You have 5 new messages in your inbox"
)
```

### System Alert

```python
await system_alert(
    "System Update", 
    "A new version of the software is available for installation"
)
```

## Animated Progress Indicators

Animated progress indicators are used to display progress through multiple steps with animations.

```python
steps = [
    "Initializing process...",
    "Loading data from database...",
    "Processing records (1/3)...",
    "Processing records (2/3)...",
    "Processing records (3/3)...",
    "Validating results...",
    "Saving changes to database..."
]

await animated_progress(
    "Data Processing", 
    "Starting data processing...", 
    steps, 
    delay=1.0  # Delay between steps in seconds
)
```

## Styled Task Lists

Styled task lists are used to display a list of tasks with their status and progress.

```python
# Create a styled task list
task_list = StyledTaskList("Document Processing", "Starting process...")
await task_list.send()

# Add tasks
task1 = await task_list.add_task(
    "Load documents", 
    "Loading documents from storage", 
    "waiting"  # Status: waiting, running, done, failed
)

# Update task status
await task_list.update_task(
    task1["id"], 
    "running", 
    "Loading documents from storage..."
)

# Later, update to done
await task_list.update_task(
    task1["id"], 
    "done", 
    "Loaded 42 documents successfully"
)

# Update task list status
task_list.status = "Process completed successfully"
await task_list.send()
```

## Toast Notifications

Toast notifications are used to display temporary messages at the bottom of the screen.

```python
await show_toast(
    "Operation completed successfully", 
    "success",  # Type: info, success, warning, error
    duration=3000  # Duration in milliseconds
)
```

## Customization

### Changing Icons

All status update functions accept an `icon` parameter that can be used to change the icon displayed. The icons are from the [Lucide icon set](https://lucide.dev/).

```python
await info_status(
    "Custom Icon", 
    "This status update has a custom icon",
    icon="star"  # Any Lucide icon name
)
```

### Styling

You can customize the appearance of status updates by modifying the CSS styles in `public/custom.css`. The main classes to modify are:

- `.status-update`: Base class for all status updates
- `.status-email`, `.status-calendar`, etc.: Classes for specific agent action status updates
- `.status-progress`, `.status-success`, etc.: Classes for specific progress status updates
- `.status-alert-important`, `.status-alert-notification`, etc.: Classes for specific alert status updates

Example of customizing the appearance of email status updates:

```css
.status-email {
  background: linear-gradient(135deg, rgba(79, 195, 247, 0.2), rgba(79, 195, 247, 0.1));
  border-left: 4px solid #4fc3f7;
  box-shadow: 0 2px 10px rgba(79, 195, 247, 0.2);
}

.status-email .status-update-icon {
  color: #4fc3f7;
}
```

## Complete Example

Here's a complete example of using various status updates in a Chainlit application:

```python
import chainlit as cl
import asyncio
from status_updates import (
    email_status,
    progress_status,
    success_status,
    important_alert,
    animated_progress,
    StyledTaskList
)

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="Welcome to the demo!").send()

@cl.on_message
async def on_message(message: cl.Message):
    if message.content.lower() == "process":
        # Show initial status
        await email_status(
            "Email Processing", 
            "Checking inbox for new messages..."
        )
        
        # Create a task list
        task_list = StyledTaskList("Document Processing", "Starting process...")
        await task_list.send()
        
        # Add and update tasks
        task1 = await task_list.add_task("Load documents", "Loading documents from storage", "waiting")
        await asyncio.sleep(1)
        await task_list.update_task(task1["id"], "running", "Loading documents from storage...")
        await asyncio.sleep(1.5)
        await task_list.update_task(task1["id"], "done", "Loaded 42 documents successfully")
        
        # Show progress with animated steps
        steps = [
            "Initializing process...",
            "Loading data from database...",
            "Processing records...",
            "Validating results...",
            "Saving changes to database..."
        ]
        await animated_progress("Data Processing", "Starting data processing...", steps, delay=0.8)
        
        # Show success status
        await success_status(
            "Operation Complete", 
            "Successfully processed all files"
        )
        
        # Show important alert if needed
        if some_condition:
            await important_alert(
                "Action Required", 
                "Please review the processed documents"
            )
```

## Running the Demo

To see all these status updates in action, run the included demo:

```bash
chainlit run status_updates_demo.py
```

Then type one of the following commands in the chat:
- `agent`: Show agent action status updates
- `progress`: Show progress status updates
- `alerts`: Show alert status updates
- `animated`: Show animated progress
- `tasklist`: Show styled task list
- `toast`: Show toast notifications
- `all`: Show all demos 