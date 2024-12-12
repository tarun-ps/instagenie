'use client'

import React, { useEffect, useState } from 'react';
import { backendUrl, CsvData, ScriptData } from '@/lib/utils';
import Step1Component from './Step1Component';
import Step2Component from './Step2Component';
import Step3Component from './Step3Component';
import Step4Component from './Step4Component';
import Step0Component from './Step0Component';
import LoadingComponent from './LoadingComponent';

const LandingPage: React.FC<{ projectId: string }> = ({ projectId }) => {
  const [questions, setQuestions] = useState<string[]>([]);
  const [step, setStep] = useState<number>(0);
  const [, setScript] = useState<ScriptData | null>(null);
  const [csvData, setCsvData] = useState<CsvData | null>(null);
  const [topic, setTopic] = useState<string | null>(null);

  useEffect(() => {
    console.log(step);
    const fetchStatus = async () => {
      const response = await fetch(`${backendUrl}/project/${projectId}/status`);
      const data = await response.json();
      setStep(data.step);
      console.log("Data with mounting Landing page", data);
    }
    fetchStatus();
  }, []);

  useEffect(() => {
    console.log("Step changed", step);
  }, [step]);

  return (
    <div className="container mx-auto p-4 min-w-[800px]">

      <h1 className="text-2xl font-bold text-center">{topic}</h1>
      <br />
      {step === -1 && <LoadingComponent animation={2}/>}
      {projectId && step >= 0 && <Step0Component projectId={projectId} setStep={setStep} step={step} setQuestions={setQuestions} setTopic={setTopic}/>}
      { step > 0 && <Step1Component questions={questions} projectId={projectId} setStep={setStep} step={step} setQuestions={setQuestions} />}
      { step > 1 && <Step2Component csvData={csvData} projectId={projectId} setStep={setStep} setCsvData={setCsvData} step={step} />}
      { step > 2 && <Step3Component setScript={setScript} projectId={projectId} setStep={setStep} step={step} />}
      {projectId && step > 3 && <Step4Component projectId={projectId} setStep={setStep} step={step} />}
    </div>
  );
};

export default LandingPage; 