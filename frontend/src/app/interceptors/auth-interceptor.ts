import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  // Grab the token from browser memory
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;

  // If a token exists, clone the request and attach it to the Headers
  if (token) {
    const authReq = req.clone({
      setHeaders: {
        Authorization: `Token ${token}`
      }
    });
    return next(authReq); // Send the secured request
  }

  // If no token (like when a customer is browsing the menu), send normally
  return next(req);
};