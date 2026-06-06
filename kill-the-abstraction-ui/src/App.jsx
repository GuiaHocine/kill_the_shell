import { useState, useEffect } from 'react';
import TerminalPane from './components/TerminalPane';
import MemoryPane from './components/MemoryPane';

export default function App() {
  const [socket, setSocket] = useState(null);
  const [terminalHistory, setTerminalHistory] = useState([]);
  const [processes, setProcesses] = useState({});

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onopen = () => console.log("Connected to Kernel Simulator!");
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      handleKernelEvent(data);
    };

    setSocket(ws);

    return () => ws.close();
  }, []);

  const handleKernelEvent = (data) => {
    switch (data.action) {
      case "INIT_MAIN_PROCESS":
        setProcesses({
          [data.pid]: { id: data.pid, local: data.local_vars, env: data.env_vars, name: "bash" }
        });
        break;
      
      case "UPDATE_PARENT_LOCAL":
        setProcesses(prev => ({
          ...prev,
          1021: { ...prev[1021], local: data.data }
        }));
        break;

      case "UPDATE_PARENT_ENV":
        setProcesses(prev => ({
          ...prev,
          1021: { ...prev[1021], env: data.data }
        }));
        break;

      case "FORK_PROCESS":
        setProcesses(prev => ({
          ...prev,
          [data.pid]: { id: data.pid, local: data.child_local, env: data.child_env, name: "bash (child clone)" }
        }));
        break;

      case "EXEC_BINARY":
        setProcesses(prev => ({
          ...prev,
          [data.pid]: { ...prev[data.pid], local: data.child_local, env: data.child_env, name: data.binary_name }
        }));
        break;

      case "KILL_CHILD":
        setProcesses(prev => {
          const newProcs = { ...prev };
          delete newProcs[data.pid];
          return newProcs;
        });
        break;

      case "TERMINAL_OUTPUT":
        if (data.output) {
          setTerminalHistory(prev => [...prev, data.output]);
        }
        break;

      default:
        console.warn("Unknown kernel action:", data.action);
    }
  };

  const sendCommand = (cmd) => {
    if (socket && cmd.trim()) {
      setTerminalHistory(prev => [...prev, `ubuntu@visual-box:~$ ${cmd}`]);
      socket.send(JSON.stringify({ command: cmd }));
    }
  };

  return (
    <div className="flex h-screen w-full bg-black">
      {/* Left Split: Terminal */}
      <div className="w-[45%] border-r border-gray-800 shadow-2xl z-10">
        <TerminalPane history={terminalHistory} onCommand={sendCommand} />
      </div>
      
      {/* Right Split: Memory VMS Viewer */}
      <div className="w-[55%] relative">
        <div className="absolute top-4 left-4 z-10 text-gray-500 font-mono text-xs font-bold uppercase tracking-widest bg-black/50 p-2 rounded">
          Live RAM / Process Allocations
        </div>
        <MemoryPane processes={processes} />
      </div>
    </div>
  );
}