'use client'
import React from 'react';
import '@/styles/theme-sky.css';
import CompletedProjectsComponent from '@components/CompletedProjectsComponent';

export default function CompletedProjectsPage() {
  return (
    <div className="flex flex-col gap-4 w-full">
      <CompletedProjectsComponent />
    </div>
  );
}