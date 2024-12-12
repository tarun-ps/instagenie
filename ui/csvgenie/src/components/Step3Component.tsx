'use client'

import React, { useEffect, useState } from 'react';
import { backendUrl, ScriptData } from '@/lib/utils';
import {Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter} from '@/components/ui/card'
import { Button } from './ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { FaPencilAlt } from 'react-icons/fa'
import { Separator } from './ui/separator';
import { RefreshCcw } from 'lucide-react';

const Step3Component: React.FC<{ projectId: string, setScript: (script: ScriptData) => void, setStep: (step: number) => void, step: number }> = ({ projectId, setScript, setStep, step }) => {
  const [editableScript, setEditableScript] = useState<{ [key: string]: { [field: string]: any } }>({});
  const [editMode, setEditMode] = useState<{ [key: string]: boolean }>({});
  const [isProceeding, setIsProceeding] = useState(false);
  const [proceedButtonText, setProceedButtonText] = useState('Generate');
  const screenStep = 3;

  const [, setStatus] = useState("pending");
  const [, setError] = useState(null);
  const pollingInterval = 1000; // 5 seconds
  const [processingComplete, setProcessingComplete] = useState(false);
  useEffect(() => {
    let interval: NodeJS.Timeout;

    const fetchStatus = async () => {
      try {
        const response = await fetch(`${backendUrl}/project/${projectId}/step3/status`); // Replace with your endpoint
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
        const response = await fetch(`${backendUrl}/project/${projectId}/step3`);
        const data = await response.json();
        if (data.status === "success") {
          console.log("Step 3 Processing complete");
          console.log(data);
          setEditableScript(data.script);
          //setStep(4);
        }
      }
      fetchData();
      setIsProceeding(false);
    } 
  }, [processingComplete]);

  const handleInputChange = (key: keyof ScriptData, field: string, value: string) => {
    setEditableScript((prevScript) => ({
      ...prevScript,
      [key]: {
        ...prevScript[key],
        [field]: value,
      },
    }));
  };

  const toggleEditMode = (key: keyof ScriptData, field: string) => {
    setEditMode((prevMode) => ({
      ...prevMode,
      [`${key}-${field}`]: !prevMode[`${key}-${field}`],
    }));
  };

  const handleBlur = (key: keyof ScriptData, field: string) => {
    setEditMode((prevMode) => ({
      ...prevMode,
      [`${key}-${field}`]: false,
    }));
  };

  useEffect(() => {
    console.log(editableScript);
  }, [editableScript]);

  const handleRegenerate = () => {
    const regenerateScript = async () => {
      try {
        //setStep(2);
        setIsProceeding(true);
        setProceedButtonText('Generating...');
        const response = await fetch(`${backendUrl}/project/${projectId}/step3/regenerate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ "project_id": projectId }),
        });
        if (response.ok) {
          const data = await response.json();
          console.log(data);
          setEditableScript(data.script);
          //setStep(3);
        }
      } catch (error) {
        console.error('Error regenerating script:', error);
      } finally {
        setIsProceeding(false);
        setProceedButtonText('Generate');
      }
      };
    regenerateScript();
  };
  const handleProceed = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // Disable submit button and show a processing message
      //setStep(3);
      setIsProceeding(true);
      setProceedButtonText('Generating...');
      console.log(`${backendUrl}/project/${projectId}/step3/proceed`);
      //send json with question that can be processed by FastAPI backend
      const response = await fetch(`${backendUrl}/project/${projectId}/step3/proceed`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "editted_script": editableScript }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data);
        setStep(4);
      } else {
        alert('Failed to proceed to next step.');
      }
    } catch (error) {
      console.error('Error proceeding to next step:', error);
      alert('An error occurred while proceeding to next step.');
    } finally {
      // Re-enable submit button and reset button text
      setIsProceeding(false);
    }
  };
  return (editableScript && (
    <>
      <br />
      <Separator />
      <br />
      
      <Card className={screenStep === step? "card-active mx-auto p-4" : "card mx-auto p-4"}>  
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle>Step 3</CardTitle>
              <CardDescription>Generated Script:</CardDescription>
            </div>
            {step === 3 && <Button variant="outline" size="icon" onClick={handleRegenerate}>
              <RefreshCcw className="w-4 h-4" />
            </Button>}
          </div>
        </CardHeader>
      <CardContent>
        <Table className={screenStep === step? "table-active" : "table"}>
          <TableHeader className={screenStep === step? "table-header-active" : "table-header"}>
            <TableRow>
              <TableHead>
                Screen
              </TableHead>
              <TableHead>
                Text
              </TableHead>
              <TableHead>
              </TableHead>
              <TableHead>
                Voice Over
              </TableHead>
              <TableHead>
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {Object.keys(editableScript).map((key, index) => (
              <TableRow key={index}>
                <TableCell>
                  {index + 1}
                </TableCell>
                <TableCell>
                  {editMode[`${key}-text`] ? (
                    <textarea
                      value={editableScript[key as keyof ScriptData].text}
                      onChange={(e) => handleInputChange(key as keyof ScriptData, 'text', e.target.value)}
                      onBlur={() => handleBlur(key as keyof ScriptData, 'text')}
                      className="w-full border border-gray-300 rounded p-1"
                      autoFocus
                    />
                  ) : (
                    <div className="flex justify-end items-center">
                      <span className="mr-2">{editableScript[key as keyof ScriptData].text}</span>
                    </div>
                  )}
                </TableCell>
                <TableCell>
                  {step === 3 && <FaPencilAlt
                          className="w-3 h-3 cursor-pointer"
                          onClick={() => toggleEditMode(key as keyof ScriptData, 'text')}
                  />}
                </TableCell>
                <TableCell>
                  {editMode[`${key}-voice_over`] ? (
                    <textarea
                      value={editableScript[key as keyof ScriptData].voice_over}
                      onChange={(e) => handleInputChange(key as keyof ScriptData, 'voice_over', e.target.value)}
                      onBlur={() => handleBlur(key as keyof ScriptData, 'voice_over')}
                      className="w-full border border-gray-300 rounded p-1"
                      autoFocus
                    />
                  ) : (
                    <div className="flex justify-end items-center">
                      <span className="mr-2">{editableScript[key as keyof ScriptData].voice_over}</span>
                    </div>
                  )}
                </TableCell>
                <TableCell>
                  {step === 3 && <FaPencilAlt
                    className="w-3 h-3 cursor-pointer"
                    onClick={() => toggleEditMode(key as keyof ScriptData, 'voice_over')}
                  />}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
      <CardFooter>
        { step === 3 && <Button
            onClick={handleProceed}
            disabled={isProceeding}
            className="button px-4 py-2 mt-4 rounded hover:bg-opacity-75"
          >
        {proceedButtonText}
          </Button>}
      </CardFooter>
    </Card>
    </>
  )
  );
};

export default Step3Component;