# 🏨 Hotel Management System

A comprehensive, professional full-stack hotel management solution built with modern technologies and best practices. This system provides complete hotel operations management including reception, food & beverage operations, analytics, and billing.

## ✨ Features

### 🏨 Reception Module
- **Guest Check-in/Check-out** - Streamlined guest arrival and departure
- **Room Management** - Real-time room status tracking and assignment
- **Reservation Handling** - Complete booking lifecycle management
- **Guest Information** - Comprehensive guest profiles and preferences

### 🍽️ Food & Beverage Operations
- **Multi-outlet POS System** - Restaurant, bar, café, and room service
- **Menu Management** - Dynamic menu with categories, pricing, and availability
- **Order Processing** - Real-time order tracking and status updates
- **Inventory Management** - Stock tracking and low-stock alerts

### 📊 Analytics & Dashboard
- **Real-time KPIs** - Revenue, occupancy, and performance metrics
- **Interactive Charts** - Visual data representation with Recharts
- **Export Capabilities** - PDF and Excel report generation
- **Business Intelligence** - Data-driven insights for decision making

### 💰 Billing & Payments
- **Unified Billing** - Combined room and F&B charges
- **Multiple Payment Methods** - Cash, card, digital wallet support
- **Invoice Generation** - Professional receipt and invoice creation
- **Financial Reporting** - Comprehensive revenue and expense tracking

### 🔐 Security & Access Control
- **JWT Authentication** - Secure token-based authentication
- **Role-based Access** - Admin, Receptionist, Cashier, Manager roles
- **Password Security** - Strong password requirements and encryption
- **Audit Logging** - Complete activity tracking for compliance

## 🏗️ Architecture

### Backend (FastAPI + PostgreSQL)
```
backend/
├── app/
│   ├── core/           # Configuration, database, security
│   ├── models/         # SQLAlchemy database models
│   ├── schemas/        # Pydantic request/response schemas
│   ├── routers/        # FastAPI route handlers
│   └── services/       # Business logic layer
├── database/           # Database setup and seed data
└── tests/              # Test suites
```

### Frontend (React + Tailwind CSS)
```
frontend/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/          # Application pages
│   ├── services/       # API integration
│   ├── hooks/          # Custom React hooks
│   └── contexts/       # State management
└── public/             # Static assets
```

## 🚀 Quick Start

### POS (Appsmith + PostgreSQL)

1. Create PostgreSQL database and load schema/seed
   ```bash
   createdb hotel_pos
   psql -d hotel_pos -f sql/schema.sql
   psql -d hotel_pos -f sql/seed.sql
   ```

2. Import Appsmith app
   - Open Appsmith
   - Create a new app → Import → select `appsmith/Hotel_POS_ready.json`
   - Configure datasource `POS_DB` with your DB host, port, database `hotel_pos`, username and password

3. Test Login (PIN)
   - Alice 1111 (Bar)
   - Bob 2222 (Restaurant)
   - Carol 3333 (Reception)
   - Dina 9999 (Manager)

4. Use Interfaces
   - Bar / Restaurant / Reception pages only show relevant items
   - Add to Bill, Update Qty, Remove, Cancel Item, Pay (Cash/Card)

5. Manager Dashboard
   - Sales by interface, pending payments, top-selling items

6. AI Assistant
   - Ask queries like: "Show all unpaid orders in Bar this week"
   - Results appear in the table

### Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL 12+
- npm or yarn

### Automated Setup (Recommended)

1. **Run the setup script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Edit configuration**
   ```bash
   # Edit backend configuration
   nano backend/.env
   
   # Edit frontend configuration (optional)
   nano frontend/.env
   ```

3. **Start the system**
   ```bash
   ./start-system.sh
   ```

### Manual Setup

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment**
   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

5. **Setup database**
   ```bash
   # Create PostgreSQL database
   createdb hotel_management
   
   # Run database setup
   psql -d hotel_management -f ../database/setup.sql
   psql -d hotel_management -f ../database/seed_data.sql
   ```

6. **Start backend server**
   ```bash
   python -m app.main
   ```

Backend API will be available at `http://localhost:8000`

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

