# E-Commerce Platform Backend

A robust, scalable backend API built with FastAPI for an e-commerce platform featuring user authentication, product management, shopping cart, order processing, and more.

## 🚀 Features

### Core Functionality
- **User Authentication & Authorization**: JWT-based authentication with role-based access control (RBAC)
- **Product Management**: CRUD operations for products with filtering, pagination, and search capabilities
- **Brand Management**: Brand creation, retrieval, and management
- **Shopping Cart**: Add, update, remove items from cart with real-time calculations
- **Order Processing**: Complete order lifecycle management from creation to fulfillment
- **Address Management**: User address book with CRUD operations
- **Payment Integration**: Supabase-powered payment processing (in development)

### Technical Features
- **Asynchronous Database Operations**: PostgreSQL with SQLAlchemy async ORM
- **Database Migrations**: Alembic for version-controlled schema changes
- **Structured Logging**: Comprehensive request/response logging middleware
- **CORS Support**: Cross-origin resource sharing configuration
- **Environment Configuration**: Secure configuration management with `.env` files
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation

## 🏗️ Architecture

### Project Structure
```
.
├── alembic/               # Database migration files
├── database/              # Database configuration and models
├── src/                   # Main source code
│   ├── address/           # Address management module
│   ├── brand/             # Brand management module  
│   ├── cart/              # Shopping cart module
│   ├── order/             # Order processing module
│   ├── payments/          # Payment processing module
│   ├── products/          # Product management module
│   └── user_auth/         # User authentication module
├── utilities/             # Shared utility functions
├── config.py              # Application configuration
├── main.py                # FastAPI application entry point
└── requirements.txt       # Python dependencies
```

### Module Organization
Each module follows a consistent structure:
```
module/
├── controller.py           # API routes and request handlers
├── model.py                # Pydantic models for validation
├── schema.py               # Database schemas
└── services/               # Business logic implementations
    ├── create_module.py
    ├── get_module.py
    ├── update_module.py
    └── delete_module.py
```

## 🛠️ Tech Stack

### Core Technologies
- **FastAPI**: High-performance Python web framework
- **PostgreSQL**: Relational database for data persistence
- **SQLAlchemy**: Async ORM for database operations
- **Alembic**: Database migration tool
- **Pydantic**: Data validation and serialization

### Authentication & Security
- **JWT**: JSON Web Tokens for stateless authentication
- **OAuth2**: Standard authentication protocol implementation
- **BCrypt**: Password hashing and verification
- **Role-Based Access Control**: Fine-grained permission management

### Utilities & Middleware
- **Uvicorn**: ASGI server for production deployment
- **CORS Middleware**: Cross-origin request handling
- **Custom Logging**: Structured request/response logging
- **Supabase**: Cloud database and storage services

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip package manager

## 🔧 Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd "Project - E-Commerce Platform"
```

2. **Create virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file in the project root:
```env
# Database Configuration
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=ecommerce_db

# CORS Configuration
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

# JWT Configuration
JWT_ACCESS_SECRET_KEY=your_secret_key_here
JWT_REFRESH_SECRET_KEY=your_refresh_key_here
ACCESS_TOKEN_EXPIRE_TIME=30
REFRESH_TOKEN_EXPIRE_TIME=2880

# Supabase Configuration
SUPABASE_PROJECT_URL=your_supabase_url
SUPABASE_API_KEY=your_supabase_api_key
SUPABASE_USER_ID=your_user_id
SUPABASE_HOST=your_supabase_host
SUPABASE_DB_PASSWORD=your_supabase_password
SUPABASE_DATABASE_NAME=your_database_name
```

5. **Run database migrations**
```bash
alembic upgrade head
```

6. **Start the development server**
```bash
uvicorn main:app --reload
```

## 🌐 API Endpoints

### Authentication
```
POST   /api/v1/users/signup           # User registration
POST   /api/v1/users/login            # User login
GET    /api/v1/users/me               # Get current user
PUT    /api/v1/users/update           # Update user profile
DELETE /api/v1/users/delete/{user_id}  # Delete user (admin)
```

### Products
```
GET    /api/v1/products/all-products              # Get all products (paginated)
GET    /api/v1/products/product-by-id/{id}        # Get product by ID
GET    /api/v1/products/product-by-name/{name}    # Search products by name
POST   /api/v1/products/add-product               # Create new product
PUT    /api/v1/products/update-product/{id}       # Update product
PATCH  /api/v1/products/partial-update-product/{id} # Partial update
DELETE /api/v1/products/delete-product/{id}       # Delete product
```

### Brands
```
GET    /api/v1/brands/get-all-brands    # Get all brands
POST   /api/v1/brands/create-brand      # Create new brand
DELETE /api/v1/brands/delete-brand/{id}  # Delete brand
```

### Cart
```
GET    /api/v1/cart/fetch-cart-items          # Get user's cart
POST   /api/v1/cart/create-cart-item          # Add item to cart
PUT    /api/v1/cart/update-cart-item/{item_id} # Update cart item
DELETE /api/v1/cart/delete-cart-item/{item_id} # Remove item from cart
```

### Orders
```
GET    /api/v1/orders/get-order/{order_id}     # Get order details
POST   /api/v1/orders/create-order             # Create new order
PUT    /api/v1/orders/update-order-status/{id} # Update order status
DELETE /api/v1/orders/cancel-order/{order_id}  # Cancel order
```

### Addresses
```
GET    /api/v1/address/get-addresses       # Get user addresses
POST   /api/v1/address/create-address      # Create new address
PUT    /api/v1/address/update-address/{id} # Update address
DELETE /api/v1/address/delete-address/{id} # Delete address
```

## 🔐 Authentication & Authorization

The platform uses JWT tokens for authentication with role-based access control:

### User Roles
- **ADMIN**: Full access to all operations including user management
- **SELLER**: Can create and manage products and brands
- **CUSTOMER**: Can browse products, manage cart, and place orders

### Protected Routes
Most endpoints require authentication via Bearer token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## 📊 Database Schema

### Core Models
- **Users**: User accounts with roles and authentication
- **Products**: Product catalog with pricing and inventory
- **Brands**: Brand information and associations
- **Cart Items**: User shopping cart contents
- **Orders**: Order history and status tracking
- **Addresses**: User shipping/billing addresses

## 🔄 Database Migrations

Manage schema changes using Alembic:

```bash
# Create new migration
alembic revision --autogenerate -m "Migration description"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1

# View migration history
alembic history
```

## 📝 Logging

The application includes comprehensive logging middleware that captures:
- Request details (method, URL, headers, body)
- Response details (status code, body)
- Processing time
- Error information

Logs are structured for easy parsing and monitoring.

## 🚀 Deployment

### Production Setup
1. Set `DEBUG=False` in environment variables
2. Configure proper CORS origins
3. Use production-grade database
4. Set up reverse proxy (Nginx/Apache)
5. Configure SSL certificates

### Docker Deployment (Recommended)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🧪 Testing

Run tests using pytest:
```bash
pytest tests/ -v
```

## 📈 Monitoring & Performance

- Built-in FastAPI metrics endpoint
- Request/response logging for performance tracking
- Database query optimization
- Connection pooling for efficient resource usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is proprietary and confidential. All rights reserved.


## 🆘 Support

For support, email vinayakkanchan03@gmail.com or create an issue in the repository.

---
*Built with ❤️ using FastAPI*