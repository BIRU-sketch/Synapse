import os
from dotenv import load_dotenv
here = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dot=os.path.join(here,'.env')
if os.path.exists(dot):
    load_dotenv(dot)
DEFAULT_RESTRICTIONS = ['rm', 'shutdown', 'reboot', 'poweroff', 'format', 'del ', 'erase', ':(){', 'mkfs', 'dd ']
def load_restrictions() -> list[str]:
    s = os.getenv('AGENT_RESTRICTIONS', '')
    if not s:
        return DEFAULT_RESTRICTIONS.copy()
    s+=DEFAULT_RESTRICTIONS
    return [r.strip() for r in s.split(',') if r.strip()]
def check_safe_shell(cmd: str, restrictions: list[str]) -> bool:
    lower = cmd.lower()
    for bad in restrictions:
        if bad in lower:
            return False
    return True
