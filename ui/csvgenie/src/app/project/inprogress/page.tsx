'use client'
import React from 'react';
//import '@/styles/theme-sky.css';
import IncompleteProjectsComponent from '@components/IncompleteProjectsComponent';

export default function IncompleteProjectsPage() {
  return (
    <div className="flex flex-col gap-4 w-full">
      <IncompleteProjectsComponent />
    </div>
  );
}