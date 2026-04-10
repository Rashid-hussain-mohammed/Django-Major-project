### Rework of my old project with complete feature set.

# AI-Powered Digital Menu & Restaurant Management System

A modern, full-stack web application designed to unify the restaurant experience for both customers and management. This platform provides a seamless digital ordering system and utilizes AI to analyze customer feedback, driving continuous service improvement.

## The Idea
The goal of this project is to bridge the gap between frontend customer experience and backend restaurant operations. By replacing physical menus with a reactive digital interface, customers can easily build their orders, while management receives structured data and sentiment analysis to improve food and service quality.

## Tech Stack
**Frontend:**
* **Angular 17:** Standalone components and modern control flow (`@for`, `@if`).
* **Angular Signals:** State-of-the-art, ultra-fast reactive state management for the shopping cart.
* **Tailwind CSS:** Enterprise-grade, responsive UI styling.

**Backend:**
* **Python / Django:** Robust relational database modeling and routing.
* **Django REST Framework (DRF):** Secure API endpoints with nested serializers.
* **Docker:** Fully containerized backend environment for seamless deployment and database volume management.

## Key Features
* **Reactive Shopping Cart:** Instant price and quantity calculations without page reloads, powered by Angular Signals.
* **Relational Ordering System:** REST API that accurately maps multiple menu items and quantities to specific restaurant tables.
* **Dynamic Data:** A fully data-driven UI where menu items, pricing, and availability are managed directly from the Django Admin portal.
* **Dockerized Architecture:** Ensures the backend runs identically on any machine without complex Python environment setup.

## How to Run Locally

**1. Start the Backend (Docker required):**
```bash
cd backend
docker build -t my-django-backend .
docker run -p 8000:8000 -v $(pwd):/app my-django-backend