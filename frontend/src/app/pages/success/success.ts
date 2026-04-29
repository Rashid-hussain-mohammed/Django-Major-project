import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApiService } from '../../services/api';
import { WebsocketService } from '../../services/websocket'; // <-- NEW IMPORT
import { FormsModule } from '@angular/forms';
import { DecimalPipe, NgClass } from '@angular/common'; // <-- ADDED NgClass

@Component({
  selector: 'app-success',
  standalone: true,
  imports: [RouterLink, FormsModule, DecimalPipe, NgClass], // <-- ADDED NgClass here
  templateUrl: './success.html'
})
export class Success implements OnInit, OnDestroy { // <-- Added OnDestroy
  orderId: number | null = null;
  foodRating = 10;     
  serviceRating = 10;  
  feedback = '';
  
  isSubmitting = false;
  isAnalyzed = false; 
  aiScore: number = 0; 

  // --- NEW: CHAT VARIABLES ---
  chatMessages: { message: string, sender: string }[] = [];
  newMessage: string = '';

  constructor(
    private route: ActivatedRoute, 
    private api: ApiService,
    private wsService: WebsocketService, // <-- NEW: Injected Websocket
    private cdr: ChangeDetectorRef 
  ) {}

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      if (params['orderId']) {
        this.orderId = Number(params['orderId']);
        
        // 🟢 CONNECT TO THE CHAT ROOM USING THE ORDER ID
        this.wsService.connectChat(this.orderId.toString());

        // 👂 LISTEN FOR INCOMING MESSAGES
        this.wsService.chatMessages.subscribe((data) => {
          this.chatMessages.push({ message: data.message, sender: data.sender });
          this.cdr.detectChanges(); // Force UI update
        });
      }
    });
  }

  // 🔴 DISCONNECT WHEN LEAVING THE PAGE
  ngOnDestroy() {
    this.wsService.disconnectChat();
  }

  // 💬 SEND MESSAGE TO KITCHEN
  sendMessage() {
    if (!this.newMessage.trim() || !this.orderId) return;
    
    this.wsService.sendChatMessage(this.newMessage, 'customer');
    this.newMessage = ''; // clear input
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
        console.log("Django AI Response:", response);
        this.aiScore = response.sentiment_score ?? 0; 
        this.isSubmitting = false;
        this.isAnalyzed = true; 
        this.cdr.detectChanges(); 
      },
      error: (err) => {
        console.error('Feedback failed:', err);
        alert('Failed to submit feedback.');
        this.isSubmitting = false;
      }
    });
  }
}