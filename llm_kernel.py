import json
import os
from openai import OpenAI
from models import ShellProcess
from dotenv import load_dotenv
load_dotenv()

API_KEY=os.environ.get("API_KEY")
MODEL_NAME=os.environ.get("MODEL")
BASE_URL=os.environ.get("BASE_URL")

# Initialize the OpenAI client (Ensure API_KEY is in your environment variables)
client = OpenAI(api_key=API_KEY,base_url=BASE_URL)

def process_with_llm(command: str, process: ShellProcess, next_pid: int):
    # 1. Serialize the current state so the LLM has perfect context
    state_context = {
        "pid": process.pid,
        "local_vars": process.local_vars,
        "env_vars": process.env_vars,
        "current_directory": process.env_vars.get("PWD", "/")
    }

    # 2. The "Dictator" System Prompt
    system_prompt = f"""
    You are a real-time Linux Kernel state simulator.
    Your ONLY job is to calculate how a shell command modifies the Virtual Memory Space (VMS) or process tree.
    
    CURRENT STATE:
    {json.dumps(state_context)}

    RULES:
    1. You must respond with a raw, valid JSON object ONLY. No markdown, no conversational text.
    2. The JSON must contain a root key called "type" (string) and "animation_steps" (array of objects).
    3. You may ONLY use the following actions for the steps:
       - UPDATE_PARENT_LOCAL (requires "data" dict)
       - UPDATE_PARENT_ENV (requires "data" dict)
       - FORK_PROCESS (requires "pid", "child_local", "child_env")
       - EXEC_BINARY (requires "pid", "binary_name", "child_local", "child_env")
       - KILL_CHILD (requires "pid")
       - TERMINAL_OUTPUT (requires "output" string)

    EXAMPLES:
    If the user types: `export DATABASE_URL=localhost`
    {{
      "type": "LLM_BUILTIN",
      "animation_steps": [
        {{"step": 1, "action": "UPDATE_PARENT_ENV", "data": {{"USER": "ubuntu", "PWD": "/home/ubuntu", "DATABASE_URL": "localhost"}}}},
        {{"step": 2, "action": "TERMINAL_OUTPUT", "output": ""}}
      ]
    }}

    If the user types an external command like: `ls`
    {{
      "type": "LLM_EXTERNAL",
      "animation_steps": [
        {{"step": 1, "action": "FORK_PROCESS", "pid": {next_pid}, "child_local": {json.dumps(process.local_vars)}, "child_env": {json.dumps(process.env_vars)}}},
        {{"step": 2, "action": "EXEC_BINARY", "pid": {next_pid}, "binary_name": "ls", "child_local": {{}}, "child_env": {json.dumps(process.env_vars)}}},
        {{"step": 3, "action": "TERMINAL_OUTPUT", "output": "file1.txt  file2.txt  script.sh"}},
        {{"step": 4, "action": "KILL_CHILD", "pid": {next_pid}}}
      ]
    }}
    """

    try:
        # 3. Call OpenAI using the prompt and force JSON mode
        response = client.chat.completions.create(
            model=MODEL_NAME, # Extremely fast and cost-effective
            response_format={"type": "json_object"},
            reasoning_effort=None,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Execute this command: {command}"}
            ],

            temperature=0.1 # Keep it deterministic and logical
        )
        
        # 4. Parse the response
        packet_string = response.choices[0].message.content
        packet = json.loads(packet_string)
        
        # 5. Sync the LLM's hallucinated state back to our actual Python object
        sync_backend_state(process, packet)

        return packet

    except Exception as e:
        return {
            "type": "ERROR",
            "animation_steps": [
                {"step": 1, "action": "TERMINAL_OUTPUT", "output": f"Kernel Panic (OpenAI): {str(e)}"}
            ]
        }

def sync_backend_state(process: ShellProcess, packet: dict):
    """
    If the LLM decides the parent's environment or local variables changed,
    we MUST update our actual Python state so the next command has the right context!
    """
    for step in packet.get("animation_steps", []):
        if step["action"] == "UPDATE_PARENT_LOCAL":
            process.local_vars = step["data"]
        elif step["action"] == "UPDATE_PARENT_ENV":
            process.env_vars = step["data"]