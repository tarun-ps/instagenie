'use client'

import { backendUrl } from '@/lib/utils';
import React, { useEffect, useState } from 'react';

const CanvaConnect: React.FC = () => {
  const [canvaConnect, setCanvaConnect] = useState<string | null>(null);
  useEffect(() => {
    const canvaConnect = async () => {
      const response = await fetch(`${backendUrl}/canva-connect`);
      const data = await response.json();
      setCanvaConnect(data.url);
    };
    canvaConnect();
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-xl font-bold mb-4">Canva Connect</h2>
      {canvaConnect && (
        <a href={canvaConnect} target="_blank" rel="noopener noreferrer">
          <button className="button px-4 py-2 rounded hover:bg-opacity-75">
            Connect to Canva
          </button>
        </a>
      )}
    </div>
  );
};

export default CanvaConnect; 