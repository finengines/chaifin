# Chainlit Webhook Integration Guide

This guide explains how to use the webhook integration to display various types of notifications and status updates in your Chainlit application.

## Overview

The webhook integration allows external systems (like n8n workflows) to send status updates and notifications to your Chainlit application. These updates can be displayed in various formats, including:

- Toast notifications
- Status updates (success, warning, error, info)
- Progress indicators
- Animated progress steps
- Alerts (important, notification, system)
- Task lists

## Webhook Server

The webhook server runs alongside your Chainlit application and listens for incoming status updates. It exposes the following endpoints:

- `GET /health` - Check if the webhook server is running
- `POST /status` - Send a status update to the Chainlit application

## Sending Status Updates

To send a status update, make a POST request to the `/status` endpoint with a JSON payload. The structure of the payload depends on the type of notification you want to display.

### Common Parameters

All status updates support the following common parameters:

- `type` (required): The type of notification to display
- `title` (optional): The title of the notification
- `content` (required): The main content of the notification
- `icon` (optional): The icon to display with the notification

### Toast Notifications

Toast notifications are temporary messages that appear at the top of the screen and automatically disappear after a specified duration.

```json
{
  "type": "toast",
  "content": "This is a toast notification",
  "toast_type": "info",
  "duration": 5000
}
```

Parameters:
- `toast_type`: The type of toast notification (`info`, `success`, `warning`, `error`)
- `duration`: The duration in milliseconds before the toast disappears

### Status Updates

Status updates are persistent messages that appear in the chat interface.

```json
{
  "type": "success",
  "title": "Success Status",
  "content": "This is a success status update",
  "icon": "check-circle"
}
```

Available status types:
- `success`
- `warning`
- `error`
- `info`
- `email`
- `calendar`
- `web-search`
- `file-system`
- `database`
- `api`

### Progress Updates

Progress updates display a progress bar with a percentage.

```json
{
  "type": "progress",
  "title": "Progress Update",
  "content": "Processing data...",
  "progress": 50,
  "icon": "loader"
}
```

Parameters:
- `progress`: The progress percentage (0-100)

### Animated Progress

Animated progress displays a series of steps with a delay between each step.

```json
{
  "type": "animated_progress",
  "title": "Animated Progress",
  "content": "Processing steps...",
  "steps": [
    "Step 1: Initializing...",
    "Step 2: Loading data...",
    "Step 3: Processing data...",
    "Step 4: Finalizing..."
  ],
  "delay": 1.0
}
```

Parameters:
- `steps`: An array of step descriptions
- `delay`: The delay in seconds between each step

### Alerts

Alerts are prominent messages that require user attention.

```json
{
  "type": "important_alert",
  "title": "Important Alert",
  "content": "This is an important alert",
  "icon": "alert-circle"
}
```

Available alert types:
- `important_alert`
- `notification_alert`
- `system_alert`

### Task Lists

Task lists display a list of tasks with their status.

```json
{
  "type": "task_list",
  "title": "Processing Tasks",
  "tasks": [
    {
      "name": "Initialize System",
      "status": "completed",
      "icon": "check-circle"
    },
    {
      "name": "Load Data",
      "status": "completed",
      "icon": "check-circle"
    },
    {
      "name": "Process Data",
      "status": "running",
      "icon": "loader"
    },
    {
      "name": "Generate Report",
      "status": "waiting",
      "icon": "clock"
    }
  ]
}
```

Parameters:
- `tasks`: An array of task objects
  - `name`: The name of the task
  - `status`: The status of the task (`completed`, `running`, `waiting`, `failed`)
  - `icon`: The icon to display with the task

## Integration with n8n

To integrate with n8n workflows, use the HTTP Request node to send POST requests to the webhook server:

1. Add an HTTP Request node to your workflow
2. Set the method to POST
3. Set the URL to `http://your-chainlit-server:5679/status`
4. Set the Content Type to `application/json`
5. Set the body to the JSON payload for the desired notification type
6. Connect the node to your workflow trigger

## Testing the Integration

You can use the provided test script to test the webhook integration:

```bash
# Test all notification types
./test_toast_notification.py --all

# Test specific notification types
./test_toast_notification.py --toast
./test_toast_notification.py --status
./test_toast_notification.py --progress
./test_toast_notification.py --animated
./test_toast_notification.py --alerts
./test_toast_notification.py --task-list
```

## Troubleshooting

If notifications are not appearing in the Chainlit UI:

1. Check if the webhook server is running:
   ```bash
   curl -X GET http://localhost:5679/health
   ```

2. Verify that the Chainlit application is running:
   ```bash
   chainlit run app.py
   ```

3. Check the logs for any errors:
   ```bash
   tail -f chainlit.log
   ```

4. Ensure that the status update payload is correctly formatted

## Available Icons

You can use any of the following icons in your status updates:

- `check-circle` - Checkmark in a circle
- `alert-triangle` - Warning triangle
- `alert-circle` - Error circle
- `info` - Information icon
- `mail` - Email icon
- `calendar` - Calendar icon
- `search` - Search icon
- `folder` - Folder icon
- `database` - Database icon
- `code` - Code icon
- `loader` - Loading spinner
- `clock` - Clock icon
- `bell` - Bell icon

## Implementation Details

The webhook integration consists of the following components:

1. **Webhook Server** (`status_webhook_integration.py`): Handles incoming webhook requests and adds them to a queue.

2. **Status Updates Processor** (`app.py`): Processes status updates from the queue and displays them in the Chainlit UI.

3. **Status Updates Functions** (`status_updates.py`): Contains functions for displaying different types of notifications.

## Advanced Configuration

You can configure the webhook server by modifying the following variables in `status_webhook_integration.py`:

- `WEBHOOK_HOST`: The host to bind the webhook server to (default: `0.0.0.0`)
- `WEBHOOK_PORT`: The port to bind the webhook server to (default: `5679`)
- `MAX_QUEUE_SIZE`: The maximum number of status updates to queue (default: `100`)

## Security Considerations

The webhook server does not implement authentication by default. In production environments, consider adding authentication to the webhook endpoints to prevent unauthorized access.

## Further Resources

- [Chainlit Documentation](https://docs.chainlit.io)
- [n8n Documentation](https://docs.n8n.io) 