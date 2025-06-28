"""
VulnebAIgent - Automated Vulnerability Scanning with Agentic AI

This is the main entry point for the vulnerability scanning application.
It orchestrates multiple AI agents to perform comprehensive vulnerability assessments.

Authors: Reşit Aydın - Ahmet Hakan Sevinç
Course: CSE473 - Network Security
"""

import json
import os
from datetime import datetime
from ..agents.strategy_generator import StrategyGenerator
from ..agents.senior_reviewer import SeniorReviewer
from ..agents.error_handler import ErrorHandler
from ..agents.execution_monitor import ExecutionMonitor
from ..agents.command_executor import CommandExecutor
from ..agents.report_writer import ReportWriter
from ..config.settings import OPENAI_API_KEY, LOG_DIRECTORY

# Get OpenAI API key from configuration
API_KEY = OPENAI_API_KEY

def initialize_log_file(target_ip, scan_description):
    """
    Initialize a timestamped log file for the vulnerability scan.
    
    Args:
        target_ip (str): The target IP address being scanned
        scan_description (str): Description of the scan being performed
        
    Returns:
        str: Path to the created log file
        
    Creates a JSON log file in the Logs directory with initial scan metadata.
    """
    log_directory = LOG_DIRECTORY
    os.makedirs(log_directory, exist_ok=True)
    
    # Create timestamp for unique log file naming
    timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    log_file_name = f"log-{timestamp}.json"
    log_file_path = os.path.join(log_directory, log_file_name)
    
    # Initialize log data structure
    log_data = {
        "target_ip": target_ip,
        "scan_description": scan_description,
        "output": []
    }
    
    # Create the log file with initial data
    with open(log_file_path, "w") as log_file:
        json.dump(log_data, log_file, indent=2)
    
    return log_file_path

def main():
    """
    Main function that orchestrates the vulnerability scanning process.
    
    This function coordinates all AI agents to perform a comprehensive vulnerability scan:
    1. Initializes all agents (StrategyGenerator, SeniorReviewer, etc.)
    2. Generates and reviews scanning strategies
    3. Executes commands and monitors output
    4. Handles errors and generates reports
    5. Iterates until satisfactory results are achieved
    
    The process continues until the SeniorReviewer approves the final report.
    """
    # Configuration - modify these values for different targets/scans
    target_ip = "scanme.nmap.org"
    scan_description = "find if this target is vulnerable to any exploit on port 22, only using nmap, nothing more"
    
    # Initialize logging for this scan session
    log_file_path = initialize_log_file(target_ip, scan_description)
    
    # Initialize all AI agents with OpenAI API key
    strategy_generator = StrategyGenerator(API_KEY)
    senior_reviewer = SeniorReviewer(API_KEY)
    error_handler = ErrorHandler(API_KEY)
    execution_monitor = ExecutionMonitor(API_KEY)
    command_executor = CommandExecutor(API_KEY)
    report_writer = ReportWriter(API_KEY)
    
    # Track all findings and agent interactions
    findings = []

    # Phase 1: Generate initial scanning strategy
    print("Initial Strategy:")
    strategy = strategy_generator.generate_strategy(target_ip, scan_description, log_file_path=log_file_path)
    findings.append({"strategy": strategy})

    # Phase 2: Main scanning loop - continue until satisfactory results
    while True:
        # Have SeniorReviewer evaluate the proposed strategy
        reviewed_strategy = senior_reviewer.review_strategy(strategy, scan_description, log_file_path=log_file_path)
        findings.append({"reviewed_strategy": reviewed_strategy})

        if reviewed_strategy["approved"]:
            # Strategy approved - execute the commands
            commands = strategy["strategy"]
            output = command_executor.execute_commands(commands, target_ip, scan_description, error_handler, strategy_generator, execution_monitor, log_file_path=log_file_path)
            print("Command Output:")
            print(output)
            findings.append({"commands": commands, "output": output})
            
            # Have SeniorReviewer assess the scan results
            print("SeniorReviewer's Thoughts on the scan result:")
            senior_reviewer_assessment = senior_reviewer.review_output(output, scan_description, log_file_path=log_file_path)
            findings.append({"senior_reviewer_assessment": senior_reviewer_assessment})

            if senior_reviewer_assessment["satisfactory"]:
                # Scan requirements met - proceed to report generation
                print("Scan completed. Client's requirements have been met.")
                break
            else:
                # Need additional scanning - generate new strategy based on feedback
                feedback = senior_reviewer_assessment["feedback"]
                strategy = strategy_generator.generate_strategy(target_ip, scan_description, feedback=feedback, log_file_path=log_file_path)
                findings.append({"updated_strategy_based_on_feedback": strategy})
                print("Updated strategy based on SeniorReviewer's feedback:")
        else:
            # Strategy not approved - revise based on feedback
            feedback = reviewed_strategy["feedback"]
            print("SeniorReviewer's feedback:")
            print("Updated strategy based on SeniorReviewer's feedback:")
            strategy = strategy_generator.generate_strategy(target_ip, scan_description, feedback=feedback, log_file_path=log_file_path)
            findings.append({"updated_strategy_based_on_feedback": strategy})

    # Phase 3: Save findings and generate report
    findings_file = "findings.json"
    with open(findings_file, "w") as f:
        json.dump(findings, f, indent=2)

    # Generate initial vulnerability report
    print("Findings Report:")
    report = report_writer.generate_report(target_ip, scan_description, findings_file, log_file_path=log_file_path)

    # Phase 4: Report review and refinement loop
    while True:
        # Have SeniorReviewer evaluate the generated report
        senior_reviewer_review = senior_reviewer.review_report(report, log_file_path=log_file_path)
        findings.append({"senior_reviewer_review": senior_reviewer_review})
        print("SeniorReviewer's Review:")
        
        if senior_reviewer_review["Report Approval"]:
            # Report approved - we're done
            print("Findings report has been approved by SeniorReviewer.")
            break
        else:
            # Report needs improvement - regenerate with feedback
            feedback = senior_reviewer_review["feedback"]
            print("SeniorReviewer's feedback:")
            report = report_writer.generate_report(target_ip, scan_description, findings_file, feedback=feedback, log_file_path=log_file_path)
            print("Updated Findings Report:")

    # Phase 5: Save final report to file
    report_file = "findings_report.md"
    with open(report_file, "w") as f:
        f.write(report)
    print(f"Findings report saved as {report_file}")

if __name__ == '__main__':
    main()
