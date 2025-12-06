"""
File Watcher - Monitors a directory for new job description files.

This module uses the watchdog library to monitor a directory for new files
and triggers the TuneIt agent to process them.
"""

import os
import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

logger = logging.getLogger(__name__)


class JobDescriptionHandler(FileSystemEventHandler):
    """Handler for new job description files."""
    
    def __init__(self, agent, allowed_extensions=None):
        """
        Initialize the file handler.
        
        Args:
            agent: TuneItAgent instance to process files
            allowed_extensions: List of allowed file extensions (default: ['.txt', '.md'])
        """
        self.agent = agent
        self.allowed_extensions = allowed_extensions or ['.txt', '.md', '.pdf']
        self.processed_files = set()
        logger.info(f"File handler initialized with extensions: {self.allowed_extensions}")
    
    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return
        
        file_path = event.src_path
        file_ext = Path(file_path).suffix.lower()
        
        # Check if file extension is allowed
        if file_ext not in self.allowed_extensions:
            logger.debug(f"Ignoring file with extension {file_ext}: {file_path}")
            return
        
        # Avoid processing the same file multiple times
        if file_path in self.processed_files:
            logger.debug(f"File already processed: {file_path}")
            return
        
        logger.info(f"New job description detected: {file_path}")
        
        # Wait a moment to ensure file is fully written
        time.sleep(1)
        
        # Mark as processed before attempting to avoid duplicate processing
        self.processed_files.add(file_path)
        
        try:
            # Process the job description
            result = self.agent.process_job_description(file_path)
            
            if result['status'] == 'completed':
                logger.info(f"Successfully processed: {file_path}")
            else:
                logger.error(f"Failed to process {file_path}: {result.get('error')}")
                # Remove from processed set so it can be retried
                self.processed_files.discard(file_path)
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            # Remove from processed set so it can be retried
            self.processed_files.discard(file_path)


class FileWatcher:
    """Watches a directory for new job description files."""
    
    def __init__(self, agent, watch_directory: str, allowed_extensions=None):
        """
        Initialize the file watcher.
        
        Args:
            agent: TuneItAgent instance to process files
            watch_directory: Directory to watch for new files
            allowed_extensions: List of allowed file extensions
        """
        self.agent = agent
        self.watch_directory = watch_directory
        self.event_handler = JobDescriptionHandler(agent, allowed_extensions)
        self.observer = Observer()
        
        # Create watch directory if it doesn't exist
        Path(watch_directory).mkdir(parents=True, exist_ok=True)
        
        logger.info(f"File watcher initialized for directory: {watch_directory}")
    
    def start(self):
        """Start watching the directory."""
        self.observer.schedule(
            self.event_handler,
            self.watch_directory,
            recursive=False
        )
        self.observer.start()
        logger.info(f"Started watching directory: {self.watch_directory}")
    
    def stop(self):
        """Stop watching the directory."""
        self.observer.stop()
        self.observer.join()
        logger.info("File watcher stopped")
    
    def run(self):
        """Run the file watcher indefinitely."""
        self.start()
        try:
            logger.info("File watcher is running. Press Ctrl+C to stop.")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received stop signal")
        finally:
            self.stop()


if __name__ == "__main__":
    from agent import TuneItAgent
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize agent
    mcp_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
    agent = TuneItAgent(mcp_url)
    
    # Initialize and run file watcher
    watch_dir = os.getenv("WATCH_DIRECTORY", "./job_descriptions")
    watcher = FileWatcher(agent, watch_dir)
    
    try:
        watcher.run()
    finally:
        agent.close()
