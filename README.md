# VulnebAIgent - Automated Vulnerability Scanning with Agentic AI

## 📖 Project Description

This project demonstrates an automated vulnerability scanning system using an Agentic AI approach. The system consists of multiple AI agents that collaborate to strategize, generate commands, and execute scans based on the client's description, without the need for human intervention.

VulnebAIgent leverages the power of Large Language Models (LLMs) to create an intelligent, adaptive vulnerability assessment framework. The multi-agent architecture allows for specialized roles, collaborative decision-making, and iterative refinement of scanning strategies based on real-time feedback.

**Key Goals:**
- Automate complex vulnerability scanning workflows
- Provide intelligent strategy generation and adaptation
- Enable collaborative AI agents for comprehensive security assessment
- Generate detailed, professional vulnerability reports
- Offer both CLI and web-based interfaces for different use cases

Please note that this project serves as a proof of concept, and not everything might work seamlessly. It's important to keep in mind that commands or scripts that are interactive and require user input, such as `msfconsole`, may not function as intended within this framework.

## 🛠️ Installation Instructions

### Prerequisites

**System Requirements:**
- Linux (preferably Kali Linux) or Windows with WSL
- Python 3.13 or higher
- OpenAI API key
- Git for cloning the repository

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/VulnebAIgent.git
cd VulnebAIgent
```

### Project Structure

```
VulnebAIgent/
├── src/                    # Source code
│   ├── agents/            # AI agent implementations
│   ├── core/              # Core functionality (main, base agent)
│   ├── utils/             # Utility functions
│   └── config/            # Configuration files
├── tests/                 # Test cases
├── docs/                  # Documentation
├── web-project/           # Web interface
├── logs/                  # Log files (created automatically)
├── main.py               # Application entry point
├── requirements.txt      # Dependencies
└── README.md            # This file
```

### Step 2: Install Security Tools (Recommended for Linux/Kali)

Before running this project, it is recommended to install the `kali-linux-default` metapackage, which includes a set of tools commonly used for penetration testing and vulnerability scanning.

**Option A: Using apt (Kali Linux)**
```bash
# Update your Kali Linux system
sudo apt update
sudo apt full-upgrade -y

# Install the kali-linux-default metapackage
sudo apt install -y kali-linux-default
```

**Option B: Using kali-tweaks**
1. Run `kali-tweaks`
2. Navigate to the "Metapackages" tab
3. Select the desired metapackages (e.g., `kali-linux-default`)
4. Click "Apply" and then "OK"
5. Supply your password when prompted

For more information on Kali Linux metapackages, refer to the [official documentation](https://www.kali.org/docs/general-use/metapackages/).

### Step 3: Install Python Dependencies

**Option A: Using uv (Recommended)**
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

**Option B: Using pip**
```bash
# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure OpenAI API Key

This project requires an OpenAI API key to function properly. The code is currently configured to use the `gpt-4.1` model, but you can modify it to use any other available model.

