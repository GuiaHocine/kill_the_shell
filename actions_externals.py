from models import ShellProcess

def execute_binary(process: ShellProcess, binary_name: str, child_pid: int, args: str = ""):
    """
    Handles ls, grep, nano, cat, ./script.sh, etc.
    All external binaries share this exact memory lifecycle.
    """
    # 1. Trigger the Kernel State Change
    child = process.fork_exect(child_pid, binary_name)
    
    # 2. Mock some terminal output based on the binary
    mock_output = f"Executing {binary_name}..."
    if binary_name == "ls":
        mock_output = "Desktop  Documents  Downloads  app.py"
    elif binary_name == "grep":
        mock_output = "(searching stream...)"
        
    return {
        "type": "EXTERNAL",
        "animation_steps": [
            {
                "step": 1, 
                "action": "FORK_PROCESS", 
                "pid": child.pid,
                "child_local": process.local_vars.copy(), 
                "child_env": process.env_vars.copy()
            },
            {
                "step": 2, 
                "action": "EXEC_BINARY", 
                "pid": child.pid,
                "binary_name": binary_name, 
                "child_local": child.local_vars.copy(), # Will be empty!
                "child_env": child.env_vars.copy()
            },
            {
                "step": 3,
                "action": "TERMINAL_OUTPUT",
                "output": mock_output
            },
            {
                "step": 4, 
                "action": "KILL_CHILD",
                "pid": child.pid
            }
        ]
    }
