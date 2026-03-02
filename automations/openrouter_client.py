import os
import re
from openai import OpenAI
from dotenv import load_dotenv


here = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dot = os.path.join(here, '.env')
if os.path.exists(dot):
    load_dotenv(dot)
def get_client():
    api_key=os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        raise RuntimeError('OPENROUTER_API_KEY environment variable is not set')
    client = OpenAI(api_key=api_key, base_url='https://openrouter.ai/api/v1')
    return client
def generate_chat_completion(prompt: str, model: str='google/gemma-3-27b-it', system_prompt: str | None=None):
    client = get_client()
    messages = []
    if system_prompt:
        messages.append({'role': 'system', 'content': system_prompt})
    else:
        messages.append({'role': 'user', 'content': prompt})
    resp = client.chat.completions.create(model=model, messages=messages)
    try:
        return resp.choices[0].message.content
    except Exception:
        return resp
def resolve_search_url(prompt:str):
    task=f"Provide a Json response identifying the item wanted and the site it can be found in for the following prompt: {prompt}.Only respond with the json. Do not add additional text."
    response=generate_chat_completion(task)
    json=json.loads(re.sub('''json|''','','response'))
    prompt2=f"Provide a single direct URL to {json.get('query')} on '{json.get('site')}'.f Respond with only the URL.No additional text."
    response=generate_chat_completion(prompt2)
    return response
def get_download_link(item:str):
    task=(f'Search the whole internet deeply and respond only with a direct download link for:{item}. ',
          f'Make sure it is from a trusted source,free to use, and Only respond with the direct url for download.',
          f'Do not add additional text. Only return the url.')
    response=generate_chat_completion(task)
    return response