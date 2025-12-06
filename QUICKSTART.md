# Quick Start Guide

This guide will help you get started with the TuneIt AI Agent quickly.

## Prerequisites

Before starting, ensure you have:
1. Python 3.11 or higher installed
2. An MCP server running locally (default: http://localhost:8000)
3. Git installed (for cloning the repository)

## Step-by-Step Setup

### 1. Clone and Navigate

```bash
git clone https://github.com/mcuellar/tuneit-ai-agent.git
cd tuneit-ai-agent
```

### 2. Run the Setup Script (Recommended)

```bash
bash setup.sh
```

This will:
- Check Python version
- Create a virtual environment
- Install all dependencies
- Create `.env` file from template
- Create the watch directory

### 3. Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Create watch directory
mkdir -p job_descriptions
```

### 4. Configure Environment

Edit `.env` to match your setup:

```bash
# Your MCP server URL
MCP_SERVER_URL=http://localhost:8000

# Directory to watch (can be relative or absolute)
WATCH_DIRECTORY=./job_descriptions

# Allowed file extensions
ALLOWED_EXTENSIONS=.txt,.md,.pdf
```

### 5. Start the Agent

Make sure your MCP server is running, then:

```bash
# Activate virtual environment (if not already activated)
source venv/bin/activate

# Run the agent
python run.py
```

You should see output like:
```
============================================================
TuneIt AI Agent - Background Runner
============================================================
... initialization messages ...
============================================================
TuneIt AI Agent is now running!
Watching for new job descriptions in: ./job_descriptions
Press Ctrl+C to stop
============================================================
```

### 6. Add a Job Description

While the agent is running, add a job description file to the watch directory:

```bash
# In another terminal
cat > job_descriptions/software_engineer.txt << 'EOF'
Position: Senior Software Engineer
Company: Tech Corp

Requirements:
- 5+ years of Python experience
- Experience with cloud platforms (AWS, Azure, GCP)
- Strong understanding of microservices architecture
- Experience with CI/CD pipelines

Responsibilities:
- Design and implement scalable backend services
- Mentor junior developers
- Collaborate with product team on feature development
EOF
```

The agent will automatically:
1. Detect the new file
2. Process it through the workflow
3. Call the MCP server tools
4. Generate and save the tailored resume
5. Save the formatted job description

### 7. Monitor Logs

Check the logs to see the agent's activity:

```bash
# View real-time logs
tail -f tuneit_agent.log

# Or check the console output where the agent is running
```

## Testing Without MCP Server

If you don't have an MCP server running yet, you can still test the file watching functionality:

```bash
# The agent will start but fail when calling MCP tools
# This is expected and helps verify the file watching works
python run.py
```

You'll see errors when it tries to connect to the MCP server, but you'll also see that files are being detected.

## Stopping the Agent

Press `Ctrl+C` in the terminal where the agent is running. The agent will gracefully shut down.

## Troubleshooting

### Virtual Environment Not Activating

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### Permission Denied on setup.sh

```bash
chmod +x setup.sh
./setup.sh
```

### MCP Server Connection Failed

1. Verify MCP server is running:
   ```bash
   curl http://localhost:8000
   ```

2. Check your `.env` file has the correct `MCP_SERVER_URL`

3. Review the agent logs for detailed error messages

### Files Not Being Detected

1. Verify you're adding files to the correct directory (check `WATCH_DIRECTORY` in `.env`)
2. Check file extensions match `ALLOWED_EXTENSIONS`
3. Review logs for any errors

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Review the code in `agent.py` to understand the workflow
- Customize the allowed file extensions in `.env`
- Set up your MCP server with the required tools

## Example MCP Server Tools

Your MCP server needs to implement these endpoints:

1. `POST /tools/format_job_description`
2. `POST /tools/generate_tailored_resume`
3. `POST /tools/save_tailored_resume`
4. `POST /tools/save_job_description`

See the README for detailed API specifications.
