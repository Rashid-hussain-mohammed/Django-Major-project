import { Routes } from '@angular/router';
import { Menu } from './pages/menu/menu';
import { Cart as CartPage } from './pages/cart/cart'; 
import { Success } from './pages/success/success';
import { Landing } from './pages/landing/landing'; //Landing page
import { Register } from './pages/register/register';
import { Login } from './pages/login/login';
import { Dashboard } from './pages/dashboard/dashboard';
import { authGuard } from './guards/auth-guard';

export const routes: Routes = [
  // 2. Make the Landing page the default route
  { path: '', component: Landing }, 
  { path: 'register', component: Register },
  { path: 'login', component: Login },
  
  // 3. Move the customer ordering system to /menu
  { path: 'menu/:restaurantId/:tableId', component: Menu }, 
  { path: 'cart', component: CartPage }, 
  { path: 'success', component: Success }, 
  { path: 'dashboard', component: Dashboard, canActivate: [authGuard] },
  { path: '**', redirectTo: '' } 
];