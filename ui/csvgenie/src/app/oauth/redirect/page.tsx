'use client'
import { backendUrl } from '@/lib/utils';
import { useSearchParams } from 'next/navigation';
import React, { useEffect } from 'react';
import '@/styles/theme-sky.css';
import { Suspense } from 'react';

function OAuthRedirect() {
  return (<Suspense>
    <OAuthRedirectSubComponent />
  </Suspense>)
}

const OAuthRedirectSubComponent: React.FC = () => {
  const params = useSearchParams();

  useEffect(() => {
    
    const code = params.get('code');

    if (code) {
      const canvaToken = async () => {
      const response = await fetch(`${backendUrl}/canva-token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
          body: JSON.stringify({ code }),
        });
        const data = await response.json();
        console.log(data);
        // close window
        window.close();
      };
      canvaToken();
    } else {
      console.error('No code found in URL');
      // Handle the case where no code is present
    }
  }, [params]);

  return (  
    <div>
      <h1>OAuth Redirect</h1>
      <p>Processing your request...</p>
    </div>
  );
};

export default OAuthRedirect;