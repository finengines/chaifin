"""
Chainlit frontend for n8n-powered personal assistant.
"""

import uuid
import json
import logging
import requests
import time
import os
from typing import Dict, Any, List, Optional
import chainlit as cl
from chainlit.types import AskFileResponse
from chainlit.input_widget import Select

# Import configuration
import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Define chat profiles
@cl.set_chat_profiles
async def chat_profiles():
    """Define available chat profiles based on providers and models."""
    profiles = []
    
    # OpenRouter profiles
    for model in config.PROVIDER_MODELS["openrouter"]:
        # Create a function factory to properly capture the model values
        def create_on_select(provider, model_id):
            return lambda: {"provider": provider, "model_id": model_id}
        
        profile = cl.ChatProfile(
            name=f"OpenRouter - {model['name']}",
            markdown_description=f"**{model['name']}**\n\n{model['description']}",
            icon="https://openrouter.ai/favicon.ico",  # OpenRouter icon
        )
        # Use the function factory to create a unique on_select for each model
        profile.on_select = create_on_select("openrouter", model['id'])
        profiles.append(profile)
    
    # OpenAI profiles
    for model in config.PROVIDER_MODELS["openai"]:
        def create_on_select(provider, model_id):
            return lambda: {"provider": provider, "model_id": model_id}
            
        profile = cl.ChatProfile(
            name=f"OpenAI - {model['name']}",
            markdown_description=f"**{model['name']}**\n\n{model['description']}",
            icon="https://openai.com/favicon.ico",  # OpenAI icon
        )
        profile.on_select = create_on_select("openai", model['id'])
        profiles.append(profile)
    
    # Anthropic profiles
    for model in config.PROVIDER_MODELS["anthropic"]:
        def create_on_select(provider, model_id):
            return lambda: {"provider": provider, "model_id": model_id}
            
        profile = cl.ChatProfile(
            name=f"Anthropic - {model['name']}",
            markdown_description=f"**{model['name']}**\n\n{model['description']}",
            icon="https://anthropic.com/favicon.ico",  # Anthropic icon
        )
        profile.on_select = create_on_select("anthropic", model['id'])
        profiles.append(profile)
    
    # Ollama profiles
    for model in config.PROVIDER_MODELS["ollama"]:
        def create_on_select(provider, model_id):
            return lambda: {"provider": provider, "model_id": model_id}
            
        profile = cl.ChatProfile(
            name=f"Ollama - {model['name']}",
            markdown_description=f"**{model['name']}**\n\n{model['description']}",
            icon="https://ollama.com/favicon.ico",  # Ollama icon
        )
        profile.on_select = create_on_select("ollama", model['id'])
        profiles.append(profile)
    
    # Set default profile to Gemini (first OpenRouter model)
    profiles[0].default = True  # OpenRouter - Gemini 2.0 Flash as default
    
    return profiles

# Initialize chat settings
@cl.on_settings_update
async def on_settings_update(settings: Dict[str, Any]):
    """Handle settings updates from the UI."""
    logger.info(f"Settings updated: {settings}")
    
    # Update the user's session with the new settings
    for key, value in settings.items():
        cl.user_session.set(key, value)
    
    # Send a confirmation message
    await cl.Message(
        content=f"Settings updated!",
        author="System",
    ).send()

