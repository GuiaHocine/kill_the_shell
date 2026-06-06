from models import ShellProcess

def builtin_cd(process: ShellProcess, path: str):
    # In a real app you'd resolve paths, here we just update the env var
    new_path = path if path else "/home/ubuntu"
    process.env_vars["PWD"] = new_path
    
    return {
        "type": "INTERNAL",
        "animation_steps": [
            {"step": 1, "action": "UPDATE_PARENT_ENV", "data": process.env_vars},
            {"step": 2, "action": "TERMINAL_OUTPUT", "output": ""}
        ]
    }

def builtin_pwd(process: ShellProcess):
    current_dir = process.env_vars.get("PWD", "/")
    return {
        "type": "INTERNAL",
        "animation_steps": [
            {"step": 1, "action": "TERMINAL_OUTPUT", "output": current_dir}
        ]
    }

def builtin_echo(process: ShellProcess, args: str):
    # Extremely basic simulation of variable expansion (e.g., echo $USER)
    output = args
    if args.startswith("$"):
        var_name = args[1:]
        # Check env first, then local
        output = process.env_vars.get(var_name, process.local_vars.get(var_name, ""))
        
    return {
        "type": "INTERNAL",
        "animation_steps": [
            {"step": 1, "action": "TERMINAL_OUTPUT", "output": output}
        ]
    }

def builtin_history(process: ShellProcess):
    # Format history like real bash: "  1  ls"
    formatted_history = "\n".join([f"{i+1}  {cmd}" for i, cmd in enumerate(process.history)])
    return {
        "type": "INTERNAL",
        "animation_steps": [
            {"step": 1, "action": "TERMINAL_OUTPUT", "output": formatted_history}
        ]
    }

# Keep your export and local assignments here too, since they are built-ins!
def assign_local_variable(process: ShellProcess, var_name: str, var_value: str):
    process.local_vars[var_name] = var_value
    return {
        "type": "INTERNAL",
        "animation_steps": [{"step": 1, "action": "UPDATE_PARENT_LOCAL", "data": process.local_vars}]
    }

def export_variable(process: ShellProcess, var_name: str, var_value: str):
    process.env_vars[var_name] = var_value
    process.local_vars.pop(var_name, None) 
    return {
        "type": "INTERNAL",
        "animation_steps": [{"step": 1, "action": "UPDATE_PARENT_ENV", "data": process.env_vars}]
    }
