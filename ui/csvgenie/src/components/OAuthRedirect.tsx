import { useRouter } from 'next/router';
import React, { useEffect } from 'react';

const OAuthRedirect: React.FC = () => {
  const router = useRouter(); // For Next.js

  useEffect(() => {
    const { code } = router.query;

    if (code) {
      const canvaToken = async () => {
      const response = await fetch('/api/canva-token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
          body: JSON.stringify({ code }),
        });
        const data = await response.json();
        console.log(data);
      };
      canvaToken();
    } else {
      console.error('No code found in URL');
      // Handle the case where no code is present
    }
  }, [router.query]); // For Next.js

  return (
    <div>
      <h1>OAuth Redirect</h1>
      <p>Processing your request...</p>
    </div>
  );
};

export default OAuthRedirect;