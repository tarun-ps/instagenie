'use client'

import React, { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { backendUrl } from '@/lib/utils';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Separator } from './ui/separator';
import { RefreshCcw } from 'lucide-react';
import { Skeleton } from './ui/skeleton';

const Step1Component: React.FC<{ projectId: string, questions: string[], 
  setStep: (step: number) => void, 
  step: number, 
  setQuestions: (questions: string[]) => void}> = ({ projectId, questions, setStep, step, setQuestions }) => {
  const { handleSubmit } = useForm();
  const [selectedQuestion, setSelectedQuestion] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [submitButtonText, setSubmitButtonText] = useState('Next');
  const screenStep = 1;
  const [, setStatus] = useState("pending");
  const [, setError] = useState(null);
  const pollingInterval = 1000; // 1 second
  const [processingComplete, setProcessingComplete] = useState(false);
  const [regenerate, setRegenerate] = useState(false);

  useEffect(() => {
    let interval: NodeJS.Timeout;

    const fetchStatus = async () => {
      setProcessingComplete(false);
      try {
        const response = await fetch(`${backendUrl}/project/${projectId}/step1/status`); // Replace with your endpoint
        if (!response.ok) {
          throw new Error("Failed to fetch job status");
        }
        const data = await response.json();
        setStatus(data.status);

        // Stop polling if job is complete
        if (data.status === "success") {
          console.log("Step 1 Processing complete");
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
    setRegenerate(false);
    // Cleanup interval on component unmount
    return () => clearInterval(interval);
  }, [regenerate]);

  useEffect(() => {
    if (screenStep === step) {
      setSubmitButtonText('Proceed');
    } else {
      setSubmitButtonText('Regenerate');
    }
  }, [step]);


  useEffect(() => {
    console.log(screenStep, step, processingComplete);
    if (screenStep <= step && processingComplete) {
      const fetchData = async () => {
        const response = await fetch(`${backendUrl}/project/${projectId}/step1`);
        const data = await response.json();
        console.log(data);
        if (data.questions) {
          setQuestions(data.questions);
        }
      }
      fetchData();
      setIsSubmitting(false);
    
    } 
  }, [processingComplete, regenerate]);

  const handleQuestionSubmit = async () => {
    if (!selectedQuestion) return;

    try {
      setStep(1);
      setIsSubmitting(true);
      setSubmitButtonText('Processing...');
      const response = await fetch(`${backendUrl}/project/${projectId}/step1/proceed`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "question": selectedQuestion }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data);
        if (data.status === "success") {
          console.log("Step 1 Processing complete");
          setProcessingComplete(true);
          setStep(2);
        }
      } else {
        alert('Failed to submit question.');
      }
    } catch (error) {
      console.error('Error submitting question:', error);
      alert('An error occurred while submitting the question.');
    } finally {
      setIsSubmitting(false);
      setSubmitButtonText('Proceed');
    }
  };

  const handleRefresh = () => {
    setSelectedQuestion('');
    const refreshQuestions = async () => {
      try {
        setStep(1);
        setIsLoading(true);
        setSubmitButtonText('Processing...');
        setQuestions([]);
        setRegenerate(true);
        const response = await fetch(`${backendUrl}/project/${projectId}/step1/regenerate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ "project_id": projectId }),
        });
        if (response.ok) {
          const data = await response.json();
          console.log(data);
          //setQuestions(data.questions.questions);
        }
      } catch (error) {
        console.error('Error refreshing questions:', error);
      } finally {
        setIsLoading(false);
        setSubmitButtonText('Proceed');
      }
    };
    refreshQuestions();
  };

  const selectQuestion = (question: string) => {
    setSelectedQuestion(question);
  }

  return (
    <>
      <br />
      <Separator />
      <br />
      <Card className={screenStep === step? "card-active mx-auto p-4" : "card mx-auto p-4"}>
      <CardHeader>
        <div className="flex justify-between items-center">
          <div>
            <CardTitle>Step 1</CardTitle>
            <CardDescription>Pick a question or type your own:</CardDescription>
          </div>
          {step === 1 && <Button variant="ghost" size="icon" onClick={handleRefresh}>
            <RefreshCcw className="w-4 h-4" />
          </Button>}
        </div>
      </CardHeader>
      <CardContent>
      {isLoading && 
            <div className="flex flex-col space-y-3">
              <Skeleton className="h-[125px] w-[350px] rounded-xl skeleton-loader" />
              <div className="space-y-2">
                <Skeleton className="h-4 w-[350px] skeleton-loader" />
                <Skeleton className="h-4 w-[300px] skeleton-loader" />
            </div>
          </div>}
        {!isLoading && questions && questions.length > 0 && <form onSubmit={handleSubmit(handleQuestionSubmit)} className="flex flex-col space-y-4">
          {questions.map((question, index) => (
            <Button
              key={index}
              type="button"
              onClick={() => selectQuestion(question)}
              className="px-4 py-2 bg-white text-gray-800 border border-gray-300 rounded hover:bg-gray-100 focus:outline-none"
            >
              {question}
            </Button>
          ))}
          <Textarea
            value={selectedQuestion}
            onChange={(e) => setSelectedQuestion(e.target.value)}
            className="px-4 py-2 bg-white text-gray-800 border border-gray-300 rounded focus:outline-none h-24"
          />
        </form>}
      </CardContent>
      <CardFooter>
      {selectedQuestion && step === 1 && (
            <Button
              onClick={handleQuestionSubmit}
              type="submit"
              disabled={isSubmitting && selectedQuestion !== '' || step !== 1}
              className="button px-4 py-2 rounded hover:bg-opacity-75 disabled:opacity-50"
            >
              {submitButtonText}
            </Button>
          )}
      </CardFooter>
    </Card>
    </>
  );
};

export default Step1Component;