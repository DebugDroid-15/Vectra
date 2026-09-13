"""
Vectra Command Line Interface (CLI) & Headless Execution Subsystem
"""

import sys
import os
import argparse
from typing import List, Optional
from .services import ExecutionService
from .logger import setup_logging, get_logger

def run_cli(args: Optional[List[str]] = None) -> int:
    setup_logging()
    logger = get_logger("cli")

    parser = argparse.ArgumentParser(description="Vectra Scientific Computing Platform CLI")
    parser.add_argument("--version", action="version", version="Vectra 1.0.0")
    parser.add_argument("--run", type=str, help="Execute a Vectra script (.m) in headless mode and exit.")
    parser.add_argument("--eval", type=str, help="Evaluate a Vectra command string and exit.")
    parser.add_argument("--no-gui", action="store_true", help="Force headless non-graphical execution.")

    parsed = parser.parse_args(args)
    exec_service = ExecutionService()

    if parsed.run:
        script_path = os.path.abspath(parsed.run)
        if not os.path.exists(script_path):
            print(f"Error: File not found '{script_path}'", file=sys.stderr)
            return 1
        try:
            logger.info(f"CLI Headless script execution: {script_path}")
            logs = exec_service.run_script_file(script_path)
            for log in logs:
                print(log)
            return 0
        except Exception as e:
            print(f"Execution Error: {e}", file=sys.stderr)
            return 1

    if parsed.eval:
        try:
            logger.info(f"CLI Evaluation: {parsed.eval}")
            logs = exec_service.execute_command(parsed.eval)
            for log in logs:
                print(log)
            return 0
        except Exception as e:
            print(f"Evaluation Error: {e}", file=sys.stderr)
            return 1

    # Interactive REPL mode in CLI
    print("Vectra Scientific Computing CLI REPL (v1.0.0)")
    print("Type 'exit' or 'quit' to exit.\n")
    while True:
        try:
            cmd = input(">> ").strip()
            if cmd.lower() in ("exit", "quit"):
                break
            if not cmd:
                continue
            logs = exec_service.execute_command(cmd)
            for log in logs:
                print(log)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Vectra CLI.")
            break
        except Exception as e:
            print(f"Error: {e}")

    return 0

if __name__ == "__main__":
    sys.exit(run_cli())

