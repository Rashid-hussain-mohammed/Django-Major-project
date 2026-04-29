import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {
  private dashboardSocket!: WebSocket;
  private chatSocket!: WebSocket; // <--- NEW
  
  public dashboardUpdates = new Subject<any>();
  public chatMessages = new Subject<any>(); // <--- NEW: To broadcast incoming texts

  // --- DASHBOARD WEBSOCKET ---
  connectDashboard(restaurantId: string) {
    this.dashboardSocket = new WebSocket(`ws://localhost:8000/ws/dashboard/${restaurantId}/`);

    this.dashboardSocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'update' && data.message === 'reload_orders') {
        this.dashboardUpdates.next(data);
      }
    };
    this.dashboardSocket.onopen = () => console.log('🟢 Dashboard WebSocket Connected!');
    this.dashboardSocket.onclose = () => console.log('🔴 Dashboard WebSocket Disconnected.');
  }

  disconnectDashboard() {
    if (this.dashboardSocket) this.dashboardSocket.close();
  }

  // --- CHAT WEBSOCKET (NEW) ---
  connectChat(orderId: string) {
    // Connect to the specific room for this exact order
    this.chatSocket = new WebSocket(`ws://localhost:8000/ws/chat/${orderId}/`);

    this.chatSocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'chat') {
        // When a message arrives, broadcast it to the Angular component!
        this.chatMessages.next(data); 
      }
    };
    this.chatSocket.onopen = () => console.log(`🟢 Chat Connected for Order ${orderId}!`);
  }

  sendChatMessage(message: string, sender: 'customer' | 'manager') {
    if (this.chatSocket && this.chatSocket.readyState === WebSocket.OPEN) {
      this.chatSocket.send(JSON.stringify({ message: message, sender: sender }));
    }
  }

  disconnectChat() {
    if (this.chatSocket) this.chatSocket.close();
  }
}