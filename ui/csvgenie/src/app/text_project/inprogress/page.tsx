'use client'
import React from 'react';
//import '@/styles/theme-sky.css';
import IncompleteAudioProjectsComponent from '@components/IncompleteAudioProjectsComponent';

export default function IncompleteAudioProjectsPage() {
  return (
    <div className="flex flex-col gap-4 w-full">
      <IncompleteAudioProjectsComponent />
    </div>
  );
}