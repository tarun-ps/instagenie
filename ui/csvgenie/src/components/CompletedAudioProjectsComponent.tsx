'use client'

import React, { useEffect, useState } from 'react';
import '@/styles/theme-sky.css';
import { backendUrl, cdnUrl } from '@/lib/utils';
import { Card, CardHeader, CardTitle, CardFooter, CardContent } from './ui/card';
import { Button } from './ui/button';
import { useRouter } from 'next/navigation';
import LoadingComponent from './LoadingComponent';

const CompletedAudioProjectsComponent: React.FC = () => {
  const [projects, setProjects] = useState<any[]>([]);
  const router = useRouter();

  useEffect(() => {
    // fetch data from backend
    const fetchData = async () => {
      const response = await fetch(`${backendUrl}/audio_projects/completed`);
      const data = await response.json();
      setProjects(data);
      console.log(data);
    };
    fetchData();
  }, []);

  return (
    <div className="flex flex-col gap-4 w-full">
      <h1 className="text-2xl font-bold text-center">Completed Projects</h1>  
      <div className="mx-auto w-full min-w-[800px] flex flex-wrap gap-4 justify-center">
        {(!projects || projects.length === 0) && <LoadingComponent animation={2}/>}
        {projects &&projects.map((project) => (
  
        <Card key={project.id} className="w-[300px] h-[350px]">
          <CardHeader>
            <CardTitle className="text-center">{project.script.script_for_timestamp.map((script: any) => script.text).join(' ').slice(0, 50) || "Untitled"}</CardTitle>
            <br />
            <CardContent className="flex justify-center p-2 align-middle">
              <img height={125} width={125} src={`${cdnUrl}/${project.selected_assets.assets[0].details.thumbnail.path}`} alt="Preview" />
            </CardContent>
            <br />
            <CardFooter className="flex justify-center">
            <Button onClick={() => router.push(`/audio_project/${project.id}`)}>View</Button>
            </CardFooter>
          </CardHeader>
        </Card>

      ))}
      </div>
    </div>
  );
};

export default CompletedAudioProjectsComponent; 