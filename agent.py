"""
TuneIt AI Agent - LangGraph agent for tailoring resumes based on job descriptions.

This module implements a LangGraph-based AI agent that:
1. Monitors a folder for new job description files
2. Connects to an MCP server over HTTP
3. Executes a workflow to format job descriptions and generate tailored resumes
"""

import os
import json
import logging
from typing import TypedDict, Annotated, Literal
from pathlib import Path

import httpx
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    """State for the TuneIt AI agent."""
    job_description_path: str
    job_description_content: str
    formatted_job_description: str
    tailored_resume: str
    status: str
    error: str | None


class MCPClient:
    """Client for interacting with MCP server over HTTP."""
    
    def __init__(self, base_url: str):
        """
        Initialize MCP client.
        
        Args:
            base_url: Base URL of the MCP server (e.g., http://localhost:8000)
        """
        self.base_url = base_url.rstrip('/')
        self.client = httpx.Client(timeout=30.0)
        logger.info(f"Initialized MCP client with base URL: {self.base_url}")
    
    def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """
        Call an MCP tool via HTTP.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool
            
        Returns:
            Tool execution result
        """
        url = f"{self.base_url}/tools/{tool_name}"
        logger.info(f"Calling MCP tool: {tool_name}")
        logger.debug(f"Arguments: {arguments}")
        
        try:
            response = self.client.post(
                url,
                json={"arguments": arguments},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            result = response.json()
            logger.info(f"Tool {tool_name} executed successfully")
            return result
        except httpx.HTTPError as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            raise
    
    def format_job_description(self, job_description: str) -> dict:
        """Format a job description using MCP tool."""
        return self.call_tool("format_to_markdown", {
            "job_description": job_description
        })
    
    def generate_tailored_resume(self, base_resume: str, job_description: str) -> str:
        """Generate a tailored resume based on job description."""
        
        base_resume_path = os.path.join(os.path.dirname(__file__), "resume_base.md")
        with open(base_resume_path, "r", encoding="utf-8") as f:
            base_resume = f.read()

        return self.call_tool("tailor_resume", {
            "base_resume": base_resume,
            "job_description": job_description
        })
    
    
    def save_tailored_resume(self, resume_content: str, job_title: str) -> str:
        """Save the tailored resume."""
        return self.call_tool("save_tailored_resume", {
            "resume_content": resume_content,
            "job_title": job_title
        })
    
    def save_job_description(self, job_description: str, job_title: str) -> str:
        """Save the formatted job description."""
        return self.call_tool("save_job", {
            "job_description": job_description,
            "job_title": job_title
        })
    
    def close(self):
        """Close the HTTP client."""
        self.client.close()


class TuneItAgent:
    """LangGraph agent for processing job descriptions and generating tailored resumes."""
    
    def __init__(self, mcp_url: str):
        """
        Initialize the TuneIt agent.
        
        Args:
            mcp_url: URL of the MCP server
        """
        self.mcp_client = MCPClient(mcp_url)
        self.graph = self._build_graph()
        logger.info("TuneIt agent initialized")
    
    def _read_job_description(self, state: AgentState) -> AgentState:
        """Read job description from file."""
        logger.info(f"Reading job description from: {state['job_description_path']}")
        try:
            with open(state['job_description_path'], 'r', encoding='utf-8') as f:
                content = f.read()
            
            state['job_description_content'] = content
            state['status'] = 'job_description_read'
            logger.info("Job description read successfully")
            return state
        except Exception as e:
            logger.error(f"Error reading job description: {e}")
            state['error'] = str(e)
            state['status'] = 'error'
            return state
    
    def _format_job_description(self, state: AgentState) -> AgentState:
        """Format job description using MCP tool."""
        logger.info("Formatting job description")
        try:
            result = self.mcp_client.format_job_description(
                state['job_description_content']
            )
            
            # Extract formatted job description from result
            formatted = result.get('formatted_job_description', result.get('result', ''))
            state['formatted_job_description'] = formatted
            state['status'] = 'job_description_formatted'
            logger.info("Job description formatted successfully")
            return state
        except Exception as e:
            logger.error(f"Error formatting job description: {e}")
            state['error'] = str(e)
            state['status'] = 'error'
            return state
    
    def _generate_tailored_resume(self, state: AgentState) -> AgentState:
        """Generate tailored resume using MCP tool."""
        logger.info("Generating tailored resume")
        try:
            result = self.mcp_client.generate_tailored_resume(
                state['formatted_job_description']
            )
            
            # Extract tailored resume from result
            resume = result.get('tailored_resume', result.get('result', ''))
            state['tailored_resume'] = resume
            state['status'] = 'resume_generated'
            logger.info("Tailored resume generated successfully")
            return state
        except Exception as e:
            logger.error(f"Error generating tailored resume: {e}")
            state['error'] = str(e)
            state['status'] = 'error'
            return state
    
    def _save_outputs(self, state: AgentState) -> AgentState:
        """Save tailored resume and job description using MCP tools."""
        logger.info("Saving outputs")
        try:
            # Extract job title from path or use default
            job_title = Path(state['job_description_path']).stem
            
            # Save tailored resume
            self.mcp_client.save_tailored_resume(
                state['tailored_resume'],
                job_title
            )
            logger.info("Tailored resume saved")
            
            # Save job description
            self.mcp_client.save_job_description(
                state['formatted_job_description'],
                job_title
            )
            logger.info("Job description saved")
            
            state['status'] = 'completed'
            logger.info("All outputs saved successfully")
            return state
        except Exception as e:
            logger.error(f"Error saving outputs: {e}")
            state['error'] = str(e)
            state['status'] = 'error'
            return state
    
    def _should_continue(self, state: AgentState) -> Literal["continue", "end"]:
        """Determine if processing should continue or end."""
        if state.get('status') == 'error':
            return "end"
        if state.get('status') == 'completed':
            return "end"
        return "continue"
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("read_job_description", self._read_job_description)
        workflow.add_node("format_job_description", self._format_job_description)
        workflow.add_node("generate_resume", self._generate_tailored_resume)
        workflow.add_node("save_outputs", self._save_outputs)
        
        # Define the flow
        workflow.set_entry_point("read_job_description")
        workflow.add_edge("read_job_description", "format_job_description")
        workflow.add_edge("format_job_description", "generate_resume")
        workflow.add_edge("generate_resume", "save_outputs")
        workflow.add_edge("save_outputs", END)
        
        return workflow.compile()
    
    def process_job_description(self, file_path: str) -> AgentState:
        """
        Process a job description file through the complete workflow.
        
        Args:
            file_path: Path to the job description file
            
        Returns:
            Final agent state
        """
        logger.info(f"Starting to process job description: {file_path}")
        
        initial_state: AgentState = {
            "job_description_path": file_path,
            "job_description_content": "",
            "formatted_job_description": "",
            "tailored_resume": "",
            "status": "initialized",
            "error": None
        }
        
        try:
            final_state = self.graph.invoke(initial_state)
            
            if final_state['status'] == 'completed':
                logger.info(f"Successfully processed: {file_path}")
            else:
                logger.error(f"Processing failed for {file_path}: {final_state.get('error')}")
            
            return final_state
        except Exception as e:
            logger.error(f"Unexpected error processing {file_path}: {e}")
            initial_state['error'] = str(e)
            initial_state['status'] = 'error'
            return initial_state
    
    def close(self):
        """Clean up resources."""
        self.mcp_client.close()
        logger.info("TuneIt agent closed")


if __name__ == "__main__":
    # Example usage
    mcp_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
    
    agent = TuneItAgent(mcp_url)
    
    # Example: Process a job description file
    # result = agent.process_job_description("path/to/job_description.txt")
    # print(f"Processing result: {result}")
    
    agent.close()
