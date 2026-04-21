import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './login.html'
})
export class Login {
  email = '';
  password = '';
  isSubmitting = false;

  constructor(private api: ApiService, private router: Router) {}

  onSubmit() {
    if (!this.email || !this.password) return;
    
    this.isSubmitting = true;

    const credentials = {
      email: this.email,
      password: this.password
    };

    this.api.loginUser(credentials).subscribe({
      next: (response) => {
        // 1. Save the secure token and manager status to the browser's memory
        localStorage.setItem('token', response.token);
        localStorage.setItem('is_manager', response.is_manager ? 'true' : 'false');
        
        // 2. Redirect to the homepage (we will build a Dashboard next!)
        alert('Welcome back!');
        this.router.navigate(['/']); 
      },
      error: (err) => {
        console.error('Login failed', err);
        alert('Invalid email or password.');
        this.isSubmitting = false;
      }
    });
  }
}