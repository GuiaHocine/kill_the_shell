import { Handle, Position } from 'reactflow';

export default function ProcessNode({ data }) {
  const { proc } = data;
  
  return (
    <div className="bg-gray-900 border-2 border-green-500 rounded-lg shadow-[0_0_15px_rgba(34,197,94,0.3)] w-80 text-sm overflow-hidden text-white transition-all duration-300">
      
      {/* Target Handle (For incoming connections) */}
      <Handle type="target" position={Position.Top} className="w-3 h-3 bg-green-500 border-none" />

      {/* Header */}
      <div className="bg-green-900 text-green-100 px-3 py-2 border-b border-green-500 font-bold flex justify-between items-center">
        <span className="truncate flex-1">{proc.name}</span>
        <span className="text-xs bg-green-950 px-2 py-1 rounded">PID: {proc.id}</span>
      </div>

      <div className="p-4 space-y-4">
        {/* Local Variables Block */}
        <div>
          <div className="text-xs font-bold text-gray-400 mb-2 uppercase tracking-wider">Local Shell Variables</div>
          <div className="bg-gray-950 p-2 rounded border border-gray-700 min-h-[40px]">
            {Object.entries(proc.local || {}).length === 0 ? (
              <span className="text-gray-600 italic text-xs">Empty (Wiped or Unset)</span>
            ) : (
              Object.entries(proc.local).map(([key, val]) => (
                <div key={key} className="flex justify-between font-mono text-xs mb-1">
                  <span className="text-blue-400 font-bold">{key}</span>
                  <span className="text-gray-300">"{val}"</span>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Environment Variables Block */}
        <div>
          <div className="text-xs font-bold text-gray-400 mb-2 uppercase tracking-wider">Environment (Exported)</div>
          <div className="bg-green-950/30 p-2 rounded border border-green-900 min-h-[40px]">
            {Object.entries(proc.env || {}).map(([key, val]) => (
              <div key={key} className="flex justify-between font-mono text-xs mb-1">
                <span className="text-purple-400 font-bold">{key}</span>
                <span className="text-green-300">"{val}"</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Source Handle (For outgoing connections) */}
      <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-green-500 border-none" />
    </div>
  );
}