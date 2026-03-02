from typing import Dict, Any, Optional, List
import json,re
try:
      from automations.openrouter_client import generate_chat_completion
except ImportError:
      from ..automations.openrouter_client import generate_chat_completion
def replan_task(error_message: str, failed_step_id: str) -> Dict[str, Any]:
      with open("chat_memory.json",'r') as f:
            original_chat_history = json.load(f)
      REPLANNER_PROMPT = (
    "You are Synapse Replanner.\n"
    "Your job is to repair failed automation plans logically and safely.\n"
    "You must return STRICT VALID JSON only.\n\n"

    "==================== CONTEXT ====================\n"
    "Execution Memory (Structured Previous Chat_log and suceessfull/ unsuccessfull actions ):\n"
    f"{original_chat_history}\n\n"

    "Failure Information:\n"
    f"Failed Step ID: {failed_step_id}\n"
    f"Error Message: {error_message}\n"
    "=================================================\n\n"

    "You must decide EXACTLY ONE strategy:\n"
    "1. continue        -> Fix the failing step only and proceed.\n"
    "2. undo_last       -> Undo the most recent successful step.\n"
    "3. undo_to_step    -> Undo back to a specific step id.\n"
    "4. restart         -> Discard current plan and generate a new one.\n"
    "5. exit            -> Only if task is impossible or unsafe.\n\n"

    "Important Decision Rules:\n"
    "- If failure is minor (e.g., wrong path, small typo), use 'continue'.\n"
    "- If system state may be inconsistent, use undo.\n"
    "- If core logic is flawed, use restart.\n"
    "- If task violates safety, permissions, or cannot be completed, use exit.\n"
    "- NEVER repeat a step that already failed with the same logic.\n"
    "- NEVER repeat steps already marked as successful.\n"
    "- Prefer minimal correction.\n"
    "- Avoid unnecessary restart.\n\n"

    "Return JSON in EXACT structure:\n\n"

    "{\n"
    '  "strategy": "continue | undo_last | undo_to_step | restart | exit",\n'
    '  "undo_until_step_id": "step_id_or_null",\n'
    '  "updated_plan": {\n'
    '      "plan_id": "string",\n'
    '      "mode": "tools | bash",\n'
    '      "steps": []\n'
    "  },\n"
    '  "explain": "short technical reasoning referencing failure"\n'
    "}\n\n"

    "Return JSON only. No markdown. No commentary."
    )
      try:
            response = generate_chat_completion(REPLANNER_PROMPT)
            return response
      except Exception as e:
            return {"strategy": "restart"}