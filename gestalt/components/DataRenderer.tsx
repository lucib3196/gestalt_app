"use client";
import { useState, useEffect } from 'react';
import api from '@/api';



type ApiConfig = {
  url: string;
  method?: 'get' | 'post' | 'put' | 'delete' | 'patch';
  params?: Record<string, any>;
  headers?: Record<string, string>;
  data?: any;
};

type DataRendererProps<T> = {
  source: ApiConfig | T[];
  loadingComponent?: React.ReactNode;
  errorComponent?: React.ReactNode;
  children: (data: T[], isLoading: boolean, error: Error | null) => React.ReactNode;
};

export function DataRenderer<T>({
  source,
  loadingComponent = <div>Loading...</div>,
  errorComponent = <div>Error loading data</div>,
  children
}: DataRendererProps<T>) {
  const [data, setData] = useState<T[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!('url' in source)) return; // Static data provided used mainly for testing 
      
      setIsLoading(true);
      setError(null);
      
      try {
        // Using your existing api client
        const response = await api({
          url: source.url,
          method: source.method || 'get',
          params: source.params,
          headers: source.headers,
          data: source.data
        });
        // Set the array 
        setData(Array.isArray(response.data) ? response.data : [response.data]);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Unknown error'));
      } finally {
        setIsLoading(false);
      }
    };

    if ('url' in source) {
      fetchData();
    } else {
      setData(source); // Set static data directly
    }
  }, [source]);

  if (error) return <>{errorComponent}</>;
  if (isLoading) return <>{loadingComponent}</>;
  
  return <>{children(data, isLoading, error)}</>;
}