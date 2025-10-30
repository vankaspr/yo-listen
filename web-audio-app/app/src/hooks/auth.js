export function useAuthFetch() {
  const authFetch = async (url, options = {}) => {
    const token = localStorage.getItem('access_token');

    const response = await fetch(url, {
      ...options,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (response.status === 401) {
        localStorage.removeItem('access_token');
        window.location.reload();
        // refresh token 
    } 

    return response;
  };

  return { authFetch };
}
