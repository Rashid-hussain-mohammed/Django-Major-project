import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './register.html'
})
export class Register {
  username = '';
  email = '';
  password = '';
  isSubmitting = false;

  constructor(private api: ApiService, private router: Router) {}

  onSubmit() {
    if (!this.username || !this.password) return;
    
    this.isSubmitting = true;
    
    const userData = {
      username: this.username,
      email: this.email,
      password: this.password
    };

    this.api.registerUser(userData).subscribe({
      next: (response) => {
        alert('Account created successfully! Please log in.');
        this.router.navigate(['/login']);
      },
      error: (err) => {
        console.error('Registration failed', err);
        alert('Could not create account. Username might be taken.');
        this.isSubmitting = false;
      }
    });
  }
}