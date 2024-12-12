'use client'

import React, { useEffect, useState } from 'react';
import { backendUrl, cdnUrl } from '@/lib/utils';
import {Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter} from '@/components/ui/card'
import { Button } from './ui/button';
import { Separator } from './ui/separator';
import { RefreshCcw } from 'lucide-react';

const Step4Component: React.FC<{ projectId: string, setStep: (step: number) => void, step: number }> = ({ projectId, setStep, step }) => {
  const [, setIsProceeding] = useState(false);
  const [, setProceedButtonText] = useState('Check Status');
  const [, setStatus] = useState({});
  const [canvaUrl, setCanvaUrl] = useState('');
  const [videoUrl, setVideoUrl] = useState('');
  const [audioUrl, setAudioUrl] = useState('');
  const [, setCanvaPreviewUrl] = useState('');
  const screenStep = 4;
  const [, setError] = useState(null);
  const pollingInterval = 1000; // 1 second
  const [processingComplete, setProcessingComplete] = useState(false);
  useEffect(() => {
    let interval: NodeJS.Timeout;

    const fetchStatus = async () => {
      try {
        const response = await fetch(`${backendUrl}/project/${projectId}/step4/status`); // Replace with your endpoint
        if (!response.ok) {
          throw new Error("Failed to fetch job status");
        }
        const data = await response.json();
        setStatus(data.status);

        // Stop polling if job is complete
        if (data.status === "success") {
          setProcessingComplete(true);
          clearInterval(interval);
        }
      } catch (err: any) {
        setError(err.message);
        clearInterval(interval); // Stop polling on error
      }
    };

    // Start polling
    interval = setInterval(fetchStatus, pollingInterval);

    // Cleanup interval on component unmount
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (screenStep <= step && processingComplete) {
      const fetchData = async () => {
        const response = await fetch(`${backendUrl}/project/${projectId}/step4`);
        const data = await response.json();
        if (data.status === "success") {
          setCanvaUrl(data["results"]["canva_url"]);
          setVideoUrl(`${cdnUrl}/${data["results"]["video_url"]}`);
          setAudioUrl(`${cdnUrl}/${data["results"]["audio_url"]}`);
          setStep(4);
        }
      }
      fetchData();
      setIsProceeding(false);
    } 
  }, [processingComplete]);

  const handleRefresh = () => {
    const refreshStatus = async () => {
      try {
        //setStep(2);
        setIsProceeding(true);
        setProceedButtonText('Checking...');
        const response = await fetch(`${backendUrl}/project/${projectId}/step4/regenerate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ "project_id": projectId }),
        });
        if (response.ok) {
          const data = await response.json();
          setStatus(data);
          if (data["job"]["status"] === "success") {
            console.log("success");
            console.log(data["job"]["result"]);
            console.log(data["job"]["result"]["design"]["urls"]["edit_url"]);
            setCanvaUrl(data["job"]["result"]["design"]["urls"]["edit_url"]);
            setCanvaPreviewUrl(data["job"]["result"]["design"]["thumbnail"]['url']);
          }
          console.log(data);
        }
        } catch (error) {
          console.error('Error refreshing status:', error);
        } finally {
          setIsProceeding(false);
          setProceedButtonText('Check Status');
        }
      };
    refreshStatus();
  };
  return (
    <>
      <br />
      <Separator />
      <br />
      <Card className={screenStep === step? "card-active mx-auto p-4" : "card mx-auto p-4"}>  
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle>Step 4</CardTitle>
              <CardDescription>Generated Design:</CardDescription>
            </div>
            <Button variant="outline" size="icon" onClick={handleRefresh}>
              <RefreshCcw className="w-4 h-4" />
            </Button>
          </div>
        </CardHeader>
      <CardContent>
        {/* <div>Status: {Object.entries(status).map(([key, value]) => (
          <div key={key}>{key}: {value}</div>
        ))}</div> */}
        {videoUrl && 
        <div className="flex flex-col items-center">
          <video src={videoUrl} controls className="h-[300px]" />
          <p>Video</p>
        </div>}
        {audioUrl && 
        <div className="flex flex-col items-center">
          <audio src={audioUrl} controls />
          <p>Audio</p>
        </div>}
        {!canvaUrl && <p>Design is being generated. Please wait....</p>}
      </CardContent>
      <CardFooter className="flex flex-col items-center">
        {canvaUrl && <Button className="bg-blue-500 hover:bg-blue-700 text-white py-2 px-4 rounded align-center" onClick={() => window.open(canvaUrl, '_blank')}>Edit Design</Button>}
      </CardFooter>
    </Card>
    </>
  );
};

export default Step4Component;