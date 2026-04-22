import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common'; // Need this for @if if not standalone-configured properly

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [RouterLink, CommonModule],
  templateUrl: './landing.html'
})
export class Landing implements OnInit {
  isLoggedIn = false;

  ngOnInit() {
    // Check if the browser has a saved token!
    if (typeof window !== 'undefined' && localStorage.getItem('token')) {
      this.isLoggedIn = true;
    }
  }

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('is_manager');
    this.isLoggedIn = false;
  }
}