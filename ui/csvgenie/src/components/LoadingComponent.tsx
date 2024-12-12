'use client'

import React, { useEffect } from 'react';

const LoadingComponent: React.FC<{ animation: number }> = ({ animation }) => {
  useEffect(() => {
    console.log("LoadingComponent");
  }, []);
  return (
    <div className="flex flex-col items-center justify-center">
      {animation && <div className="flex justify-center">
        <img src={`/loading_${animation}.gif`} alt="Loading" />
      </div>}
    </div>
  );
};

export default LoadingComponent;