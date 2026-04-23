import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api';
import { DatePipe, DecimalPipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [DatePipe, DecimalPipe, RouterLink, FormsModule],
  templateUrl: './dashboard.html'
})
export class Dashboard implements OnInit {
  // Added 'tables' to the activeTab types
  activeTab: 'overview' | 'orders' | 'menu' | 'tables' = 'overview'; 
  
  orders: any[] = [];
  reviews: any[] = [];
  dishes: any[] = []; 
  tables: any[] = []; // Array to hold your tables
  
  averageSentiment = 0;
  isLoading = true;

  // Buckets for the Kanban Board
  pendingOrders: any[] = [];
  preparingOrders: any[] = [];
  completedOrders: any[] = [];

  newDish = { name: '', description: '', price: null, is_available: true };
  newTableNumber: number | null = null; // For the create table input

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadDashboardData();
  }

  loadDashboardData() {
    // 1. Fetch Orders & Sort them into buckets
    this.api.getOrders().subscribe({
      next: (data) => {
        this.orders = data;
        this.sortOrders(); 
      },
      error: (err) => console.error('Failed to load orders', err)
    });

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
    });

    // 4. Fetch Tables
    this.api.getTables().subscribe(data => {
      this.tables = data;
      this.isLoading = false; 
    });
  }

  // --- Order Management Functions ---

  sortOrders() {
    this.pendingOrders = this.orders.filter(o => o.status === 'PENDING');
    this.preparingOrders = this.orders.filter(o => o.status === 'PREPARING');
    this.completedOrders = this.orders.filter(o => o.status === 'SERVED' || o.status === 'PAID');
  }

  changeOrderStatus(orderId: number, newStatus: string) {
    this.api.updateOrderStatus(orderId, newStatus).subscribe({
      next: () => {
        this.loadDashboardData(); // Reload the board to visually move the card
      },
      error: (err) => console.error('Failed to update status', err)
    });
  }

  // --- Menu Management Functions ---

  addNewDish() {
    if (!this.newDish.name || !this.newDish.price) return; 
    
    this.api.addDish(this.newDish).subscribe({
      next: (createdDish) => {
        this.dishes.push(createdDish); 
        this.newDish = { name: '', description: '', price: null, is_available: true }; 
      },
      error: (err) => console.error('Failed to add dish', err)
    });
  }

  removeDish(dishId: number) {
    if (confirm('Are you sure you want to delete this dish?')) {
      this.api.deleteDish(dishId).subscribe({
        next: () => {
          this.dishes = this.dishes.filter(d => d.id !== dishId);
        },
        error: (err) => console.error('Failed to delete dish', err)
      });
    }
  }

  // --- Table Management Functions ---

  addNewTable() {
    if (!this.newTableNumber) return;
    this.api.createTable({ number: this.newTableNumber }).subscribe({
      next: (createdTable) => {
        this.tables.push(createdTable);
        // Sort tables numerically so they stay organized
        this.tables.sort((a, b) => a.number - b.number);
        this.newTableNumber = null; // reset input
      },
      error: (err) => alert('Failed to create table. Make sure the number is unique!')
    });
  }

  removeTable(tableId: number) {
    if (confirm('Are you sure you want to delete this table? Customers using this QR code will get an error.')) {
      this.api.deleteTable(tableId).subscribe({
        next: () => {
          this.tables = this.tables.filter(t => t.id !== tableId);
        },
        error: (err) => console.error('Failed to delete table', err)
      });
    }
  }

  // Instantly generates a QR code image URL for the specific table!
  getQrCodeUrl(secureId: string): string {
    const tableUrl = `http://localhost:4200/menu/${secureId}`;
    return `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(tableUrl)}`;
  }
}