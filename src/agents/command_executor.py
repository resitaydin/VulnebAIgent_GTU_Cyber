import json
import pexpect
import time
from ..core.agent import Agent
import subprocess
class CommandExecutor(Agent):
    def __init__(self, api_key):
        super().__init__("CommandExecutor", api_key)

    def execute_commands(self, commands, target_ip, scan_description, error_handler, strategy_generator, execution_monitor, log_file_path=None):
        output = ""
        executed_commands = []
        pending_commands = commands.copy()
        command_index = 0
        
        while command_index < len(commands):
            command = commands[command_index]
            try:
                output += f"Executing command: {command}\n"
                child = pexpect.spawn(command, timeout=300, encoding='utf-8')
                print(output)
                executed_commands.append(command)
                pending_commands = commands[command_index+1:]
                
                command_output = ""
                start_time = time.time()
                while True:
                    try:
                        child.expect('\r\n')  # Wait for a maximum of 10 seconds for each line of output
                        output_line = child.before
                        command_output += output_line + "\n"
                        
                        elapsed_time = time.time() - start_time
                        if elapsed_time >= 10:
                            execution_monitor_response = execution_monitor.monitor_output(target_ip, scan_description, command_output, executed_commands, pending_commands, log_file_path)
                            if execution_monitor_response["input_needed"]:
                                strategy_generator_response = strategy_generator.generate_input(target_ip, scan_description, command_output, pending_commands, log_file_path)
                                input_command = strategy_generator_response["input"]
                                
                                if input_command:
                                    command_index += 1
                                    print(f"Input: {input_command}")
                                    child.sendline(input_command)
                                else:
                                    command_index += 1
                                    break
                            start_time = time.time()
                            command_output = ""
                            
                    except pexpect.TIMEOUT:
                        output_line = child.before
                        print(output_line)
                        command_output += output_line + "\n"
                        
                    except pexpect.EOF:
                        output_line = child.before
                        print(output_line)
                        command_output += output_line + "\n"
                        output += command_output
                        command_index += 1
                        break
                    
            except pexpect.exceptions.ExceptionPexpect as e:
                error_message = f"Error executing command: {command}\nError message: {str(e)}\n\n"
                context = f"Target IP: {target_ip}\nScan Description: {scan_description}\nCommand Output:\n{output}"
                error_handler_response = error_handler.handle_error(error_message, context, log_file_path)
                self.add_to_chat_history("ErrorHandler", "user", f"Error Message:\n{error_message}\n\nContext:\n{context}")
                self.add_to_chat_history("ErrorHandler", "assistant", json.dumps(error_handler_response))
                print("Error encountered. ErrorHandler's response:")
                print(json.dumps(error_handler_response, indent=2))
                if "fix" in error_handler_response:
                    fix_commands = error_handler_response["fix"]
                    print("Executing fix commands:")
                    for fix_command in fix_commands:
                        print(f"Executing command: {fix_command}")
                        try:
                            fix_output = subprocess.check_output(fix_command, shell=True, universal_newlines=True)
                            print(f"Command output: {fix_output}")
                        except subprocess.CalledProcessError as e:
                            print(f"Error executing fix command: {fix_command}")
                            print(f"Error message: {e.output}")
                output += error_message
                command_index += 1
                
        return output