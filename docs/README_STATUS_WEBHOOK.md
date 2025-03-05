# Status Updates Webhook Server

This webhook server allows you to trigger status updates, progress indicators, alerts, and toast notifications in the Chainlit UI by sending HTTP requests to a dedicated endpoint.

## Overview

The status webhook server runs as a separate service on port 5679 but is automatically started when you run the Chainlit application. It receives HTTP requests and forwards them to the Chainlit UI through a shared queue mechanism.

## Getting Started

### Prerequisites

- Python 3.7+
- FastAPI
- Uvicorn
- Requests
- Chainlit

These dependencies should already be installed if you're using the main application.

### Running the Server

The status webhook server is automatically started when you run the Chainlit application:

```bash
chainlit run app.py
```

The webhook server will be available at `http://localhost:5679/status`.

## API Reference

### Send a Status Update

**Endpoint:** `POST /status`

**Request Body:**

```json
{
  "content": "Your status message here",
  "type": "progress",
  "title": "Optional title",
  "icon": "optional-icon-name",
  "progress": 50,
  "duration": 3000
}
```

**Parameters:**

- `content` (required): The main message content to display
- `type` (optional): The type of status update. Default is "info". Available types:
  - `progress`: Shows a progress indicator
  - `success`: Shows a success message
  - `warning`: Shows a warning message
  - `error`: Shows an error message
  - `info`: Shows an informational message
  - `email`: Shows an email-related status
  - `calendar`: Shows a calendar-related status
  - `web-search`: Shows a web search status
  - `file-system`: Shows a file system operation status
  - `database`: Shows a database operation status
  - `api`: Shows an API operation status
  - `important-alert`: Shows an important alert
  - `notification-alert`: Shows a notification alert
  - `system-alert`: Shows a system alert
  - `toast`: Shows a toast notification
- `title` (optional): The title of the status update
- `icon` (optional): The icon to display (uses Lucide icon names)
- `progress` (optional): For progress type, the percentage complete (0-100)
- `duration` (optional): For toast notifications, the duration in milliseconds

**Response:**

```json
{
  "status": "success",
  "message": "Status update received"
}
```

### Health Check

**Endpoint:** `GET /health`

**Response:**

```json
{
  "status": "healthy",
  "queue_size": 0
}
```

## Examples

### Using cURL

```bash
# Send a progress update
curl -X POST http://localhost:5679/status \
  -H "Content-Type: application/json" \
  -d '{"content": "Processing data... 50% complete", "type": "progress", "title": "Data Processing", "progress": 50}'

# Send a success message
curl -X POST http://localhost:5679/status \
  -H "Content-Type: application/json" \
  -d '{"content": "Task completed successfully!", "type": "success", "title": "Success"}'

# Send a toast notification
curl -X POST http://localhost:5679/status \
  -H "Content-Type: application/json" \
  -d '{"content": "This is a toast notification", "type": "toast", "duration": 5000}'
```

### Using Python

```python
import requests

# Send a progress update
requests.post(
    "http://localhost:5679/status",
    json={
        "content": "Processing data... 50% complete",
        "type": "progress",
        "title": "Data Processing",
        "progress": 50
    }
)

# Send a success message
requests.post(
    "http://localhost:5679/status",
    json={
        "content": "Task completed successfully!",
        "type": "success",
        "title": "Success"
    }
)
```

## Integration with n8n

To integrate with n8n:

1. In your n8n workflow, add an HTTP Request node
2. Configure it with the following settings:
   - Method: POST
   - URL: http://localhost:5679/status
   - Headers: Content-Type: application/json
   - Body: JSON
   - JSON Body:
     ```json
     {
       "content": "Your status message here",
       "type": "progress",
       "title": "Optional title"
     }
     ```
3. Connect this node to your workflow where you want to display status updates

## How It Works

1. The webhook server runs as a separate service on port 5679
2. When a status update is received, it's added to a shared queue
3. A background task in the Chainlit application processes the queue and displays the status updates in the UI
4. This approach ensures that status updates are displayed correctly in the Chainlit UI without requiring direct integration with the Chainlit application

## Troubleshooting

- **Connection refused**: Make sure the Chainlit application is running
- **Status updates not showing**: Ensure the Chainlit UI is open and connected
- **Invalid JSON format**: Check that your request body is valid JSON
- **Chainlit context not found**: This error should no longer occur with the new approach

## License

This project is licensed under the same license as the main application. 