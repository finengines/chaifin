import chainlit as cl
from status_updates import show_toast
import asyncio

@cl.on_chat_start
async def start():
    """Initialize the chat session and demonstrate toast notifications."""
    # Welcome message
    await cl.Message(
        content="# Toast Notification Test\nThis demo showcases the updated styling for toast notifications in Chainlit."
    ).send()
    
    # Show a welcome toast
    await show_toast("Welcome to the Toast Test!", "success", 5000)
    
    # Wait a bit and show different types of toasts
    await asyncio.sleep(1)
    await show_toast("This is an info toast", "info", 5000)
    
    await asyncio.sleep(1)
    await show_toast("This is a success toast", "success", 5000)
    
    await asyncio.sleep(1)
    await show_toast("This is a warning toast", "warning", 5000)
    
    await asyncio.sleep(1)
    await show_toast("This is an error toast", "error", 5000)
    
    # Final instructions
    await cl.Message(
        content="Type 'toast' to see more toast notifications, or specify a type like 'info toast', 'success toast', 'warning toast', or 'error toast'."
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    """Handle user messages and demonstrate toast notifications."""
    # Echo the user's message
    await cl.Message(
        content=f"You said: {message.content}"
    ).send()
    
    # Show toast notifications based on the message content
    content = message.content.lower()
    
    if "toast" in content:
        if "info" in content:
            await show_toast("This is an information toast notification", "info", 5000)
        elif "success" in content:
            await show_toast("This is a success toast notification", "success", 5000)
        elif "warning" in content:
            await show_toast("This is a warning toast notification", "warning", 5000)
        elif "error" in content:
            await show_toast("This is an error toast notification", "error", 5000)
        else:
            # Show all toast types in sequence
            await show_toast("This is an information toast", "info", 5000)
            await asyncio.sleep(1)
            await show_toast("This is a success toast", "success", 5000)
            await asyncio.sleep(1)
            await show_toast("This is a warning toast", "warning", 5000)
            await asyncio.sleep(1)
            await show_toast("This is an error toast", "error", 5000)
    else:
        await show_toast(f"Processing: {message.content[:20]}...", "info", 3000) 