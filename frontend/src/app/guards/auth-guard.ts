import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';

export const authGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  
  // Check if we are running in the browser and if a token exists
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('token');
    
    if (token) {
      return true; // The door opens!
    }
  }

  // No token? Kick them to the login page.
  router.navigate(['/login']);
  return false; 
};