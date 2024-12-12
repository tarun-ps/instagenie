'use client'
import React, { useEffect, useState } from 'react';
import { ChartConfig, ChartContainer } from './ui/chart';
import { BarChart, Bar, XAxis, CartesianGrid, Line, LineChart, YAxis, LabelList } from 'recharts';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { DropdownMenu, DropdownMenuCheckboxItem, DropdownMenuContent, DropdownMenuTrigger } from './ui/dropdown-menu';
import { Button } from './ui/button';
import { Pie, PieChart } from "recharts"
import { useRef } from 'react';
import { toPng } from 'html-to-image';

const ChatPreviewComponent: React.FC<{ x_axis: string, columns: string[], 
    chart_data: any, chart_type: string, selectedColumns: string[], 
    setSelectedColumns: (columns: string[]) => void, setXAxis: (xAxis: string) => void, 
    setChartType: (chartType: string) => void }> = ({ x_axis, columns, chart_data, 
    chart_type, selectedColumns, setSelectedColumns, setXAxis, setChartType }) => {
    const [chartConfig, setChartConfig] = useState<ChartConfig>({});
    const [chartData, setChartData] = useState<any>(chart_data);
    //const [selectedColumns, setSelectedColumns] = useState<string[]>(columns);
    const chartRef = useRef<HTMLDivElement>(null);

    const downloadImage = async () => {
      if (!chartRef.current) return;
  
      const dataUrl = await toPng(chartRef.current);
  
      const link = document.createElement('a');
      link.href = dataUrl;
      link.download = 'chart.png';
      link.click();
    };


    useEffect(() => {
      generateChartData(chart_type);
    }, [chart_type, x_axis, selectedColumns]);

    const generateChartData = (chartType: string) => {
      const cConfig: ChartConfig = {};
      if (chartType === "bar" || chartType === "line") {
        console.log("In bar or line");
        var i = 1;
        for (const column of selectedColumns) {
          if (column === x_axis) {
            continue;
          }
          cConfig[column] = {
            label: column,
            color: "hsl(var(--chart-" + i + "))",
          };
          i++;
        }
      } else if (chartType === "pie") {
        console.log("In pie");
        cConfig[selectedColumns[0]] = {
          label: selectedColumns[0],
          color: "#60a5fa",
        };
        var i = 1;
        for (const row of chartData) {
          cConfig[row[x_axis]] = {
            label: row[x_axis],
            color: "#DDDD33",
          };
          i++;
        }
      }
      var j = 1;
      for (const row of chartData) {
        row["fill"] = "hsl(var(--chart-" + j + "))";
        j++;
      }
      setChartConfig(cConfig);
      console.log(chartData);
      console.log(cConfig);
      console.log(chartConfig);
    }

    const removeColumn = (column: string) => {
      setSelectedColumns(selectedColumns.filter((c) => c !== column));
    }

    const addColumn = (column: string) => {
      if (selectedColumns.includes(column)) {
        removeColumn(column);
      } else {
        setSelectedColumns([...selectedColumns, column]);
      }
      console.log(selectedColumns);
      generateChartData(chart_type);
    }
    return (
      <div className="flexgap-4 align-middle text-center content-center">
        <br />
        <div className="flex items-center gap-4 content-center">
          <div className="text-center text-sm">Chart Type</div>
          <Select onValueChange={(value) => {
            setChartType(value);
            generateChartData(value);
          }}>
          <SelectTrigger className="min-w-[80px] rounded-md">
            <SelectValue placeholder={chart_type} />
          </SelectTrigger>
          <SelectContent className="border-none min-w-[80px] card">
            {["bar", "pie", "line"].map((type) => (
              <SelectItem 
                key={type}
                value={type}
              >
                {type}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <div>XAxis</div>
          <Select onValueChange={(value) => {
            setXAxis(value);
            generateChartData(chart_type);
          }}>
          <SelectTrigger className="min-w-[80px] rounded-md">
            <SelectValue placeholder={x_axis} />
          </SelectTrigger>
          <SelectContent className="border-none min-w-[80px] card">
            {columns.map((column) => (
              <SelectItem 
                key={column}
                value={column}
              >
                {column}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <div>Values</div>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline">Select Columns</Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="border-none card">
            {columns.map((column) => (
              <DropdownMenuCheckboxItem
                key={column}
                checked={selectedColumns.includes(column)}
                onCheckedChange={() => addColumn(column)}
              >
                {column}
              </DropdownMenuCheckboxItem>
            ))}
          </DropdownMenuContent>
        </DropdownMenu>
        </div>
        <div className="w-full">
            {chartConfig && chartData && (
              <div ref={chartRef}>
              <ChartContainer config={chartConfig as ChartConfig} className="min-h-[100px] max-h-[500px] pt-8">
                {chart_type === "bar" ? (
                  <BarChart data={chartData as any}>
                    <XAxis
                      dataKey={x_axis}
                      tickLine={true}
                      tickMargin={4}
                      axisLine={true}
                      tickFormatter={(value) => typeof value === 'string' ? value.slice(0, 3) : value}
                    />
                    <YAxis />
                    {Object.values(chartConfig).map((config) => (
                      <Bar key={config.label as any} dataKey={config.label as any} fill={config.color} radius={4} />
                    ))}
                  </BarChart>
                ) : chart_type === "pie" ? (
                  <PieChart data={chartData as any}>
                    {selectedColumns.length > 0 && (
                      <Pie data={chartData as any} dataKey={selectedColumns[0]} nameKey={x_axis}>
                        <LabelList dataKey={x_axis} position="top" />
                      </Pie>
                    )}
                  </PieChart>
                ) : chart_type === "line" ? (
                    <LineChart data={chartData as any} className="pt-8">
                      <CartesianGrid vertical={false} />
                      <XAxis
                        dataKey={x_axis}
                        tickLine={true}
                        axisLine={true}
                        tickMargin={4}
                        tickFormatter={(value) => typeof value === 'string' ? value.slice(0, 3) : value}
                      />
                      <YAxis />
                      {selectedColumns.filter((column) => column !== x_axis).map((column) => (
                        <Line key={column} type="monotone" dataKey={column} stroke={chartConfig[column]?.color || "#60a5fa"}/>
                        ))}
                    </LineChart>
                ) : <div>No chart type selected</div>}
              </ChartContainer>
              </div>
            )}
        </div>
        <Button onClick={downloadImage}>Download PNG</Button>
      </div>
    )
  
};

export default ChatPreviewComponent;