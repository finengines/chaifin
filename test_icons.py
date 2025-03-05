import chainlit as cl
from status_updates import (
    system_alert,
    important_alert,
    notification_alert,
    email_status,
    database_status,
    success_status,
    warning_status,
    error_status,
    info_status,
    show_toast
)

@cl.on_chat_start
async def start():
    """Initialize the chat session and demonstrate styling."""
    # Welcome message
    await cl.Message(
        content="# Icon Styling Test\nThis demo showcases the updated styling for status updates, alerts, and toast notifications with icons."
    ).send()
    
    # Show a toast notification on startup
    await show_toast("Welcome to the styling test!", "success", 5000)
    
    # Show status updates with icons
    await email_status("Email Sent", "Your message has been sent to john@example.com")
    await database_status("Database Updated", "Added 25 new records to the database")
    await success_status("Task Complete", "Your task has been completed successfully")
    await warning_status("Warning", "Your account is approaching its usage limit")
    await error_status("Error", "Failed to connect to the database")
    await info_status("Information", "The system will be updated tomorrow")
    
    # Show alerts with icons
    await important_alert("Important Notice", "Your subscription will expire in 3 days")
    await notification_alert("New Message", "You have 5 unread messages")
    await system_alert("System Update", "The system will be undergoing maintenance in 30 minutes")

@cl.on_message
async def on_message(message: cl.Message):
    """Handle user messages and demonstrate toast notifications."""
    # Echo the user's message with a styled response
    await cl.Message(
        content=f"You said: {message.content}\n\nThis is a styled response to demonstrate the new UI."
    ).send()
    
    # Show a toast notification for every message
    await show_toast(f"Processing: {message.content[:20]}...", "info", 3000)
    
    # Show a random status update based on the message content
    if "email" in message.content.lower():
        await email_status("Email Action", "Processing your email request")
        await show_toast("Email processed", "success")
    elif "database" in message.content.lower():
        await database_status("Database Action", "Querying the database")
        await show_toast("Database query complete", "success")
    elif "error" in message.content.lower():
        await error_status("Error Simulation", "This is a simulated error message")
        await show_toast("Error encountered", "error")
    elif "warning" in message.content.lower():
        await warning_status("Warning Simulation", "This is a simulated warning message")
        await show_toast("Warning issued", "warning")
    elif "success" in message.content.lower():
        await success_status("Success Simulation", "This is a simulated success message")
        await show_toast("Operation successful", "success")
    elif "alert" in message.content.lower():
        await system_alert("Alert Simulation", "This is a simulated system alert")
        await show_toast("Alert triggered", "info")
    elif "toast" in message.content.lower():
        # Test all toast types
        await show_toast("This is an info toast", "info", 3000)
        await cl.sleep(1)
        await show_toast("This is a success toast", "success", 3000)
        await cl.sleep(1)
        await show_toast("This is a warning toast", "warning", 3000)
        await cl.sleep(1)
        await show_toast("This is an error toast", "error", 3000)
    else:
        await info_status("Info", "Type keywords like 'email', 'database', 'error', 'warning', 'success', 'alert', or 'toast' to see different status updates and notifications") 