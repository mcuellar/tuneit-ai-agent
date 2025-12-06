#!/usr/bin/env python3
"""
Simple validation script to test the TuneIt AI Agent components.
This validates imports and basic structure without needing a running MCP server.
"""

import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_imports():
    """Test that all modules can be imported."""
    logger.info("Testing imports...")
    
    try:
        import agent
        logger.info("✓ agent module imported")
        
        import file_watcher
        logger.info("✓ file_watcher module imported")
        
        import run
        logger.info("✓ run module imported")
        
        return True
    except Exception as e:
        logger.error(f"✗ Import failed: {e}")
        return False


def test_agent_structure():
    """Test agent class structure."""
    logger.info("Testing agent structure...")
    
    try:
        from agent import TuneItAgent, MCPClient, AgentState
        
        # Check MCPClient has required methods
        assert hasattr(MCPClient, 'call_tool')
        assert hasattr(MCPClient, 'format_job_description')
        assert hasattr(MCPClient, 'generate_tailored_resume')
        assert hasattr(MCPClient, 'save_tailored_resume')
        assert hasattr(MCPClient, 'save_job_description')
        logger.info("✓ MCPClient has all required methods")
        
        # Check TuneItAgent has required methods
        assert hasattr(TuneItAgent, 'process_job_description')
        assert hasattr(TuneItAgent, '_build_graph')
        logger.info("✓ TuneItAgent has all required methods")
        
        # Check AgentState structure
        assert 'job_description_path' in AgentState.__annotations__
        assert 'job_description_content' in AgentState.__annotations__
        assert 'formatted_job_description' in AgentState.__annotations__
        assert 'tailored_resume' in AgentState.__annotations__
        assert 'status' in AgentState.__annotations__
        logger.info("✓ AgentState has all required fields")
        
        return True
    except Exception as e:
        logger.error(f"✗ Agent structure test failed: {e}")
        return False


def test_file_watcher_structure():
    """Test file watcher class structure."""
    logger.info("Testing file watcher structure...")
    
    try:
        from file_watcher import FileWatcher, JobDescriptionHandler
        
        # Check FileWatcher has required methods
        assert hasattr(FileWatcher, 'start')
        assert hasattr(FileWatcher, 'stop')
        assert hasattr(FileWatcher, 'run')
        logger.info("✓ FileWatcher has all required methods")
        
        # Check JobDescriptionHandler has required methods
        assert hasattr(JobDescriptionHandler, 'on_created')
        logger.info("✓ JobDescriptionHandler has all required methods")
        
        return True
    except Exception as e:
        logger.error(f"✗ File watcher structure test failed: {e}")
        return False


def test_runner_structure():
    """Test background runner structure."""
    logger.info("Testing background runner structure...")
    
    try:
        from run import BackgroundRunner
        
        # Check BackgroundRunner has required methods
        assert hasattr(BackgroundRunner, 'start')
        assert hasattr(BackgroundRunner, 'stop')
        assert hasattr(BackgroundRunner, 'setup_signal_handlers')
        logger.info("✓ BackgroundRunner has all required methods")
        
        return True
    except Exception as e:
        logger.error(f"✗ Background runner structure test failed: {e}")
        return False


def test_files_exist():
    """Test that all required files exist."""
    logger.info("Testing file existence...")
    
    required_files = [
        'agent.py',
        'file_watcher.py',
        'run.py',
        'requirements.txt',
        'README.md',
        '.env.example',
        '.gitignore',
        'setup.sh'
    ]
    
    all_exist = True
    for filename in required_files:
        path = Path(filename)
        if path.exists():
            logger.info(f"✓ {filename} exists")
        else:
            logger.error(f"✗ {filename} missing")
            all_exist = False
    
    return all_exist


def main():
    """Run all validation tests."""
    logger.info("=" * 60)
    logger.info("TuneIt AI Agent - Validation Tests")
    logger.info("=" * 60)
    logger.info("")
    
    tests = [
        ("File Existence", test_files_exist),
        ("Imports", test_imports),
        ("Agent Structure", test_agent_structure),
        ("File Watcher Structure", test_file_watcher_structure),
        ("Background Runner Structure", test_runner_structure),
    ]
    
    results = []
    for name, test_func in tests:
        logger.info("")
        logger.info(f"Running: {name}")
        logger.info("-" * 60)
        result = test_func()
        results.append((name, result))
        logger.info("")
    
    logger.info("=" * 60)
    logger.info("Test Results Summary")
    logger.info("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        logger.info(f"{symbol} {name}: {status}")
        if not result:
            all_passed = False
    
    logger.info("")
    if all_passed:
        logger.info("All tests passed! ✓")
        return 0
    else:
        logger.error("Some tests failed! ✗")
        return 1


if __name__ == "__main__":
    sys.exit(main())
