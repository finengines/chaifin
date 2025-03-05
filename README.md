# Chainlit Frontend for n8n Personal Assistant

## Project Overview

This project provides a Chainlit-based frontend UI for a personal assistant, with the backend running on n8n. The application connects to an n8n webhook to process user messages and display responses.

## Features

- **Modern UI**: Clean, responsive interface powered by Chainlit
- **Chat Profiles**: Select from predefined AI models across multiple providers
- **Multi-Provider Support**: Choose between different AI providers (OpenRouter, OpenAI, Anthropic, Ollama)
- **Extensive Model Selection**: Access a wide range of models including:
  - OpenRouter: Gemini 2.0 Flash, DeepSeek R1, DeepSeek Chat
  - OpenAI: GPT-4o, GPT-4o Mini, GPT-3.5 Turbo
  - Anthropic: Claude 3 Haiku, Claude 3.7
  - Ollama: 20+ local models including Llama, Mistral, Qwen, and more
- **Conversation History**: Preserve conversation context during the session
- **Customizable Settings**: Adjust settings through the UI or configuration files
- **Error Handling**: Robust error handling for API failures and timeouts
- **Authentication**: Optional password-based authentication
- **Feedback Collection**: Enable user feedback on responses
- **Markdown Support**: Rich text formatting in messages
- **Multi-Modal Support**: Display images and files from the backend
- **Status Updates**: Real-time status updates, progress indicators, alerts, and toast notifications
- **Status Webhook Server**: Dedicated webhook server for receiving status updates from n8n

## Requirements

- Python 3.9+
- Chainlit 2.2.0+
- Requests 2.31.0+
- FastAPI 0.104.0+
- Uvicorn 0.23.0+
- n8n backend running with the macAssistant webhook configured

## Project Structure

```
ChainFin/
├── app.py                     # Main application file
├── config.py                  # Configuration settings
├── requirements.txt           # Dependencies
├── README.md                  # Documentation
├── .env                       # Environment variables (create from .env.example)
├── .env.example               # Example environment variables
├── chainlit.md                # Welcome screen content
├── status_updates.py          # Status updates module
├── status_webhook_server.py   # Status webhook server
├── test_status_webhook.py     # Test script for status webhook
├── n8n_integration_example.py # n8n integration example
├── README_STATUS_WEBHOOK.md   # Status webhook documentation
└── .chainlit/                 # Chainlit configuration
    └── config.json            # Chainlit UI configuration
```

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and adjust settings as needed

## Configuration

### Environment Variables

The application can be configured using environment variables in the `.env` file:

