import chainlit as cl
from chainlit.input_widget import Select, Slider, Switch, Tags, TextInput
import asyncio
from typing import Dict, Any

# Default settings
DEFAULT_SETTINGS = {
    "Model": "gpt-3.5-turbo",
    "Temperature": 0.7,
    "MaxTokens": 1000,
    "Streaming": True,
    "Topics": ["General", "Coding"],
    "SystemPrompt": "You are a helpful assistant."
}

# Simulated response generation
async def generate_response(message: str, settings: Dict[str, Any]) -> str:
    # In a real app, this would call an actual LLM API
    model = settings.get("Model", DEFAULT_SETTINGS["Model"])
    temperature = settings.get("Temperature", DEFAULT_SETTINGS["Temperature"])
    streaming = settings.get("Streaming", DEFAULT_SETTINGS["Streaming"])
    system_prompt = settings.get("SystemPrompt", DEFAULT_SETTINGS["SystemPrompt"])
    
    # Create a response message
    response = cl.Message(content="")
    
    # Simulate thinking time
    await asyncio.sleep(0.5)
    
    # Prepare the response text
    full_response = f"""
I'm responding as if I were the {model} model with:
- Temperature: {temperature}
- System Prompt: "{system_prompt}"

Your message: "{message}"

This is a simulated response to demonstrate Chat Settings in Chainlit. In a real application, this would be generated by the selected AI model.

The settings you've configured are:
```json
{settings}
```
"""
    
    # If streaming is enabled, stream the response token by token
    if streaming:
        for token in full_response.split():
            await response.stream_token(token + " ")
            await asyncio.sleep(0.05)  # Simulate token generation time
        
        await response.send()
    else:
        # If not streaming, send the full response at once
        response.content = full_response
        await response.send()

@cl.on_settings_update
async def on_settings_update(settings: Dict[str, Any]):
    # This function is called when the user updates the settings
    await cl.Message(
        content=f"Settings updated:\n```json\n{settings}\n```"
    ).send()

@cl.on_chat_start
async def on_chat_start():
    # Define the chat settings with various input widgets
    settings = await cl.ChatSettings([
        # Model selection dropdown
        Select(
            id="Model",
            label="AI Model",
            values=[
                "gpt-3.5-turbo", 
                "gpt-4", 
                "claude-3-sonnet",
                "claude-3-opus",
                "gemini-pro",
                "llama-3-70b"
            ],
            initial_index=0
        ),
        
        # Temperature slider
        Slider(
            id="Temperature",
            label="Temperature",
            initial=DEFAULT_SETTINGS["Temperature"],
            min=0,
            max=2,
            step=0.1,
            tooltip="Controls randomness: Lower values are more deterministic, higher values are more creative."
        ),
        
        # Max tokens slider
        Slider(
            id="MaxTokens",
            label="Max Tokens",
            initial=DEFAULT_SETTINGS["MaxTokens"],
            min=100,
            max=4000,
            step=100,
            tooltip="Maximum number of tokens to generate."
        ),
        
        # Streaming toggle
        Switch(
            id="Streaming",
            label="Stream Tokens",
            initial=DEFAULT_SETTINGS["Streaming"],
            tooltip="Enable to see tokens appear in real-time."
        ),
        
        # Topics tags
        Tags(
            id="Topics",
            label="Topics of Interest",
            initial=DEFAULT_SETTINGS["Topics"],
            tooltip="Select topics you're interested in discussing."
        ),
        
        # System prompt text input
        TextInput(
            id="SystemPrompt",
            label="System Prompt",
            initial=DEFAULT_SETTINGS["SystemPrompt"],
            tooltip="Instructions for the AI model."
        )
    ]).send()
    
    # Store settings in the user session
    cl.user_session.set("settings", settings)
    
    # Send a welcome message
    await cl.Message(
        content=f"""
# Chat Settings Demo

This demo shows how to use Chat Settings in Chainlit with various input widgets.

## Current Settings

- **Model**: {settings.get("Model", DEFAULT_SETTINGS["Model"])}
- **Temperature**: {settings.get("Temperature", DEFAULT_SETTINGS["Temperature"])}
- **Max Tokens**: {settings.get("MaxTokens", DEFAULT_SETTINGS["MaxTokens"])}
- **Streaming**: {settings.get("Streaming", DEFAULT_SETTINGS["Streaming"])}
- **Topics**: {", ".join(settings.get("Topics", DEFAULT_SETTINGS["Topics"]))}
- **System Prompt**: "{settings.get("SystemPrompt", DEFAULT_SETTINGS["SystemPrompt"])}"

Click the ⚙️ icon in the chat input bar to adjust these settings.
"""
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    # Get the current settings from the user session
    settings = cl.user_session.get("settings", DEFAULT_SETTINGS)
    
    # Generate a response based on the settings
    await generate_response(message.content, settings)
    
    # Add action buttons to the message
    actions = [
        cl.Action(
            name="show_settings", 
            label="Show Current Settings", 
            icon="settings"
        ),
        cl.Action(
            name="reset_settings", 
            label="Reset Settings", 
            icon="refresh-cw"
        )
    ]
    
    await cl.Message(
        content="You can view or reset your current settings:",
        actions=actions
    ).send()

@cl.action_callback("show_settings")
async def on_show_settings(action):
    # Get the current settings from the user session
    settings = cl.user_session.get("settings", DEFAULT_SETTINGS)
    
    # Format the settings as markdown
    settings_md = "## Current Settings\n\n"
    for key, value in settings.items():
        settings_md += f"- **{key}**: {value}\n"
    
    await cl.Message(content=settings_md).send()

@cl.action_callback("reset_settings")
async def on_reset_settings(action):
    # Reset to default settings
    cl.user_session.set("settings", DEFAULT_SETTINGS)
    
    # Update the chat settings in the UI
    await cl.ChatSettings([
        Select(
            id="Model",
            label="AI Model",
            values=[
                "gpt-3.5-turbo", 
                "gpt-4", 
                "claude-3-sonnet",
                "claude-3-opus",
                "gemini-pro",
                "llama-3-70b"
            ],
            initial_index=0
        ),
        Slider(
            id="Temperature",
            label="Temperature",
            initial=DEFAULT_SETTINGS["Temperature"],
            min=0,
            max=2,
            step=0.1
        ),
        Slider(
            id="MaxTokens",
            label="Max Tokens",
            initial=DEFAULT_SETTINGS["MaxTokens"],
            min=100,
            max=4000,
            step=100
        ),
        Switch(
            id="Streaming",
            label="Stream Tokens",
            initial=DEFAULT_SETTINGS["Streaming"]
        ),
        Tags(
            id="Topics",
            label="Topics of Interest",
            initial=DEFAULT_SETTINGS["Topics"]
        ),
        TextInput(
            id="SystemPrompt",
            label="System Prompt",
            initial=DEFAULT_SETTINGS["SystemPrompt"]
        )
    ]).send()
    
    await cl.Message(content="Settings have been reset to defaults.").send()

if __name__ == "__main__":
    # This file can be run directly with: chainlit run example_chat_settings.py
    pass 