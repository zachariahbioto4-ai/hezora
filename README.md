# BookBase - Online Book Store Platform

A Django REST Framework based e-commerce platform for buying and managing books online.

## Features

- User authentication and profiles
- Book catalog with categories
- Book reviews and ratings
- Personal library management
- Shopping cart and orders
- Payment processing (Stripe)
- Order tracking and delivery management
- Admin dashboard

## Tech Stack

- Django 6.0.5
- Django REST Framework 3.17.1
- PostgreSQL
- Stripe Payment Gateway
- AWS S3 Storage
- Gunicorn

## Installation

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate venv: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Create .env file with database and API credentials
6. Run migrations: `python manage.py migrate`
7. Create superuser: `python manage.py createsuperuser`
8. Start server: `python manage.py runserver`

## API Endpoints

### Accounts
- `GET/POST /api/accounts/users/` - List/Create users
- `GET /api/accounts/users/me/` - Get current user profile
- `PUT /api/accounts/users/{id}/update_profile/` - Update profile

### Books
- `GET /api/books/books/` - List books
- `GET /api/books/books/{id}/` - Book details
- `POST /api/books/books/{id}/add_review/` - Add/Update review
- `GET /api/books/categories/` - List categories
- `GET /api/books/books/featured/` - Featured books

### Library
- `GET /api/library/` - Get user's library
- `POST /api/library/add_book/` - Add book to library
- `DELETE /api/library/remove_book/` - Remove book from library

### Orders
- `GET/POST /api/orders/orders/` - List/Create orders
- `GET /api/orders/orders/{id}/` - Order details
- `GET /api/orders/orders/my_orders/` - My orders

### Payments
- `GET/POST /api/payments/payments/` - List/Create payments
- `GET /api/payments/payments/{id}/` - Payment details

### Delivery
- `GET /api/delivery/deliveries/` - List deliveries
- `GET /api/delivery/deliveries/track/` - Track delivery

## Environment Variables

Create a `.env` file with:
```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=bookbase_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
USE_S3=False
```

## License

MIT License