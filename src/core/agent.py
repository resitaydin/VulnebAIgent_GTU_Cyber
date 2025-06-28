"""
Base Agent Class for VulnebAIgent

This module provides the base Agent class that all specialized AI agents inherit from.
It handles common functionality like OpenAI API communication, chat history management,
and formatted output display.

"""

from openai import OpenAI
from colorama import init, Fore, Style
import json

class Agent:
    """
    Base class for all AI agents in the VulnebAIgent system.
    
    This class provides common functionality for:
    - OpenAI API communication
    - Chat history management between agents
    - Formatted output display with color coding
    - Logging to JSON files
    
    Attributes:
        name (str): The name/role of this agent
        client (OpenAI): OpenAI API client instance
        chat_histories (dict): Conversation histories with other agents
    """
    
    def __init__(self, name, api_key):
        """
        Initialize the agent with a name and OpenAI API key.
        
        Args:
            name (str): The name/role of this agent (e.g., "StrategyGenerator")
            api_key (str): OpenAI API key for making requests
        """
        self.name = name
        self.client = OpenAI(api_key=api_key)
        self.chat_histories = {}  # Stores conversation history with each recipient

    def get_chat_history(self, recipient):
        if recipient not in self.chat_histories:
            self.chat_histories[recipient] = [
                {"role": "system", "content": f"You are {self.name}, an AI agent. You are communicating with {recipient}."},
            ]
        return self.chat_histories[recipient]

    def add_to_chat_history(self, recipient, role, content):
        chat_history = self.get_chat_history(recipient)
        chat_history.append({"role": role, "content": content})

    def print_agent_output(self, text=None, log_file_path=None):
        color = {
            "StrategyGenerator": Fore.BLUE,
            "SeniorReviewer": Fore.GREEN,
            "ErrorHandler": Fore.LIGHTGREEN_EX,
            "ExecutionMonitor": Fore.MAGENTA,
            "CommandExecutor": Fore.YELLOW,
            "ReportWriter": Fore.CYAN,
            "Output": Fore.RED
        }.get(self.name, Fore.RESET)
        
        print(f"{color}{self.name}:{Style.RESET_ALL}")
        
        if text:
            try:
                data = json.loads(text)
                for key, value in data.items():
                    formatted_key = key.capitalize()
                    if isinstance(value, bool):
                        formatted_value = "Yes" if value else "No"
                    elif isinstance(value, list):
                        formatted_value = ", ".join(value)
                    else:
                        formatted_value = value
                    print(f"{color}{formatted_key}: {formatted_value}{Style.RESET_ALL}")
            except json.JSONDecodeError:
                print(f"{color}Text: {text}{Style.RESET_ALL}")
        
        print()

        log_entry = {
            "agent_name": self.name,
            "text": text
        }
        
        if log_file_path:
            with open(log_file_path, "r+") as log_file:
                log_data = json.load(log_file)
                log_data["output"].append(log_entry)
                log_file.seek(0)
                json.dump(log_data, log_file, indent=2)
                log_file.truncate()

    def generate_chat_messages(self, recipient, system_message, user_message):
        chat_history = self.get_chat_history(recipient)
        messages = [
            {"role": "system", "content": system_message},
            *chat_history[-10:],
            {"role": "user", "content": user_message}
        ]
        return messages

    def generate_response(self, recipient, user_message, system_message, model="gpt-4.1", response_format=None):
        chat_history = self.get_chat_history(recipient)
        self.add_to_chat_history(recipient, "user", user_message)
        messages = [
            {"role": "system", "content": system_message},
            *chat_history,
            {"role": "user", "content": user_message}
        ]
        if response_format:
            response = self.client.chat.completions.create(
                model=model,
                response_format=response_format,
                messages=messages
            )
        else:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages
            )
        assistant_response = response.choices[0].message.content
        self.add_to_chat_history(recipient, "assistant", assistant_response)
        return assistant_response