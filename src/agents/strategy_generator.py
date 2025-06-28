import json
from ..core.agent import Agent

class StrategyGenerator(Agent):
    def __init__(self, api_key):
        super().__init__("StrategyGenerator", api_key)

    def generate_strategy(self, target_ip, scan_description, approved_strategy=None, feedback=None, log_file_path=None):
        system_message = "You are StrategyGenerator, an experienced penetration tester. Your role is to generate a comprehensive strategy to conduct a successful and comprehensive vulnerability scan based on the provided target IP and scan description. The strategy should include a set of relevant Linux terminal commands to gather information and detect potential vulnerabilities. Respond with the strategy in JSON format, using the 'strategy' key as an array of command strings. Ensure the commands are tailored to the specific target and scan description, and are ready to be executed without any manual modifications. Include any necessary explanation or context in the 'description' key. Always start with recon, and ask SeniorReviewer, the senior what command should you execute next based on the result. Note, Always include your name and role at the end of each Description."
        
        user_message = f"Target IP: {target_ip}\nScan Description: {scan_description}\n\nGenerate a comprehensive strategy to complete the vulnerability scan based on the provided IP and description. Provide the strategy in JSON format, along with any relevant explanation or context. Ensure that all commands are complete and can be executed as-is without requiring manual changes. and send it to SeniorReviewer, Your senior for review. Always include your name and role at the end of each Description."
        
        if approved_strategy:
            user_message += f"\n\nApproved Strategy:\n{json.dumps(approved_strategy, indent=2)}\n\nPlease update the strategy based on the approved strategy, ensuring that all commands are complete and ready to be executed without modifications."
        elif feedback:
            user_message += f"\n\nFeedback from SeniorReviewer: {feedback}\n\nPlease update the strategy based on the provided feedback, ensuring that all commands are complete and ready to be executed without modifications. Return in JSON format."

        strategy = self.generate_response("SeniorReviewer", user_message, system_message, response_format={"type": "json_object"})
        self.print_agent_output(text=strategy, log_file_path=log_file_path)
        return json.loads(strategy)

    def generate_input(self, target_ip, scan_description, command_output, commands, log_file_path=None):
        system_message = "You are StrategyGenerator, an experienced penetration tester. Based on the provided command output, determine if the executed command requires input. If input is required, provide the next command from the given list of commands in the correct order. If no input is required or the output suggests the current task is complete, provide an empty string. Respond with the input in JSON format, using the 'input' key to provide the input string."
        
        user_message = f"Target IP: {target_ip}\nScan Description: {scan_description}\nCommand Output:\n{command_output}\nCommands: {json.dumps(commands)}\n\nBased on the command output, determine if input is required. If input is required, provide the next command from the given list of commands in the correct order. If no input is required or the output suggests the current task is complete, provide an empty string. Respond with the input in JSON format."
        
        strategy_generator_response = self.generate_response("CommandExecutor", user_message,system_message,response_format={"type": "json_object"})
        self.add_to_chat_history("CommandExecutor", "user", user_message)
        self.add_to_chat_history("CommandExecutor", "assistant", strategy_generator_response)
        self.print_agent_output(text=strategy_generator_response, log_file_path=log_file_path)
        return json.loads(strategy_generator_response)