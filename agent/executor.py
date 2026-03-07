from agent.planner import plan_task
from agent.replaner import replan_task
import os,subprocess
try:
    from tools.local_tools import run_shell,FileSystemTools
    from automations.openrouter_client import generate_chat_completion
except ImportError:
    from ..tools.local_tools import run_shell,FileSystemTools,Tasks
    from ..automations.openrouter_client import generate_chat_completion
prompt = "use nmap to scan the local network"
def execute_task(prompt: str):
    plan=plan_task(prompt)
    mode=plan.get('mode') or None
    steps=plan.get('steps') or None
    if mode == 'shell' or mode == 'bash':
        for step in steps:
            id=step.get('id')
            bash_command=step.get('params').get('command')
            if bash_command.startswith('start'):
                try:
                    result=subprocess.run(bash_command,shell=True,capture_output=True,text=True,check=True)
                except subprocess.CalledProcessError:
                    print('failed to execute command')
            else:    
                result=subprocess.run(bash_command,shell=True,capture_output=True,text=True,check=True)
                if result.stdout == 0:
                    continue
                else:
                    replan_result=replan_task(result,id)
                    execute_task(replan_result)
        return {'status':'success!'}
    elif mode == 'tools':
        for step in steps:
            params = step.get('params')
            tool = step.get('tool')
            if tool == 'move_file':
                source = params.get('source_path')
                destination = params.get('destination_path')
                result=FileSystemTools.move_file(source, destination)
            elif tool == 'create_file':
                FileSystemTools.create_file(params.get('path'))
            elif tool == 'overwrite_file':
                FileSystemTools.overwrite_file(params.get('path'), params.get('content'))
            elif tool == 'delete_file':
                FileSystemTools.delete_file(params.get('path'))
            else: 
                print(f"Unknown tool: {tool}")
    else:
        return {'status': 'error', 'reason':'Check you internet connection and try again!'}
execute_task(prompt)