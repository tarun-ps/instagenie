'use client'

import React, { useEffect, useState } from 'react';
import { backendUrl, CsvData, ScriptData, transformCsvData } from '@/lib/utils';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { Separator } from './ui/separator';
import ChatPreviewComponent from './ChatPreviewComponent';

const Step2Component: React.FC<{ projectId: string, csvData: CsvData, 
        setStep: (step: number) => void, setCsvData: (csvData: CsvData) => void, 
        step: number }> = ({ projectId, csvData, setStep, setCsvData, step }) => {
  const [isProceeding, setIsProceeding] = useState(false);
  const [proceedButtonText, setProceedButtonText] = useState('Next');
  const screenStep = 2;
  const [, setStatus] = useState("pending");
  const [, setError] = useState(null);
  const pollingInterval = 1000; // 1 second
  const [processingComplete, setProcessingComplete] = useState(false);
  const [selectedColumns, setSelectedColumns] = useState<string[]>([]);
  const [xAxis, setXAxis] = useState<string>("");
  const [chartType, setChartType] = useState<string>("bar");
  const [columns, setColumns] = useState<string[]>([]);
  useEffect(() => {
    let interval: NodeJS.Timeout;

    const fetchStatus = async () => {
      try {
        const response = await fetch(`${backendUrl}/project/${projectId}/step2/status`); // Replace with your endpoint
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
        const response = await fetch(`${backendUrl}/project/${projectId}/step2`);
        const data = await response.json();
        if (data.transformed_csv) {
          setCsvData(data.transformed_csv);
          initChart(data.transformed_csv);
        }
      }
      fetchData();
      setIsProceeding(false);
    }
  }, [processingComplete]);

  const handleProceed = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // Disable submit button and show a processing message
      setStep(2);
      setIsProceeding(true);
      setProceedButtonText('Processing...');
      console.log("Proceeding to step 3");
      console.log(xAxis);
      console.log(selectedColumns);
      console.log(chartType);
      console.log(`${backendUrl}/project/${projectId}/step2/proceed`);
      //send json with question that can be processed by FastAPI backend
      const response = await fetch(`${backendUrl}/project/${projectId}/step2/proceed`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          x_axis: xAxis,
          selected_columns: selectedColumns,
          chart_type: chartType
        })
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data.status);
        if (data.status === "success") {
          setStep(3);
        }
      } else {
        alert('Failed to proceed to next step.');
      }
    } catch (error) {
      console.error('Error proceeding to next step:', error);
      alert('An error occurred while proceeding to next step.');
    } finally {
      // Re-enable submit button and reset button text
      setIsProceeding(false);
      setProceedButtonText('Next');
    }
  };

  // const generateChartData = (csvData: CsvData) => {
  //   const csv = transformCsvData(csvData);
  //   console.log("3");
  //   console.log(csv.transformed_csv);
  //   setChartData(csv.transformed_csv as any);
  //   const cConfig: ChartConfig = {};
  //   for (const column of csv.columns.slice(1)) {
  //     cConfig[column] = {
  //       label: column,
  //       color: "#60a5fa",
  //     };
  //   }
  //   setChartXAxisKey(csv.columns[0]);
  //   console.log("4");
  //   console.log(cConfig);
  //   setChartConfig(cConfig);
  // }
  const initChart = (csvData: CsvData) => {
    console.log("Init chart");
    setXAxis(transformCsvData(csvData).columns[0]);
    setSelectedColumns(transformCsvData(csvData).columns);
    setChartType(chartType);
    setColumns(transformCsvData(csvData).columns);
  }

  return (
    <>
      <br />
      <Separator />
      <br />
      {processingComplete && csvData && <Card className={screenStep === step? "card-active mx-auto p-4 w-full" : "card mx-auto p-4 w-full"}>
        <CardHeader>
        <CardTitle>Step 2</CardTitle>
        <CardDescription>Validate your data:</CardDescription>
        </CardHeader>
        <CardContent className="overflow-x-auto max-w-full w-full">
        <Table className={screenStep === step? "w-full max-w-full table-active" : "w-full max-w-full table"}>
          <TableHeader className={screenStep === step? "table-header-active" : "table-header"}>
            <TableRow>
              {transformCsvData(csvData).columns.map((column) => (
                <TableHead key={column}>
                  {column}
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody className={screenStep === step? "table-body-active" : "table-body"}>
            {transformCsvData(csvData).transformed_csv.map((row, index) => (
              <TableRow key={index}>
                {transformCsvData(csvData).columns.map((column) => (
                  <TableCell key={column} className={screenStep === step? "table-cell-active" : "table-cell"}>
                    {typeof row[column] === 'number' ? row[column].toFixed(2) : row[column]}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <div className="w-full flex justify-center items-center">
          <ChatPreviewComponent 
            x_axis={xAxis} 
            columns={columns} 
            chart_data={transformCsvData(csvData).transformed_csv} 
            chart_type={chartType} 
            selectedColumns={selectedColumns} 
            setSelectedColumns={setSelectedColumns} 
            setXAxis={setXAxis} 
            setChartType={setChartType} />
        </div>
        </CardContent>
        <CardFooter className="flex justify-between">
          {Object.keys(csvData).length > 0 && (
            <form onSubmit={handleProceed} className="flex flex-col space-y-4">
              { step === 2 && <Button type="submit" disabled={isProceeding} className="button px-4 py-2 rounded hover:bg-opacity-75 disabled:opacity-50">
                {proceedButtonText}
              </Button>}
            </form>
          )}
        </CardFooter>
      </Card>
      }
    </>
  );
};

export default Step2Component;