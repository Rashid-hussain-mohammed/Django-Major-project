import { Injectable, signal, computed } from '@angular/core';

export interface CartItem {
  id: number;
  name: string;
  price: number | string; // Django sometimes sends prices as strings
  quantity: number;
}

@Injectable({
  providedIn: 'root'
})
export class Cart {
  // 1. The Core State (This is our Signal)
  cartItems = signal<CartItem[]>([]);

  // 2. Computed Signals (These automatically recalculate when cartItems change!)
  totalItems = computed(() => 
    this.cartItems().reduce((sum, item) => sum + item.quantity, 0)
  );

  totalPrice = computed(() => 
    this.cartItems().reduce((sum, item) => sum + (Number(item.price) * item.quantity), 0)
  );

  // 3. Actions
  addToCart(dish: any) {
    // .update() safely creates a new state array based on the old one
    this.cartItems.update(items => {
      const existingItem = items.find(item => item.id === dish.id);
      
      if (existingItem) {
        // If it's already in the cart, just add 1 to the quantity
        return items.map(item => 
          item.id === dish.id ? { ...item, quantity: item.quantity + 1 } : item
        );
      }
      
      // If it's new, add the whole object to the array
      return [...items, { id: dish.id, name: dish.name, price: dish.price, quantity: 1 }];
    });
  }
  clearCart() {
    this.cartItems.set([]); // This instantly resets the Signal to an empty array!
  }
}