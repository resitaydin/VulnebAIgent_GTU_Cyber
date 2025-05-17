import json
import os
from datetime import datetime
from Agents.strategy_generator import StrategyGenerator
from Agents.senior_reviewer import SeniorReviewer
from Agents.error_handler import ErrorHandler
from Agents.execution_monitor import ExecutionMonitor
from Agents.command_executor import CommandExecutor
from Agents.report_writer import ReportWriter

API_KEY = os.getenv("OPENAI_API_KEY") or 'YOUR_API_KEY'

def initialize_log_file(target_ip, scan_description):
    log_directory = "./Logs"
    os.makedirs(log_directory, exist_ok=True)
    
    timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    log_file_name = f"log-{timestamp}.json"
    log_file_path = os.path.join(log_directory, log_file_name)
    
    log_data = {
        "target_ip": target_ip,
        "scan_description": scan_description,
        "output": []
    }
    
    with open(log_file_path, "w") as log_file:
        json.dump(log_data, log_file, indent=2)
    
    return log_file_path

def main():
    target_ip = "scanme.nmap.org"
    scan_description = "find if this target is vulnerable to any exploit on port 22, only using nmap, nothing more"
    log_file_path = initialize_log_file(target_ip, scan_description)
    
    strategy_generator = StrategyGenerator(API_KEY)
    senior_reviewer = SeniorReviewer(API_KEY)
    error_handler = ErrorHandler(API_KEY)
    execution_monitor = ExecutionMonitor(API_KEY)
    command_executor = CommandExecutor(API_KEY)
    report_writer = ReportWriter(API_KEY)
    
    findings = []

    print("Initial Strategy:")
    strategy = strategy_generator.generate_strategy(target_ip, scan_description, log_file_path=log_file_path)
    findings.append({"strategy": strategy})

    while True:
        reviewed_strategy = senior_reviewer.review_strategy(strategy, scan_description, log_file_path=log_file_path)
        findings.append({"reviewed_strategy": reviewed_strategy})

        if reviewed_strategy["approved"]:
            commands = strategy["strategy"]
            output = command_executor.execute_commands(commands, target_ip, scan_description, error_handler, strategy_generator, execution_monitor, log_file_path=log_file_path)
            print("Command Output:")
            print(output)
            findings.append({"commands": commands, "output": output})
            print("SeniorReviewer's Thoughts on the scan result:")
            senior_reviewer_assessment = senior_reviewer.review_output(output, scan_description, log_file_path=log_file_path)
            findings.append({"senior_reviewer_assessment": senior_reviewer_assessment})

            if senior_reviewer_assessment["satisfactory"]:
                print("Scan completed. Client's requirements have been met.")
                break
            else:
                feedback = senior_reviewer_assessment["feedback"]
                strategy = strategy_generator.generate_strategy(target_ip, scan_description, feedback=feedback, log_file_path=log_file_path)
                findings.append({"updated_strategy_based_on_feedback": strategy})
                print("Updated strategy based on SeniorReviewer's feedback:")
        else:
            feedback = reviewed_strategy["feedback"]
            print("SeniorReviewer's feedback:")
            print("Updated strategy based on SeniorReviewer's feedback:")
            strategy = strategy_generator.generate_strategy(target_ip, scan_description, feedback=feedback, log_file_path=log_file_path)
            findings.append({"updated_strategy_based_on_feedback": strategy})

    findings_file = "findings.json"
    with open(findings_file, "w") as f:
        json.dump(findings, f, indent=2)

    print("Findings Report:")
    report = report_writer.generate_report(target_ip, scan_description, findings_file, log_file_path=log_file_path)

    while True:
        senior_reviewer_review = senior_reviewer.review_report(report, log_file_path=log_file_path)
        findings.append({"senior_reviewer_review": senior_reviewer_review})
        print("SeniorReviewer's Review:")
        if senior_reviewer_review["Report Approval"]:
            print("Findings report has been approved by SeniorReviewer.")
            break
        else:
            feedback = senior_reviewer_review["feedback"]
            print("SeniorReviewer's feedback:")
            report = report_writer.generate_report(target_ip, scan_description, findings_file, feedback=feedback, log_file_path=log_file_path)
            print("Updated Findings Report:")

    report_file = "findings_report.md"
    with open(report_file, "w") as f:
        f.write(report)
    print(f"Findings report saved as {report_file}")

if __name__ == '__main__':
    main()
