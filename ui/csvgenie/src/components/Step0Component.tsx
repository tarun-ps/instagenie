'use client'

import React, { useEffect, useState } from 'react';
import { backendUrl, transformCsvData } from '@/lib/utils';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';

const Step0Component: React.FC<{ projectId: string, setStep: (step: number) => void, step: number, setQuestions: (questions: string[]) => void, setTopic: (topic: string) => void}> = ({ projectId, setStep, step, setQuestions, setTopic }) => {
  const [, setIsSubmitting] = useState(false);
  const [, setSubmitButtonText] = useState('Next');
  const screenStep = 0;
  const [csvData, setCsvData] = useState<any>();
  
  useEffect(() => {
    if (screenStep === step) {
      const fetchData = async () => {
        const response = await fetch(`${backendUrl}/project/${projectId}/step0`);
        const data = await response.json();
        setCsvData(transformCsvData(data.raw_csv));
        console.log(data);
        //setQuestions(data.questions?.questions);
        setTopic(data.domain);
      }
      fetchData();
      setSubmitButtonText('Lets start');
      setIsSubmitting(false);
      
    } else {
      setSubmitButtonText('Lets start');
    }
  }, [projectId]);


  return (
      <Card className={screenStep === step? "card-active mx-auto p-4" : "card mx-auto p-4"}>
      <CardHeader>
        <div className="flex justify-between items-center">
          <div>
            <CardTitle>Data Sample</CardTitle>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        {csvData && <div>
          <Table className={screenStep === step? "w-full max-w-full table-active" : "w-full max-w-full table"}>
          <TableHeader className={screenStep === step? "table-header-active" : "table-header"}>
            <TableRow>
              {csvData.columns.map((column: string) => (
                <TableHead key={column}>
                  {column}
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody className={screenStep === step? "table-body-active" : "table-body"}>
            {csvData.transformed_csv.map((row: any, index: number) => (
              <TableRow key={index}>
                {csvData.columns.map((column: string) => (
                  <TableCell key={column} className={screenStep === step? "table-cell-active" : "table-cell"}>
                    {typeof row[column] === 'number' ? row[column].toFixed(2) : row[column]}
                  </TableCell>
                ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>}
      </CardContent>
      <CardFooter>
      </CardFooter>
    </Card>
  );
};

export default Step0Component;