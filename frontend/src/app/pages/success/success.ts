import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api';
import { FormsModule } from '@angular/forms';
import { DecimalPipe } from '@angular/common';

@Component({
  selector: 'app-success',
  standalone: true,
  imports: [RouterLink, FormsModule, DecimalPipe],
  templateUrl: './success.html'
})
export class Success implements OnInit {
  orderId: number | null = null;
  foodRating = 10;     
  serviceRating = 10;  
  feedback = '';
  
  isSubmitting = false;
  isAnalyzed = false; // <-- NEW: Bulletproof screen toggle
  aiScore: number = 0; 

  constructor(
    private route: ActivatedRoute, 
    private api: ApiService,
    private cdr: ChangeDetectorRef // <-- NEW: Forces UI to update
  ) {}

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      if (params['orderId']) {
        this.orderId = Number(params['orderId']);
      }
    });
  }

  submitFeedback() {
    if (!this.orderId || !this.feedback.trim()) return;
    
    this.isSubmitting = true;

    const payload = {
      order: this.orderId,
      food_rating: this.foodRating,
      service_rating: this.serviceRating,
      feedback_text: this.feedback
    };

    this.api.submitReview(payload).subscribe({
      next: (response) => {
        console.log("Django AI Response:", response); // View the raw data in console!
        
        // Grab the score (fallback to 0 if it's missing)
        this.aiScore = response.sentiment_score ?? 0; 
        
        this.isSubmitting = false;
        this.isAnalyzed = true; // Trigger the screen flip!
        this.cdr.detectChanges(); // Force the screen to update
      },
      error: (err) => {
        console.error('Feedback failed:', err);
        alert('Failed to submit feedback.');
        this.isSubmitting = false;
      }
    });
  }
}