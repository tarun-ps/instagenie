'use client'

import React, { useEffect, useState } from 'react';
import '@/styles/theme-sky.css';
import { backendUrl } from '@/lib/utils';
import { Card, CardHeader, CardTitle, CardFooter } from './ui/card';
import { Button } from './ui/button';
import { useRouter } from 'next/navigation';
import LoadingComponent from './LoadingComponent';
import { Separator } from './ui/separator';

const IncompleteAudioProjectsComponent: React.FC = () => {
  const [projects, setProjects] = useState<any[]>([]);
  const router = useRouter();
  useEffect(() => {
    console.log("IncompleteProjectsComponent");
    // fetch data from backend
    const fetchData = async () => {
      const response = await fetch(`${backendUrl}/audio_projects/incomplete`);
      const data = await response.json();
      setProjects(data);
      console.log(data);
    };
    fetchData();
  }, []);

  return (
    <div className="flex flex-col gap-4 w-full">
      <h1 className="text-2xl font-bold text-center">In Progress Projects</h1>  
      <br />
      <div className="mx-auto w-full min-w-[800px] flex flex-wrap gap-4 justify-center">
        {(!projects || projects.length === 0) && <LoadingComponent animation={2}/>}
        {projects && projects.map((project) => (
          <div key={project.id} className="w-[300px] h-[150px]">
            <Card className="h-full">
              <CardHeader>
                <CardTitle className="text-center">
                  {project.script.script_for_timestamp.map((script: any) => script.text).join(' ').slice(0, 50) || "Untitled"}
                </CardTitle>
                <br />
                <CardFooter className="flex justify-center">
                  <Button onClick={() => router.push(`/audio_project/${project.id}`)}>Continue editing</Button>
                </CardFooter>
              </CardHeader>
            </Card>
            <br />
            <Separator />
            <br />
          </div>
        ))}
      </div>
    </div>
  );
};

export default IncompleteAudioProjectsComponent; 