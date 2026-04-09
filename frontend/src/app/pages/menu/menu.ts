import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ApiService } from '../../services/api';
import { Cart } from '../../services/cart'; // <-- 1. Import the Cart

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [],
  templateUrl: './menu.html',
  styleUrl: './menu.scss'
})
export class Menu implements OnInit {
  dishes: any[] = [];

  // 2. Inject the cart into the constructor
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

  // 3. Create the function that the HTML will call
  addToCart(dish: any) {
    this.cart.addToCart(dish);
    console.log("Current Cart:", this.cart.cartItems()); // Just to prove it works!
  }
}