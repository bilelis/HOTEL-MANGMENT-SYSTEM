# Hotel Management System

A professional full-stack hotel management system built with React, FastAPI, and PostgreSQL. This comprehensive solution provides complete hotel operations management including reception, food & beverage operations, and real-time analytics.

## 🏨 System Overview

The Hotel Management System is designed to streamline hotel operations through three core modules:

- **Reception Module**: Guest check-in/check-out, room management, and reservations
- **F&B Module**: Point of Sale system for restaurants, bars, and cafés
- **Analytics Dashboard**: Real-time KPIs and business intelligence

## ✨ Key Features

### Analytics Dashboard
- 📊 **Revenue Today**: Daily revenue breakdown (rooms vs F&B)
- 🏨 **Occupancy Rate**: Real-time room occupancy tracking
- 🍔 **Top 5 Items Sold**: Best-selling menu items with quantities and revenue
- 👤 **Guest Spending**: Guest ranking by total spending
- 💰 **Revenue Split**: Visual pie chart of revenue sources
- 📈 **ARPR**: Average Revenue Per Room calculation

### Reception Management
- Guest check-in and check-out processing
- Room status visualization with color coding
- Reservation management and tracking
- Guest information storage and retrieval

### F&B Operations
- Complete POS system for multiple outlets
- Menu management with categories and pricing
- Order tracking with status updates
- Invoice and receipt generation
- Integration with guest accounts

### Technical Features
- **Responsive Design**: Works on desktop and tablet devices
- **Real-time Updates**: Live data synchronization
- **Role-based Access**: Admin, Receptionist, and Cashier roles
- **Modern UI**: Built with shadcn/ui components and Tailwind CSS
- **Data Visualization**: Interactive charts with Recharts
- **API-first Architecture**: RESTful APIs with comprehensive documentation

## 🛠 Tech Stack

### Frontend
- **React 18**: Modern React with hooks and functional components
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: High-quality UI components
- **Recharts**: Responsive chart library
- **Lucide React**: Beautiful icon library
- **React Router**: Client-side routing

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **PostgreSQL**: Advanced open-source relational database
- **JWT Authentication**: Secure token-based authentication
- **Uvicorn**: ASGI server for production

### Database
- **PostgreSQL 14+**: Primary database
- **12 Normalized Tables**: Optimized schema design
- **Foreign Key Constraints**: Data integrity enforcement
- **Indexes**: Performance optimization

## 📁 Project Structure

```
hotel_management_system/
├── backend/                    # FastAPI backend application
│   ├── app/
│   │   ├── core/              # Core configuration and database
│   │   ├── models/            # SQLAlchemy database models
│   │   ├── schemas/           # Pydantic schemas for validation
│   │   ├── routers/           # API route handlers
│   │   └── main.py           # FastAPI application entry point
│   ├── requirements.txt       # Python dependencies
│   └── .env                  # Environment configuration
├── frontend/                  # React frontend application
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── services/         # API service layer
│   │   ├── App.jsx           # Main application component
│   │   └── main.jsx          # React entry point
│   ├── package.json          # Node.js dependencies
│   └── vite.config.js        # Vite configuration
├── database_schema.sql        # PostgreSQL database schema
├── sample_data.sql           # Sample data for testing
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm/pnpm
- Python 3.11+
- PostgreSQL 14+

### 1. Database Setup
```bash
# Create database
createdb hotel_management

# Import schema
psql hotel_management < database_schema.sql

# Import sample data (optional)
psql hotel_management < sample_data.sql
```

### 2. Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📊 Database Schema

The system uses a normalized PostgreSQL database with the following key tables:

| Table | Purpose | Key Relationships |
|-------|---------|------------------|
| `users` | System users and authentication | - |
| `room_types` | Room categories and pricing | → `rooms` |
| `rooms` | Individual hotel rooms | → `reservations` |
| `guests` | Guest information | → `reservations` |
| `reservations` | Booking and stay records | → `rooms`, `guests` |
| `outlets` | F&B outlets (restaurant, bar, café) | → `items`, `orders` |
| `item_categories` | Menu categories | → `items` |
| `items` | Menu items and pricing | → `order_lines` |
| `orders` | F&B orders and transactions | → `order_lines` |
| `order_lines` | Individual order items | → `orders`, `items` |
| `payments` | Financial transactions | → `orders`, `reservations` |
| `audit_logs` | System activity tracking | - |

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/hotel_management

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# Application
APP_NAME=Hotel Management System
APP_VERSION=1.0.0
DEBUG=true
```

#### Frontend
```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_USE_REAL_API=false
```

## 📱 User Interface

### Dashboard Analytics
The analytics dashboard provides six key performance indicators accessible through intuitive buttons:

1. **Revenue Today** - Shows daily revenue breakdown between rooms and F&B
2. **Occupancy Rate** - Displays current room occupancy percentage
3. **Top 5 Items** - Bar chart of best-selling menu items
4. **Guest Spending** - Ranking of guests by total expenditure
5. **Revenue Split** - Pie chart comparing room vs F&B revenue
6. **ARPR** - Average Revenue Per Room calculation

