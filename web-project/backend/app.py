import os
import sys
import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import eventlet

# Add parent directory to path to import from parent project
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Agents.strategy_generator import StrategyGenerator
from Agents.senior_reviewer import SeniorReviewer
from Agents.error_handler import ErrorHandler
from Agents.execution_monitor import ExecutionMonitor
from Agents.command_executor import CommandExecutor
from Agents.report_writer import ReportWriter

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Custom logger to send output to WebSocket
class WebSocketLogger:
    def __init__(self, scan_id):
        self.scan_id = scan_id
        self.log_file_path = None
        
    def initialize_log_file(self, target_ip, scan_description):
        log_directory = "./Logs"
        os.makedirs(log_directory, exist_ok=True)
        
        timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        log_file_name = f"log-{self.scan_id}-{timestamp}.json"
        self.log_file_path = os.path.join(log_directory, log_file_name)
        
        log_data = {
            "target_ip": target_ip,
            "scan_description": scan_description,
            "output": []
        }
        
        with open(self.log_file_path, "w") as log_file:
            json.dump(log_data, log_file, indent=2)
        
        return self.log_file_path

    def log(self, agent_name, text):
        log_entry = {
            "agent_name": agent_name,
            "text": text,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Send to WebSocket
        socketio.emit(f'scan_update_{self.scan_id}', log_entry)
        
        # Also log to file
        if self.log_file_path:
            try:
                with open(self.log_file_path, "r+") as log_file:
                    log_data = json.load(log_file)
                    log_data["output"].append(log_entry)
                    log_file.seek(0)
                    json.dump(log_data, log_file, indent=2)
                    log_file.truncate()
            except Exception as e:
                print(f"Error writing to log file: {e}")

# Modified Agent classes to use WebSocket
class WebSocketAgent:
    def __init__(self, original_agent, ws_logger):
        self.original_agent = original_agent
        self.ws_logger = ws_logger
        self.name = original_agent.name
        
    def __getattr__(self, name):
        original_method = getattr(self.original_agent, name)
        
        if name == 'print_agent_output':
            # Special handling for print_agent_output
            def print_wrapper(text=None, log_file_path=None):
                # Call the original print_agent_output
                original_method(text, log_file_path)
                
                # Also log to WebSocket
                if text:
                    self.ws_logger.log(self.original_agent.name, text)
                
                return None
            return print_wrapper
        elif callable(original_method):
            # For all other methods
            def method_wrapper(*args, **kwargs):
                result = original_method(*args, **kwargs)
                
                # For methods that return results (not print_agent_output)
                if isinstance(result, dict) or isinstance(result, str):
                    # Try to log the result
                    text = result if isinstance(result, str) else json.dumps(result)
                    self.ws_logger.log(self.original_agent.name, text)
                
                return result
            return method_wrapper
        return original_method

# Keep track of running scans
active_scans = {}

@app.route('/api/scan', methods=['POST'])
def start_scan():
    data = request.json
    target_ip = data.get('target_ip')
    scan_description = data.get('scan_description')
    api_key = data.get('api_key')
    
    if not all([target_ip, scan_description, api_key]):
        return jsonify({"error": "Missing required parameters"}), 400
    
    scan_id = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Start scan in background
    socketio.start_background_task(
        run_scan, scan_id, target_ip, scan_description, api_key
    )
    
    return jsonify({"scan_id": scan_id}), 201

@app.route('/api/scan/<scan_id>', methods=['GET'])
def get_scan_status(scan_id):
    if scan_id in active_scans:
        return jsonify({
            "scan_id": scan_id,
            "status": active_scans[scan_id]["status"],
            "start_time": active_scans[scan_id]["start_time"],
            "target_ip": active_scans[scan_id]["target_ip"],
            "scan_description": active_scans[scan_id]["scan_description"]
        })
    else:
        return jsonify({"error": "Scan not found"}), 404

@app.route('/api/scan/<scan_id>/report', methods=['GET'])
def get_scan_report(scan_id):
    report_path = f"findings_report_{scan_id}.md"
    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            report_content = f.read()
        return jsonify({"report": report_content})
    else:
        return jsonify({"error": "Report not found"}), 404

def run_scan(scan_id, target_ip, scan_description, api_key):
    # Initialize WebSocket logger
    ws_logger = WebSocketLogger(scan_id)
    log_file_path = ws_logger.initialize_log_file(target_ip, scan_description)
    
    # Initialize agents
    strategy_generator = StrategyGenerator(api_key)
    senior_reviewer = SeniorReviewer(api_key)
    error_handler = ErrorHandler(api_key)
    execution_monitor = ExecutionMonitor(api_key)
    command_executor = CommandExecutor(api_key)
    report_writer = ReportWriter(api_key)
    
    # Wrap with WebSocket loggers
    strategy_generator = WebSocketAgent(strategy_generator, ws_logger)
    senior_reviewer = WebSocketAgent(senior_reviewer, ws_logger)
    error_handler = WebSocketAgent(error_handler, ws_logger)
    execution_monitor = WebSocketAgent(execution_monitor, ws_logger)
    command_executor = WebSocketAgent(command_executor, ws_logger)
    report_writer = WebSocketAgent(report_writer, ws_logger)
    
    # Track scan status
    active_scans[scan_id] = {
        "status": "running",
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target_ip": target_ip,
        "scan_description": scan_description
    }
    
    # Log start of scan
    ws_logger.log("System", json.dumps({
        "status": "started",
        "target_ip": target_ip,
        "scan_description": scan_description
    }))
    
    findings = []
    
    try:
        # Initial Strategy
        ws_logger.log("System", "Generating initial strategy...")
        strategy = strategy_generator.generate_strategy(target_ip, scan_description, log_file_path=log_file_path)
        findings.append({"strategy": strategy})
        
        while True:
            # Review Strategy
            ws_logger.log("System", "Reviewing strategy...")
            reviewed_strategy = senior_reviewer.review_strategy(strategy, scan_description, log_file_path=log_file_path)
            findings.append({"reviewed_strategy": reviewed_strategy})
            
            if reviewed_strategy["approved"]:
                # Execute Commands
                commands = strategy["strategy"]
                ws_logger.log("System", f"Executing commands: {json.dumps(commands)}")
                output = command_executor.execute_commands(
                    commands, target_ip, scan_description, 
                    error_handler, strategy_generator, execution_monitor, 
                    log_file_path=log_file_path
                )
                
                ws_logger.log("System", f"Command output complete")
                findings.append({"commands": commands, "output": output})
                
                # Review Output
                ws_logger.log("System", "Senior reviewer assessing results...")
                senior_reviewer_assessment = senior_reviewer.review_output(output, scan_description, log_file_path=log_file_path)
                findings.append({"senior_reviewer_assessment": senior_reviewer_assessment})
                
                if senior_reviewer_assessment["satisfactory"]:
                    ws_logger.log("System", "Scan completed. Client's requirements have been met.")
                    break
                else:
                    feedback = senior_reviewer_assessment["feedback"]
                    ws_logger.log("System", f"Updating strategy based on feedback: {feedback}")
                    strategy = strategy_generator.generate_strategy(
                        target_ip, scan_description, 
                        feedback=feedback, log_file_path=log_file_path
                    )
                    findings.append({"updated_strategy_based_on_feedback": strategy})
            else:
                feedback = reviewed_strategy["feedback"]
                ws_logger.log("System", f"Strategy not approved. Feedback: {feedback}")
                strategy = strategy_generator.generate_strategy(
                    target_ip, scan_description, 
                    feedback=feedback, log_file_path=log_file_path
                )
                findings.append({"updated_strategy_based_on_feedback": strategy})
        
        # Generate and review report
        findings_file = f"findings_{scan_id}.json"
        with open(findings_file, "w") as f:
            json.dump(findings, f, indent=2)
        
        ws_logger.log("System", "Generating findings report...")
        report = report_writer.generate_report(target_ip, scan_description, findings_file, log_file_path=log_file_path)
        
        while True:
            ws_logger.log("System", "Senior reviewer reviewing report...")
            senior_reviewer_review = senior_reviewer.review_report(report, log_file_path=log_file_path)
            findings.append({"senior_reviewer_review": senior_reviewer_review})
            
            if senior_reviewer_review["Report Approval"]:
                ws_logger.log("System", "Findings report has been approved by Senior Reviewer.")
                break
            else:
                feedback = senior_reviewer_review["feedback"]
                ws_logger.log("System", f"Report needs revision. Feedback: {feedback}")
                report = report_writer.generate_report(
                    target_ip, scan_description, findings_file, 
                    feedback=feedback, log_file_path=log_file_path
                )
        
        report_file = f"findings_report_{scan_id}.md"
        with open(report_file, "w") as f:
            f.write(report)
        
        ws_logger.log("System", json.dumps({
            "status": "completed",
            "report_file": report_file
        }))
        
        active_scans[scan_id]["status"] = "completed"
        
    except Exception as e:
        error_message = f"Error during scan: {str(e)}"
        ws_logger.log("System", json.dumps({
            "status": "error",
            "error": error_message
        }))
        active_scans[scan_id]["status"] = "error"
        
        # Try to save what we have
        try:
            findings_file = f"findings_{scan_id}.json"
            with open(findings_file, "w") as f:
                json.dump(findings, f, indent=2)
        except:
            pass

if __name__ == '__main__':
    # Create Logs directory if it doesn't exist
    os.makedirs("./Logs", exist_ok=True)
    
    # Start the server
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 