Frontend will be available at `http://localhost:3000`

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

#### Authentication
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/refresh` - Refresh token

#### Reception
- `GET /api/v1/rooms` - List rooms
- `GET /api/v1/guests` - List guests
- `POST /api/v1/reservations` - Create reservation

#### F&B Operations
- `GET /api/v1/outlets` - List outlets
- `GET /api/v1/items` - List menu items
- `POST /api/v1/orders` - Create order

#### Analytics
- `GET /api/v1/analytics/revenue-today` - Today's revenue
- `GET /api/v1/analytics/occupancy-rate` - Room occupancy
- `GET /api/v1/analytics/dashboard-kpis` - All KPIs

## 🎨 User Interface

### Modern Dashboard
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Dark/Light Mode** - Theme switching capability
- **Real-time Updates** - Live data refresh
- **Interactive Charts** - Data visualization with Recharts

### Key Screens
- **Login Page** - Secure authentication
- **Dashboard** - KPI overview and analytics
- **Reception** - Guest and room management
- **F&B POS** - Order processing interface
- **Analytics** - Detailed reporting and insights

## 🗄️ Database Schema

### Core Entities
- **Users** - System users with role-based access
- **Rooms** - Hotel room inventory and management
- **Guests** - Customer information and preferences
- **Reservations** - Booking and stay management
- **Outlets** - F&B locations and settings
- **Items** - Menu items and pricing
- **Orders** - F&B transaction records
- **Payments** - Financial transaction tracking

### Key Features
- **UUID Primary Keys** - Better security and scalability
- **Audit Logging** - Complete activity tracking
- **Soft Deletes** - Data integrity preservation
- **Optimized Indexes** - Performance optimization

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/hotel_management
SECRET_KEY=your-super-secret-key-change-in-production
DEBUG=true
HOST=0.0.0.0
PORT=8000
```

#### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Hotel Management System
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app  # With coverage
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

## 🚀 Deployment

### Production Setup

1. **Environment Configuration**
   ```bash
   export DEBUG=false
   export DATABASE_URL=postgresql://user:pass@host:port/db
   export SECRET_KEY=your-production-secret-key
   ```

2. **Database Migration**
   ```bash
   psql -d hotel_management -f database/setup.sql
   ```

3. **Build and Deploy**
   ```bash
   # Backend
   cd backend
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   
   # Frontend
   cd frontend
   npm run build
   # Deploy dist/ folder to your web server
   ```

### Docker Deployment
```bash
docker-compose up -d
```

## 📊 Performance Features

### Backend Optimization
- **Connection Pooling** - Efficient database connections
- **Query Optimization** - Indexed queries and caching
- **Async Operations** - Non-blocking I/O operations
- **Response Compression** - Reduced bandwidth usage

### Frontend Optimization
- **Code Splitting** - Lazy loading of components
- **Image Optimization** - Compressed and responsive images
- **Caching** - Browser and API response caching
- **Bundle Optimization** - Minified and tree-shaken code

## 🔒 Security Features

### Authentication & Authorization
- JWT tokens with configurable expiration
- Role-based access control
- Password strength validation
- Account lockout protection

### Data Protection
- Password hashing with bcrypt
- SQL injection prevention
- XSS protection
- CORS configuration
- Input validation

## 📈 Monitoring & Logging

### Backend Monitoring
- Health check endpoints
- Database connection monitoring
- Request/response logging
- Error tracking and alerting

### Frontend Monitoring
- Performance metrics
- Error boundary handling
- User interaction tracking
- Real-time status updates

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Run the test suite
6. Submit a pull request

### Code Standards
- Follow PEP 8 for Python
- Use ESLint for JavaScript/TypeScript
- Write comprehensive tests
- Document new features

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the API documentation at `/docs`

## 🔄 Changelog

### Version 2.0.0
- Complete system rewrite with modern technologies
- Enhanced security and performance
- Comprehensive analytics dashboard
- Multi-role access control
- Real-time data updates
- Professional UI/UX design

---

**Built with ❤️ for modern hotel operations**

*This system represents a production-ready hotel management solution that can be immediately deployed and used in real hotel operations.*
