import { useState, useRef, useEffect } from 'react';

export default function TerminalPane({ history, onCommand }) {
  const [input, setInput] = useState("");
  const endOfTerminalRef = useRef(null);

  // Auto-scroll to the bottom of the terminal when history updates
  useEffect(() => {
    endOfTerminalRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [history]);

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      onCommand(input);
      setInput("");
    }
  };

  return (
    <div className="flex flex-col h-full p-4 bg-black text-green-500 font-mono text-sm overflow-hidden">
      <div className="mb-6 opacity-70">
        <div>#KillTheAbstraction - Linux VMS Visualizer</div>
        <div>Kernel Version 1.0.0-simulation</div>
      </div>

      <div className="flex-1 overflow-y-auto mb-4 custom-scrollbar">
        {history.map((line, idx) => (
          <div key={idx} className="whitespace-pre-wrap leading-relaxed mt-1">
            {line}
          </div>
        ))}
        <div ref={endOfTerminalRef} />
      </div>

      <div className="flex items-center mt-2">
        <span className="mr-3 font-bold text-green-400">ubuntu@visual-box:~$</span>
        <input 
          type="text" 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          className="flex-1 bg-transparent outline-none text-gray-200 border-none focus:ring-0"
          autoFocus
          spellCheck="false"
          autoComplete="off"
        />
      </div>
    </div>
  );
}