import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  // Our proxy intercepts this and sends it to Django port 8000
  private baseUrl = '/accounts/api';

  constructor(private http: HttpClient) { }

  getDishes(): Observable<any> {
    return this.http.get(`${this.baseUrl}/dishes/`);
  }
  submitOrder(orderData: any): Observable<any> {
    // Assuming your Django urls.py has an endpoint for /orders/
    return this.http.post(`${this.baseUrl}/orders/`, orderData);
  }
  // Send a raw sentence to Django's AI parser
  parseOrderText(text: string) {
    return this.http.post<any>(`${this.baseUrl}/ai-order/`, { text });
  }
  // Submit a review to the AI Engine
  submitReview(reviewData: any) {
    return this.http.post<any>(`${this.baseUrl}/reviews/`, reviewData);
  }
  // Register a new restaurant owner
// Register a new restaurant owner
  registerUser(userData: any) {
    return this.http.post<any>(`${this.baseUrl}/register/`, userData);
  }

  // Login an existing owner
  loginUser(credentials: any) {
    return this.http.post<any>(`${this.baseUrl}/login/`, credentials);
  }
}