#!/usr/bin/env python3
"""
Mock MCP Server - A simple test server that simulates MCP tool responses.

This is useful for testing the TuneIt AI Agent without a real MCP server.
Run this in one terminal, then run the agent in another terminal.

Usage:
    python mock_mcp_server.py

The server will listen on http://localhost:8000 by default.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MockMCPHandler(BaseHTTPRequestHandler):
    """Handler for mock MCP tool requests."""
    
    def do_POST(self):
        """Handle POST requests to tool endpoints."""
        # Parse the path
        if not self.path.startswith('/tools/'):
            self.send_error(404, "Not Found")
            return
        
        tool_name = self.path[7:]  # Remove '/tools/' prefix
        
        # Read request body
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        
        try:
            request_data = json.loads(body)
            arguments = request_data.get('arguments', {})
            
            logger.info(f"Received request for tool: {tool_name}")
            logger.debug(f"Arguments: {arguments}")
            
            # Generate mock response based on tool name
            if tool_name == 'format_job_description':
                response = self._format_job_description(arguments)
            elif tool_name == 'generate_tailored_resume':
                response = self._generate_tailored_resume(arguments)
            elif tool_name == 'save_tailored_resume':
                response = self._save_tailored_resume(arguments)
            elif tool_name == 'save_job_description':
                response = self._save_job_description(arguments)
            else:
                self.send_error(404, f"Unknown tool: {tool_name}")
                return
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
            logger.info(f"Sent response for tool: {tool_name}")
            
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            self.send_error(500, str(e))
    
    def _format_job_description(self, arguments):
        """Mock format_job_description tool."""
        job_desc = arguments.get('job_description', '')
        
        # Simple formatting (just add some structure)
        formatted = f"""
FORMATTED JOB DESCRIPTION
========================

Original Content:
{job_desc[:200]}...

[This is a mock formatted version]

Key Requirements Extracted:
- Requirement 1
- Requirement 2
- Requirement 3

Responsibilities Identified:
- Responsibility 1
- Responsibility 2
"""
        
        return {
            "formatted_job_description": formatted,
            "status": "success"
        }
    
    def _generate_tailored_resume(self, arguments):
        """Mock generate_tailored_resume tool."""
        job_desc = arguments.get('job_description', '')
        
        resume = f"""
TAILORED RESUME
===============

PROFESSIONAL SUMMARY
-------------------
Experienced professional with relevant skills for this position.

RELEVANT EXPERIENCE
------------------
- Experience aligned with job requirements
- Skills matching the job description
- Achievements relevant to the role

TECHNICAL SKILLS
---------------
- Skill 1 (matching job requirement)
- Skill 2 (matching job requirement)
- Skill 3 (matching job requirement)

[This is a mock tailored resume based on the job description]
"""
        
        return {
            "tailored_resume": resume,
            "status": "success"
        }
    
    def _save_tailored_resume(self, arguments):
        """Mock save_tailored_resume tool."""
        resume_content = arguments.get('resume_content', '')
        job_title = arguments.get('job_title', 'untitled')
        
        # In a real implementation, this would save to a file
        logger.info(f"Mock saving resume for: {job_title}")
        logger.debug(f"Resume length: {len(resume_content)} characters")
        
        return {
            "status": "success",
            "message": f"Resume saved for {job_title}",
            "filename": f"{job_title}_resume.txt"
        }
    
    def _save_job_description(self, arguments):
        """Mock save_job_description tool."""
        job_desc = arguments.get('job_description', '')
        job_title = arguments.get('job_title', 'untitled')
        
        # In a real implementation, this would save to a file
        logger.info(f"Mock saving job description for: {job_title}")
        logger.debug(f"Job description length: {len(job_desc)} characters")
        
        return {
            "status": "success",
            "message": f"Job description saved for {job_title}",
            "filename": f"{job_title}_job_description.txt"
        }
    
    def log_message(self, format, *args):
        """Override to use custom logger."""
        logger.info(f"{self.address_string()} - {format % args}")


def main():
    """Run the mock MCP server."""
    host = 'localhost'
    port = 8000
    
    server = HTTPServer((host, port), MockMCPHandler)
    
    logger.info("=" * 60)
    logger.info("Mock MCP Server")
    logger.info("=" * 60)
    logger.info(f"Server running at http://{host}:{port}")
    logger.info("Available tools:")
    logger.info("  - POST /tools/format_job_description")
    logger.info("  - POST /tools/generate_tailored_resume")
    logger.info("  - POST /tools/save_tailored_resume")
    logger.info("  - POST /tools/save_job_description")
    logger.info("")
    logger.info("Press Ctrl+C to stop")
    logger.info("=" * 60)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("\nShutting down server...")
        server.shutdown()
        logger.info("Server stopped")


if __name__ == "__main__":
    main()
