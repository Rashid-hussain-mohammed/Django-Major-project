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
  // Add a new dish to the menu
  addDish(dishData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/dishes/`, dishData);
  }

  // Delete a dish from the menu
  deleteDish(dishId: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/dishes/${dishId}/`);
  }
  // Fetch all orders for the dashboard
  getOrders(): Observable<any> {
    return this.http.get(`${this.baseUrl}/orders/`);
  }

  // Fetch all AI reviews for the dashboard
  getReviews(): Observable<any> {
    return this.http.get(`${this.baseUrl}/reviews/`);
  }
  submitOrder(orderData: any): Observable<any> {
    // Assuming your Django urls.py has an endpoint for /orders/
    return this.http.post(`${this.baseUrl}/orders/`, orderData);
  }
  // Send a raw sentence to Django's AI parser
// Send the customer's text AND their restaurant ID to the AI
  parseOrderText(text: string, restaurantId: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/ai-parse/`, { 
      text: text, 
      restaurant_id: restaurantId 
    });
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
  // Fetch dishes for a specific restaurant ID
getDishesByRestaurant(restaurantId: string): Observable<any> {
  // We send the ID as a "query parameter" (e.g., ?restaurant=5)
  return this.http.get(`${this.baseUrl}/dishes/?restaurant=${restaurantId}`);
}
}