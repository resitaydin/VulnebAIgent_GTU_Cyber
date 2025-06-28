#!/usr/bin/env python3
"""
VulnebAIgent - Entry Point

This is the main entry point for the VulnebAIgent application.
It imports and runs the main function from the src.core.main module.

Authors: Reşit Aydın, Ahmet Hakan Sevinç
Course: CSE473 - Network Security
"""

import sys
import os

# Add the current directory to Python path to enable imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from src.core.main import main
    
    if __name__ == '__main__':
        main()
        
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure all dependencies are installed and the project structure is correct.")
    sys.exit(1)
except Exception as e:
    print(f"Error running application: {e}")
    sys.exit(1) 