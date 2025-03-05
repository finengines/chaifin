# Chainlit UI Updates Webhook Templates

This document provides templates for all the different types of UI updates available in the Chainlit application, along with examples of how to call them via the webhook API.

## Webhook Endpoint

All status updates should be sent as POST requests to:

```
http://localhost:5679/status
```

## Common JSON Structure

All webhook requests follow this basic structure:

```json
{
  "type": "<update_type>",
  "content": "<message_content>",
  "title": "<title>",
  "icon": "<icon_name>"
}
```

Additional fields may be required depending on the update type.

## Toast Notifications

### Basic Toast

```json
{
  "type": "toast",
  "content": "This is a toast notification",
  "toast_type": "info",
  "duration": 3000
}
```

- `toast_type`: Can be "info", "success", "warning", or "error"
- `duration`: Time in milliseconds the toast should be displayed (default: 3000)

### Examples

#### Info Toast

```json
{
  "type": "toast",
  "content": "This is an information message",
  "toast_type": "info",
  "duration": 3000
}
```

#### Success Toast

```json
{
  "type": "toast",
  "content": "Operation completed successfully",
  "toast_type": "success",
  "duration": 4000
}
```

#### Warning Toast

```json
{
  "type": "toast",
  "content": "This action may have consequences",
  "toast_type": "warning",
  "duration": 5000
}
```

#### Error Toast

```json
{
  "type": "toast",
  "content": "An error occurred during the operation",
  "toast_type": "error",
  "duration": 6000
}
```

## Status Messages

### Email Status

```json
{
  "type": "email",
  "title": "Email Status",
  "content": "Email has been sent to recipient@example.com",
  "icon": "mail"
}
```

### Calendar Status

```json
{
  "type": "calendar",
  "title": "Calendar Update",
  "content": "Meeting scheduled for tomorrow at 2:00 PM",
  "icon": "calendar"
}
```

### Web Search Status

```json
{
  "type": "web-search",
  "title": "Search Results",
  "content": "Found 5 results for your query",
  "icon": "search"
}
```

### File System Status

```json
{
  "type": "file-system",
  "title": "File System Update",
  "content": "File has been saved to /documents/report.pdf",
  "icon": "folder"
}
```

### Database Status

```json
{
  "type": "database",
  "title": "Database Operation",
  "content": "Records updated successfully in the database",
  "icon": "database"
}
```

### API Status

```json
{
  "type": "api",
  "title": "API Request",
  "content": "API request completed with status code 200",
  "icon": "code"
}
```

### Progress Status

```json
{
  "type": "progress",
  "title": "Processing Data",
  "content": "Processing large dataset",
  "progress": 75,
  "icon": "loader"
}
```

- `progress`: Integer value between 0 and 100 representing completion percentage

### Success Status

```json
{
  "type": "success",
  "title": "Success",
  "content": "Operation completed successfully",
  "icon": "check-circle"
}
```

### Warning Status

```json
{
  "type": "warning",
  "title": "Warning",
  "content": "This action may have consequences",
  "icon": "alert-triangle"
}
```

### Error Status

```json
{
  "type": "error",
  "title": "Error",
  "content": "An error occurred during the operation",
  "icon": "alert-circle"
}
```

### Info Status

```json
{
  "type": "info",
  "title": "Information",
  "content": "Here is some important information",
  "icon": "info"
}
```

## Alert Messages

### Important Alert

```json
{
  "type": "important-alert",
  "title": "Important Notice",
  "content": "This is a critical update that requires your attention",
  "icon": "alert-circle"
}
```

### Notification Alert

```json
{
  "type": "notification-alert",
  "title": "New Notification",
  "content": "You have a new notification from the system",
  "icon": "bell"
}
```

### System Alert

```json
{
  "type": "system-alert",
  "title": "System Update",
  "content": "The system will be undergoing maintenance in 30 minutes",
  "icon": "info"
}
```

## Animated Progress

```json
{
  "type": "animated-progress",
  "title": "Multi-step Process",
  "content": "Processing your request",
  "steps": [
    "Initializing process",
    "Gathering data",
    "Processing information",
    "Finalizing results"
  ],
  "delay": 0.5
}
```

- `steps`: Array of strings representing each step in the process
- `delay`: Time in seconds between each step (default: 0.5)

## Task List

### Create Task List

```json
{
  "type": "task-list-create",
  "title": "Processing Tasks"
}
```

### Add Task

```json
{
  "type": "task-list-add",
  "name": "Data Processing",
  "status": "running",
  "icon": "loader"
}
```

- `status`: Can be "running", "done", "failed", or "pending"
- `icon`: Optional icon name

### Update Task

```json
{
  "type": "task-list-update",
  "name": "Data Processing",
  "status": "done",
  "icon": "check-circle"
}
```

## Testing with cURL

You can test these webhook templates using cURL:

```bash
curl -X POST http://localhost:5679/status \
  -H "Content-Type: application/json" \
  -d '{
    "type": "toast",
    "content": "This is a test toast notification",
    "toast_type": "info",
    "duration": 3000
  }'
```

## Available Icons

Here are some commonly used icons:

- "mail"
- "calendar"
- "search"
- "folder"
- "database"
- "code"
- "loader"
- "check-circle"
- "alert-triangle"
- "alert-circle"
- "info"
- "bell"

For a complete list of available icons, refer to the Lucide icon set: [https://lucide.dev/icons/](https://lucide.dev/icons/) 