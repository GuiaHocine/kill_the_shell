import re
from models import ShellProcess
import actions_internals as builtin
import actions_externals as external

def route_terminal_command(command: str, process: ShellProcess, next_pid: int):
    cmd = command.strip()
    
    # Add to history (unless it's empty)
    if cmd:
        process.history.append(cmd)

    # --- 1. VARIABLE ASSIGNMENTS (Built-in) ---
    export_match = re.match(r"^export\s+([a-zA-Z_]\w*)=(.*)$", cmd)
    if export_match:
        return builtin.export_variable(process, *export_match.groups())

    local_match = re.match(r"^([a-zA-Z_]\w*)=(.*)$", cmd)
    if local_match:
        return builtin.assign_local_variable(process, *local_match.groups())

    # --- 2. SHELL BUILT-INS (No Forks) ---
    parts = cmd.split(" ", 1)
    base_cmd = parts[0]
    args = parts[1] if len(parts) > 1 else ""

    if base_cmd == "cd":
        return builtin.builtin_cd(process, args)
    elif base_cmd == "pwd":
        return builtin.builtin_pwd(process)
    elif base_cmd == "echo":
        return builtin.builtin_echo(process, args)
    elif base_cmd == "history":
        return builtin.builtin_history(process)

    # --- 3. EXTERNAL BINARIES (Fork + Exec) ---
    # Any command not caught above (like ls, grep, nano, python) falls down here!
    return external.execute_binary(process, base_cmd, next_pid, args)