export { signInWithGoogle, signOut } from './googleAuth';

export { signInWithKakao, subscribeToAuthChanges } from './kakaoAuth';

export function handleTokenFromUrl(url) {
  const params = new URLSearchParams(url.search);
  const token = params.get('token');
  
  if (token) {
    localStorage.setItem('auth_token', token);
    
    params.delete('token');
    const newUrl = window.location.pathname + (params.toString() ? `?${params.toString()}` : '');
    window.history.replaceState({}, document.title, newUrl);
    
    return token;
  }
  
  return null;
}

export function getAuthToken() {
  return localStorage.getItem('auth_token');
}

export async function getCurrentUser() {
  const token = getAuthToken();
  
  if (!token) {
    return null;
  }
  
  try {
    const response = await fetch('http://localhost:3000/api/auth/session', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      if (response.status === 401) {
        localStorage.removeItem('auth_token');
      }
      return null;
    }
    
    const user = await response.json();
    return user;
  } catch (error) {
    console.error('Failed to get user information:', error);
    return null;
  }
}

export async function isAuthenticated() {
  const user = await getCurrentUser();
  return !!user;
}

export async function authFetch(url, options = {}) {
  const token = getAuthToken();
  
  if (url.startsWith('/api')) {
    url = `http://localhost:3000${url}`;
  }
  
  if (token) {
    const headers = {
      ...(options.headers || {}),
      'Authorization': `Bearer ${token}`
    };
    
    return fetch(url, {
      ...options,
      headers
    });
  }
  
  return fetch(url, options);
}

import { supabase } from '$lib/supabase';

export async function getCurrentSession() {
  if (!supabase) {
    console.error('Supabase client is not initialized.');
    return null;
  }

  const { data, error } = await supabase.auth.getSession();
  
  if (error) {
    console.error('Failed to get session information:', error.message);
    return null;
  }
  
  return data.session;
}

export async function handleAuthChange(event, session) {
  if (!supabase) {
    console.error('Supabase client is not initialized.');
    return;
  }

  if (event === 'SIGNED_IN' && session) {
    const user = session.user;
    
    const now = new Date().toISOString();
    
    const provider = user.app_metadata?.provider || '';
    
    const { error } = await supabase.from('users').upsert({
      uuid: user.id,
      display_name: user.user_metadata?.full_name || user.user_metadata?.name || user.email,
      email: user.email,
      phone: user.phone || '',
      provider: provider,
      provider_type: 'social',
      user_status: true,
      created_at: user.created_at || now,
      last_sign_in_at: now
    }, { onConflict: 'uuid' });
    
    if (error) {
      console.error('Error saving user information:', error);
    }
  }
} 