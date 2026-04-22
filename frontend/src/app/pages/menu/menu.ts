import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ApiService } from '../../services/api';
import { Router, RouterLink, ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [RouterLink, FormsModule],
  templateUrl: './menu.html'
})
export class Menu implements OnInit {
  dishes: any[] = [];
  isLoading = true;
  
  // SaaS Routing Variables
  restaurantId: string | null = null;
  tableId: string | null = null;
  
  orderText: string = '';
  isParsing = false;

  constructor(
    private api: ApiService, 
    private router: Router,
    private route: ActivatedRoute,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit() {
    this.restaurantId = this.route.snapshot.paramMap.get('restaurantId');
    this.tableId = this.route.snapshot.paramMap.get('tableId');

    if (this.restaurantId && this.tableId) {
      localStorage.setItem('currentRestaurant', this.restaurantId);
      localStorage.setItem('currentTable', this.tableId);
      
      this.api.getDishesByRestaurant(this.restaurantId).subscribe({
        next: (data) => {
          console.log('✅ UI RECEIVED DATA:', data); // <--- This will prove Angular sees it!
          this.dishes = data;
          this.isLoading = false; // <--- This turns off the loading screen!
          this.cdr.detectChanges();
        },
        error: (err) => {
          console.error('❌ UI FAILED TO LOAD:', err);
          this.isLoading = false;
          this.cdr.detectChanges();
        }
      });
    } else {
      this.isLoading = false;
    }
  }

  submitToAI() {
    if (!this.orderText.trim() || !this.restaurantId) return;
    this.isParsing = true;

    // Send BOTH the text and the restaurant ID!
    this.api.parseOrderText(this.orderText, this.restaurantId).subscribe({
      next: (response) => {
        localStorage.setItem('cartItems', JSON.stringify(response.parsed_items));
        this.router.navigate(['/cart']);
      },
      error: (err) => {
        console.error('AI Parsing failed', err);
        this.isParsing = false;
        this.cdr.detectChanges();
      }
    });
  }
}