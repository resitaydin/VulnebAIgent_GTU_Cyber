import json
from ..core.agent import Agent

class ReportWriter(Agent):
    def __init__(self, api_key):
        super().__init__("ReportWriter", api_key)

    def generate_report(self, target_ip, scan_description, findings_file, feedback=None, log_file_path=None):
        with open(findings_file, "r") as f:
            findings = json.load(f)

        system_message = "You are ReportWriter, an expert findings report writer. Your role is to generate a comprehensive and professional findings report based on the provided JSON file containing the vulnerability scan findings. The report should include an appropriate title, an executive summary, detailed findings for each vulnerability, and recommendations for remediation. Structure the report in a clear and concise manner, using Markdown formatting."
        
        user_message = f"Target IP: {target_ip}\nScan Description: {scan_description}\nFindings File: {json.dumps(findings, indent=2)}\n\nPlease generate a comprehensive findings report based on the provided vulnerability scan findings. Use Markdown formatting for the report."
        
        if feedback:
            user_message += f"\n\nFeedback from SeniorReviewer: {feedback}\n\nPlease update the findings report based on the provided feedback, ensuring that the report is comprehensive, professional, and addresses all the necessary aspects."

        report = self.generate_response("SeniorReviewer", user_message, system_message)
        self.add_to_chat_history("SeniorReviewer", "user", user_message)
        self.add_to_chat_history("SeniorReviewer", "assistant", report)
        self.print_agent_output(text=report, log_file_path=log_file_path)
        return report.strip()