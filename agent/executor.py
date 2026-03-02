from planner import plan_task
try:
    from tools.local_tools import run_shell,FileSystemTools
    from automations.openrouter_client import generate_chat_completion
except ImportError:
    from ..tools.local_tools import run_shell,FileSystemTools,Tasks
    from ..automations.openrouter_client import generate_chat_completion
prompt = "Move the skill-bridge2 folder to the Downloads directory."
