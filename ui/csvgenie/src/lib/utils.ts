import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const backendUrl = 'http://localhost:8000';
export const cdnUrl = 'https://d3v7i4t2a934fu.cloudfront.net';
export type CsvData = any;
export type ScriptData = {
  screen_1: {
    text: string;
    voice_over: string;
  },
  screen_2: {
    text: string;
    voice_over: string;
  },
  screen_3: {
    text: string;
    voice_over: string;
  },
  screen_4: {
    text: string;
    voice_over: string;
  },
  screen_5: {
    text: string;
    voice_over: string;
  }
};
export const transformCsvData = (csvData: CsvData) => {
  const transformed_csv = [];
  const columns = Object.keys(csvData);
  const numRows = Object.keys(csvData[columns[0]]).length;
  for (let i = 0; i < numRows; i++) {
    const row: { [key: string]: string | number } = {};
    for (const column of columns) {
      row[column] = csvData[column][i.toString()];
    }
    transformed_csv.push(row);
  }
  return {columns: columns, transformed_csv: transformed_csv};
};