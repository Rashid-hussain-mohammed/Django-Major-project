import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api';
import { DatePipe, DecimalPipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms'; // <-- Need this for the add dish form!

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [DatePipe, DecimalPipe, RouterLink, FormsModule],
  templateUrl: './dashboard.html'
})
export class Dashboard implements OnInit {
  activeTab: 'overview' | 'menu' = 'overview'; // State for our tabs
  
  orders: any[] = [];
  reviews: any[] = [];
  dishes: any[] = []; // Store the menu items
  averageSentiment = 0;
  isLoading = true;

  // Temporary object for our new dish form
  newDish = { name: '', description: '', price: null, is_available: true };

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadDashboardData();
  }

  loadDashboardData() {
    // 1. Fetch Orders
    this.api.getOrders().subscribe(data => this.orders = data);

    // 2. Fetch Reviews
    this.api.getReviews().subscribe(data => {
      this.reviews = data;
      if (this.reviews.length > 0) {
        const totalScore = this.reviews.reduce((sum, review) => sum + (review.sentiment_score || 0), 0);
        this.averageSentiment = totalScore / this.reviews.length;
      }
    });

    // 3. Fetch Dishes
    this.api.getDishes().subscribe(data => {
      this.dishes = data;
      this.isLoading = false; // Turn off loading when everything is done
    });
  }

  // --- Menu Management Functions ---

  addNewDish() {
    if (!this.newDish.name || !this.newDish.price) return; // Basic validation
    
    this.api.addDish(this.newDish).subscribe({
      next: (createdDish) => {
        this.dishes.push(createdDish); // Add it to the UI immediately
        this.newDish = { name: '', description: '', price: null, is_available: true }; // Reset form
      },
      error: (err) => console.error('Failed to add dish', err)
    });
  }

  removeDish(dishId: number) {
    if (confirm('Are you sure you want to delete this dish?')) {
      this.api.deleteDish(dishId).subscribe({
        next: () => {
          // Remove the dish from the UI array without refreshing the page!
          this.dishes = this.dishes.filter(d => d.id !== dishId);
        },
        error: (err) => console.error('Failed to delete dish', err)
      });
    }
  }
}