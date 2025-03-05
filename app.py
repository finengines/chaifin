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

# Import status updates
from status_updates import (
    web_search_status,
    email_status,
    calendar_status,
    file_system_status,
    database_status,
    api_status,
    progress_status,
    success_status,
    warning_status,
    error_status,
    info_status,
    important_alert,
    notification_alert,
    system_alert,
    animated_progress,
    StyledTaskList,
    show_toast
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("chainlit_app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@cl.set_chat_profiles
def chat_profiles():
    """Define available chat profiles based on providers and models."""
    profiles = []
    default_set = False
    
    print("Creating chat profiles...")
    
    # Create a factory function outside the loops to properly capture values
    def create_on_select_function(provider, model_id):
        """Create an on_select function with fixed provider and model_id values."""
        def on_select():
            print(f"Selected profile with provider: {provider}, model_id: {model_id}")
            logger.info(f"Selected profile with provider: {provider}, model_id: {model_id}")
            return {"provider": provider, "model_id": model_id}
        return on_select
    
    # Create OpenRouter profiles
    if "openrouter" in config.PROVIDER_MODELS:
        print(f"Creating OpenRouter profiles: {len(config.PROVIDER_MODELS['openrouter'])} models")
        for model in config.PROVIDER_MODELS["openrouter"]:
            profile = cl.ChatProfile(
                name=f"OpenRouter - {model['name']}",
                markdown_description=f"**{model['name']}**\n\n{model.get('description', 'OpenRouter model')}",
                icon="openrouter"
            )
            
            # Use the factory function to create a closure with fixed values
            profile.on_select = create_on_select_function("openrouter", model["id"])
            
            # Set  2.0 Flash as the default
            if model["id"] == "google/gemini-2.0-flash-001":
                profile.default = True
                default_set = True
                print(f"Setting default profile: OpenRouter - {model['name']}")
                
            profiles.append(profile)
    
    # Create OpenAI profiles
    if "openai" in config.PROVIDER_MODELS:
        for model in config.PROVIDER_MODELS["openai"]:
            profile = cl.ChatProfile(
                name=f"OpenAI - {model['name']}",
                markdown_description=f"**{model['name']}**\n\n{model.get('description', 'OpenAI model')}",
                icon="openai"
            )
            
            # Use the factory function to create a closure with fixed values
            profile.on_select = create_on_select_function("openai", model["id"])
            
            profiles.append(profile)
    
    # Create Anthropic profiles
    if "anthropic" in config.PROVIDER_MODELS:
        for model in config.PROVIDER_MODELS["anthropic"]:
            profile = cl.ChatProfile(
                name=f"Anthropic - {model['name']}",
                markdown_description=f"**{model['name']}**\n\n{model.get('description', 'Anthropic model')}",
                icon="anthropic"
            )
            
            # Use the factory function to create a closure with fixed values
            profile.on_select = create_on_select_function("anthropic", model["id"])
            
            profiles.append(profile)
    
    # Create Ollama profiles
    if "ollama" in config.PROVIDER_MODELS:
        for model in config.PROVIDER_MODELS["ollama"]:
            profile = cl.ChatProfile(
                name=f"Ollama - {model['name']}",
                markdown_description=f"**{model['name']}**\n\n{model.get('description', 'Ollama model')}",
                icon="ollama"
            )
            
            # Use the factory function to create a closure with fixed values
            profile.on_select = create_on_select_function("ollama", model["id"])
            
            profiles.append(profile)
    
    # Set a default profile if there are any profiles and no default was set
    if profiles and not default_set:
        profiles[0].default = True
    
    return profiles

@cl.on_chat_start
async def on_chat_start():
    """
    Initialize the chat session.
    
    This function is called when a new chat session is started.
    It initializes the conversation history and sets the initial model.
    """
    print("Starting new chat session...")
    
    # Generate a unique session ID
    session_id = str(uuid.uuid4())
    cl.user_session.set("session_id", session_id)
    print(f"Session ID: {session_id}")
    logger.info(f"Starting new chat session with ID: {session_id}")
    
    # Get the selected chat profile from the user session
    profile_name = cl.user_session.get("chat_profile")
    print(f"Selected chat profile from session: {profile_name}")
    logger.info(f"Selected chat profile from session: {profile_name}")
    
    # Get all available profiles
    profiles = chat_profiles()
    print(f"Available profiles: {[p.name for p in profiles]}")
    logger.info(f"Available profiles: {[p.name for p in profiles]}")
    
    # Find the matching profile
    profile_data = None
    
    # If a profile name is provided, find the matching profile
    if profile_name:
        profile_data = next((p for p in profiles if p.name == profile_name), None)
        
        if not profile_data:
            logger.warning(f"No matching profile found for name: {profile_name}")
            
            # Find the default profile
            profile_data = next((p for p in profiles if hasattr(p, 'default') and p.default), None)
            
            if profile_data:
                logger.info(f"Using default profile: {profile_data.name}")
                # Update the profile name in the session
                cl.user_session.set("chat_profile", profile_data.name)
            else:
                # Use the first profile as a fallback
                profile_data = profiles[0] if profiles else None
                if profile_data:
                    logger.info(f"Using first profile as fallback: {profile_data.name}")
                    # Update the profile name in the session
                    cl.user_session.set("chat_profile", profile_data.name)
        else:
            logger.info(f"Found matching profile: {profile_data.name}")
    else:
        # No profile name provided, use the default profile
        profile_data = next((p for p in profiles if hasattr(p, 'default') and p.default), None)
        
        if profile_data:
            logger.info(f"Using default profile: {profile_data.name}")
            # Update the profile name in the session
            cl.user_session.set("chat_profile", profile_data.name)
        else:
            # Use the first profile as a fallback
            profile_data = profiles[0] if profiles else None
            if profile_data:
                logger.info(f"Using first profile as fallback: {profile_data.name}")
                # Update the profile name in the session
                cl.user_session.set("chat_profile", profile_data.name)
    
    # Get the callback data from the profile
    profile_settings = {}
    if profile_data and hasattr(profile_data, 'on_select') and callable(profile_data.on_select):
        profile_settings = profile_data.on_select()
        logger.info(f"Profile on_select returned: {profile_settings}")
    else:
        if profile_data:
            logger.warning(f"Profile {profile_data.name} does not have an on_select method")
        else:
            logger.warning("No valid profile data found")
    
    # Set the provider and model from the profile
    provider = profile_settings.get("provider", config.DEFAULT_PROVIDER)
    model_id = profile_settings.get("model_id", config.DEFAULT_MODEL)
    
    # Store the provider and model in the user session
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
    
    # Remove the system notification about the selected profile
    # Send only the welcome message
    await cl.Message(
        content=f"Hello! I'm your personal assistant powered by {model_name}. How can I help you today?",
        author="Assistant"
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    """
    Handle incoming messages from the user.
    
    This function is called when a user sends a message.
    It processes the message and sends it to n8n for processing.
    
    Args:
        message: The incoming message from the user
    """
    try:
        print(f"Received message: {message.content}")
        
        # Get the session ID
        session_id = cl.user_session.get("session_id")
        if not session_id:
            session_id = str(uuid.uuid4())
            cl.user_session.set("session_id", session_id)
            print(f"Created new session ID: {session_id}")
            logger.info(f"Created new session ID: {session_id}")
        
        # Get the current chat profile from the user session
        current_profile_name = cl.user_session.get("chat_profile")
        print(f"Current chat profile from session: {current_profile_name}")
        logger.info(f"Current chat profile from session: {current_profile_name}")
        
        # Get all available profiles
        profiles = chat_profiles()
        print(f"Available profiles: {[p.name for p in profiles]}")
        logger.info(f"Available profiles: {[p.name for p in profiles]}")
        
        # Find the matching profile
        selected_profile = None
        if current_profile_name:
            selected_profile = next((p for p in profiles if p.name == current_profile_name), None)
            if selected_profile:
                print(f"Found matching profile: {selected_profile.name}")
                logger.info(f"Found matching profile: {selected_profile.name}")
            else:
                print(f"No matching profile found for name: {current_profile_name}")
                logger.warning(f"No matching profile found for name: {current_profile_name}")
        
        # Get the provider and model from the user session
        provider = cl.user_session.get("provider")
        model_id = cl.user_session.get("model")
        
        # If we have a selected profile, update the provider and model
        if selected_profile and hasattr(selected_profile, 'on_select') and callable(selected_profile.on_select):
            profile_settings = selected_profile.on_select()
            if profile_settings and isinstance(profile_settings, dict):
                provider = profile_settings.get("provider", provider)
                model_id = profile_settings.get("model_id", model_id)
                print(f"Selected profile with provider: {provider}, model_id: {model_id}")
                logger.info(f"Selected profile with provider: {provider}, model_id: {model_id}")
                print(f"Profile on_select returned: {profile_settings}")
                logger.info(f"Profile on_select returned: {profile_settings}")
                
                # Update the session with the new provider and model
                cl.user_session.set("provider", provider)
                cl.user_session.set("model", model_id)
                print(f"Updated provider to {provider} and model to {model_id}")
                logger.info(f"Updated provider to {provider} and model to {model_id}")
        
        # Check if the message is a model command
        if message.content.startswith("/model"):
            try:
                # Parse the model command
                parts = message.content.split()
                if len(parts) < 2:
                    await cl.Message(
                        content="Please specify a model name. Example: /model gpt-4",
                        author="System"
                    ).send()
                    return
                
                model_name = parts[1]
                
                # Find the profile that matches the model name
                matching_profile = None
                for profile in profiles:
                    if model_name.lower() in profile.name.lower():
                        matching_profile = profile
                        break
                
                if not matching_profile:
                    await cl.Message(
                        content=f"No model found with name: {model_name}",
                        author="System"
                    ).send()
                    return
                
                # Update the session with the new profile
                cl.user_session.set("chat_profile", matching_profile.name)
                
                # Get the provider and model from the profile
                if hasattr(matching_profile, 'on_select') and callable(matching_profile.on_select):
                    profile_settings = matching_profile.on_select()
                    if profile_settings and isinstance(profile_settings, dict):
                        provider = profile_settings.get("provider", provider)
                        model_id = profile_settings.get("model_id", model_id)
                        
                        # Update the session with the new provider and model
                        cl.user_session.set("provider", provider)
                        cl.user_session.set("model", model_id)
                
                await cl.Message(
                    content=f"Switched to model: {matching_profile.name}",
                    author="System"
                ).send()
                return
            except Exception as e:
                logger.error(f"Error processing model command: {str(e)}")
                await cl.Message(
                    content=f"Error changing model: {str(e)}",
                    author="System"
                ).send()
                return
        
        # Double-check that we have valid provider and model_id
        if not provider or not model_id:
            logger.warning(f"Missing provider ({provider}) or model_id ({model_id}). Using defaults.")
            provider = config.DEFAULT_PROVIDER
            model_id = config.DEFAULT_MODEL
            
            # Update the session with the defaults
            cl.user_session.set("provider", provider)
            cl.user_session.set("model", model_id)
        
        # Prepare the request payload for n8n
        payload = {
            "chatInput": message.content,
            "sessionID": session_id,
            "provider": provider,
            "model": model_id,  # This is the model ID that n8n expects
            "temperature": 0.7,
            "max_tokens": 2048
        }
        
        # Log the payload for verification
        logger.info(f"Sending payload to n8n: {json.dumps(payload, indent=2)}")
        print(f"Current session settings - provider: {provider}, model: {model_id}")
        logger.info(f"Current session settings - provider: {provider}, model: {model_id}")
        
        # Show processing status with task list
        task_list = StyledTaskList("Processing Request", "Initializing...")
        await task_list.send()
        
        # Add initial task
        request_task = await task_list.add_task("Sending request to AI service", "Preparing to send request", "waiting")
        
        # Update task status to running
        await task_list.update_task(request_task["id"], "running", "Sending request to AI service...")
        
        # Measure response time
        start_time = time.time()
        
        # Make the API call to n8n
        try:
            # Update task list status
            task_list.status = "Processing request..."
            await task_list.send()
            
            response = make_n8n_request(payload)
            
            # Calculate and log response time
            end_time = time.time()
            response_time = end_time - start_time
            logger.info(f"n8n response received in {response_time:.2f} seconds")
            
            # Update task status to done
            await task_list.update_task(request_task["id"], "done", f"Request processed in {response_time:.2f} seconds")
            
            # Add response processing task
            response_task = await task_list.add_task("Processing response", "Preparing to process response", "waiting")
            await task_list.update_task(response_task["id"], "running", "Processing response...")
            
            # Process the response
            if response:
                # Check for agent actions in the response
                if isinstance(response, dict) and "actions" in response:
                    actions = response["actions"]
                    for action in actions:
                        action_type = action.get("type", "").lower()
                        action_status = action.get("status", "").lower()
                        action_message = action.get("message", "")
                        
                        # Show appropriate status update based on action type
                        if action_type == "web_search":
                            await web_search_status("Web Search", action_message)
                        elif action_type == "email":
                            await email_status("Email Action", action_message)
                        elif action_type == "calendar":
                            await calendar_status("Calendar Action", action_message)
                        elif action_type == "file_system":
                            await file_system_status("File System Action", action_message)
                        elif action_type == "database":
                            await database_status("Database Action", action_message)
                        elif action_type == "api":
                            await api_status("API Action", action_message)
                
                # Update task status to done
                await task_list.update_task(response_task["id"], "done", "Response processed successfully")
                
                # Update task list status
                task_list.status = "Request completed successfully"
                await task_list.send()
                
                # Check if the response is a dictionary with an 'output' field
                if isinstance(response, dict) and "output" in response:
                    # Send the response to the user
                    await cl.Message(content=response["output"], author="Assistant").send()
                    
                    # Show success toast
                    await show_toast("Response received successfully", "success")
                # Check if the response is a list with at least one item
                elif isinstance(response, list) and len(response) > 0:
                    # Get the first response
                    first_response = response[0]
                    
                    # Check if the response has the expected format
                    if "content" in first_response:
                        # Send the response to the user
                        await cl.Message(content=first_response["content"], author="Assistant").send()
                        
                        # Show success toast
                        await show_toast("Response received successfully", "success")
                    elif "output" in first_response:
                        # Send the response to the user
                        await cl.Message(content=first_response["output"], author="Assistant").send()
                        
                        # Show success toast
                        await show_toast("Response received successfully", "success")
                    else:
                        # Log the unexpected response format
                        logger.warning(f"Unexpected response format: {first_response}")
                        print(f"Unexpected response format: {first_response}")
                        
                        # Show warning status
                        await warning_status(
                            "Unexpected Response Format", 
                            "The response from the AI service has an unexpected format."
                        )
                        
                        # Send a generic message to the user
                        await cl.Message(
                            content="I received a response in an unexpected format. Please try again.",
                            author="Assistant"
                        ).send()
                        
                        # Update task status to failed
                        await task_list.update_task(response_task["id"], "failed", "Unexpected response format")
                        
                        # Update task list status
                        task_list.status = "Request completed with warnings"
                        await task_list.send()
                else:
                    # Log the empty response
                    logger.warning(f"Empty response from n8n: {response}")
                    print(f"Empty response from n8n: {response}")
                    
                    # Show error status
                    await error_status(
                        "Empty Response", 
                        "The AI service returned an empty response."
                    )
                    
                    # Send an error message to the user
                    await cl.Message(
                        content="I didn't receive a proper response from the AI service. Please try again.",
                        author="Assistant"
                    ).send()
                    
                    # Update task status to failed
                    await task_list.update_task(response_task["id"], "failed", "Empty response")
                    
                    # Update task list status
                    task_list.status = "Request failed"
                    await task_list.send()
            else:
                # Log the empty response
                logger.warning("No response from n8n")
                print("No response from n8n")
                
                # Show error status
                await error_status(
                    "No Response", 
                    "No response was received from the AI service."
                )
                
                # Send an error message to the user
                await cl.Message(
                    content="I didn't receive a response from the AI service. Please try again.",
                    author="Assistant"
                ).send()
                
                # Update task status to failed
                await task_list.update_task(response_task["id"], "failed", "No response received")
                
                # Update task list status
                task_list.status = "Request failed"
                await task_list.send()
        except Exception as e:
            # Log the exception
            logger.error(f"Error making request to n8n: {str(e)}")
            print(f"Error making request to n8n: {str(e)}")
            
            # Show error status
            await error_status(
                "Request Error", 
                f"An error occurred while making the request: {str(e)}"
            )
            
            # Send an error message to the user
            await cl.Message(
                content=f"An error occurred while processing your request: {str(e)}",
                author="System"
            ).send()
            
            # Update task status to failed
            await task_list.update_task(request_task["id"], "failed", f"Error: {str(e)}")
            
            # Update task list status
            task_list.status = "Request failed"
            await task_list.send()
            
            # Show error toast
            await show_toast("Error processing request", "error")
    except Exception as e:
        # Log the exception
        logger.error(f"Error in on_message: {str(e)}")
        print(f"Error in on_message: {str(e)}")
        
        # Show error status
        await error_status(
            "System Error", 
            f"An unexpected error occurred: {str(e)}"
        )
        
        # Send an error message to the user
        await cl.Message(
            content=f"An unexpected error occurred: {str(e)}",
            author="System"
        ).send()
        
        # Show error toast
        await show_toast("Unexpected error occurred", "error")

def make_n8n_request(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Make a request to the n8n webhook.
    
    Args:
        payload: The payload to send to n8n
        
    Returns:
        The parsed response from n8n
    """
    try:
        # Log the original payload for debugging
        print(f"Original payload to n8n: {json.dumps(payload, indent=2)}")
        logger.info(f"Original payload to n8n: {json.dumps(payload, indent=2)}")
        
        # Ensure the provider and model are correctly set
        if not payload.get("provider"):
            print("Provider missing in payload. Using default provider.")
            logger.warning("Provider missing in payload. Using default provider.")
            payload["provider"] = config.DEFAULT_PROVIDER
        
        if not payload.get("model"):
            print("Model missing in payload. Using default model.")
            logger.warning("Model missing in payload. Using default model.")
            payload["model"] = config.DEFAULT_MODEL
        
        # Get the current provider and model from the payload
        provider = payload.get("provider")
        model = payload.get("model")
        
        # Log the provider and model for debugging
        print(f"Final payload provider: {provider}, model: {model}")
        logger.info(f"Final payload provider: {provider}, model: {model}")
        print(f"Full payload being sent to n8n: {json.dumps(payload, indent=2)}")
        logger.info(f"Full payload being sent to n8n: {json.dumps(payload, indent=2)}")
        
        # Make the POST request to the n8n webhook
        response = requests.post(
            config.N8N_WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=config.REQUEST_TIMEOUT
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse the response
        try:
            response_data = response.json()
            logger.info(f"Received response from n8n: {json.dumps(response_data, indent=2)}")
            return response_data
        except json.JSONDecodeError:
            logger.error(f"Failed to parse response as JSON: {response.text}")
            raise ValueError(f"Invalid JSON response from n8n: {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to n8n failed: {str(e)}")
        raise RuntimeError(f"Failed to communicate with n8n: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in make_n8n_request: {str(e)}")
        raise RuntimeError(f"Unexpected error: {str(e)}")

@cl.on_chat_end
async def on_chat_end():
    """Clean up resources when the chat session ends."""
    logger.info("Chat session ended")

@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    """Authenticate a user with username and password."""
    if username == "admin" and password == "admin":
        return cl.User(identifier="admin", metadata={"role": "admin"})
    return None

if __name__ == "__main__":
    # This block will be executed when running the script directly
    pass 