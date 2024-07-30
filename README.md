# Harness AI Integration

This project aims to integrate AI capabilities into the Harness platform. The main components include an AI controller, AI engine, and tool executor to handle user requests and execute commands via the CLI.

## Project Setup

### Prerequisites

- Python 3.12
- pip

### Installation

1. Clone the repository:

```bash
$ git clone <repository-url>
$ cd harness-ai-integration
```

2. Set up a Python virtual environment:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

3. Install the required Python modules:

```bash
$ pip install /path/to/py-gptscript-main
$ pip install fastapi uvicorn
```

4. Set the `GPTSCRIPT_API_KEY` environment variable:

```bash
$ export GPTSCRIPT_API_KEY=<your-gptscript-api-key>
```

### Directory Structure

```
.
├── ai_controller
│   └── ai_controller.py
├── ai_engine
│   └── ai_engine.py
├── context.gpt
├── main_app
│   └── main.py
├── tests
│   ├── test_ai_controller.py
│   ├── test_ai_engine.py
│   └── test_tool_executor.py
├── tool_executor
│   └── tool_executor.py
└── venv
```

## Running the Application

To run the FastAPI server:

```bash
$ python main_app/main.py
```

## Using the Chat Endpoint

To interact with the chat endpoint, send a POST request to `http://localhost:8000/chat` with the following CURL request:

curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d '{"user_id": "user123", "input": "Example Prompt"}'

## Testing

To run the tests:

```bash
$ python -m unittest discover -s tests
```

## References

- [Harness Developer Documentation](https://docs.harness.io/)
- [GPTScript Python Module](https://github.com/py-gptscript)
- [GPTScript Documentation](https://docs.gptscript.io/)

## Example Usage

### Creating a GPTScript Instance

```python
from gptscript.gptscript import GPTScript

gptscript = GPTScript(api_key="your-api-key")
```

### Defining and Running a Tool

```python
from gptscript.tool import ToolDef

tool = ToolDef(
    tools=["sys.write"],
    jsonResponse=True,
    cache=False,
    instructions="""
    Create three short graphic artist descriptions and their muses.
    These should be descriptive and explain their point of view.
    Also come up with a made-up name, they each should be from different
    backgrounds and approach art differently.
    the JSON response format should be:
    {
        artists: [{
            name: "name"
            description: "description"
        }]
    }
    """
)

run = gptscript.evaluate(tool)
print(await run.text())
gptscript.close()
```

### Using Multiple Tools

```python
from gptscript.gptscript import GPTScript
from gptscript.tool import ToolDef

gptscript = GPTScript()
tools = [
    ToolDef(tools=["echo"], instructions="echo hello times"),
    ToolDef(
        name="echo",
        tools=["sys.exec"],
        description="Echo's the input",
        args={"input": "the string input to echo"},
        instructions="""
        #!/bin/bash
        echo ${input}
        """,
    ),
]
run = gptscript.evaluate(tools)
print(await run.text())
gptscript.close()
```
