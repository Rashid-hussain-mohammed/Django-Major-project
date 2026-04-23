import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ApiService } from '../../services/api';
import { Router, RouterLink, ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Cart as CartService } from '../../services/cart'; 

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [RouterLink, FormsModule],
  templateUrl: './menu.html'
})
export class Menu implements OnInit {
  dishes: any[] = [];
  isLoading = true;
  
  // NEW: Only looking for the secret UUID now
  secureId: string | null = null; 
  
  searchQuery: string = ''; 

  constructor(
    private api: ApiService, 
    private router: Router,
    private route: ActivatedRoute,
    private cdr: ChangeDetectorRef,
    public cartService: CartService 
  ) {}

  ngOnInit() {
    // Grab the UUID from the URL (e.g., /menu/a1b2c3d4-...)
    this.secureId = this.route.snapshot.paramMap.get('secureId');

    if (this.secureId) {
      // Save the secret ID to memory so the Cart can use it later
      localStorage.setItem('currentSecureId', this.secureId);
      
      this.api.getDishesByRestaurant(this.secureId).subscribe({
        next: (data) => {
          this.dishes = data;
          this.isLoading = false; 
          this.cdr.detectChanges(); 
        },
        error: (err) => {
          console.error('Failed to load menu', err);
          this.isLoading = false;
          this.cdr.detectChanges();
        }
      });
    } else {
      this.isLoading = false;
    }
  }

  get filteredDishes() {
    if (!this.searchQuery) return this.dishes;
    const lowerCaseQuery = this.searchQuery.toLowerCase();
    return this.dishes.filter(dish => 
      dish.name.toLowerCase().includes(lowerCaseQuery) || 
      dish.description.toLowerCase().includes(lowerCaseQuery)
    );
  }

  addToCart(dish: any) {
    this.cartService.addToCart(dish);
  }
}