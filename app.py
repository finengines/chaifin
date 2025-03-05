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

# Import configuration
import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

@cl.set_chat_profiles
def chat_profiles():
    """Define available chat profiles based on providers and models."""
    profiles = []
    default_set = False
    
    # Create OpenRouter profiles
    if "openrouter" in config.PROVIDER_MODELS:
        for model in config.PROVIDER_MODELS["openrouter"]:
            profile = cl.ChatProfile(
                name=f"OpenRouter - {model['name']}",
                markdown_description=f"**{model['name']}**\n\n{model.get('description', 'OpenRouter model')}",
                icon="openrouter"
            )
            
            def make_on_select(provider, model_id):
                def on_select():
                    return {"provider": provider, "model_id": model_id}
                return on_select
            
            profile.on_select = make_on_select("openrouter", model["id"])
            
            # Set Gemini 2.0 Flash as the default
            if model["id"] == "google/gemini-2.0-flash-001":
                profile.default = True
                default_set = True
                
            profiles.append(profile)
    
    # Create OpenAI profiles
    if "openai" in config.PROVIDER_MODELS:
        for model in config.PROVIDER_MODELS["openai"]:
            profile = cl.ChatProfile(
                name=f"OpenAI - {model['name']}",
                markdown_description=f"**{model['name']}**\n\n{model.get('description', 'OpenAI model')}",
                icon="openai"
            )
            
            # Create a closure to capture the current values
            def make_on_select(provider, model_id):
                def on_select():
                    return {"provider": provider, "model_id": model_id}
                return on_select
            
            profile.on_select = make_on_select("openai", model["id"])
            profiles.append(profile)
    
    # Create Anthropic profiles
    if "anthropic" in config.PROVIDER_MODELS:
        for model in config.PROVIDER_MODELS["anthropic"]:
            profile = cl.ChatProfile(
                name=f"Anthropic - {model['name']}",
                markdown_description=f"**{model['name']}**\n\n{model.get('description', 'Anthropic model')}",
                icon="anthropic"
            )
            
            def make_on_select(provider, model_id):
                def on_select():
                    return {"provider": provider, "model_id": model_id}
                return on_select
            
            profile.on_select = make_on_select("anthropic", model["id"])
            profiles.append(profile)
    
    # Create Ollama profiles
    if "ollama" in config.PROVIDER_MODELS:
        for model in config.PROVIDER_MODELS["ollama"]:
            profile = cl.ChatProfile(
                name=f"Ollama - {model['name']}",
                markdown_description=f"**{model['name']}**\n\n{model.get('description', 'Ollama model')}",
                icon="ollama"
            )
            
            def make_on_select(provider, model_id):
                def on_select():
                    return {"provider": provider, "model_id": model_id}
                return on_select
            
            profile.on_select = make_on_select("ollama", model["id"])
            profiles.append(profile)
    
    # Set a default profile if there are any profiles and no default was set
    if profiles and not default_set:
        profiles[0].default = True
    
    return profiles

@cl.on_chat_start
async def on_chat_start():
    """Initialize a new chat session."""
    try:
        # Generate a unique session ID
        session_id = str(uuid.uuid4())
        cl.user_session.set("session_id", session_id)
        logger.info(f"New chat session started with ID: {session_id}")
        
        # Get the selected chat profile
        profile_name = cl.user_session.get("chat_profile_name", "Default")
        logger.info(f"Selected chat profile: {profile_name}")
        
        # Get the profile data
        profiles = chat_profiles()
        profile_data = next((p for p in profiles if p.name == profile_name), profiles[0])
        
        # Get the callback data from the profile
        if hasattr(profile_data, 'on_select') and callable(profile_data.on_select):
            profile_data = profile_data.on_select()
        else:
            profile_data = {}
        
        # Set the provider and model from the profile
        provider = profile_data.get("provider", config.DEFAULT_PROVIDER)
        model_id = profile_data.get("model_id", config.DEFAULT_MODEL)
        cl.user_session.set("provider", provider)
        cl.user_session.set("model", model_id)
        logger.info(f"Using provider: {provider}, model: {model_id}")
        
        # Initialize conversation history
        cl.user_session.set("conversation_history", [])
        
        # Send a welcome message
        model_name = "Unknown Model"
        if provider in config.PROVIDER_MODELS:
            for model_config in config.PROVIDER_MODELS[provider]:
                if model_config["id"] == model_id:
                    model_name = model_config["name"]
                    break
        
        welcome_message = f"Welcome! I'm using the {model_name} model from {provider}. How can I help you today?"
        await cl.Message(content=welcome_message, author="Assistant").send()
        
    except Exception as e:
        logger.error(f"Error in on_chat_start: {str(e)}")
        await cl.Message(content=f"Error initializing chat: {str(e)}", author="System").send()

