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
import asyncio

# Import configuration
import config

# Import status webhook integration
import status_webhook_integration

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

# Stop any existing webhook server
status_webhook_integration.stop_webhook_server()
logger.info("Stopped any existing webhook server")

# Start the webhook server - ONLY ONCE at application startup
webhook_server_thread = status_webhook_integration.start_webhook_server(port=5679)
if webhook_server_thread:
    logger.info("Started status webhook server on port 5679")
else:
    logger.error("Failed to start webhook server. Notifications may not work correctly.")

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
    
    This function is called when a new chat session starts.
    It initializes the session with a unique ID and sets up the chat interface.
    """
    try:
        # Generate a unique session ID
        session_id = str(uuid.uuid4())
        cl.user_session.set("session_id", session_id)
        print(f"Created new session ID: {session_id}")
        logger.info(f"Created new session ID: {session_id}")
        
        # Set up the chat settings with input widgets for reasoning and privacy modes
        settings = await cl.ChatSettings(
            [
                cl.input_widget.Switch(
                    id="reasoning_mode",
                    label="🧠 Reasoning Mode",
                    initial=False,
                    tooltip="Enable detailed reasoning in responses",
                    description="When enabled, the AI will show its reasoning process"
                ),
                cl.input_widget.Switch(
                    id="privacy_mode",
                    label="🛡️ Privacy Mode",
                    initial=False,
                    tooltip="Enable enhanced privacy for sensitive conversations",
                    description="When enabled, your conversation won't be stored for training"
                )
            ]
        ).send()
        
        # Store the initial settings in the session
        cl.user_session.set("reasoning_mode", settings.get("reasoning_mode", False))
        cl.user_session.set("privacy_mode", settings.get("privacy_mode", False))
        
        # Create a welcome message
        welcome_message = f"""
        # Welcome to ChainFin AI Assistant
        
        I'm here to help you with your questions and tasks. Feel free to ask me anything!
        
        **Session ID:** `{session_id}`
        """
        
        # Create action buttons for quick access to reasoning and privacy modes
        reasoning_action = cl.Action(
            name="toggle_reasoning",
            label="🧠 Reasoning Mode: OFF",
            description="Toggle reasoning mode on/off",
            payload={}
        )
        
        privacy_action = cl.Action(
            name="toggle_privacy",
            label="🛡️ Privacy Mode: OFF",
            description="Toggle privacy mode on/off",
            payload={}
        )
        
        # Send the welcome message with action buttons
        await cl.Message(
            content=welcome_message,
            actions=[reasoning_action, privacy_action]
        ).send()
        
    except Exception as e:
        error_message = f"Error in on_chat_start: {str(e)}"
        print(error_message)
        logger.error(error_message)
        await cl.Message(content=f"Error initializing chat: {str(e)}").send()

@cl.on_settings_update
async def on_settings_update(settings):
    """
    Handle updates to chat settings.
    
    This function is called when the user updates the chat settings.
    It updates the session with the new settings.
    
    Args:
        settings: The updated settings
    """
    try:
        # Update the reasoning mode setting
        if "reasoning_mode" in settings:
            reasoning_mode = settings.get("reasoning_mode", False)
            cl.user_session.set("reasoning_mode", reasoning_mode)
            logger.info(f"Updated reasoning_mode to {reasoning_mode}")
            
        # Update the privacy mode setting
        if "privacy_mode" in settings:
            privacy_mode = settings.get("privacy_mode", False)
            cl.user_session.set("privacy_mode", privacy_mode)
            logger.info(f"Updated privacy_mode to {privacy_mode}")
        
        # Update any custom toggles
        custom_widgets = cl.user_session.get("custom_widgets", {})
        for widget_id, widget_info in custom_widgets.items():
            if widget_info.get("type") == "toggle" and widget_id in settings:
                cl.user_session.set(widget_id, settings.get(widget_id, False))
                logger.info(f"Updated custom toggle {widget_id} to {settings.get(widget_id, False)}")
            
        # Log the updated settings
        logger.info(f"Settings updated: {settings}")
        
    except Exception as e:
        error_message = f"Error in on_settings_update: {str(e)}"
        print(error_message)
        logger.error(error_message)

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
        
        # Check if the message is a command to add a custom button or toggle
        if message.content.startswith("/add_button") or message.content.startswith("/add_toggle"):
            await handle_custom_widget_command(message.content)
            return
        
        # Check if the message is a command to list custom widgets
        if message.content.strip() == "/list_widgets":
            await list_custom_widgets()
            return
        
        # Check if the message is a help command
        if message.content.strip() == "/help_widgets":
            await show_widgets_help()
            return
            
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
            "max_tokens": 2048,
            "reasoning_mode": cl.user_session.get("reasoning_mode", False),
            "privacy_mode": cl.user_session.get("privacy_mode", False)
        }
        
        # Add any custom toggles to the payload
        custom_widgets = cl.user_session.get("custom_widgets", {})
        for widget_id, widget_info in custom_widgets.items():
            if widget_info.get("type") == "toggle":
                # Add the toggle value to the payload
                payload[widget_id] = cl.user_session.get(widget_id, False)
        
        # Log the payload for verification
        logger.info(f"Sending payload to n8n: {json.dumps(payload, indent=2)}")
        print(f"Current session settings - provider: {provider}, model: {model_id}")
        logger.info(f"Current session settings - provider: {provider}, model: {model_id}")
        
        # Create a simple "thinking" message instead of a task list
        thinking_msg = cl.Message(content="Thinking...", author="Assistant")
        await thinking_msg.send()
        
        # Measure response time
        start_time = time.time()
        
        # Make the API call to n8n
        try:
            # Make the request to n8n
            response = make_n8n_request(payload)
            
            # Calculate and log response time
            end_time = time.time()
            response_time = end_time - start_time
            logger.info(f"n8n response received in {response_time:.2f} seconds")
            
            # Remove the thinking message
            await thinking_msg.remove()
            
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
                        
                        # Show appropriate status update based on action status
                        if action_status == "success":
                            await success_status(f"{action_type.title()} Success", action_message)
                        elif action_status == "warning":
                            await warning_status(f"{action_type.title()} Warning", action_message)
                        elif action_status == "error":
                            await error_status(f"{action_type.title()} Error", action_message)
                        elif action_status == "info":
                            await info_status(f"{action_type.title()} Info", action_message)
                
                # Process the main response
                if isinstance(response, list) and len(response) > 0:
                    for item in response:
                        if isinstance(item, dict):
                            # Extract the output text
                            output = item.get("output", "")
                            
                            # Extract any elements (images, files, etc.)
                            elements = item.get("elements", [])
                            
                            # Create a message with the output and elements
                            if output or elements:
                                await cl.Message(
                                    content=output,
                                    elements=elements,
                                    author="Assistant"
                                ).send()
                            
                            # Extract and process any metadata
                            metadata = item.get("metadata", {})
                            if metadata:
                                # Process any specific metadata fields here
                                pass
                        else:
                            # If the item is not a dict, just send it as a string
                            await cl.Message(content=str(item), author="Assistant").send()
                elif isinstance(response, dict):
                    # Extract the output text
                    output = response.get("output", "")
                    
                    # Extract any elements (images, files, etc.)
                    elements = response.get("elements", [])
                    
                    # Create a message with the output and elements
                    if output or elements:
                        await cl.Message(
                            content=output,
                            elements=elements,
                            author="Assistant"
                        ).send()
                else:
                    # If the response is not a list or dict, just send it as a string
                    await cl.Message(content=str(response), author="Assistant").send()
            else:
                # Handle empty response
                await cl.Message(
                    content="I'm sorry, I didn't receive a response from the backend. Please try again.",
                    author="System"
                ).send()
        except Exception as e:
            logger.error(f"Error making n8n request: {str(e)}", exc_info=True)
            
            # Remove the thinking message
            await thinking_msg.remove()
            
            # Send an error message
            await cl.Message(
                content=f"I'm sorry, there was an error processing your request: {str(e)}",
                author="System",
                type="error"
            ).send()
    except Exception as e:
        logger.error(f"Error in on_message: {str(e)}", exc_info=True)
        
        # Send an error message
        await cl.Message(
            content=f"I'm sorry, there was an error processing your message: {str(e)}",
            author="System",
            type="error"
        ).send()

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
    """
    Clean up when the chat session ends.
    
    This function is called when a chat session ends.
    It cleans up any resources used by the chat session.
    """
    # Log the chat end
    logger.info("Chat session ended")

@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    """Authenticate a user with username and password."""
    if username == "admin" and password == "admin":
        return cl.User(identifier="admin", metadata={"role": "admin"})
    return None

async def handle_custom_widget_command(command):
    """
    Handle commands to add custom buttons or toggles.
    
    Args:
        command: The command string from the user
    """
    try:
        parts = command.split(maxsplit=4)
        
        if len(parts) < 3:
            await cl.Message(content="Invalid command format. Use `/add_button ID Label [Icon] [Description]` or `/add_toggle ID Label [Icon] [Description]`").send()
            return
            
        cmd_type = parts[0]
        widget_id = parts[1]
        widget_label = parts[2]
        
        # Check if an icon is provided
        widget_icon = ""
        widget_description = None
        
        if len(parts) > 3:
            # Check if the third part is an emoji icon (usually starts with 🧠, 🛡️, etc.)
            if any(ord(c) > 127 for c in parts[3]) and len(parts[3].strip()) <= 2:
                widget_icon = parts[3].strip()
                widget_description = parts[4] if len(parts) > 4 else None
            else:
                widget_description = parts[3]
                
                # Check if there's a fifth part and it's an emoji
                if len(parts) > 4 and any(ord(c) > 127 for c in parts[4]) and len(parts[4].strip()) <= 2:
                    widget_icon = parts[4].strip()
        
        # Get existing custom widgets
        custom_widgets = cl.user_session.get("custom_widgets", {})
        
        # Add the new widget
        if cmd_type == "/add_button":
            # Create an Action for a button
            display_label = f"{widget_icon} {widget_label}".strip()
            
            custom_widgets[widget_id] = {
                "type": "button",
                "label": widget_label,
                "icon": widget_icon,
                "description": widget_description
            }
            
            # Create and send the button as an Action
            action = cl.Action(
                name=widget_id,
                label=display_label,
                description=widget_description,
                payload={}
            )
            
            await cl.Message(
                content=f"Button '{display_label}' added with ID '{widget_id}'",
                actions=[action]
            ).send()
            
        elif cmd_type == "/add_toggle":
            # Create a Switch for a toggle
            display_label = f"{widget_icon} {widget_label}".strip()
            
            custom_widgets[widget_id] = {
                "type": "toggle",
                "label": widget_label,
                "icon": widget_icon,
                "description": widget_description
            }
            
            # Get current chat settings
            current_settings = cl.user_session.get("chat_settings", [])
            
            # Add the new toggle to chat settings
            new_settings = current_settings + [
                cl.input_widget.Switch(
                    id=widget_id,
                    label=display_label,
                    initial=False,
                    description=widget_description
                )
            ]
            
            # Update chat settings
            settings = await cl.ChatSettings(new_settings).send()
            
            # Store the updated value in the session
            cl.user_session.set(widget_id, settings.get(widget_id, False))
            
            # Create an action button for the toggle
            toggle_action_name = f"toggle_{widget_id}"
            action = cl.Action(
                name=toggle_action_name,
                label=f"{display_label}: OFF",
                description=f"Toggle {widget_label} on/off",
                payload={}
            )
            
            # Register a dynamic action callback for this toggle
            @cl.action_callback(toggle_action_name)
            async def on_custom_toggle(action):
                try:
                    # Toggle the value
                    current_value = cl.user_session.get(widget_id, False)
                    new_value = not current_value
                    cl.user_session.set(widget_id, new_value)
                    
                    # Update the settings in the UI
                    current_settings = cl.user_session.get("chat_settings", [])
                    new_settings = [
                        setting for setting in current_settings 
                        if not (isinstance(setting, cl.input_widget.Switch) and setting.id == widget_id)
                    ]
                    
                    new_settings.append(
                        cl.input_widget.Switch(
                            id=widget_id,
                            label=display_label,
                            initial=new_value,
                            description=widget_description
                        )
                    )
                    
                    await cl.ChatSettings(new_settings).send()
                    
                    # Create a new action button with updated state
                    status = "ON" if new_value else "OFF"
                    new_action = cl.Action(
                        name=toggle_action_name,
                        label=f"{display_label}: {status}",
                        description=f"Toggle {widget_label} on/off",
                        payload={}
                    )
                    
                    # Send a message to confirm the change
                    await cl.Message(
                        content=f"{display_label} turned **{status}**",
                        actions=[new_action]
                    ).send()
                    
                except Exception as e:
                    error_message = f"Error handling custom toggle action: {str(e)}"
                    print(error_message)
                    logger.error(error_message)
                    await cl.Message(content=f"Error toggling {display_label}: {str(e)}").send()
            
            await cl.Message(
                content=f"Toggle '{display_label}' added with ID '{widget_id}'",
                actions=[action]
            ).send()
            
            # Add the toggle action to custom widgets
            custom_widgets[toggle_action_name] = {
                "type": "toggle_action",
                "toggle_id": widget_id,
                "label": widget_label,
                "icon": widget_icon,
                "description": widget_description
            }
        
        # Store the updated custom widgets
        cl.user_session.set("custom_widgets", custom_widgets)
        
    except Exception as e:
        error_message = f"Error handling custom widget command: {str(e)}"
        print(error_message)
        logger.error(error_message)
        await cl.Message(content=f"Error adding custom widget: {str(e)}").send()

@cl.action_callback("toggle_reasoning")
async def on_toggle_reasoning(action):
    """
    Handle the toggle_reasoning action.
    
    This function is called when the user clicks the reasoning mode toggle button.
    It toggles the reasoning mode and updates the UI.
    
    Args:
        action: The action object containing information about the button click
    """
    try:
        # Toggle the reasoning mode
        current_value = cl.user_session.get("reasoning_mode", False)
        new_value = not current_value
        cl.user_session.set("reasoning_mode", new_value)
        
        # Update the settings in the UI
        await cl.ChatSettings(
            [
                cl.input_widget.Switch(
                    id="reasoning_mode",
                    label="🧠 Reasoning Mode",
                    initial=new_value,
                    tooltip="Enable detailed reasoning in responses",
                    description="When enabled, the AI will show its reasoning process"
                )
            ]
        ).send()
        
        # Create a new action button with updated state
        status = "ON" if new_value else "OFF"
        new_action = cl.Action(
            name="toggle_reasoning",
            label=f"🧠 Reasoning Mode: {status}",
            description="Toggle reasoning mode on/off",
            payload={}
        )
        
        # Send a message to confirm the change
        await cl.Message(
            content=f"Reasoning mode turned **{status}**",
            actions=[new_action]
        ).send()
        
    except Exception as e:
        error_message = f"Error handling toggle_reasoning action: {str(e)}"
        print(error_message)
        logger.error(error_message)
        await cl.Message(content=f"Error toggling reasoning mode: {str(e)}").send()

@cl.action_callback("toggle_privacy")
async def on_toggle_privacy(action):
    """
    Handle the toggle_privacy action.
    
    This function is called when the user clicks the privacy mode toggle button.
    It toggles the privacy mode and updates the UI.
    
    Args:
        action: The action object containing information about the button click
    """
    try:
        # Toggle the privacy mode
        current_value = cl.user_session.get("privacy_mode", False)
        new_value = not current_value
        cl.user_session.set("privacy_mode", new_value)
        
        # Update the settings in the UI
        await cl.ChatSettings(
            [
                cl.input_widget.Switch(
                    id="privacy_mode",
                    label="🛡️ Privacy Mode",
                    initial=new_value,
                    tooltip="Enable enhanced privacy for sensitive conversations",
                    description="When enabled, your conversation won't be stored for training"
                )
            ]
        ).send()
        
        # Create a new action button with updated state
        status = "ON" if new_value else "OFF"
        new_action = cl.Action(
            name="toggle_privacy",
            label=f"🛡️ Privacy Mode: {status}",
            description="Toggle privacy mode on/off",
            payload={}
        )
        
        # Send a message to confirm the change
        await cl.Message(
            content=f"Privacy mode turned **{status}**",
            actions=[new_action]
        ).send()
        
    except Exception as e:
        error_message = f"Error handling toggle_privacy action: {str(e)}"
        print(error_message)
        logger.error(error_message)
        await cl.Message(content=f"Error toggling privacy mode: {str(e)}").send()

@cl.action_callback
async def on_action(action):
    """
    Handle button actions.
    
    This function is called when a user clicks a button.
    It processes the action and updates the session accordingly.
    
    Args:
        action: The action object containing information about the button click
    """
    try:
        action_name = action.name
        
        # Get custom widgets
        custom_widgets = cl.user_session.get("custom_widgets", {})
        
        # Check if this is a custom toggle action
        if action_name.startswith("toggle_") and action_name in custom_widgets and custom_widgets[action_name].get("type") == "toggle_action":
            # Get the toggle ID
            toggle_id = custom_widgets[action_name].get("toggle_id")
            
            if toggle_id and toggle_id in custom_widgets:
                # Toggle the value
                current_value = cl.user_session.get(toggle_id, False)
                new_value = not current_value
                cl.user_session.set(toggle_id, new_value)
                
                # Get toggle info
                toggle_label = custom_widgets[toggle_id].get("label", "Unknown")
                toggle_icon = custom_widgets[toggle_id].get("icon", "")
                toggle_description = custom_widgets[toggle_id].get("description", "")
                display_label = f"{toggle_icon} {toggle_label}".strip()
                
                # Update the settings in the UI
                current_settings = cl.user_session.get("chat_settings", [])
                new_settings = [
                    setting for setting in current_settings 
                    if not (isinstance(setting, cl.input_widget.Switch) and setting.id == toggle_id)
                ]
                
                new_settings.append(
                    cl.input_widget.Switch(
                        id=toggle_id,
                        label=display_label,
                        initial=new_value,
                        description=toggle_description
                    )
                )
                
                await cl.ChatSettings(new_settings).send()
                
                # Create a new action button with updated state
                status = "ON" if new_value else "OFF"
                new_action = cl.Action(
                    name=action_name,
                    label=f"{display_label}: {status}",
                    description=f"Toggle {toggle_label} on/off",
                    payload={}
                )
                
                # Send a message to confirm the change
                await cl.Message(
                    content=f"{display_label} turned **{status}**",
                    actions=[new_action]
                ).send()
                
                return
        
        # Check if this is a custom button
        if action_name in custom_widgets and custom_widgets[action_name].get("type") == "button":
            # Get button info
            button_label = custom_widgets[action_name].get("label", "Unknown")
            button_icon = custom_widgets[action_name].get("icon", "")
            display_label = f"{button_icon} {button_label}".strip()
            
            # Create a message to acknowledge the button click
            await cl.Message(content=f"Button '{display_label}' clicked").send()
            
            # Prepare a payload to send to n8n
            session_id = cl.user_session.get("session_id")
            provider = cl.user_session.get("provider")
            model_id = cl.user_session.get("model")
            
            # Create a payload with the button action
            payload = {
                "action": action_name,
                "sessionID": session_id,
                "provider": provider,
                "model": model_id,
                "reasoning_mode": cl.user_session.get("reasoning_mode", False),
                "privacy_mode": cl.user_session.get("privacy_mode", False)
            }
            
            # Add any custom toggles to the payload
            for widget_id, widget_info in custom_widgets.items():
                if widget_info.get("type") == "toggle":
                    # Add the toggle value to the payload
                    payload[widget_id] = cl.user_session.get(widget_id, False)
            
            # Log the payload for verification
            logger.info(f"Sending button action payload to n8n: {json.dumps(payload, indent=2)}")
            
            # Make the API call to n8n
            response = make_n8n_request(payload)
            
            # Process the response
            if response:
                # Process the main response
                if isinstance(response, list) and len(response) > 0:
                    for item in response:
                        if isinstance(item, dict):
                            # Extract the output text
                            output = item.get("output", "")
                            
                            # Extract any elements (images, files, etc.)
                            elements = item.get("elements", [])
                            
                            # Create a message with the output and elements
                            if output or elements:
                                await cl.Message(
                                    content=output,
                                    elements=elements,
                                    author="Assistant"
                                ).send()
        
    except Exception as e:
        error_message = f"Error handling action: {str(e)}"
        print(error_message)
        logger.error(error_message)
        await cl.Message(content=f"Error processing button action: {str(e)}").send()

async def list_custom_widgets():
    """
    List all custom widgets that have been created.
    """
    try:
        custom_widgets = cl.user_session.get("custom_widgets", {})
        
        if not custom_widgets:
            await cl.Message(content="No custom widgets have been created yet.").send()
            return
        
        # Create a message with the list of widgets
        widgets_list = "# Custom Widgets\n\n"
        
        # List buttons
        buttons = [
            (widget_id, widget_info) 
            for widget_id, widget_info in custom_widgets.items() 
            if widget_info.get("type") == "button"
        ]
        
        if buttons:
            widgets_list += "## Buttons\n\n"
            for widget_id, widget_info in buttons:
                label = widget_info.get("label", "Unnamed Button")
                icon = widget_info.get("icon", "")
                description = widget_info.get("description", "No description")
                display_label = f"{icon} {label}".strip()
                widgets_list += f"- **{display_label}** (ID: `{widget_id}`): {description}\n"
            widgets_list += "\n"
        
        # List toggles
        toggles = [
            (widget_id, widget_info) 
            for widget_id, widget_info in custom_widgets.items() 
            if widget_info.get("type") == "toggle"
        ]
        
        if toggles:
            widgets_list += "## Toggles\n\n"
            for widget_id, widget_info in toggles:
                label = widget_info.get("label", "Unnamed Toggle")
                icon = widget_info.get("icon", "")
                description = widget_info.get("description", "No description")
                value = cl.user_session.get(widget_id, False)
                status = "Enabled" if value else "Disabled"
                display_label = f"{icon} {label}".strip()
                widgets_list += f"- **{display_label}** (ID: `{widget_id}`): {description} - *{status}*\n"
        
        # Add built-in toggles
        widgets_list += "\n## Built-in Toggles\n\n"
        
        # Reasoning Mode
        reasoning_mode = cl.user_session.get("reasoning_mode", False)
        reasoning_status = "Enabled" if reasoning_mode else "Disabled"
        widgets_list += f"- **🧠 Reasoning Mode**: When enabled, the AI will show its reasoning process - *{reasoning_status}*\n"
        
        # Privacy Mode
        privacy_mode = cl.user_session.get("privacy_mode", False)
        privacy_status = "Enabled" if privacy_mode else "Disabled"
        widgets_list += f"- **🛡️ Privacy Mode**: When enabled, your conversation won't be stored for training - *{privacy_status}*\n"
        
        # Create action buttons for the toggles
        actions = []
        
        # Add built-in toggle actions
        reasoning_btn_status = "ON" if reasoning_mode else "OFF"
        privacy_btn_status = "ON" if privacy_mode else "OFF"
        
        actions.append(
            cl.Action(
                name="toggle_reasoning",
                label=f"🧠 Reasoning Mode: {reasoning_btn_status}",
                description="Toggle reasoning mode on/off",
                payload={}
            )
        )
        
        actions.append(
            cl.Action(
                name="toggle_privacy",
                label=f"🛡️ Privacy Mode: {privacy_btn_status}",
                description="Toggle privacy mode on/off",
                payload={}
            )
        )
        
        # Add custom toggle actions
        for widget_id, widget_info in toggles:
            if widget_info.get("type") == "toggle":
                label = widget_info.get("label", "Unnamed Toggle")
                icon = widget_info.get("icon", "")
                display_label = f"{icon} {label}".strip()
                value = cl.user_session.get(widget_id, False)
                btn_status = "ON" if value else "OFF"
                
                actions.append(
                    cl.Action(
                        name=f"toggle_{widget_id}",
                        label=f"{display_label}: {btn_status}",
                        description=f"Toggle {label} on/off",
                        payload={}
                    )
                )
        
        # Send the message with action buttons
        await cl.Message(
            content=widgets_list,
            actions=actions
        ).send()
        
    except Exception as e:
        error_message = f"Error listing custom widgets: {str(e)}"
        print(error_message)
        logger.error(error_message)
        await cl.Message(content=f"Error listing custom widgets: {str(e)}").send()

async def show_widgets_help():
    """
    Show help information about custom widgets.
    """
    try:
        help_text = """
        # Custom Widgets Help
        
        You can create custom buttons and toggles that will send additional flags to n8n along with your messages.
        
        ## Available Commands
        
        - `/add_button ID Label [Icon] [Description]` - Add a custom button
        - `/add_toggle ID Label [Icon] [Description]` - Add a custom toggle switch
        - `/list_widgets` - List all custom widgets
        - `/help_widgets` - Show this help message
        
        ## Examples
        
        ```
        /add_button search_web Search Web 🔍 Search the web for information
        /add_toggle debug_mode Debug Mode 🐛 Enable detailed debugging information
        ```
        
        ## Icons
        
        You can use emoji icons with your buttons and toggles. Here are some useful ones:
        
        - 🧠 Brain (for reasoning/thinking)
        - 🛡️ Shield (for privacy/security)
        - 🔍 Magnifying Glass (for search)
        - 📊 Chart (for analytics)
        - 🐛 Bug (for debugging)
        - 📝 Note (for notes/documentation)
        - ⚙️ Gear (for settings)
        - 📁 Folder (for file operations)
        - 📧 Email (for email operations)
        - 🔔 Bell (for notifications)
        
        ## How It Works
        
        - **Buttons**: When clicked, they send an action to n8n with the button's ID
        - **Toggles**: Their state (on/off) is included with every message sent to n8n
        
        ## Action Buttons vs. Settings
        
        There are two ways to interact with toggles:
        
        1. **Action Buttons**: Visible buttons in the chat interface that you can click to toggle features on/off
        2. **Settings Panel**: Access by clicking the settings icon (⚙️) in the top-right corner
        
        Both methods control the same settings, so use whichever is more convenient for you.
        
        ## Built-in Toggles
        
        - **🧠 Reasoning Mode**: When enabled, the AI will show its reasoning process
        - **🛡️ Privacy Mode**: When enabled, your conversation won't be stored for training
        """
        
        # Create action buttons for the help message
        reasoning_status = "ON" if cl.user_session.get("reasoning_mode", False) else "OFF"
        privacy_status = "ON" if cl.user_session.get("privacy_mode", False) else "OFF"
        
        reasoning_action = cl.Action(
            name="toggle_reasoning",
            label=f"🧠 Reasoning Mode: {reasoning_status}",
            description="Toggle reasoning mode on/off",
            payload={}
        )
        
        privacy_action = cl.Action(
            name="toggle_privacy",
            label=f"🛡️ Privacy Mode: {privacy_status}",
            description="Toggle privacy mode on/off",
            payload={}
        )
        
        await cl.Message(
            content=help_text,
            actions=[reasoning_action, privacy_action]
        ).send()
        
    except Exception as e:
        error_message = f"Error showing widgets help: {str(e)}"
        print(error_message)
        logger.error(error_message)
        await cl.Message(content=f"Error showing widgets help: {str(e)}").send()

if __name__ == "__main__":
    # This block will be executed when running the script directly
    pass 