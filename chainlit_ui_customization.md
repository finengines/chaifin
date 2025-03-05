# Chainlit UI Customization Guide

This guide provides a comprehensive overview of UI customization options in Chainlit, focusing on interactive elements, status updates, progress indicators, and data routing capabilities.

## Table of Contents

1. [Status Updates & Progress Indicators](#status-updates--progress-indicators)
2. [Interactive UI Elements](#interactive-ui-elements)
3. [Custom Buttons & Toggles](#custom-buttons--toggles)
4. [Webhook Data & Backend Routing](#webhook-data--backend-routing)
5. [Theme Customization](#theme-customization)
6. [Custom Elements Implementation](#custom-elements-implementation)

## Status Updates & Progress Indicators

### TaskList

The `TaskList` element provides a powerful way to display progress and status updates for multi-step operations.

```python
import chainlit as cl

@cl.on_chat_start
async def main():
    # Create the TaskList
    task_list = cl.TaskList()
    task_list.status = "Running..."

    # Create a task and put it in the running state
    task1 = cl.Task(title="Processing data", status=cl.TaskStatus.RUNNING)
    await task_list.add_task(task1)
    
    # Create another task that is in the ready state
    task2 = cl.Task(title="Performing calculations")
    await task_list.add_task(task2)

    # Optional: link a message to each task to allow task navigation in the chat history
    message = await cl.Message(content="Started processing data").send()
    task1.forId = message.id

    # Update the task list in the interface
    await task_list.send()

    # Perform some action on your end
    await cl.sleep(1)

    # Update the task statuses
    task1.status = cl.TaskStatus.DONE
    task2.status = cl.TaskStatus.FAILED
    task_list.status = "Failed"
    await task_list.send()
```

### Loading Indicators

Chainlit provides built-in loading indicators for various operations:

1. **Running Loader**: When `cot` is set to `"hidden"`, a running loader is displayed under the last message during task execution.

```python
# In your config.toml
[ui]
cot = "hidden"  # Options: "hidden", "tool_call", "full"
```

2. **Custom Loading Messages**: You can create custom loading messages during long operations.

```python
import chainlit as cl

@cl.on_message
async def on_message(message: cl.Message):
    # Show a loading message
    msg = cl.Message(content="Processing your request...")
    await msg.send()
    
    # Perform long operation
    result = await some_long_operation()
    
    # Update the message with the result
    await msg.update(content=f"Result: {result}")
```

## Interactive UI Elements

### Chat Settings

Chat Settings provide a way to let users configure their chat experience with various input widgets.

```python
import chainlit as cl
from chainlit.input_widget import Select, Slider, Switch, Tags, TextInput

@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings([
        Select(
            id="Model",
            label="AI Model",
            values=["gpt-3.5-turbo", "gpt-4", "claude-3-sonnet"],
            initial_index=0
        ),
        Slider(
            id="Temperature",
            label="Temperature",
            initial=0.7,
            min=0,
            max=2,
            step=0.1
        ),
        Switch(
            id="Streaming",
            label="Stream Tokens",
            initial=True
        ),
        Tags(
            id="Topics",
            label="Topics of Interest",
            initial=["AI", "Programming"]
        ),
        TextInput(
            id="SystemPrompt",
            label="System Prompt",
            initial="You are a helpful assistant."
        )
    ]).send()
    
    # Access settings values
    model = settings["Model"]
    temperature = settings["Temperature"]
    streaming = settings["Streaming"]
    topics = settings["Topics"]
    system_prompt = settings["SystemPrompt"]
    
    # Store in user session for later use
    cl.user_session.set("settings", settings)
```

## Custom Buttons & Toggles

### Action Buttons

Action buttons allow users to trigger specific functions in your application.

```python
import chainlit as cl

@cl.action_callback("regenerate")
async def on_regenerate(action):
    # Get the message that the action is attached to
    message_id = action.for_id
    
    # Perform regeneration logic
    new_content = "This is the regenerated content"
    
    # Update the message
    await cl.Message(content=new_content, id=message_id).update()
    
    # Optionally remove the action button
    await action.remove()

@cl.on_message
async def on_message(message: cl.Message):
    # Create action buttons
    actions = [
        cl.Action(
            name="regenerate", 
            label="Regenerate", 
            icon="refresh-cw",  # Lucide icon name
            payload={"message_id": message.id}
        ),
        cl.Action(
            name="save", 
            label="Save", 
            icon="save",
            payload={"content": message.content}
        )
    ]
    
    # Send a message with the actions
    await cl.Message(content="Here's your response", actions=actions).send()
```

### Custom Header Buttons (v2.2.0+)

As of Chainlit v2.2.0, you can add custom buttons to the header.

```python
import chainlit as cl

@cl.on_chat_start
async def on_chat_start():
    # Add a custom button to the header
    await cl.header_button(
        name="settings",
        label="Settings",
        icon="settings",
        payload={"action": "open_settings"}
    )

@cl.action_callback("settings")
async def on_settings_click(action):
    # Handle the settings button click
    await cl.Message(content="Settings button clicked").send()
```

## Webhook Data & Backend Routing

### Custom Headers Authentication

Chainlit supports authentication based on custom headers, which can be useful for webhook integration.

```python
# In your config.toml
[auth]
type = "header"
secret = "your-secret-key"  # Used to sign the JWT token

[auth.header]
user_id = "X-User-Id"  # The header containing the user ID
```

### Handling Webhook Data

You can use FastAPI alongside Chainlit to handle webhook data and route it to your Chainlit application.

```python
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import APIKeyHeader
import chainlit as cl
from chainlit.server import app as chainlit_app

app = FastAPI()

# Mount Chainlit as a sub-application
app.mount("/chat", chainlit_app)

# API key security
API_KEY_NAME = "X-API-Key"
API_KEY = "your-secret-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME)

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

@app.post("/webhook", dependencies=[Depends(verify_api_key)])
async def webhook(request: Request):
    data = await request.json()
    
    # Process webhook data
    user_id = data.get("user_id")
    message = data.get("message")
    
    # You can store this data to be used by Chainlit
    # or trigger actions in your Chainlit app
    
    return {"status": "success"}
```

### Window Messaging

Chainlit provides a window messaging API that allows communication between the parent window and the Chainlit iframe, useful for integrating with external systems.

```javascript
// In your parent application
window.addEventListener("message", (event) => {
  if (event.data.type === "chainlit:message") {
    console.log("Message from Chainlit:", event.data.message);
  }
});

// Send message to Chainlit
const chainlitIframe = document.getElementById("chainlit-iframe");
chainlitIframe.contentWindow.postMessage(
  {
    type: "chainlit:message",
    message: { action: "process_data", data: { key: "value" } }
  },
  "https://your-chainlit-app.com"
);
```

```python
# In your Chainlit app
import chainlit as cl
import json

@cl.on_chat_start
async def on_chat_start():
    # Set up a listener for window messages
    cl.user_session.set("listening_for_messages", True)

@cl.on_message
async def on_message(message: cl.Message):
    if message.content.startswith("/window:"):
        # This is a special message from the window messaging API
        try:
            data = json.loads(message.content[8:])
            action = data.get("action")
            
            if action == "process_data":
                # Process the data
                result = process_data(data.get("data"))
                await cl.Message(content=f"Processed data: {result}").send()
        except json.JSONDecodeError:
            await cl.Message(content="Invalid JSON data").send()
```

## Theme Customization

### Theme Configuration

Chainlit allows extensive theme customization through a `theme.json` file in the `/public` directory.

```json
{
  "light": {
    "colors": {
      "primary": "#0D6EFD",
      "secondary": "#6C757D",
      "success": "#198754",
      "danger": "#DC3545",
      "warning": "#FFC107",
      "info": "#0DCAF0",
      "background": "#FFFFFF",
      "paper": "#F8F9FA"
    },
    "shape": {
      "borderRadius": 8
    },
    "typography": {
      "fontFamily": "Inter, sans-serif"
    }
  },
  "dark": {
    "colors": {
      "primary": "#0D6EFD",
      "secondary": "#6C757D",
      "success": "#198754",
      "danger": "#DC3545",
      "warning": "#FFC107",
      "info": "#0DCAF0",
      "background": "#212529",
      "paper": "#343A40"
    },
    "shape": {
      "borderRadius": 8
    },
    "typography": {
      "fontFamily": "Inter, sans-serif"
    }
  }
}
```

### Custom CSS

You can add custom CSS to further customize the appearance of your Chainlit application.

1. Create a CSS file in the `/public` directory (e.g., `custom.css`).
2. Configure Chainlit to use this CSS file in `.chainlit/config.toml`:

```toml
[UI]
custom_css = "/custom.css"
```

Example CSS for customizing the appearance of status indicators:

```css
/* Custom styling for TaskList */
.cl-tasklist {
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.cl-task-running {
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

/* Custom styling for action buttons */
.cl-action-button {
  transition: transform 0.2s;
}

.cl-action-button:hover {
  transform: scale(1.05);
}
```

### Custom JavaScript

For advanced customization, you can inject custom JavaScript into your Chainlit application.

1. Create a JavaScript file in the `/public` directory (e.g., `custom.js`).
2. Configure Chainlit to use this JavaScript file in `.chainlit/config.toml`:

```toml
[UI]
custom_js = "/custom.js"
```

Example JavaScript for enhancing UI interactions:

```javascript
// Add custom event listeners
document.addEventListener('DOMContentLoaded', () => {
  // Custom keyboard shortcuts
  document.addEventListener('keydown', (e) => {
    // Alt+R to trigger regenerate action
    if (e.altKey && e.key === 'r') {
      const regenerateButtons = document.querySelectorAll('[data-action="regenerate"]');
      if (regenerateButtons.length > 0) {
        regenerateButtons[regenerateButtons.length - 1].click();
      }
    }
  });
  
  // Enhance TaskList with additional functionality
  const enhanceTaskList = () => {
    const taskLists = document.querySelectorAll('.cl-tasklist');
    taskLists.forEach(taskList => {
      // Add custom behavior
    });
  };
  
  // Run enhancement when content changes
  const observer = new MutationObserver(enhanceTaskList);
  observer.observe(document.body, { childList: true, subtree: true });
});
```

## Custom Elements Implementation

Chainlit allows you to create custom UI elements using JSX. This is a powerful feature that enables you to build rich, interactive components for your application.

### Creating Custom Elements

1. **Create a JSX file**: Place your JSX file in the `public/elements/` directory. The filename should match the name you'll use in your Python code.

```jsx
// public/elements/StatusUpdate.jsx
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"

export default function StatusUpdate() {
  // Get the type from props to determine styling
  const type = props.type || "info";
  const icon = props.icon || "info";
  const title = props.title || "";
  const message = props.message || "";
  const progress = props.progress || null;
  
  // Define class names based on type
  const getTypeClass = () => {
    switch(type) {
      case "email": return "status-email";
      case "calendar": return "status-calendar";
      case "web-search": return "status-web-search";
      default: return "status-info";
    }
  };
  
  return (
    <Card className={`status-update ${getTypeClass()} border-0 my-4`}>
      <CardContent className="p-4 flex items-start">
        <div className="status-update-icon mr-4 mt-1">
          <i data-lucide={icon}></i>
        </div>
        <div className="flex-1">
          <h4 className="text-base font-semibold mb-1">{title}</h4>
          <p className="text-sm opacity-90">{message}</p>
          {progress !== null && (
            <div className="mt-3">
              <Progress value={progress} className="h-2" />
            </div>
          )}
        </div>
        <Badge variant="outline" className="ml-2 capitalize">
          {type.replace('-', ' ')}
        </Badge>
      </CardContent>
    </Card>
  );
}
```

2. **Use the custom element in your Python code**:

```python
import chainlit as cl

async def email_status(title: str, message: str, icon: str = "mail") -> cl.Message:
    """
    Display an email agent status update.
    
    Args:
        title: The title of the status update
        message: The message content
        icon: Lucide icon name (default: "mail")
        
    Returns:
        The sent message object
    """
    element = cl.CustomElement(
        name="StatusUpdate",
        props={
            "type": "email",
            "icon": icon,
            "title": title,
            "message": message
        }
    )
    msg = cl.Message(content="", elements=[element])
    return await msg.send()
```

### Important Notes for Custom Elements

1. **Props are globally injected**: In your JSX file, props are globally injected, not passed as function arguments. Never define your component with props as a parameter:

```jsx
// CORRECT
export default function MyComponent() {
  const myProp = props.myProp || "default";
  // ...
}

// INCORRECT - Don't do this
export default function MyComponent(props) {
  const myProp = props.myProp || "default";
  // ...
}
```

2. **Use Shadcn UI components**: Chainlit provides access to Shadcn UI components, which you can import and use in your custom elements:

```jsx
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
```

3. **Use Tailwind for styling**: Chainlit supports Tailwind CSS for styling your custom elements:

```jsx
<div className="flex items-center justify-between p-4 bg-primary-100 rounded-md">
  {/* Component content */}
</div>
```

4. **Update element props**: You can update a custom element's props from your Python code:

```python
import chainlit as cl

@cl.on_chat_start
async def start():
    element = cl.CustomElement(name="StatusUpdate", props={"type": "info", "title": "Initial Title"})
    cl.user_session.set("status_element", element)
    await cl.Message(content="", elements=[element]).send()

@cl.on_message
async def on_message(message: cl.Message):
    element = cl.user_session.get("status_element")
    element.props["title"] = "Updated Title"
    element.props["progress"] = 75
    await element.update()
```

### Styling Custom Elements

You can style your custom elements using a combination of Tailwind classes and custom CSS:

1. **Tailwind classes**: Apply Tailwind classes directly in your JSX:

```jsx
<div className="bg-blue-100 p-4 rounded-lg shadow-md hover:shadow-lg transition-all">
  {/* Content */}
</div>
```

2. **Custom CSS**: Define custom styles in your `custom.css` file:

```css
.status-update {
  border-radius: 10px;
  padding: 14px 18px;
  margin: 12px 0;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  transition: all 0.3s ease;
}

.status-email {
  background: linear-gradient(135deg, rgba(79, 195, 247, 0.2), rgba(79, 195, 247, 0.05));
  border-left: 5px solid #4fc3f7;
}
```

## Conclusion

Chainlit offers a rich set of UI customization options that allow you to create interactive, responsive, and visually appealing conversational AI applications. By leveraging status updates, progress indicators, interactive elements, and custom styling, you can build applications that provide excellent user experiences while maintaining robust backend functionality.

For more information, refer to the [official Chainlit documentation](https://docs.chainlit.io/). 