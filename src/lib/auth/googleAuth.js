export async function signInWithGoogle() {
  try {
    window.location.href = 'http://localhost:3000/api/auth/google';
  } catch (error) {
    console.error('Error during Google login:', error);
    throw error;
  }
}

export async function signOut(redirectTo = '/') {
  try {
    const response = await fetch('http://localhost:3000/api/auth/logout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    });
    
    if (!response.ok) {
      throw new Error('An error occurred during logout.');
    }
    
    console.log('Logout successful');
    
    localStorage.removeItem('auth_token');
    
    window.location.href = redirectTo;
  } catch (error) {
    console.error('Error during logout:', error);
    throw error;
  }
} 