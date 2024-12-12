'use client'

import React, { useEffect, useState } from 'react';
import '@/styles/theme-sky.css';
import { backendUrl } from '@/lib/utils';
import { Card, CardHeader, CardTitle, CardFooter, CardContent } from './ui/card';
import { Button } from './ui/button';
import { useRouter } from 'next/navigation';
import LoadingComponent from './LoadingComponent';

const CompletedProjectsComponent: React.FC = () => {
  const [projects, setProjects] = useState<any[]>([]);
  const router = useRouter();

  useEffect(() => {
    // fetch data from backend
    const fetchData = async () => {
      const response = await fetch(`${backendUrl}/projects/completed`);
      const data = await response.json();
      setProjects(data);
    };
    fetchData();
  }, []);

  return (
    <div className="flex flex-col gap-4 w-full">
      <h1 className="text-2xl font-bold text-center">Completed Projects</h1>  
      <div className="mx-auto w-full min-w-[800px] flex flex-wrap gap-4 justify-center">
        {(!projects || projects.length === 0) && <LoadingComponent animation={2}/>}
        {projects && projects.map((project) => (
  
        <Card key={project.id} className="w-[400px] h-[550px]">
          <CardHeader>
            <CardTitle className="text-center">{project.domain || "Untitled"}</CardTitle>
            <br />
            <CardContent className="flex justify-center p-0">
              <img src={project.job.result.design.thumbnail.url} alt="Canva Preview" />
            </CardContent>
            <br />
            <CardFooter className="flex justify-center">
            <Button onClick={() => router.push(`/project/${project.id}`)}>View</Button>
              <Button onClick={() => window.open(project.job.result.design.urls.edit_url, '_blank')}>Edit On Canva</Button>
            </CardFooter>
          </CardHeader>
        </Card>

      ))}
      </div>
    </div>
  );
};

export default CompletedProjectsComponent; 