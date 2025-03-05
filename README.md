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

## Requirements

- Python 3.9+
- Chainlit 2.2.0+
- Requests 2.31.0+
- n8n backend running with the macAssistant webhook configured

## Project Structure

```
ChainFin/
├── app.py                 # Main application file
├── config.py              # Configuration settings
├── requirements.txt       # Dependencies
├── README.md              # Documentation
├── .env                   # Environment variables (create from .env.example)
├── .env.example           # Example environment variables
├── chainlit.md            # Welcome screen content
└── .chainlit/             # Chainlit configuration
    └── config.json        # Chainlit UI configuration
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