@cl.on_message
async def on_message(message: cl.Message):
    """Handle incoming user messages."""
    try:
        # Get session information
        session_id = cl.user_session.get("session_id")
        provider = cl.user_session.get("provider")
        model_id = cl.user_session.get("model")
        
        # Log the incoming message
        logger.info(f"Received message from user: {message.content}")
        logger.info(f"Using provider: {provider}, model: {model_id}")
        
        # Prepare the request payload for n8n
        payload = {
            "chatInput": message.content,
            "sessionID": session_id,
            "provider": provider,
            "model": model_id,  # This is the model ID that n8n expects
            "temperature": 0.7,
            "max_tokens": 2048
        }
        
        # Show thinking indicator
        thinking_msg = cl.Message(content="Thinking...", author="Assistant")
        await thinking_msg.send()
        
        # Measure response time
        start_time = time.time()
        
        # Make the API call to n8n
        try:
            response = make_n8n_request(payload)
            
            # Calculate and log response time
            response_time = time.time() - start_time
            logger.info(f"Response time: {response_time:.2f} seconds")
            
            # Remove the thinking message
            await thinking_msg.remove()
            
            # Check if the response is valid and contains an output
            if response and "output" in response[0]:
                # Get the assistant's response
                assistant_response = response[0]["output"]
                
                # Update conversation history with user and assistant messages
                conversation_history = cl.user_session.get("conversation_history", [])
                conversation_history.append({"role": "user", "content": message.content})
                conversation_history.append({"role": "assistant", "content": assistant_response})
                cl.user_session.set("conversation_history", conversation_history)
                
                # Check for any special elements in the response
                elements = []
                
                # Check if there are any images in the response
                if "images" in response[0] and response[0]["images"]:
                    for img_url in response[0]["images"]:
                        elements.append(cl.Image(url=img_url, name="Generated Image"))
                
                # Send the assistant's response
                await cl.Message(
                    content=assistant_response,
                    author="Assistant",
                    elements=elements
                ).send()
            else:
                logger.error(f"Invalid response format: {response}")
                await cl.Message(content="I'm sorry, I received an invalid response. Please try again.").send()
        
        except Exception as e:
            logger.error(f"Error in on_message: {str(e)}")
            await thinking_msg.remove()
            await cl.Message(content=f"I'm sorry, an error occurred: {str(e)}").send()
    
    except Exception as e:
        logger.error(f"Unexpected error in on_message: {str(e)}")
        await cl.Message(content=f"I'm sorry, an unexpected error occurred: {str(e)}").send()

def make_n8n_request(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Make a request to the n8n webhook.
    
    Args:
        payload: The payload to send to n8n
        
    Returns:
        The parsed response from n8n
    """
    try:
        # Log the payload for debugging
        logger.debug(f"Sending payload to n8n: {payload}")
        
        # Make the POST request to the n8n webhook
        response = requests.post(
            config.N8N_WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=config.REQUEST_TIMEOUT
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse the JSON response
        parsed_response = response.json()
        logger.debug(f"Received response from n8n: {parsed_response}")
        
        # Ensure the response is a list
        if not isinstance(parsed_response, list):
            logger.info(f"Converting non-list response to list: {type(parsed_response)}")
            
            # If it's a dictionary with an 'output' field, wrap it in a list
            if isinstance(parsed_response, dict) and "output" in parsed_response:
                parsed_response = [parsed_response]
            # If it's a dictionary without an 'output' field, create one
            elif isinstance(parsed_response, dict):
                # If there's a text or content field, use that as output
                if "text" in parsed_response:
                    parsed_response = [{"output": parsed_response["text"]}]
                elif "content" in parsed_response:
                    parsed_response = [{"output": parsed_response["content"]}]
                else:
                    # Create a simple wrapper with the whole response as output
                    parsed_response = [{"output": str(parsed_response)}]
            else:
                # For any other type, convert to string and wrap
                parsed_response = [{"output": str(parsed_response)}]
        
        # Validate that the response contains the expected fields
        for item in parsed_response:
            if not isinstance(item, dict):
                logger.warning(f"Response item is not a dictionary: {item}")
                item = {"output": str(item)}
            elif "output" not in item:
                logger.warning(f"Response item missing 'output' field: {item}")
                # Try to find alternative fields that might contain the output
                if "text" in item:
                    item["output"] = item["text"]
                elif "content" in item:
                    item["output"] = item["content"]
                elif "response" in item:
                    item["output"] = item["response"]
                else:
                    item["output"] = str(item)
        
        return parsed_response
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        raise Exception(f"Error communicating with n8n: {str(e)}")
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        raise Exception("Invalid JSON response from n8n")

@cl.on_chat_end
async def on_chat_end():
    """Handle chat session end."""
    logger.info("Chat session ended")

@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    """
    Authenticate users based on username and password.
    Only used if authentication is enabled in config.
    """
    # Simple authentication for demo purposes
    # In a production environment, use a secure authentication method
    if username == "admin" and password == "password":
        return cl.User(identifier="admin", metadata={"role": "admin"})
    return None

if __name__ == "__main__":
    # This block will be executed when running the script directly
    print(f"Starting {config.APP_TITLE}...")
    print(f"Run 'chainlit run app.py -w' to start the application") 