@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session."""
    # Generate a unique session ID
    session_id = str(uuid.uuid4())
    cl.user_session.set("session_id", session_id)
    
    # Get the selected chat profile
    chat_profile_name = cl.user_session.get("chat_profile")
    logger.info(f"Selected chat profile: {chat_profile_name}")
    
    # Get the provider and model from the on_select callback data
    profile_data = cl.user_session.get("chat_profile_callback_data", {})
    
    # Set provider and model from the selected profile
    provider = profile_data.get("provider", config.DEFAULT_PROVIDER)
    model_id = profile_data.get("model_id", config.DEFAULT_MODEL)
    
    logger.info(f"Using provider: {provider}, model: {model_id}")
    
    cl.user_session.set("provider", provider)
    cl.user_session.set("model", model_id)
    
    # Initialize conversation history
    cl.user_session.set("conversation_history", [])
    
    # Note: Avatar component is no longer supported in Chainlit 2.2.1
    # Instead, place avatar images in public/avatars directory
    # The image file should be named after the author of the message
    # For example: public/avatars/assistant.png for messages with author="Assistant"
    
    # Send welcome message
    await cl.Message(
        content=f"Welcome to {config.APP_TITLE}! I'm using {chat_profile_name}. How can I assist you today?",
        author="Assistant",
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    """Handle incoming user messages."""
    try:
        # Get session information
        session_id = cl.user_session.get("session_id")
        provider = cl.user_session.get("provider")
        model = cl.user_session.get("model")
        
        # Log the incoming message
        logger.info(f"Received message from user: {message.content}")
        
        # Prepare the request payload for n8n
        payload = {
            "chatInput": message.content,
            "sessionID": session_id,
            "provider": provider,
            "model": model
        }
        
        # Show thinking indicator
        thinking_msg = cl.Message(content="Thinking...", author="Assistant")
        await thinking_msg.send()
        
        # Make the API request to n8n
        start_time = time.time()
        response = make_n8n_request(payload)
        response_time = time.time() - start_time
        
        # Remove the thinking message
        await thinking_msg.remove()
        
        # Process the response
        if response and isinstance(response, list) and len(response) > 0 and "output" in response[0]:
            # Get the AI response
            ai_response = response[0]["output"]
            
            # Update the conversation history
            conversation_history = cl.user_session.get("conversation_history", [])
            conversation_history.append({
                "role": "user",
                "content": message.content
            })
            conversation_history.append({
                "role": "assistant",
                "content": ai_response
            })
            cl.user_session.set("conversation_history", conversation_history)
            
            # Create elements for the response if needed
            elements = []
            
            # Check if the response contains any special elements (like images, files, etc.)
            if "elements" in response[0]:
                for element in response[0]["elements"]:
                    if element["type"] == "image" and "url" in element:
                        elements.append(cl.Image(url=element["url"], name=element.get("name", "Image")))
                    elif element["type"] == "file" and "url" in element:
                        elements.append(cl.File(url=element["url"], name=element.get("name", "File")))
            
            # Send the response to the user
            response_message = cl.Message(
                content=ai_response, 
                author="Assistant",
                elements=elements
            )
            
            # Add metadata if available
            if "metadata" in response[0]:
                response_message.metadata = response[0]["metadata"]
            
            await response_message.send()
            
            # Log response time for monitoring
            logger.info(f"Response generated in {response_time:.2f} seconds")
            
            # Add feedback buttons if enabled
            if config.ENABLE_FEEDBACK:
                await response_message.update()
        else:
            # Handle empty or invalid response
            error_msg = "I received an invalid response. Please try again."
            await cl.Message(content=error_msg, author="System").send()
            logger.error(f"Invalid response from n8n: {response}")
    
    except requests.exceptions.Timeout:
        # Handle timeout specifically
        error_message = "The request to the assistant backend timed out. Please try again later."
        await cl.Message(content=error_message, author="System").send()
        logger.error("Request to n8n timed out")
    
    except requests.exceptions.ConnectionError:
        # Handle connection errors
        error_message = "Could not connect to the assistant backend. Please check if the n8n service is running."
        await cl.Message(content=error_message, author="System").send()
        logger.error("Connection error to n8n")
    
    except Exception as e:
        # Handle any other errors
        error_message = f"An error occurred: {str(e)}"
        await cl.Message(content=error_message, author="System").send()
        logger.exception("Error processing message")

def make_n8n_request(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Make a request to the n8n webhook and return the response.
    
    Args:
        payload: The data to send to the n8n webhook
        
    Returns:
        The parsed response from n8n
    """
    try:
        # Make the POST request to n8n
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            config.N8N_WEBHOOK_URL,
            headers=headers,
            json=payload,
            timeout=config.REQUEST_TIMEOUT  # Use the configured timeout
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse the JSON response
        json_response = response.json()
        
        # Ensure the response is in the expected format (a list)
        if not isinstance(json_response, list):
            json_response = [json_response]
            
        # Validate that the response contains the expected fields
        if not json_response or "output" not in json_response[0]:
            logger.warning(f"Unexpected response format from n8n: {json_response}")
            # Return a default response structure
            return [{"output": "I received an unexpected response format. Please try again."}]
            
        return json_response
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making request to n8n: {str(e)}")
        raise Exception(f"Failed to communicate with the assistant backend: {str(e)}")
    
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response: {str(e)}")
        raise Exception("Received an invalid response from the assistant backend")

@cl.on_chat_end
async def on_chat_end():
    """Handle chat end event."""
    logger.info("Chat session ended")
    
    # Clean up any resources if needed
    # For example, you could send a notification to n8n that the session has ended
    
    # Send a goodbye message
    await cl.Message(content="Thank you for using our assistant. The session has ended.", author="System").send()

@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    """
    Authenticate users with username and password.
    Only used if ENABLE_AUTH is set to true.
    """
    if not config.ENABLE_AUTH:
        # If authentication is disabled, auto-authenticate everyone
        return cl.User(identifier=username)
    
    # Simple hardcoded authentication for demo purposes
    # In a real application, you would check against a database or external auth service
    if username == "admin" and password == "password":
        return cl.User(identifier=username, metadata={"role": "admin"})
    elif username == "user" and password == "password":
        return cl.User(identifier=username, metadata={"role": "user"})
    
    # Authentication failed
    return None

if __name__ == "__main__":
    # This block will be executed when running the script directly
    print(f"Starting {config.APP_TITLE}...")
    print(f"Run 'chainlit run app.py -w' to start the application") 