- `N8N_WEBHOOK_URL`: URL of the n8n webhook (default: `http://localhost:5678/webhook/macAssistant`)
- `DEFAULT_PROVIDER`: Default AI provider (default: `openai`)
- `DEFAULT_MODEL`: Default AI model (default: `gpt-4o`)
- `APP_TITLE`: Application title (default: `Personal Assistant`)
- `APP_DESCRIPTION`: Application description
- `ENABLE_AUTH`: Enable authentication (default: `false`)
- `ENABLE_FEEDBACK`: Enable feedback collection (default: `true`)
- `REQUEST_TIMEOUT`: Timeout for n8n requests in seconds (default: `60`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

### Chat Profiles Configuration

The available chat profiles are configured in the `config.py` file. Each profile includes:

- Provider name
- Model ID
- Model name
- Description
- Icon

You can customize the available models by editing the `PROVIDER_MODELS` dictionary in `config.py`.

### Chainlit Configuration

The Chainlit UI can be customized by editing the `.chainlit/config.json` file. See the [Chainlit documentation](https://docs.chainlit.io) for more details.

## Usage

1. Ensure your n8n backend is running with the macAssistant webhook configured
2. Test the connection: `python test_n8n_connection.py`
3. Start the Chainlit application: `chainlit run app.py -w`
4. Access the UI at http://localhost:8000
5. Select a chat profile from the dropdown menu to start chatting with a specific model

### Status Webhook Server

The application includes a dedicated webhook server for receiving status updates from external systems (like n8n workflows). This allows you to display real-time progress indicators, alerts, and notifications in the Chainlit UI.

### How It Works

The status webhook server runs as a separate service on port 5679 and is automatically started when you launch the Chainlit application. It receives HTTP POST requests with status update information and displays them in the Chainlit UI.

### Using the Status Webhook Server

To send a status update, make an HTTP POST request to `http://localhost:5679/status` with a JSON payload containing the status update information:

```bash
curl -X POST http://localhost:5679/status \
  -H "Content-Type: application/json" \
  -d '{"type": "success", "title": "Task Completed", "content": "The task has been completed successfully!"}'
```

### Supported Status Update Types

- `progress`: Shows a progress bar with percentage
- `success`: Displays a success message
- `warning`: Displays a warning message
- `error`: Displays an error message
- `info`: Displays an informational message
- `toast`: Shows a temporary toast notification
- Custom types: Displayed using a custom element

### Testing and Diagnostics

The repository includes several tools to help you test and diagnose the status webhook server:

1. **Test Script**: Run `python test_status_webhook.py --demo` to send various types of status updates to the webhook server.

2. **Diagnostic Script**: Run `python diagnose_webhook.py` to check if the webhook server is running correctly and diagnose any issues.

3. **Health Check**: Access `http://localhost:5679/health` in your browser to check the status of the webhook server.

For more detailed information, see the [Status Webhook Documentation](README_STATUS_WEBHOOK.md) and [Webhook Integration Fixes](WEBHOOK_FIXES.md).

### Notification System Improvements

The notification system has been enhanced with the following features:

1. **Robust Error Handling**: The system now includes comprehensive error handling for all notification types, with fallback mechanisms to ensure notifications are always displayed.

2. **Custom JavaScript Integration**: A custom JavaScript implementation in `.chainlit/custom.js` provides an independent toast notification system that operates alongside Chainlit's built-in system.

3. **Multiple Display Methods**: Notifications can now be displayed through multiple methods, ensuring they reach the user even if one method fails.

4. **Comprehensive Testing**: The `test_all_notifications.py` script allows testing of all notification types to verify functionality.

5. **Port Conflict Resolution**: The webhook server now handles port conflicts gracefully, with automatic detection and resolution.

6. **Health Monitoring**: Enhanced health checks provide detailed information about the status of the webhook server and notification processing.

7. **Fallback Mechanisms**: If a notification cannot be displayed through the primary method, it will automatically fall back to alternative methods.

## API Integration

The application communicates with the n8n backend using a webhook. The payload sent to the webhook includes:

- `chatInput`: The user's message
- `sessionID`: A unique session identifier
- `provider`: The selected AI provider
- `model`: The selected AI model

The expected response format is a JSON array containing an object with:

- `output`: The AI's response text
- `elements` (optional): Array of elements to display (images, files, etc.)
- `metadata` (optional): Additional metadata for the response

### Status Updates Integration

The status webhook server can be integrated with n8n to display real-time status updates in the Chainlit UI. In your n8n workflow, add an HTTP Request node with the following configuration:

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

## Customization

### Welcome Screen

The welcome screen content can be customized by editing the `chainlit.md` file.

### UI Appearance

The UI appearance can be customized by editing the `.chainlit/config.json` file.

### Adding New Models

To add new models:

1. Edit the `PROVIDER_MODELS` dictionary in `config.py`
2. Add the new model with its ID, name, and description
3. Restart the application

## Best Practices

- **Clean Architecture**: The application follows a modular design with separation of concerns
- **Error Handling**: Comprehensive error handling for API failures and timeouts
- **Security**: Optional authentication and secure handling of user data
- **Performance**: Optimized for responsiveness with appropriate timeouts
- **Documentation**: Clear documentation for configuration and usage

## Troubleshooting

- If you encounter connection issues, check if the n8n backend is running
- Verify the webhook URL in the `.env` file
- Check the logs for detailed error messages
- Ensure you have the correct dependencies installed

## License

This project is licensed under the MIT License - see the LICENSE file for details.

# Chainlit Webhook Integration

This project provides a webhook integration for Chainlit applications, allowing external systems to send status updates and notifications that are displayed in the Chainlit UI.

## Features

- **Webhook Server**: A lightweight server that receives status updates from external systems
- **Multiple Notification Types**: Support for various notification types including:
  - Toast notifications
  - Status updates (success, warning, error, info)
  - Progress indicators
  - Animated progress steps
  - Alerts (important, notification, system)
  - Task lists
- **n8n Integration**: Example workflow for integrating with n8n
- **Testing Tools**: Scripts to test the webhook integration

## Getting Started

### Prerequisites

- Python 3.8+
- Chainlit 2.1.0+

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/chainlit-webhook-integration.git
   cd chainlit-webhook-integration
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the Chainlit application:
   ```bash
   chainlit run app.py
   ```

2. The webhook server will start automatically with the Chainlit application.

3. Test the webhook integration:
   ```bash
   ./test_toast_notification.py --all
   ```

## Usage

### Sending Status Updates

To send a status update to the webhook server, make a POST request to the `/status` endpoint:

```bash
curl -X POST http://localhost:5679/status \
  -H "Content-Type: application/json" \
  -d '{
    "type": "toast",
    "content": "This is a toast notification",
    "toast_type": "info",
    "duration": 5000
  }'
```

### Checking Server Health

To check if the webhook server is running:

```bash
curl -X GET http://localhost:5679/health
```