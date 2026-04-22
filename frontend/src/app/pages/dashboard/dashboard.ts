import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api';
import { DatePipe, DecimalPipe } from '@angular/common';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [DatePipe, DecimalPipe, RouterLink],
  templateUrl: './dashboard.html'
})
export class Dashboard implements OnInit {
  orders: any[] = [];
  reviews: any[] = [];
  averageSentiment = 0;
  isLoading = true;

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadDashboardData();
  }

  loadDashboardData() {
    // 1. Fetch Orders
    this.api.getOrders().subscribe({
      next: (data) => {
        console.log('✅ Orders received:', data);
        this.orders = data.reverse(); // Safely reverse in TS, not HTML!
      },
      error: (err) => console.error('Failed to load orders', err)
    });

    // 2. Fetch Reviews and calculate the AI average
    this.api.getReviews().subscribe({
      next: (data) => {
        console.log('✅ Reviews received:', data);
        this.reviews = data.reverse(); // Safely reverse in TS, not HTML!
        
        if (this.reviews.length > 0) {
          const totalScore = this.reviews.reduce((sum, review) => sum + (review.sentiment_score || 0), 0);
          this.averageSentiment = totalScore / this.reviews.length;
        }
        
        // Turn off the loading screen
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Failed to load reviews', err);
        this.isLoading = false;
      }
    });
  }
}