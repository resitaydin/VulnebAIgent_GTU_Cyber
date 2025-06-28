"""
Unit Tests for VulnebAIgent AI Agents

This module contains basic unit tests for the AI agent classes.
These tests verify the basic functionality and initialization of agents.

"""

import unittest
import sys
import os
import json

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.agent import Agent
from src.agents.strategy_generator import StrategyGenerator
from src.agents.senior_reviewer import SeniorReviewer
from src.agents.error_handler import ErrorHandler
from src.agents.execution_monitor import ExecutionMonitor
from src.agents.command_executor import CommandExecutor
from src.agents.report_writer import ReportWriter

class TestBaseAgent(unittest.TestCase):
    """Test cases for the base Agent class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_api_key = "test_api_key"
        self.agent = Agent("TestAgent", self.test_api_key)
    
    def test_agent_initialization(self):
        """Test that agents are initialized correctly."""
        self.assertEqual(self.agent.name, "TestAgent")
        self.assertIsNotNone(self.agent.client)
        self.assertEqual(self.agent.chat_histories, {})
    
    def test_get_chat_history(self):
        """Test chat history management."""
        recipient = "TestRecipient"
        history = self.agent.get_chat_history(recipient)
        
        # Should create a new history for new recipients
        self.assertIsInstance(history, list)
        self.assertEqual(len(history), 1)  # Should have system message
        self.assertEqual(history[0]["role"], "system")
    
    def test_add_to_chat_history(self):
        """Test adding messages to chat history."""
        recipient = "TestRecipient"
        self.agent.add_to_chat_history(recipient, "user", "Test message")
        
        history = self.agent.get_chat_history(recipient)
        self.assertEqual(len(history), 2)  # System message + added message
        self.assertEqual(history[1]["role"], "user")
        self.assertEqual(history[1]["content"], "Test message")

class TestAgentInstantiation(unittest.TestCase):
    """Test cases for agent instantiation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_api_key = "test_api_key"
    
    def test_strategy_generator_creation(self):
        """Test StrategyGenerator instantiation."""
        agent = StrategyGenerator(self.test_api_key)
        self.assertEqual(agent.name, "StrategyGenerator")
        self.assertIsInstance(agent, Agent)
    
    def test_senior_reviewer_creation(self):
        """Test SeniorReviewer instantiation."""
        agent = SeniorReviewer(self.test_api_key)
        self.assertEqual(agent.name, "SeniorReviewer")
        self.assertIsInstance(agent, Agent)
    
    def test_error_handler_creation(self):
        """Test ErrorHandler instantiation."""
        agent = ErrorHandler(self.test_api_key)
        self.assertEqual(agent.name, "ErrorHandler")
        self.assertIsInstance(agent, Agent)
    
    def test_execution_monitor_creation(self):
        """Test ExecutionMonitor instantiation."""
        agent = ExecutionMonitor(self.test_api_key)
        self.assertEqual(agent.name, "ExecutionMonitor")
        self.assertIsInstance(agent, Agent)
    
    def test_command_executor_creation(self):
        """Test CommandExecutor instantiation."""
        agent = CommandExecutor(self.test_api_key)
        self.assertEqual(agent.name, "CommandExecutor")
        self.assertIsInstance(agent, Agent)
    
    def test_report_writer_creation(self):
        """Test ReportWriter instantiation."""
        agent = ReportWriter(self.test_api_key)
        self.assertEqual(agent.name, "ReportWriter")
        self.assertIsInstance(agent, Agent)

class TestUtilityFunctions(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_json_parsing(self):
        """Test JSON parsing functionality."""
        test_data = {"test": "value", "number": 123}
        json_string = json.dumps(test_data)
        parsed_data = json.loads(json_string)
        
        self.assertEqual(parsed_data, test_data)
    
    def test_file_operations(self):
        """Test basic file operations."""
        test_file = "test_temp.json"
        test_data = {"test": "data"}
        
        # Write test file
        with open(test_file, "w") as f:
            json.dump(test_data, f)
        
        # Read test file
        with open(test_file, "r") as f:
            loaded_data = json.load(f)
        
        self.assertEqual(loaded_data, test_data)
        
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)

class TestConfiguration(unittest.TestCase):
    """Test cases for configuration validation."""
    
    def test_environment_variables(self):
        """Test environment variable handling."""
        # Test that we can access environment variables
        test_var = os.getenv("PATH")
        self.assertIsNotNone(test_var)
    
    def test_directory_creation(self):
        """Test directory creation functionality."""
        test_dir = "test_temp_dir"
        os.makedirs(test_dir, exist_ok=True)
        
        self.assertTrue(os.path.exists(test_dir))
        self.assertTrue(os.path.isdir(test_dir))
        
        # Clean up
        if os.path.exists(test_dir):
            os.rmdir(test_dir)

if __name__ == "__main__":
    # Create a test suite
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTest(unittest.makeSuite(TestBaseAgent))
    suite.addTest(unittest.makeSuite(TestAgentInstantiation))
    suite.addTest(unittest.makeSuite(TestUtilityFunctions))
    suite.addTest(unittest.makeSuite(TestConfiguration))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\nTests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, error in result.failures:
            print(f"- {test}: {error}")
    
    if result.errors:
        print("\nErrors:")
        for test, error in result.errors:
            print(f"- {test}: {error}") 