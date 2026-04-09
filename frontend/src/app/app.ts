import { Component } from '@angular/core';
import { Cart } from './services/cart';
import { DecimalPipe } from '@angular/common';
import { RouterOutlet, RouterLink } from '@angular/router';
//import { Menu } from './pages/menu/menu'; 

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink, DecimalPipe],//imports: [Menu, DecimalPipe], // 2. Add it to this array (and remove RouterOutlet)
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  title = 'frontend';
  constructor(public cart: Cart) {}
}