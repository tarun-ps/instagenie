'use client'

import { backendUrl } from '@/lib/utils';
import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { ArrowRightIcon, ChartBarIcon, VideoCameraIcon} from '@heroicons/react/24/solid'
import { Database, FileSpreadsheetIcon, InstagramIcon, Mic, Pointer} from "lucide-react"

const CanvaConnect: React.FC = () => {
  const [canvaConnect, setCanvaConnect] = useState<string | null>(null);
  useEffect(() => {
    const canvaConnect = async () => {
      const response = await fetch(`${backendUrl}/canva-connect`);
      const data = await response.json();
      setCanvaConnect(data.url);
    };
    canvaConnect();
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4 items-center">Welcome to Instagenie</h1>
      <p className="text-sm text-gray-500 mb-4">Instagenie is a platform that allows you to create AI-powered videos and images.</p>
      <Card className='p-4 m-4'>
        <CardHeader>
          <CardTitle>Spreadsheet to Video</CardTitle>
        </CardHeader>
        <CardContent>
          <div className='flex flex-row gap-2'>
            <div className="flex flex-col gap-2 items-center">
                <FileSpreadsheetIcon className="w-16 h-16" />
                <p>Upload a spreadsheet.</p>
            </div>
            <div className='flex flex-row gap-2'>
              <ArrowRightIcon className='w-8 h-8 items-center  h-full ' />
            </div>
            <div className='flex flex-col gap-2 items-center'> 
              <Database className="w-16 h-16" />
              <p>Transform data</p>
            </div>
            <div className='flex flex-row gap-2'>
              <ArrowRightIcon className='w-8 h-8 items-center  h-full ' />
            </div>
            <div className='flex flex-col gap-2 items-center'>
              <ChartBarIcon className="w-16 h-16" />
              <p>Generate screens</p>
            </div>
            <div className='flex flex-row gap-2'>
              <ArrowRightIcon className='w-8 h-8 items-center  h-full ' />
            </div>
            <div className='flex flex-col gap-2 items-center'>
              <VideoCameraIcon className="w-16 h-16" />
              <p>Customize video.</p>
            </div>
            <div className='flex flex-row gap-2'>
              <ArrowRightIcon className='w-8 h-8 items-center  h-full ' />
            </div>
            <div className='flex flex-col gap-2 items-center'>
              <InstagramIcon className='w-16 h-16'></InstagramIcon>
              <p>Generate & Publish</p>
            </div>
          </div>
        </CardContent>
      </Card>
      <Card  className='p-4 m-4'>
        <CardHeader>
          <CardTitle>Audio to Video</CardTitle>
        </CardHeader>
        <CardContent>
          <div className='flex flex-row gap-2'>
            <div className="flex flex-col gap-2 items-center">
                <Mic className="w-16 h-16" />
                <p>Upload an audio script.</p>
            </div>
            <div className='flex flex-row gap-2'>
              <ArrowRightIcon className='w-8 h-8 items-center  h-full ' />
            </div>
            <div className='flex flex-col gap-2 items-center'>
              <ChartBarIcon className="w-16 h-16" />
              <p>Generate screens</p>
            </div>
            <div className='flex flex-row gap-2'>
              <ArrowRightIcon className='w-8 h-8 items-center  h-full ' />
            </div>
            <div className='flex flex-col gap-2 items-center'>
              <Pointer className="w-16 h-16" />
              <p>Pick Assets</p>
            </div>
            <div className='flex flex-row gap-2'>
              <ArrowRightIcon className='w-8 h-8 items-center  h-full ' />
            </div>
            <div className='flex flex-col gap-2 items-center'>
              <VideoCameraIcon className="w-16 h-16" />
              <p>Customize video.</p>
            </div>
            <div className='flex flex-row gap-2'>
              <ArrowRightIcon className='w-8 h-8 items-center  h-full ' />
            </div>
            <div className='flex flex-col gap-2 items-center'>
              <InstagramIcon className='w-16 h-16'></InstagramIcon>
              <p>Generate & Publish</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card  className='p-4 m-4'>
        <CardHeader>
          <CardTitle>Text to Video</CardTitle>
        </CardHeader>
        <CardContent>
          <div className='flex flex-row gap-2'>
            <div className="flex flex-col gap-2 items-center">
                <Mic className="w-16 h-16" />
                <p>Upload a text script.</p>
            </div>
            <div className='flex flex-row gap-2'>
              <ArrowRightIcon className='w-8 h-8 items-center  h-full ' />
            </div>
            <div className='flex flex-col gap-2 items-center'>
              <ChartBarIcon className="w-16 h-16" />
              <p>Generate screens</p>
            </div>
            <div className='flex flex-row gap-2'>
              <ArrowRightIcon className='w-8 h-8 items-center  h-full ' />
            </div>
            <div className='flex flex-col gap-2 items-center'>
              <Pointer className="w-16 h-16" />
              <p>Pick Assets</p>
            </div>
            <div className='flex flex-row gap-2'>
              <ArrowRightIcon className='w-8 h-8 items-center  h-full ' />
            </div>
            <div className='flex flex-col gap-2 items-center'>
              <VideoCameraIcon className="w-16 h-16" />
              <p>Customize video.</p>
            </div>
            <div className='flex flex-row gap-2'>
              <ArrowRightIcon className='w-8 h-8 items-center  h-full ' />
            </div>
            <div className='flex flex-col gap-2 items-center'>
              <InstagramIcon className='w-16 h-16'></InstagramIcon>
              <p>Generate & Publish</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default CanvaConnect; 