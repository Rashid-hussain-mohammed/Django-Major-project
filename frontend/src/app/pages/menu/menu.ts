import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ApiService } from '../../services/api';
import { Cart } from '../../services/cart'; 

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [],
  templateUrl: './menu.html',
  styleUrl: './menu.scss'
})
export class Menu implements OnInit {
  dishes: any[] = [];
  isAiLoading = false; 

  constructor(
    private api: ApiService, 
    private cdr: ChangeDetectorRef,
    public cart: Cart 
  ) {}

  ngOnInit(): void {
    this.api.getDishes().subscribe({
      next: (data) => {
        this.dishes = data;
        this.cdr.detectChanges(); 
      },
      error: (err) => console.error("Failed to fetch menu:", err)
    });
  }

  // 1. ADD TO CART
  addToCart(dish: any) {
    this.cart.addToCart(dish);
  }

  // 2. REMOVE FROM CART (This was missing!)
  removeFromCart(dish: any) {
    this.cart.removeFromCart(dish);
  }

  // 3. GET QUANTITY (This was missing!)
  getItemQuantity(dishId: number): number {
    const items = this.cart.cartItems(); 
    const item = items.find((i: any) => i.id === dishId);
    return item ? item.quantity : 0;
  }

  // 4. THE AI COMMAND
  submitAiCommand(inputElement: HTMLInputElement) {
    const text = inputElement.value;
    if (!text.trim()) return; 

    this.isAiLoading = true;

    this.api.parseOrderText(text).subscribe({
      next: (response) => {
        const items = response.parsed_items;
        
        if (items && items.length > 0) {
          items.forEach((item: any) => {
            for (let i = 0; i < item.quantity; i++) {
              this.cart.addToCart(item); 
            }
          });
          
          inputElement.value = ''; 
          alert(`🪄 Magic! Added ${items.length} type(s) of items to your cart.`);
        } else {
          alert("🤖 Hmm, I couldn't find any menu items in that sentence. Try asking for a Burger or Pizza!");
        }
        
        this.isAiLoading = false;
      },
      error: (err) => {
        console.error('AI Error:', err);
        alert("Oops, the AI is taking a nap. Make sure your Django server is running!");
        this.isAiLoading = false;
      }
    });
  }
}