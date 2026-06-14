import { useState, useRef, useEffect } from 'react';

export default function TerminalPane({ history, onCommand, kernelMode, setKernelMode }) {
  const [input, setInput] = useState("");
  const endOfTerminalRef = useRef(null);

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
      
      {/* HEADER WITH TOGGLE */}
      <div className="mb-6 flex justify-between items-start border-b border-gray-800 pb-2">
        <div className="opacity-70">
          <div>#KillTheAbstraction - Linux VMS Visualizer</div>
          <div>Kernel Version 1.0.0-hybrid</div>
        </div>
    
        {/* The Engine Toggle */}
        <div className="flex items-center space-x-2 bg-gray-900 p-1 rounded border border-gray-700">
          <button 
            onClick={() => setKernelMode("hardcoded")}
            className={`px-3 py-1 rounded text-xs font-bold transition-all ${kernelMode === "hardcoded" ? "bg-green-600 text-black shadow-[0_0_10px_rgba(34,197,94,0.5)]" : "text-gray-500 hover:text-gray-300"}`}
          >
            Rules Engine
          </button>
          <button 
            onClick={() => setKernelMode("llm")}
            className={`px-3 py-1 rounded text-xs font-bold transition-all ${kernelMode === "llm" ? "bg-purple-600 text-white shadow-[0_0_10px_rgba(147,51,234,0.5)]" : "text-gray-500 hover:text-gray-300"}`}
          >
            LLM Kernel
          </button>
        </div>
      </div>

      {/* TERMINAL HISTORY */}
      <div className="flex-1 overflow-y-auto mb-4 custom-scrollbar">
        {history.map((line, idx) => (
          <div key={idx} className="whitespace-pre-wrap leading-relaxed mt-1">
            {line}
          </div>
        ))}
        <div ref={endOfTerminalRef} />
      </div>

      {/* TERMINAL INPUT */}
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