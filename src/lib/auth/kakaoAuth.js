export async function signInWithKakao() {
  try {
    window.location.href = 'http://localhost:3000/api/auth/kakao';
  } catch (error) {
    console.error('Error during Kakao login:', error);
    throw error;
  }
}

export function subscribeToAuthChanges(callback) {
  const checkTokenInterval = setInterval(() => {
    const token = localStorage.getItem('auth_token');
    const authenticated = !!token;
    
    callback('TOKEN_CHANGE', { authenticated });
  }, 2000);
  
  return {
    unsubscribe: () => {
      clearInterval(checkTokenInterval);
    }
  };
} 