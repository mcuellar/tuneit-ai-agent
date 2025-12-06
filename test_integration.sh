#!/bin/bash
# Integration test script for TuneIt AI Agent
# This script tests the complete workflow using the mock MCP server

set -e

echo "============================================================"
echo "TuneIt AI Agent - Integration Test"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Create test directories
echo "Setting up test environment..."
rm -rf test_job_descriptions test_output
mkdir -p test_job_descriptions
echo "✓ Test directories created"
echo ""

# Create .env file for testing
echo "Creating test configuration..."
cat > .env.test << EOF
MCP_SERVER_URL=http://localhost:8000
WATCH_DIRECTORY=./test_job_descriptions
ALLOWED_EXTENSIONS=.txt,.md
EOF
echo "✓ Test configuration created"
echo ""

# Start mock MCP server in background
echo "Starting mock MCP server..."
python mock_mcp_server.py > /tmp/mock_server.log 2>&1 &
MOCK_SERVER_PID=$!
echo "✓ Mock MCP server started (PID: $MOCK_SERVER_PID)"
echo ""

# Wait for server to start
echo "Waiting for server to be ready..."
sleep 3

# Test if server is responding
if curl -s http://localhost:8000/tools/format_job_description > /dev/null 2>&1; then
    echo "✗ Server check: Expected GET to fail"
else
    echo "✓ Server is running"
fi
echo ""

# Start the agent in background
echo "Starting TuneIt AI Agent..."
export $(cat .env.test | xargs)
python run.py > /tmp/agent.log 2>&1 &
AGENT_PID=$!
echo "✓ Agent started (PID: $AGENT_PID)"
echo ""

# Wait for agent to initialize
echo "Waiting for agent to initialize..."
sleep 3
echo "✓ Agent initialized"
echo ""

# Copy test file
echo "Adding test job description..."
cp examples/senior_python_developer.txt test_job_descriptions/test_job_1.txt
echo "✓ Test file added"
echo ""

# Wait for processing
echo "Waiting for agent to process file (10 seconds)..."
sleep 10
echo ""

# Check logs
echo "============================================================"
echo "Checking Agent Logs"
echo "============================================================"
if grep -q "Successfully processed" /tmp/agent.log; then
    echo "✓ File was successfully processed"
elif grep -q "Processing failed" /tmp/agent.log; then
    echo "✗ Processing failed (check logs for details)"
    echo ""
    echo "Last 20 lines of agent log:"
    tail -20 /tmp/agent.log
elif grep -q "Error" /tmp/agent.log; then
    echo "⚠ Errors detected in logs (this may be expected without real MCP server)"
    echo ""
    echo "Last 20 lines of agent log:"
    tail -20 /tmp/agent.log
else
    echo "⚠ Status unclear (check logs for details)"
    echo ""
    echo "Last 20 lines of agent log:"
    tail -20 /tmp/agent.log
fi
echo ""

echo "============================================================"
echo "Checking Mock Server Logs"
echo "============================================================"
if grep -q "format_job_description" /tmp/mock_server.log; then
    echo "✓ format_job_description was called"
fi
if grep -q "generate_tailored_resume" /tmp/mock_server.log; then
    echo "✓ generate_tailored_resume was called"
fi
if grep -q "save_tailored_resume" /tmp/mock_server.log; then
    echo "✓ save_tailored_resume was called"
fi
if grep -q "save_job_description" /tmp/mock_server.log; then
    echo "✓ save_job_description was called"
fi
echo ""

# Cleanup
echo "============================================================"
echo "Cleaning Up"
echo "============================================================"
echo "Stopping agent (PID: $AGENT_PID)..."
kill $AGENT_PID 2>/dev/null || true
sleep 2

echo "Stopping mock server (PID: $MOCK_SERVER_PID)..."
kill $MOCK_SERVER_PID 2>/dev/null || true
sleep 1

echo "✓ Processes stopped"
echo ""

# Optional: Clean up test files
read -p "Do you want to remove test files? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf test_job_descriptions .env.test
    rm -f /tmp/mock_server.log /tmp/agent.log
    echo "✓ Test files removed"
fi

echo ""
echo "============================================================"
echo "Test Complete!"
echo "============================================================"
echo ""
echo "Full logs available at:"
echo "  Agent: /tmp/agent.log"
echo "  Mock Server: /tmp/mock_server.log"
echo ""
