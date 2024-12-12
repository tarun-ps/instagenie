'use client'

import React from 'react';

const Creations: React.FC<{ setSelectedTaskId: (id: string) => void, setSelectedOption: (option: 'create' | 'view' | 'task') => void }> = ({ setSelectedTaskId, setSelectedOption }) => {
  const handleSelectTask = (id: string) => {
    setSelectedTaskId(id);
    setSelectedOption('task');
  };

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-xl font-bold mb-4">Creations</h2>
      <ul className="space-y-2">
        {/* Example task items */}
        <li>
          <button
            onClick={() => handleSelectTask('task-1')}
            className="button px-4 py-2 rounded hover:bg-opacity-75"
          >
            Task 1
          </button>
        </li>
        <li>
          <button
            onClick={() => handleSelectTask('task-2')}
            className="button px-4 py-2 rounded hover:bg-opacity-75"
          >
            Task 2
          </button>
        </li>
      </ul>
    </div>
  );
};

export default Creations; 