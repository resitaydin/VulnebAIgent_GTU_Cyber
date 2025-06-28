# utils.py

from colorama import init, Fore, Style
import json

init()

def print_agent_output(agent_name, text=None, log_file_path=None):
    color = {
        "StrategyGenerator": Fore.BLUE,
        "SeniorReviewer": Fore.GREEN,
        "ErrorHandler": Fore.LIGHTGREEN_EX,
        "ExecutionMonitor": Fore.MAGENTA,
        "CommandExecutor": Fore.YELLOW,
        "ReportWriter": Fore.CYAN,
        "Output": Fore.RED
    }.get(agent_name, Fore.RESET)
    
    print(f"{color}{agent_name}:{Style.RESET_ALL}")
    
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
        "agent_name": agent_name,
        "text": text
    }
    
    if log_file_path:
        with open(log_file_path, "r+") as log_file:
            log_data = json.load(log_file)
            log_data["output"].append(log_entry)
            log_file.seek(0)
            json.dump(log_data, log_file, indent=2)
            log_file.truncate()