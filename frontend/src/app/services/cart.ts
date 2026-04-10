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
  // Add this inside your Cart service class
  // Add this inside your Cart service class
  removeFromCart(dish: any) {
    this.cartItems.update(items => {
      // FIX: We only check for i.id now!
      const index = items.findIndex(i => i.id === dish.id);
      
      if (index !== -1) {
        if (items[index].quantity > 1) {
          // If they have more than 1, just decrease the quantity by 1
          const newItems = [...items];
          newItems[index] = { ...newItems[index], quantity: newItems[index].quantity - 1 };
          return newItems;
        } else {
          // If they only have 1, remove it from the cart entirely
          return items.filter((_, i) => i !== index);
        }
      }
      return items;
    });
  }
  clearCart() {
    this.cartItems.set([]); // This instantly resets the Signal to an empty array!
  }
}