**To obtain an API key:**
1. Sign up for an account at [OpenAI](https://www.openai.com/) if you haven't already
2. Go to the [API Keys](https://platform.openai.com/account/api-keys) page in your account dashboard
3. Click on "Create new secret key" and copy the generated key

**Configuration Options:**

**Option A: Environment Variable (Recommended)**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

**Option B: Direct Assignment**
Edit the `main.py` file and set the `API_KEY` variable:
```python
API_KEY = "your-api-key-here"
```

**Note:** Using the OpenAI API incurs costs based on the number of tokens processed. Make sure to review the [pricing](https://openai.com/pricing) and set up appropriate limits and monitoring for your usage.

### Step 5: Install Web Interface Dependencies (Optional)

If you want to use the web interface:

**Backend:**
```bash
cd web-project/backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd web-project/frontend
npm install
```

# **WARNING**

Please be aware that this script will execute commands on the system without prompting for authorization. Running this script implies that you grant permission for all commands suggested by the StrategyGenerator. Exercise caution and ensure that you fully understand the implications before proceeding.

Note: This project is designed to run on Linux.

## Overview

The vulnerability scanning process is automated through the coordination of several AI agents, each with specific roles and responsibilities:

- **StrategyGenerator**: Generates the initial strategy and provides input when needed.
- **SeniorReviewer**: Reviews strategies, command outputs, and the final report.
- **ErrorHandler**: Handles error scenarios and suggests fixes.
- **ExecutionMonitor**: Monitors the command execution output and determines if additional input is required.
- **CommandExecutor**: Executes the commands generated by the agents.
- **ReportWriter**: Generates the final findings report.

The agents communicate with each other, exchanging information and feedback to iteratively refine the scanning process until a satisfactory result is achieved.

### Flowchart

![diagram](https://github.com/salah9003/Automated-Vulnerability-Scanning-with-Agentic-AI/assets/81641886/93a9fc04-1e7a-42c6-a5c3-d17167de1473)

## ▶️ Usage Examples

### Basic CLI Usage

**1. Run the default scan:**
```bash
python main.py
```

**2. Using uv:**
```bash
uv run python main.py
```

### Customizing Scan Parameters

Edit the `main.py` file to customize your scan:

```python
def main():
    target_ip = "your-target-ip-here"  # Change this
    scan_description = "Your custom scan description"  # Change this
    # ... rest of the code
```

**Example configurations:**
```python
# Example 1: Basic port scan
target_ip = "scanme.nmap.org"
scan_description = "Perform a comprehensive port scan to identify open services"

# Example 2: Web application scan
target_ip = "192.168.1.100"
scan_description = "Scan for web application vulnerabilities on ports 80 and 443"

# Example 3: SSH-specific scan
target_ip = "10.0.0.5"
scan_description = "Check for SSH vulnerabilities and misconfigurations on port 22"
```

### Web Interface Usage

**1. Start the backend server:**
```bash
cd web-project/backend
uv run app.py
```

**2. Start the frontend (in a new terminal):**
```bash
cd web-project/frontend
npm start
```

**3. Access the web interface:**
Open your browser and navigate to `http://localhost:3000`

### Sample Input/Output

**Sample Input:**
- Target IP: `scanme.nmap.org`
- Scan Description: `"Find vulnerabilities on port 22 using nmap"`

**Sample Output:**
The scanning process will:
1. Generate an initial strategy using StrategyGenerator
2. Review the strategy with SeniorReviewer
3. Execute commands through CommandExecutor
4. Monitor execution with ExecutionMonitor
5. Handle any errors with ErrorHandler
6. Generate a comprehensive report with ReportWriter

**Expected Files Generated:**
- `findings.json` - Structured scan results
- `findings_report.md` - Human-readable report
- `Logs/log-DD-MM-YYYY-HH-MM-SS.json` - Detailed execution log

The scanning process will continue until a satisfactory result is achieved or if the agents determine that no further actions are required. All findings and outputs are logged and stored in the `Logs` directory.

### Running Tests

To verify that the installation is working correctly, you can run the included test suite:

```bash
# Run all tests
python tests/run_tests.py

# Run specific test file
python tests/test_agents.py

# Run tests with verbose output
python -m unittest discover tests -v
```

### Findings Report

The `findings_report.md` file, generated by ReportWriter, provides a comprehensive overview of the vulnerability scanning results.

## Configuration

The main configuration options can be found in the `main.py` file:

- `target_ip`: Specify the target IP address for the vulnerability scan.
- `scan_description`: Provide a description of the desired scan to guide the agents.

## Logging

The system generates log files in the `Logs` directory, capturing the outputs, findings, and agent interactions during the scanning process.

## 🧩 Troubleshooting

### Common Issues and Solutions

**1. OpenAI API Key Issues**
- **Error**: `openai.AuthenticationError` or `Invalid API key`
- **Solution**: 
  - Verify your API key is correct
  - Check that the environment variable is set: `echo $OPENAI_API_KEY`
  - Ensure you have sufficient credits in your OpenAI account

**2. Permission Denied Errors**
- **Error**: `Permission denied` when executing commands
- **Solution**: 
  - Run with appropriate privileges: `sudo python main.py`
  - Ensure user has permission to execute security tools
  - Check file permissions: `chmod +x main.py`

**3. Command Not Found Errors**
- **Error**: `nmap: command not found` or similar
- **Solution**: 
  - Install missing security tools: `sudo apt install nmap`
  - Install the full Kali metapackage: `sudo apt install kali-linux-default`
  - Verify PATH includes tool directories

**4. Interactive Command Issues**
- **Error**: Commands hang or don't respond
- **Solution**: 
  - Some interactive tools like `msfconsole` may not work properly
  - Use non-interactive alternatives when possible
  - Check the scan description to avoid interactive tools

**5. Web Interface Connection Issues**
- **Error**: Cannot connect to backend or frontend
- **Solution**: 
  - Ensure both backend (port 5000) and frontend (port 3000) are running
  - Check firewall settings
  - Verify correct URLs in frontend configuration

**6. Python Version Compatibility**
- **Error**: `SyntaxError` or import errors
- **Solution**: 
  - Ensure Python 3.13+ is installed: `python --version`
  - Use virtual environment to avoid conflicts
  - Install dependencies with correct Python version

**7. Memory or Performance Issues**
- **Error**: System slowdown or out of memory
- **Solution**: 
  - Monitor system resources during scans
  - Reduce scan scope for large networks
  - Close unnecessary applications
  - Consider running on a dedicated system

### Getting Help

If you encounter issues not covered here:
1. Check the log files in the `Logs/` directory for detailed error information
2. Review the `findings.json` file for agent interactions
3. Ensure all prerequisites are properly installed
4. Try running with verbose output for debugging

## Why an Agentic AI Approach Was Used

Recent research has demonstrated promising results in utilizing multi-agent systems based on Large Language Models (LLMs) for solving various complex tasks[\[1\]](https://arxiv.org/abs/2308.10848). The agentic AI approach, where multiple autonomous agents collaborate to strategize, generate commands, and execute scans, offers several key benefits over relying on a single AI agent:

1. **Specialization and division of labor**: Each agent in the system can specialize in a particular area (e.g., strategy generation, error handling, command execution), allowing them to develop deep expertise and perform their roles more effectively[\[1\]](https://arxiv.org/abs/2308.10848)[\[2\]](https://arxiv.org/abs/2307.07924). This division of labor mirrors how human teams tackle complex projects.

2. **Improved collaboration and problem-solving**: By enabling interactions and information sharing between diverse specialized agents, the overall system gains enhanced capabilities to understand requirements, decompose problems, explore multiple solutions, and adapt to changing conditions[\[1\]](https://arxiv.org/abs/2308.10848)[\[3\]](https://arxiv.org/abs/2402.16713). This collaborative approach has been shown to boost problem-solving accuracy and efficiency.

3. **Robustness and adaptability**: With multiple agents involved, the system can be more robust to errors or limitations of any single agent[\[3\]](https://arxiv.org/abs/2402.16713). If one agent struggles, others can help compensate. Moreover, the multi-agent system can dynamically adjust roles, goals, and plans based on feedback and changing circumstances[\[1\]](https://arxiv.org/abs/2308.10848).

4. **Scalability**: The agentic AI approach provides a scalable framework for tackling increasingly complex and open-ended problems that would overwhelm a single agent[1]. New specialized agents can be added to expand the system's capabilities as needed.

5. **Alignment with real-world problem-solving**: Many real-world tasks, like vulnerability scanning, intrinsically involve multiple parties (e.g., scanners, strategists, reviewers) working together. The multi-agent approach more closely mirrors this reality compared to a single generalist agent[\[2\]](https://arxiv.org/abs/2307.07924).

While research on agentic AI systems is still in early stages, results so far point to their potential to enable more sophisticated, flexible, and effective problem-solving than single-agent approaches. As the technology matures, agentic AI could become an increasingly powerful paradigm to tackle complex challenges in cybersecurity and beyond.

Citations:

[1] Chen, Y., Perez, Y., & Shoham, Y. (2023). AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors in Agents. arXiv preprint arXiv:2308.10848.
https://arxiv.org/abs/2308.10848

[2] Quan, A., Jiang, L., Bing, L., & Lyu, M. R. (2023). Communicative Agents for Software Development. arXiv preprint arXiv:2307.07924.
https://arxiv.org/abs/2307.07924

[3] Navigating Complexity: Orchestrated Problem Solving with Multi-Agent LLMs. (2024).
https://arxiv.org/abs/2402.16713

## Differences Between This Project and Automatic Vulnerability Scanners

1. Multi-agent collaboration: This project uses multiple specialized AI agents that work together, while most scanners are monolithic systems.

2. Adaptability: The agents iteratively refine the scanning strategy based on feedback and results, while traditional scanners follow a fixed, linear process.

3. Natural language understanding: The agents can interpret natural language descriptions to guide the scanning process, while scanners typically require structured configurations.

4. Contextual decision-making: The agents consider the context and results of each step to make decisions, while scanners simply execute a predefined set of checks.

This project leverages the context of previous scan results to determine the next logical scan to perform. The agents, particularly SeniorReviewer, review the output of each command and provide feedback on whether the results are satisfactory or if additional scans are needed. This iterative, context-aware approach allows the system to dynamically adapt the scanning process based on the findings at each stage, ensuring a more comprehensive and targeted vulnerability assessment.

## 🤝 Acknowledgments

**Course Information:**
- **Course**: CSE473 - Network Security
- **Instructor**: Dr. Salih Sarp
- **Institution**: Gebze Technical University - Department of Computer Engineering
- **Academic Year**: 2025

**Contributors:**
- Reşit Aydın
- Ahmet Hakan Sevinç

**Special Thanks:**
- OpenAI for providing the GPT models that power the AI agents
- The Kali Linux team for the comprehensive security tool suite
- The open-source community for the various libraries and tools used
- Research papers and publications that inspired the multi-agent architecture
- github:salah9003 for providing a baseline for this project.

**Research Citations:**
This project was inspired by recent research in multi-agent systems and LLM collaboration:
- Chen, Y., Perez, Y., & Shoham, Y. (2023). AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors in Agents
- Quan, A., Jiang, L., Bing, L., & Lyu, M. R. (2023). Communicative Agents for Software Development
- Various research papers on multi-agent LLM systems and their applications in cybersecurity

## 📄 File Structure Reference

For detailed information about each file in this project, please refer to:
- `docs/FILE_OVERVIEW.md` - Comprehensive explanation of all project files
- `SampleRun.md` - Example execution and sample outputs
- `web-project/README.md` - Web interface specific documentation

## Disclaimer

This project is intended for educational and research purposes only. The authors and contributors are not responsible for any misuse or damage caused by the use of this system. Always obtain proper authorization before performing vulnerability scans on any target system.

**Legal Notice**: This tool should only be used on systems you own or have explicit permission to test. Unauthorized vulnerability scanning may be illegal in your jurisdiction.
