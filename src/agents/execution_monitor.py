import json
from ..core.agent import Agent

class ExecutionMonitor(Agent):
    def __init__(self, api_key):
        super().__init__("ExecutionMonitor", api_key)

    def monitor_output(self, target_ip, scan_description, command_output, executed_commands, pending_commands, log_file_path=None):
        system_message = "You are ExecutionMonitor, an expert in monitoring command execution output. Your role is to analyze the provided command output and determine if the executed command requires input or if it is still running a previous command or loading up. If input is required, indicate that it is time to provide input. If the command is still running or loading up, indicate that no input is needed at the moment. Respond with your analysis in JSON format, using the 'input_needed' key as a boolean value."
        
        user_message = f"Target IP: {target_ip}\nScan Description: {scan_description}\nCommand Output:\n{command_output}\nExecuted Commands: {json.dumps(executed_commands)}\nPending Commands: {json.dumps(pending_commands)}\n\nAnalyze the command output and determine if input is required or if the command is still running or loading up. Respond with your analysis in JSON format, using the 'input_needed' key as a boolean value."
        
        execution_monitor_response = self.generate_response("CommandExecutor", user_message, system_message, response_format={"type": "json_object"})
        self.add_to_chat_history("CommandExecutor", "user", user_message)
        self.add_to_chat_history("CommandExecutor", "assistant", execution_monitor_response)
        self.print_agent_output(text=execution_monitor_response, log_file_path=log_file_path)
        return json.loads(execution_monitor_response)