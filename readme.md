# Smart Restaurant Operating System (POS & Kitchen Management)

A fully functional, multi-tenant real-time Restaurant Operating System built with Angular 17, Django, and Django Channels. 

## Project Goal
The primary objective of this project is to modernize the dining experience by bridging the communication gap between front-of-house customers and back-of-house kitchen staff. It aims to eliminate stale data in traditional Point of Sale (POS) systems by utilizing WebSockets for real-time state synchronization, while also leveraging Natural Language Processing (NLP) to provide management with instant, actionable metrics on customer satisfaction.

## System Architecture & Workflow



The application follows a decoupled client-server architecture:
* **Frontend (Client):** Built with Angular 17 using Standalone Components and RxJS for reactive state management. It communicates with the backend via standard HTTP REST protocols for fetching static data, and persistent WebSocket connections for real-time events.
* **Backend (Server):** Built with Django and Django REST Framework (DRF). It operates on an ASGI server (Daphne) to support asynchronous WebSocket connections via Django Channels.
* **Data Layer:** SQLite (containerized), designed with a multi-tenant schema where tables, menus, and orders are isolated by the authenticated restaurant manager.

## Core Features

* **Real-Time Kanban Order Board:** Orders flow seamlessly through states (Pending, Preparing, Served, Paid). State changes are broadcasted via WebSockets, instantly updating all connected client dashboards without HTTP polling or page refreshes.
* **Two-Way Live Kitchen Chat:** Customers and kitchen staff can communicate dynamically. A dedicated WebSocket channel is opened per order, allowing customers to request modifications and staff to reply instantly.
* **AI-Powered Sentiment Analysis:** Customer reviews are processed through a Natural Language Processing pipeline using the VADER lexicon. It evaluates text feedback and assigns an instant positive, negative, or neutral sentiment score to help managers track service quality.
* **Dynamic Table & QR Generation:** Managers can dynamically generate secure, UUID-based URLs for specific tables. The system automatically converts these into downloadable QR codes for frictionless customer ordering.

## System Requirements

To run this project locally, ensure you have the following installed on your machine:
* Docker & Docker Compose
* Node.js (v18.0 or higher)
* Node Package Manager (NPM)
* Angular CLI (v17.0 or higher)
* Git

## Project Structure

Below is a high-level overview of the application's file structure to demonstrate the separation of concerns:

```text
Django-Major-project/
├── backend/                       # Django ASGI Application
│   ├── rra/                       # Main Project Configuration (settings.py, asgi.py)
│   ├── accounts/                  # Primary App (Models, Views, DRF Serializers)
│   │   ├── consumers.py           # WebSocket Event Handlers (Dashboard & Chat)
│   │   ├── routing.py             # WebSocket URL Routing
│   │   ├── signals.py             # Django ORM Post-Save Hooks for broadcasting
│   │   └── models.py              # Multi-tenant Database Schema
│   ├── Dockerfile                 # Backend Container Instructions
│   └── requirements.txt           # Python Dependencies
│
├── frontend/                      # Angular 17 Application
│   ├── src/app/
│   │   ├── pages/                 # UI Components (Dashboard, Cart, Success)
│   │   ├── services/              # Injectables
│   │   │   ├── api.ts             # HTTP REST Interceptors
│   │   │   └── websocket.ts       # RxJS Subject-based WebSocket Manager
│   └── package.json               # Node Dependencies
└── docker-compose.yml             # Orchestration for Backend Services

## Quick Start Guide

**1. Clone the repository**
```bash
git clone [https://github.com/Rashid-hussain-mohammed/Django-Major-project.git](https://github.com/Rashid-hussain-mohammed/Django-Major-project.git)
cd Django-Major-project

**2, setup and running backend(Django)**
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

**3, Setup and running Frontend(Angular)**
```bash
cd frontend
npm install
npm start


Access Application : - 

Manager Dashboard: http://localhost:4200

Django Backend/API: http://localhost:8000