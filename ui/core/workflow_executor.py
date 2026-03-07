import json
import subprocess
from pathlib import Path
from typing import Dict, Any


def execute_workflow(workflow_name: str) -> Dict[str, Any]:

    workflow_path = Path("workflows") / f"{workflow_name}.json"

    if not workflow_path.exists():
        return {"status": "error", "message": "Workflow not found"}

    with open(workflow_path, "r", encoding="utf-8") as f:
        workflow = json.load(f)

    steps = workflow.get("steps", [])

    results = []

    for step in steps:

        step_type = step.get("type", "").lower()

        if step_type in ("shell", "bash"):

            command = step.get("params", {}).get("command", "")

            if not command:
                continue

            print(f"Running command: {command}")

            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True
                    )
                step_result = {
                    "command": command,
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr
                    }
                results.append(step_result)

                if result.returncode != 0:
                    print(f"Command failed: {command}")
                    break

            except Exception as e:
                print(f"Execution error: {e}")
                break

        else:
            print(f"Skipping unsupported step type: {step_type}")

    return {
        "status": "completed",
        "results": results
    }