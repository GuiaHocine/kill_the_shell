import ReactFlow, { Background, Controls, MarkerType } from 'reactflow';
import 'reactflow/dist/style.css';
import ProcessNode from './ProcessNode';

const nodeTypes = { processNode: ProcessNode };

export default function MemoryPane({ processes }) {
  // 1. Transform process dictionary into React Flow Nodes
  const nodes = Object.values(processes).map((proc, index) => ({
    id: proc.id.toString(),
    type: 'processNode',
    // Simple deterministic positioning: Parent top center, child below it
    position: { x: 250, y: index === 0 ? 50 : 450 },
    data: { proc },
  }));

  // 2. Create animated edges showing 'Fork' relationships
  const edges = Object.values(processes)
    .filter(p => p.id !== 1021) // 1021 is the root Bash process
    .map(p => ({
      id: `edge-1021-${p.id}`,
      source: '1021',
      target: p.id.toString(),
      animated: true,
      style: { stroke: '#4ade80', strokeWidth: 2 },
      markerEnd: {
        type: MarkerType.ArrowClosed,
        color: '#4ade80',
      },
    }));

  return (
    <div className="h-full w-full bg-gray-950">
      <ReactFlow 
        nodes={nodes} 
        edges={edges} 
        nodeTypes={nodeTypes}
        fitView
        fitViewOptions={{ padding: 0.5 }}
        proOptions={{ hideAttribution: true }} // Hides the React Flow logo
      >
        <Background color="#22c55e" gap={20} size={1} opacity={0.1} />
        <Controls className="bg-gray-800 border-gray-700 fill-white" />
      </ReactFlow>
    </div>
  );
}