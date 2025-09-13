# Hotel Management System - Database Design Documentation

## Overview

The Hotel Management System database is designed to support a comprehensive hotel operation including reception management, food & beverage operations, and analytics. The database uses PostgreSQL with UUID primary keys for better scalability and security.

## Database Schema Architecture

### Core Entities

#### 1. Users and Authentication
- **users**: System users with role-based access (admin, receptionist, cashier)
- Supports password hashing and role-based permissions
- Tracks user activity through audit logs

#### 2. Room Management
- **room_types**: Defines different categories of rooms with pricing and amenities
- **rooms**: Individual room inventory with status tracking
- Room statuses: available, occupied, maintenance, cleaning

#### 3. Guest Management
- **guests**: Customer information with contact details and identification
- **reservations**: Booking records linking guests to rooms with dates and status
- Supports walk-in guests and advance reservations

#### 4. Food & Beverage Operations
- **outlets**: Different F&B locations (restaurant, bar, café, room service)
- **item_categories**: Menu organization by category
- **items**: Menu items with pricing, allergens, and dietary information
- **orders**: Transaction records for F&B sales
- **order_lines**: Individual items within each order

#### 5. Financial Management
- **payments**: Payment tracking for both room charges and F&B
- Supports multiple payment methods and types
- Links to both reservations and orders

#### 6. Audit and Compliance
- **audit_logs**: Change tracking for all critical operations
- Automatic timestamp updates for data integrity

## Key Relationships

### Guest Journey Flow
```
Guest → Reservation → Room → Check-in → Orders → Payments → Check-out
```

### F&B Operations Flow
```
Outlet → Items → Orders → Order Lines → Payments
```

### Analytics Data Sources
- Revenue: payments table aggregated by type and date
- Occupancy: reservations and rooms status
- F&B Performance: orders and order_lines with item details
- Guest Spending: payments linked to guests through reservations

## Database Features

### 1. Automatic Functions
- **Order Number Generation**: Auto-generates unique order numbers with date prefix
- **Timestamp Updates**: Automatic updated_at field maintenance
- **UUID Generation**: Secure unique identifiers for all records

### 2. Data Integrity
- Foreign key constraints ensure referential integrity
- Check constraints validate enum values and business rules
- Triggers maintain data consistency

### 3. Performance Optimization
- Strategic indexes on frequently queried columns
- Optimized for analytics queries with date-based indexing
- Efficient joins between related entities

### 4. Extensibility
- JSONB fields for flexible data storage (operating hours, amenities)
- Array fields for multi-value attributes (allergens, dietary info)
- Audit logging for compliance and debugging

## Analytics Capabilities

The database design supports all required KPI calculations:

### 1. Revenue Today
```sql
SELECT SUM(amount) FROM payments 
WHERE DATE(created_at) = CURRENT_DATE
```

### 2. Occupancy Rate
```sql
SELECT 
    COUNT(CASE WHEN status = 'occupied' THEN 1 END) * 100.0 / COUNT(*) as occupancy_rate
FROM rooms 
WHERE status != 'maintenance'
```

### 3. Top 5 Items Sold
```sql
SELECT i.name, SUM(ol.quantity) as total_sold, SUM(ol.line_total) as revenue
FROM order_lines ol
JOIN items i ON ol.item_id = i.id
JOIN orders o ON ol.order_id = o.id
WHERE DATE(o.created_at) = CURRENT_DATE
GROUP BY i.id, i.name
ORDER BY total_sold DESC
LIMIT 5
```

### 4. Guest Spending Ranking
```sql
SELECT g.first_name, g.last_name, SUM(p.amount) as total_spending
FROM guests g
JOIN reservations r ON g.id = r.guest_id
JOIN payments p ON r.id = p.reservation_id OR p.order_id IN (
    SELECT id FROM orders WHERE guest_id = g.id
)
GROUP BY g.id, g.first_name, g.last_name
ORDER BY total_spending DESC
```

### 5. Revenue Split (Rooms vs F&B)
```sql
SELECT 
    payment_type,
    SUM(amount) as revenue
FROM payments
WHERE DATE(created_at) = CURRENT_DATE
GROUP BY payment_type
```

### 6. Average Revenue per Room (ARPR)
```sql
SELECT 
    AVG(total_amount) as arpr
FROM reservations
WHERE status IN ('checked_in', 'checked_out')
AND DATE(created_at) = CURRENT_DATE
```

## Security Considerations

### 1. Data Protection
- UUID primary keys prevent enumeration attacks
- Password hashing using bcrypt
- Audit logging for compliance

### 2. Access Control
- Role-based user system
- Created_by fields track user actions
- Soft deletes where appropriate

### 3. Data Validation
- Check constraints on critical fields
- Foreign key constraints prevent orphaned records
- Enum validation for status fields

## Scalability Features

### 1. Horizontal Scaling
- UUID primary keys support distributed systems
- Partitioning-ready date-based queries
- Minimal cross-table dependencies

### 2. Performance
- Optimized indexes for common queries
- Efficient aggregation for analytics
- Minimal N+1 query patterns

### 3. Maintenance
- Automatic cleanup through triggers
- Audit trail for debugging
- Clear separation of concerns

## Sample Data Overview

The sample data includes:
- 4 system users with different roles
- 4 room types with 10 individual rooms
- 6 sample guests with realistic information
- 4 F&B outlets with categorized menu items
- Current day orders and historical data for analytics
- Payment records for both room and F&B charges

This provides a realistic dataset for testing all system features and analytics calculations.

## Next Steps

With the database schema complete, the next phase involves:
1. Setting up the FastAPI backend with database connections
2. Implementing API endpoints for all CRUD operations
3. Creating analytics endpoints for dashboard KPIs
4. Adding authentication and authorization middleware
5. Implementing data validation and error handling

The database design provides a solid foundation for a production-ready hotel management system with comprehensive analytics capabilities.

