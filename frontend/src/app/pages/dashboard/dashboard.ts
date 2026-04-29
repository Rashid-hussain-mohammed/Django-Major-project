import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { ApiService } from '../../services/api';
import { WebsocketService } from '../../services/websocket';
import { DatePipe, DecimalPipe, NgClass } from '@angular/common'; // <-- ADDED NgClass HERE
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [DatePipe, DecimalPipe, RouterLink, FormsModule, NgClass], // <-- ADDED NgClass HERE
  templateUrl: './dashboard.html'
})
export class Dashboard implements OnInit, OnDestroy { // <-- Implement OnDestroy
  activeTab: 'overview' | 'orders' | 'menu' | 'tables' = 'overview'; 
  
  orders: any[] = [];
  reviews: any[] = [];
  dishes: any[] = []; 
  tables: any[] = []; 
  
  averageSentiment = 0;
  isLoading = true;

  pendingOrders: any[] = [];
  preparingOrders: any[] = [];
  completedOrders: any[] = [];

  newDish = { name: '', description: '', price: null, is_available: true };
  newTableNumber: number | null = null; 

  // --- NEW: Inject the WebsocketService ---
  constructor(private api: ApiService, private wsService: WebsocketService, private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    this.loadDashboardData();

    // --- NEW: Start the Real-Time Connection! ---
    // (We use '2' here assuming your test manager account ID is 2. 
    // In a final production app, you would pull this dynamically from the logged-in user profile).
    this.wsService.connectDashboard('1');

    // Listen for the magic signal. If we hear it, reload the orders!
    this.wsService.dashboardUpdates.subscribe(() => {
      // We only need to reload the orders to save bandwidth
      this.api.getOrders().subscribe(data => {
        this.orders = data;
        this.sortOrders();
        this.cdr.detectChanges();
      });
    });
  }

  // Clean up the connection if the manager logs out or leaves the page
  ngOnDestroy() {
    this.wsService.disconnectDashboard();
  }

  loadDashboardData() {
    // ... (Keep the rest of your file exactly the same from here down!)
    this.api.getOrders().subscribe({
      next: (data) => {
        this.orders = data;
        this.sortOrders(); 
      },
      error: (err) => console.error('Failed to load orders', err)
    });

    this.api.getReviews().subscribe(data => {
      this.reviews = data;
      if (this.reviews.length > 0) {
        const totalScore = this.reviews.reduce((sum, review) => sum + (review.sentiment_score || 0), 0);
        this.averageSentiment = totalScore / this.reviews.length;
      }
    });

    this.api.getDishes().subscribe(data => this.dishes = data);

    this.api.getTables().subscribe(data => {
      this.tables = data;
      this.isLoading = false; 
    });
  }
  
  // ... (Keep sortOrders, changeOrderStatus, etc. exactly the same)
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

  // --- MANAGER CHAT VARIABLES ---
  activeChatOrderId: string | null = null;
  chatMessages: { message: string, sender: string }[] = [];
  newChatMessage: string = '';
  chatSub?: Subscription;

  // --- MANAGER CHAT FUNCTIONS ---
  openChat(orderId: number) {
    this.activeChatOrderId = orderId.toString();
    this.chatMessages = []; // Clear old messages
    this.wsService.connectChat(this.activeChatOrderId);

    // Unsubscribe from any previous chat to prevent double-messages
    if (this.chatSub) this.chatSub.unsubscribe();

    // Listen for messages in this specific room
    this.chatSub = this.wsService.chatMessages.subscribe((data) => {
      this.chatMessages.push({ message: data.message, sender: data.sender });
      this.cdr.detectChanges(); // Force UI to update
    });
  }

  closeChat() {
    this.activeChatOrderId = null;
    if (this.chatSub) this.chatSub.unsubscribe();
    this.wsService.disconnectChat();
  }

  sendChatMessage() {
    if (!this.newChatMessage.trim() || !this.activeChatOrderId) return;
    // Send message as 'manager'
    this.wsService.sendChatMessage(this.newChatMessage, 'manager');
    this.newChatMessage = '';
  }
}