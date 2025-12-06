# TuneIt AI Agent

An intelligent LangGraph-based AI agent that automates the process of tailoring resumes based on job descriptions using MCP (Model Context Protocol) Server tools.

## Overview

The TuneIt AI Agent continuously monitors a specified directory for new job description files and automatically:

1. **Formats** the job description using the `format_job_description` MCP tool
2. **Generates** a tailored resume using the `generate_tailored_resume` MCP tool  
3. **Saves** the tailored resume using the `save_tailored_resume` MCP tool
4. **Saves** the formatted job description using the `save_job_description` MCP tool

## Features

- 🤖 **LangGraph Workflow**: Structured AI agent with a clear state graph
- 📁 **File Watching**: Automatic detection of new job description files
- 🔌 **MCP Integration**: Seamless integration with MCP server over HTTP
- 🔄 **Background Runner**: Continuous processing service
- 📝 **Comprehensive Logging**: Detailed logs for monitoring and debugging
- ⚙️ **Configurable**: Environment-based configuration

## Architecture

The agent is built using LangGraph and consists of several components:

```
┌─────────────────────────────────────────────────┐
│          Background Runner (run.py)              │
│  - Manages lifecycle of agent and file watcher  │
└────────────────┬────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
┌───────▼──────┐   ┌──────▼────────┐
│ File Watcher │   │  TuneIt Agent │
│              │   │  (LangGraph)  │
│ - Monitors   │──▶│               │
│   directory  │   │ - State graph │
│ - Triggers   │   │ - MCP client  │
│   agent      │   │ - Workflow    │
└──────────────┘   └───────┬───────┘
                           │
                    ┌──────▼──────┐
                    │  MCP Server │
                    │  (HTTP API) │
                    └─────────────┘
```

### Workflow

```
Start
  │
  ▼
Read Job Description
  │
  ▼
Format Job Description (MCP)
  │
  ▼
Generate Tailored Resume (MCP)
  │
  ▼
Save Outputs (MCP x2)
  │
  ▼
End
```

## Prerequisites

- Python 3.11 or higher
- MCP Server running locally (default: http://localhost:8000)
- The MCP server must expose the following tools:
  - `format_job_description`
  - `generate_tailored_resume`
  - `save_tailored_resume`
  - `save_job_description`

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/mcuellar/tuneit-ai-agent.git
cd tuneit-ai-agent
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
```

Edit `.env` to configure your settings:

```bash
# MCP Server URL
MCP_SERVER_URL=http://localhost:8000

# Directory to watch for job descriptions
WATCH_DIRECTORY=./job_descriptions

# Allowed file extensions
ALLOWED_EXTENSIONS=.txt,.md,.pdf
```

## Usage

### Running the Background Service

Start the background runner to continuously monitor for new job descriptions:

```bash
python run.py
```

The agent will:
- Create the watch directory if it doesn't exist
- Monitor for new files with allowed extensions (.txt, .md, .pdf)
- Automatically process each new job description file
- Log all activities to console and `tuneit_agent.log`

### Processing a Job Description

Simply drop a job description file into the watched directory:

```bash
# Example
echo "Software Engineer position at XYZ Corp..." > job_descriptions/software_engineer.txt
```

The agent will automatically:
1. Detect the new file
2. Process it through the complete workflow
3. Generate and save the tailored resume
4. Save the formatted job description

### Stopping the Service

Press `Ctrl+C` to gracefully stop the background service.

## Project Structure

```
tuneit-ai-agent/
├── agent.py              # Core LangGraph agent implementation
├── file_watcher.py       # File monitoring using watchdog
├── run.py               # Background runner / main entry point
├── requirements.txt      # Python dependencies
├── .env.example         # Environment configuration template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## MCP Server Integration

The agent connects to an MCP server over HTTP. The MCP server must implement the following endpoints:

### Expected Tool Endpoints

1. **POST** `/tools/format_job_description`
   - Input: `{"arguments": {"job_description": "..."}}`
   - Output: `{"formatted_job_description": "..."}`

2. **POST** `/tools/generate_tailored_resume`
   - Input: `{"arguments": {"job_description": "..."}}`
   - Output: `{"tailored_resume": "..."}`

3. **POST** `/tools/save_tailored_resume`
   - Input: `{"arguments": {"resume_content": "...", "job_title": "..."}}`
   - Output: `{"status": "success"}`

4. **POST** `/tools/save_job_description`
   - Input: `{"arguments": {"job_description": "...", "job_title": "..."}}`
   - Output: `{"status": "success"}`

## Development

### Running in Development Mode

```bash
# Activate virtual environment
source venv/bin/activate

# Run with debug logging
python run.py
```

### Testing Individual Components

```python
# Test the agent
from agent import TuneItAgent

agent = TuneItAgent("http://localhost:8000")
result = agent.process_job_description("path/to/job_description.txt")
print(result)
agent.close()
```

```python
# Test the MCP client
from agent import MCPClient

client = MCPClient("http://localhost:8000")
result = client.format_job_description("Sample job description")
print(result)
client.close()
```

## Logging

Logs are written to:
- **Console**: Real-time monitoring
- **File**: `tuneit_agent.log` for persistent logs

Log levels:
- `INFO`: Normal operations
- `ERROR`: Errors and failures
- `DEBUG`: Detailed debugging information

## Error Handling

The agent includes comprehensive error handling:
- Failed file processing is logged and can be retried
- MCP tool failures are caught and logged
- Graceful shutdown on SIGINT/SIGTERM
- All errors include stack traces in logs

## Troubleshooting

### Agent can't connect to MCP server

- Verify MCP server is running: `curl http://localhost:8000`
- Check `MCP_SERVER_URL` in `.env`
- Review logs for connection errors

### Files not being processed

- Check file extensions match `ALLOWED_EXTENSIONS`
- Verify files are in the correct `WATCH_DIRECTORY`
- Check file permissions
- Review logs for processing errors

### MCP tool calls failing

- Verify MCP server implements all required tools
- Check MCP server logs for errors
- Validate tool input/output formats match expectations

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.
