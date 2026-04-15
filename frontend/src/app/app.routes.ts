import { Routes } from '@angular/router';
import { Menu } from './pages/menu/menu';
// Note: We alias the component as CartPage so it doesn't conflict with our Cart service!
import { Cart as CartPage } from './pages/cart/cart'; 
import { Success } from './pages/success/success';

export const routes: Routes = [
  { path: '', component: Menu }, // Default route is the menu
  { path: 'cart', component: CartPage }, // /cart goes to the checkout
  {path: 'success', component: Success},
  { path: '**', redirectTo: '' } // Fallback for bad URLs
];