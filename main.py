## WEB SOCKET SERVER


import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from models import ShellProcess
from router import route_terminal_command

app = FastAPI()

# Allow our React frontend to connect without CORS blocking
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # 1. Boot Sequence: Initialize a fresh Bash process for this user session
    main_process = ShellProcess(pid=1021, name="bash")
    next_pid = 1022

    # 2. Send the initial "Boot" state to React so it can draw the first box
    await websocket.send_json({
        "action": "INIT_MAIN_PROCESS",
        "pid": main_process.pid,
        "local_vars": main_process.local_vars,
        "env_vars": main_process.env_vars
    })

    try:
        while True:
            # 3. Wait for the user to type a command and hit Enter in React
            data = await websocket.receive_text()
            payload = json.loads(data)
            command = payload.get("command", "")
            mode = payload.get("mode", "hardcoded") # Default to hardcoded

            if not command:
                continue

            # 4. Route the command and get the animation steps
            response_packet = route_terminal_command(command, main_process, next_pid, mode) # adding mode
            
            if response_packet["type"] == "FORK_AND_EXEC":
                next_pid += 1

            # 5. STREAM THE EVENTS (The #KillTheAbstraction magic)
            for step in response_packet["animation_steps"]:
                await websocket.send_json(step)
                
                # We artificially slow down time by 800ms so the human eye 
                # can watch the memory boxes split, flash, and die on the frontend!
                await asyncio.sleep(0.8)

    except WebSocketDisconnect:
        print("Client disconnected or closed browser tab.")