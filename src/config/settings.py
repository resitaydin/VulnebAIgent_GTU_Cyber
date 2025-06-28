"""
Configuration Settings for VulnebAIgent

Simple configuration management for the vulnerability scanning application.
"""

import os

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")
OPENAI_MODEL = "gpt-4.1"

# Default Scan Configuration
DEFAULT_TARGET_IP = "scanme.nmap.org"
DEFAULT_SCAN_DESCRIPTION = "find if this target is vulnerable to any exploit on port 22, only using nmap, nothing more"

# Directories
LOG_DIRECTORY = "./logs"
FINDINGS_FILE = "findings.json"
REPORT_FILE = "findings_report.md"

# Command timeout in seconds
COMMAND_TIMEOUT = 300 