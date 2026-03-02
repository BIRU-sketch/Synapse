from ..automations.openrouter_client import generate_chat_completion

def tool_selector(prompt: str)-> str:
    Task=('You are part of desktop automation Agent. Your role is to look at the prompt of the user and select the right tool to use.',
          'The tools that the agent can use include: bash(returning a windows bash program to get the task done) or the following  built in agent local tools: {tools}')
    response=generate_chat_completion(prompt)
    