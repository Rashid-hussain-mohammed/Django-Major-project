import { Component } from '@angular/core';
import { DecimalPipe } from '@angular/common';
import { RouterLink, Router } from '@angular/router'; // 1. Add Router
import { Cart as CartService } from '../../services/cart'; 
import { ApiService } from '../../services/api'; // 2. Import API Service

@Component({
  selector: 'app-cart',
  standalone: true,
  imports: [DecimalPipe, RouterLink],
  templateUrl: './cart.html',
  styleUrl: './cart.scss'
})
export class Cart {
  isSubmitting = false; // Prevents double-clicking the checkout button

  // 3. Inject the Router and API Service
  constructor(
    public cartService: CartService,
    private api: ApiService,
    private router: Router
  ) {}

  getItemTotal(price: string | number, quantity: number): number {
    return Number(price) * quantity;
  }

  // 4. The actual checkout function
  checkout() {
    if (this.cartService.totalItems() === 0) return;
    
    this.isSubmitting = true;

    // Package the cart data for Django
    const payload = {
      table : 1,
      total_price: this.cartService.totalPrice(),
      items: this.cartService.cartItems().map(item => ({
        dish_id: item.id,
        quantity: item.quantity
      }))
    };

    this.api.submitOrder(payload).subscribe({
      next: (response) => {
        alert('🎉 Order sent successfully to the kitchen!');
        this.cartService.clearCart(); // Empty the cart
        this.router.navigate(['/']); // Redirect to the main menu
      },
      error: (err) => {
        console.error('Checkout failed:', err);
        alert('There was an issue sending your order. Check the console.');
        this.isSubmitting = false;
      }
    });
  }
}