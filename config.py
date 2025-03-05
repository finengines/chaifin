"""
Configuration settings for the Chainlit frontend application.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# n8n Webhook Configuration
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/macAssistant")

# Default AI Provider and Model
DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "openrouter")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "google/gemini-2.0-flash-001")

# UI Configuration
APP_TITLE = os.getenv("APP_TITLE", "Personal Assistant")
APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "Your personal AI assistant powered by n8n")

# Model configurations by provider
PROVIDER_MODELS = {
    "openrouter": [
        {"id": "google/gemini-2.0-flash-001", "name": "Gemini 2.0 Flash", "description": "Google's Gemini 2.0 Flash model - fast and efficient"},
        {"id": "deepseek/deepseek-r1", "name": "DeepSeek R1", "description": "DeepSeek's R1 model for advanced reasoning"},
        {"id": "deepseek/deepseek-chat", "name": "DeepSeek Chat", "description": "DeepSeek's conversational model"}
    ],
    "openai": [
        {"id": "gpt-4o", "name": "GPT-4o", "description": "OpenAI's most advanced multimodal model"},
        {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "description": "Smaller, faster version of GPT-4o"},
        {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "description": "Fast and efficient model for most tasks"}
    ],
    "anthropic": [
        {"id": "claude-3-haiku", "name": "Claude 3 Haiku", "description": "Anthropic's fastest Claude model"},
        {"id": "claude-3.5-sonnet", "name": "Claude 3.7", "description": "Anthropic's most advanced model"}
    ],
    "ollama": [
        {"id": "qwen2.5:0.5b", "name": "Qwen 2.5 (0.5B)", "description": "Qwen 2.5 with 0.5B parameters"},
        {"id": "dolphin3:latest", "name": "Dolphin 3", "description": "Latest version of Dolphin 3"},
        {"id": "deepscaler:latest", "name": "DeepScaler", "description": "Latest DeepScaler model"},
        {"id": "nemotron-mini:latest", "name": "Nemotron Mini", "description": "Compact Nemotron model"},
        {"id": "phi4:latest", "name": "Phi-4", "description": "Microsoft's Phi-4 model"},
        {"id": "qwen2.5:7b", "name": "Qwen 2.5 (7B)", "description": "Qwen 2.5 with 7B parameters"},
        {"id": "qwen2.5:3b", "name": "Qwen 2.5 (3B)", "description": "Qwen 2.5 with 3B parameters"},
        {"id": "smollm2:360m", "name": "SmoLLM2 (360M)", "description": "SmoLLM2 with 360M parameters"},
        {"id": "mistral-nemo:latest", "name": "Mistral Nemo", "description": "Latest Mistral Nemo model"},
        {"id": "granite3.1-dense:2b", "name": "Granite 3.1 Dense (2B)", "description": "Granite 3.1 Dense with 2B parameters"},
        {"id": "dwightfoster03/functionary-small-v3.1:latest", "name": "Functionary Small v3.1", "description": "Function calling optimized model"},
        {"id": "llama3.1:latest", "name": "Llama 3.1", "description": "Latest Llama 3.1 model"},
        {"id": "mxbai-embed-large:latest", "name": "MxBai Embed Large", "description": "Large embedding model from MxBai"},
        {"id": "command-r7b:latest", "name": "Command R (7B)", "description": "Command R model with 7B parameters"},
        {"id": "llama3.2:1b", "name": "Llama 3.2 (1B)", "description": "Llama 3.2 with 1B parameters"},
        {"id": "mistral:7b", "name": "Mistral (7B)", "description": "Mistral model with 7B parameters"},
        {"id": "llama3.2:3b", "name": "Llama 3.2 (3B)", "description": "Llama 3.2 with 3B parameters"},
        {"id": "nomic-embed-text:latest", "name": "Nomic Embed Text", "description": "Text embedding model from Nomic"},
        {"id": "deepseek-r1:1.5b", "name": "DeepSeek R1 (1.5B)", "description": "DeepSeek R1 with 1.5B parameters"},
        {"id": "deepseek-r1:8b", "name": "DeepSeek R1 (8B)", "description": "DeepSeek R1 with 8B parameters"}
    ]
}

# Available providers for the dropdown
AVAILABLE_PROVIDERS = [
    {"value": "openrouter", "label": "OpenRouter"},
    {"value": "openai", "label": "OpenAI"},
    {"value": "anthropic", "label": "Anthropic"},
    {"value": "ollama", "label": "Ollama (Local)"}
]

# Authentication Configuration
ENABLE_AUTH = os.getenv("ENABLE_AUTH", "false").lower() == "true"

# Feedback Configuration
ENABLE_FEEDBACK = os.getenv("ENABLE_FEEDBACK", "true").lower() == "true"

# Request Configuration
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO") 