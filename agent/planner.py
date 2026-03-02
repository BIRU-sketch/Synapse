from typing import Dict, Any
import json,re
try:
      from automations.openrouter_client import generate_chat_completion
      from tools.local_tools import tools_list
except ImportError:
      from ..automations.openrouter_client import generate_chat_completion
      from ..tools.local_tools import tools_list
def plan_task(user_request: str) -> Dict[str, Any]:
      system_prompt = f"""You are Synapse Planner, an AI that converts human instructions into a structured plan for automating tasks on a desktop computer.Your response **MUST BE VALID JSON ONLY**. No explanations outside the JSON.
If you include any extra text, it will break the automation.
## Available tools: 
"""+tools_list()+"""
Each tool can be used by including it in a step with the proper parameters. You may also choose "bash" mode for commands that are not covered by tools. Always prefer a safe tool over bash when possible.
## Plan schema
Return a JSON object with the following structure:
{{
  "plan_id": "a unique identifier string",
  "mode": "tools" or "bash",
  "steps": [
    {{
      "id": "step identifier",
      "tool": "tool name (or 'bash' if using a shell command)",
      "params": {{}},
      "precondition": "optional description of required state before execution, or null",
      "undo": "dictionary describing how to reverse this step"
    }}
  ],
  "explain": "short human-friendly summary of what this plan will do"
}}
- Each step must be atomic (do one thing only).  
- Params should be as specific as possible. For file/folder paths, use absolute paths or placeholders like {downloads}.  
- Use `undo` only for safe reversible actions. For destructive steps like delete, leave undo as null.  
- `mode` at top level is "tools" if all steps use tools, otherwise "bash".
## User request
"""+user_request+"""
Return the plan as valid JSON only. Do not add any text outside the JSON.
"""
      try:
            response = generate_chat_completion(system_prompt)
            match = re.search(r"```(?:json)?\s*(.*?)\s*```", response, re.DOTALL)
            json_str = json.loads(match.group(1) if match else None)
            with open('chat_memory.json', 'w') as f:
                  json.dump(json_str, f, indent=4)
            return json_str
      except Exception as e:
            return None
plan_task("Move the skill-bridge2 folder to the Downloads directory.")