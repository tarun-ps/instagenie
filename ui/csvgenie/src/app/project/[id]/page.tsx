'use client'
import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import LandingPage from '@components/LandingPage';
import '@/styles/theme-sky.css';

export default function ProjectPage() {
  const params = useParams();
  const [projectId, setProjectId] = useState<string | null>(null);

  useEffect(() => {
    if (!params) {
      console.error('NextRouter was not mounted.');
    } else{
      const id = params.id;
      setProjectId(id as string);
    }
    console.log(projectId);
  }, [params]);

  if (!params) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      {projectId && <LandingPage projectId={projectId as string} />}
    </div>
  );
}