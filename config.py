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
DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "openai")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4")

# UI Configuration
APP_TITLE = os.getenv("APP_TITLE", "Personal Assistant")
APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "Your personal AI assistant powered by n8n")

# Available models for the dropdown
AVAILABLE_MODELS = [
    {"value": "gpt-4", "label": "GPT-4"},
    {"value": "gpt-3.5-turbo", "label": "GPT-3.5 Turbo"},
    {"value": "claude-3-opus", "label": "Claude 3 Opus"},
    {"value": "claude-3-sonnet", "label": "Claude 3 Sonnet"},
    {"value": "claude-3-haiku", "label": "Claude 3 Haiku"},
]

# Available providers for the dropdown
AVAILABLE_PROVIDERS = [
    {"value": "openai", "label": "OpenAI"},
    {"value": "anthropic", "label": "Anthropic"},
]

# Authentication Configuration
ENABLE_AUTH = os.getenv("ENABLE_AUTH", "false").lower() == "true"

# Feedback Configuration
ENABLE_FEEDBACK = os.getenv("ENABLE_FEEDBACK", "true").lower() == "true"

# Request Configuration
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO") 