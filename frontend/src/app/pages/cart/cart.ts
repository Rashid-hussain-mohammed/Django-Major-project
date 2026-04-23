import { Component } from '@angular/core';
import { DecimalPipe } from '@angular/common';
import { RouterLink, Router } from '@angular/router'; 
import { Cart as CartService } from '../../services/cart'; 
import { ApiService } from '../../services/api'; 

@Component({
  selector: 'app-cart',
  standalone: true,
  imports: [DecimalPipe, RouterLink],
  templateUrl: './cart.html',
  styleUrl: './cart.scss'
})
export class Cart {
  isSubmitting = false; 

  constructor(
    public cartService: CartService,
    private api: ApiService,
    private router: Router
  ) {}

  getItemTotal(price: string | number, quantity: number): number {
    return Number(price) * quantity;
  }

  addToCart(item: any) {
    this.cartService.addToCart(item);
  }

  removeFromCart(item: any) {
    this.cartService.removeFromCart(item);
  }

  // --- UPDATED: Navigate back using the secure UUID ---
  goBackToMenu() {
    const secureId = localStorage.getItem('currentSecureId');
    
    if (secureId) {
      this.router.navigate([`/menu/${secureId}`]);
    } else {
      this.router.navigate(['/login']); 
    }
  }

  checkout() {
    if (this.cartService.totalItems() === 0) return;
    
    this.isSubmitting = true;

    // --- UPDATED: Grab the UUID from the browser's memory ---
    const secureId = localStorage.getItem('currentSecureId');

    // Package the cart data for Django using the table_uuid
    const payload = {
      table_uuid: secureId, 
      total_price: this.cartService.totalPrice(),
      items: this.cartService.cartItems().map(item => ({
        dish_id: item.id,
        quantity: item.quantity
      }))
    };

    this.api.submitOrder(payload).subscribe({
      next: (response) => {
        alert('Order sent successfully to the kitchen!');
        this.cartService.clearCart(); 
        this.router.navigate(['/success'], { queryParams: { orderId: response.id } }); 
      },
      error: (err) => {
        console.error('Checkout failed:', err);
        alert('There was an issue sending your order. Check the console.');
        this.isSubmitting = false;
      }
    });
  }
}