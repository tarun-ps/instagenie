'use client'
import React from 'react';
import '@/styles/theme-sky.css';
import CompletedAudioProjectsComponent from '@components/CompletedAudioProjectsComponent';

export default function CompletedProjectsPage() {
  return (
    <div className="flex flex-col gap-4 w-full">
      <CompletedAudioProjectsComponent />
    </div>
  );
}