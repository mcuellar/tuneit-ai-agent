#!/usr/bin/env python3
"""
Background Runner - Main entry point for the TuneIt AI Agent.

This script starts the file watcher as a background service that continuously
monitors for new job description files and processes them.
"""

import os
import sys
import logging
import signal
from pathlib import Path
from dotenv import load_dotenv

from agent import TuneItAgent
from file_watcher import FileWatcher

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('tuneit_agent.log')
    ]
)
logger = logging.getLogger(__name__)


class BackgroundRunner:
    """Background service runner for the TuneIt AI Agent."""
    
    def __init__(self):
        """Initialize the background runner."""
        self.agent = None
        self.watcher = None
        self.running = False
        
        # Get configuration from environment
        self.mcp_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
        self.watch_directory = os.getenv("WATCH_DIRECTORY", "./job_descriptions")
        self.allowed_extensions = os.getenv(
            "ALLOWED_EXTENSIONS", 
            ".txt,.md,.pdf"
        ).split(",")
        
        logger.info("Background runner initialized")
        logger.info(f"MCP Server URL: {self.mcp_url}")
        logger.info(f"Watch Directory: {self.watch_directory}")
        logger.info(f"Allowed Extensions: {self.allowed_extensions}")
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, shutting down...")
        self.stop()
    
    def start(self):
        """Start the background service."""
        logger.info("Starting TuneIt AI Agent background service...")
        
        try:
            # Initialize the agent
            logger.info("Initializing TuneIt agent...")
            self.agent = TuneItAgent(self.mcp_url)
            
            # Initialize the file watcher
            logger.info("Initializing file watcher...")
            self.watcher = FileWatcher(
                self.agent,
                self.watch_directory,
                self.allowed_extensions
            )
            
            # Setup signal handlers
            self.setup_signal_handlers()
            
            # Start watching
            self.running = True
            logger.info("=" * 60)
            logger.info("TuneIt AI Agent is now running!")
            logger.info(f"Watching for new job descriptions in: {self.watch_directory}")
            logger.info("Press Ctrl+C to stop")
            logger.info("=" * 60)
            
            self.watcher.run()
            
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        except Exception as e:
            logger.error(f"Error running background service: {e}", exc_info=True)
            raise
        finally:
            self.stop()
    
    def stop(self):
        """Stop the background service."""
        if not self.running:
            return
        
        logger.info("Stopping TuneIt AI Agent background service...")
        self.running = False
        
        if self.watcher:
            try:
                self.watcher.stop()
                logger.info("File watcher stopped")
            except Exception as e:
                logger.error(f"Error stopping file watcher: {e}")
        
        if self.agent:
            try:
                self.agent.close()
                logger.info("Agent closed")
            except Exception as e:
                logger.error(f"Error closing agent: {e}")
        
        logger.info("Background service stopped")


def main():
    """Main entry point."""
    logger.info("=" * 60)
    logger.info("TuneIt AI Agent - Background Runner")
    logger.info("=" * 60)
    
    # Create and start the runner
    runner = BackgroundRunner()
    runner.start()


if __name__ == "__main__":
    main()