### Reception Interface
- **Check-in/Check-out**: Streamlined guest processing
- **Reservations**: Complete booking management
- **Room Management**: Visual room status grid with color coding
  - 🔴 Red: Occupied rooms
  - 🟢 Green: Available rooms
  - 🟡 Yellow: Cleaning/maintenance

### F&B Interface
- **Point of Sale**: Menu item selection and order processing
- **Active Orders**: Real-time order status tracking
- **Menu Management**: Item availability and pricing control

## 🔐 Authentication & Authorization

The system implements role-based access control with three user types:

### Admin
- Full system access
- User management
- System configuration
- All analytics and reports

### Receptionist
- Guest check-in/check-out
- Reservation management
- Room status updates
- Guest-related analytics

### Cashier
- F&B order processing
- Menu item management
- F&B analytics
- Payment processing

## 📈 Analytics & Reporting

### Real-time KPIs
- **Daily Revenue Tracking**: Automatic calculation of room and F&B revenue
- **Occupancy Metrics**: Live room availability and utilization rates
- **Sales Analytics**: Top-performing menu items and revenue analysis
- **Guest Analytics**: Spending patterns and customer insights

### Data Visualization
- Interactive charts using Recharts library
- Responsive design for all screen sizes
- Real-time data updates
- Export capabilities (planned feature)

## 🌐 API Documentation

### Authentication Endpoints
```
POST /api/v1/auth/login          # User login
POST /api/v1/auth/refresh        # Token refresh
GET  /api/v1/auth/me            # Current user info
```

### Analytics Endpoints
```
GET /api/v1/analytics/revenue-today     # Daily revenue data
GET /api/v1/analytics/occupancy-rate    # Room occupancy metrics
GET /api/v1/analytics/top-items         # Best-selling items
GET /api/v1/analytics/guest-spending    # Guest expenditure ranking
GET /api/v1/analytics/revenue-split     # Revenue source breakdown
GET /api/v1/analytics/arpr              # Average Revenue Per Room
```

### Reception Endpoints
```
GET  /api/v1/reservations              # List reservations
POST /api/v1/reservations              # Create reservation
PUT  /api/v1/reservations/{id}/checkin # Check-in guest
PUT  /api/v1/reservations/{id}/checkout # Check-out guest
GET  /api/v1/rooms/status              # Room status overview
```

### F&B Endpoints
```
GET  /api/v1/items                     # Menu items
POST /api/v1/orders                    # Create order
GET  /api/v1/orders/active             # Active orders
PUT  /api/v1/orders/{id}/status        # Update order status
```

## 🚀 Deployment

### Production Deployment

#### Backend Deployment
```bash
# Install production dependencies
pip install -r requirements.txt

# Set production environment variables
export DATABASE_URL=postgresql://user:pass@prod-db:5432/hotel_db
export SECRET_KEY=production-secret-key
export DEBUG=false

# Run with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

#### Frontend Deployment
```bash
# Build for production
npm run build

# Serve static files (example with nginx)
# Copy dist/ contents to web server directory
```

### Docker Deployment (Optional)
```dockerfile
# Backend Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Frontend Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
```

## 🧪 Testing

### Frontend Testing
```bash
cd frontend
npm run test
```

### Backend Testing
```bash
cd backend
pytest
```

### Integration Testing
The system includes comprehensive integration tests covering:
- API endpoint functionality
- Database operations
- Authentication flows
- Analytics calculations

## 🔧 Development

### Adding New Features

#### Backend (FastAPI)
1. Create new models in `app/models/`
2. Add Pydantic schemas in `app/schemas/`
3. Implement API routes in `app/routers/`
4. Update database migrations

#### Frontend (React)
1. Create components in `src/components/`
2. Add API calls in `src/services/`
3. Update routing in `App.jsx`
4. Style with Tailwind CSS

### Code Style
- **Backend**: Follow PEP 8 Python style guide
- **Frontend**: Use Prettier and ESLint configurations
- **Database**: Use snake_case for table and column names

## 📋 Roadmap

### Planned Features
- [ ] Multi-language support (English + Arabic)
- [ ] Dark/Light mode toggle
- [ ] PDF/Excel export for analytics
- [ ] Email notifications
- [ ] Mobile app (React Native)
- [ ] Advanced reporting dashboard
- [ ] Integration with payment gateways
- [ ] Housekeeping management module

### Version History
- **v1.0.0** - Initial release with core functionality
  - Analytics dashboard with 6 KPIs
  - Reception management
  - F&B operations
  - User authentication

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation in `/docs`

## 🙏 Acknowledgments

- Built with modern web technologies
- UI components from shadcn/ui
- Icons from Lucide React
- Charts powered by Recharts
- Database design following hospitality industry best practices

---

**Hotel Management System** - Streamlining hotel operations with modern technology.

