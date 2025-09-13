# Hotel Management System - Deployment Guide

This comprehensive guide provides step-by-step instructions for deploying the Hotel Management System in production environments.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Ubuntu 20.04+ or CentOS 8+
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 50GB available disk space
- **Network**: Stable internet connection

### Software Dependencies
- **Node.js**: Version 18.0 or higher
- **Python**: Version 3.11 or higher
- **PostgreSQL**: Version 14 or higher
- **Nginx**: For reverse proxy (recommended)
- **SSL Certificate**: For HTTPS (recommended)

## 🗄️ Database Setup

### 1. Install PostgreSQL

#### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start and enable PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### CentOS/RHEL
```bash
# Install PostgreSQL repository
sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm

# Install PostgreSQL
sudo dnf install -y postgresql14-server postgresql14

# Initialize database
sudo /usr/pgsql-14/bin/postgresql-14-setup initdb

# Start and enable PostgreSQL
sudo systemctl start postgresql-14
sudo systemctl enable postgresql-14
```

### 2. Configure PostgreSQL

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE hotel_management;
CREATE USER hotel_user WITH ENCRYPTED PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE hotel_management TO hotel_user;

# Exit PostgreSQL
\q
```

### 3. Import Database Schema

```bash
# Navigate to project directory
cd /path/to/hotel_management_system

# Import schema
sudo -u postgres psql hotel_management < database_schema.sql

# Import sample data (optional for testing)
sudo -u postgres psql hotel_management < sample_data.sql
```

### 4. Configure PostgreSQL for Production

Edit PostgreSQL configuration:
```bash
sudo nano /etc/postgresql/14/main/postgresql.conf
```

Key settings for production:
```conf
# Connection settings
listen_addresses = 'localhost'
port = 5432
max_connections = 100

# Memory settings
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB

# Logging
log_destination = 'stderr'
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_statement = 'all'
```

Restart PostgreSQL:
```bash
sudo systemctl restart postgresql
```

## 🐍 Backend Deployment

### 1. Prepare Environment

```bash
# Create application user
sudo useradd -m -s /bin/bash hotelapp

# Create application directory
sudo mkdir -p /opt/hotel-management
sudo chown hotelapp:hotelapp /opt/hotel-management

# Switch to application user
sudo -u hotelapp -i
cd /opt/hotel-management
```

### 2. Install Python Dependencies

```bash
# Install Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install application dependencies
pip install -r backend/requirements.txt

# Install production server
pip install gunicorn
```

### 3. Configure Environment Variables

Create production environment file:
```bash
nano backend/.env
```

Production environment configuration:
```env
# Database Configuration
DATABASE_URL=postgresql://hotel_user:secure_password_here@localhost:5432/hotel_management

# Security Configuration
SECRET_KEY=your-super-secure-secret-key-here-minimum-32-characters
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256

# Application Configuration
APP_NAME=Hotel Management System
APP_VERSION=1.0.0
DEBUG=false
HOST=0.0.0.0
PORT=8000

# CORS Configuration
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com

# Logging Configuration
LOG_LEVEL=INFO
```

### 4. Create Systemd Service

Create service file:
```bash
sudo nano /etc/systemd/system/hotel-backend.service
```

Service configuration:
```ini
[Unit]
Description=Hotel Management System Backend
After=network.target postgresql.service
Requires=postgresql.service

[Service]
Type=exec
User=hotelapp
Group=hotelapp
WorkingDirectory=/opt/hotel-management/backend
Environment=PATH=/opt/hotel-management/venv/bin
ExecStart=/opt/hotel-management/venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 5. Start Backend Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable and start service
sudo systemctl enable hotel-backend
sudo systemctl start hotel-backend

# Check status
sudo systemctl status hotel-backend

# View logs
sudo journalctl -u hotel-backend -f
```

## ⚛️ Frontend Deployment

### 1. Install Node.js

#### Ubuntu/Debian
```bash
# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### CentOS/RHEL
```bash
# Install Node.js 18
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo dnf install -y nodejs
```

### 2. Build Frontend Application

```bash
# Navigate to frontend directory
cd /opt/hotel-management/frontend

# Install dependencies
npm install

# Create production environment file
nano .env.production
```

Production environment:
```env
REACT_APP_API_URL=https://your-domain.com/api/v1
REACT_APP_USE_REAL_API=true
GENERATE_SOURCEMAP=false
```

Build for production:
```bash
# Build application
npm run build

# Verify build
ls -la dist/
```

### 3. Configure Nginx

Install Nginx:
```bash
# Ubuntu/Debian
sudo apt install nginx

# CentOS/RHEL
sudo dnf install nginx
```

Create Nginx configuration:
```bash
sudo nano /etc/nginx/sites-available/hotel-management
```

Nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    
    # SSL Configuration
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Frontend Static Files
    location / {
        root /opt/hotel-management/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
        
        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
    
    # Backend API Proxy
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Health Check Endpoint
    location /health {
        proxy_pass http://localhost:8000/health;
        access_log off;
    }
}
```

Enable site and restart Nginx:
```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/hotel-management /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

## 🔒 SSL Certificate Setup

### Using Let's Encrypt (Recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test automatic renewal
sudo certbot renew --dry-run
```

### Using Custom Certificate

```bash
# Copy certificate files
sudo cp your-certificate.crt /etc/ssl/certs/
sudo cp your-private.key /etc/ssl/private/

# Set proper permissions
sudo chmod 644 /etc/ssl/certs/your-certificate.crt
sudo chmod 600 /etc/ssl/private/your-private.key
```

## 🔥 Firewall Configuration

Configure UFW (Ubuntu) or firewalld (CentOS):

### Ubuntu (UFW)
```bash
# Enable UFW
sudo ufw enable

# Allow SSH
sudo ufw allow ssh

# Allow HTTP and HTTPS
sudo ufw allow 80
sudo ufw allow 443

# Allow PostgreSQL (if external access needed)
sudo ufw allow 5432

# Check status
sudo ufw status
```

### CentOS (firewalld)
```bash
# Start firewalld
sudo systemctl start firewalld
sudo systemctl enable firewalld

# Allow HTTP and HTTPS
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https

# Allow PostgreSQL (if external access needed)
sudo firewall-cmd --permanent --add-port=5432/tcp

# Reload firewall
sudo firewall-cmd --reload
```

## 📊 Monitoring and Logging

### 1. Application Monitoring

Create monitoring script:
```bash
sudo nano /opt/hotel-management/monitor.sh
```

Monitoring script:
```bash
#!/bin/bash

# Check backend service
if ! systemctl is-active --quiet hotel-backend; then
    echo "Backend service is down, restarting..."
    systemctl restart hotel-backend
fi

# Check Nginx
if ! systemctl is-active --quiet nginx; then
    echo "Nginx is down, restarting..."
    systemctl restart nginx
fi

# Check PostgreSQL
if ! systemctl is-active --quiet postgresql; then
    echo "PostgreSQL is down, restarting..."
    systemctl restart postgresql
fi

# Check disk space
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "Warning: Disk usage is ${DISK_USAGE}%"
fi

# Check memory usage
MEMORY_USAGE=$(free | awk 'NR==2{printf "%.2f", $3*100/$2}')
if (( $(echo "$MEMORY_USAGE > 80" | bc -l) )); then
    echo "Warning: Memory usage is ${MEMORY_USAGE}%"
fi
```

Make executable and add to cron:
```bash
sudo chmod +x /opt/hotel-management/monitor.sh

# Add to crontab (run every 5 minutes)
sudo crontab -e
# Add line: */5 * * * * /opt/hotel-management/monitor.sh >> /var/log/hotel-monitor.log 2>&1
```

### 2. Log Rotation

Configure log rotation:
```bash
sudo nano /etc/logrotate.d/hotel-management
```

Log rotation configuration:
```
/var/log/hotel-*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 hotelapp hotelapp
    postrotate
        systemctl reload hotel-backend
    endscript
}
```

## 🚀 Performance Optimization

### 1. Database Optimization

```sql
-- Connect to database
sudo -u postgres psql hotel_management

-- Create indexes for better performance
CREATE INDEX idx_reservations_checkin_date ON reservations(checkin_date);
CREATE INDEX idx_reservations_checkout_date ON reservations(checkout_date);
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_order_lines_order_id ON order_lines(order_id);
CREATE INDEX idx_rooms_status ON rooms(status);

-- Update table statistics
ANALYZE;
```

### 2. Application Caching

Install Redis for caching:
```bash
# Ubuntu/Debian
sudo apt install redis-server

# CentOS/RHEL
sudo dnf install redis

# Start and enable Redis
sudo systemctl start redis
sudo systemctl enable redis
```

### 3. Nginx Optimization

Add to Nginx configuration:
```nginx
# Enable gzip compression
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

# Enable HTTP/2
listen 443 ssl http2;

# Optimize worker processes
worker_processes auto;
worker_connections 1024;

# Enable sendfile
sendfile on;
tcp_nopush on;
tcp_nodelay on;
```

## 🔧 Backup Strategy

### 1. Database Backup

Create backup script:
```bash
sudo nano /opt/hotel-management/backup-db.sh
```

Backup script:
```bash
#!/bin/bash

BACKUP_DIR="/opt/hotel-management/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="hotel_management"

# Create backup directory
mkdir -p $BACKUP_DIR

# Create database backup
sudo -u postgres pg_dump $DB_NAME > $BACKUP_DIR/hotel_db_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/hotel_db_$DATE.sql

# Remove backups older than 30 days
find $BACKUP_DIR -name "hotel_db_*.sql.gz" -mtime +30 -delete

echo "Database backup completed: hotel_db_$DATE.sql.gz"
```

Schedule daily backups:
```bash
sudo chmod +x /opt/hotel-management/backup-db.sh

# Add to crontab (daily at 2 AM)
sudo crontab -e
# Add line: 0 2 * * * /opt/hotel-management/backup-db.sh >> /var/log/backup.log 2>&1
```

### 2. Application Backup

```bash
#!/bin/bash

BACKUP_DIR="/opt/hotel-management/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup application files
tar -czf $BACKUP_DIR/app_backup_$DATE.tar.gz \
    /opt/hotel-management/backend \
    /opt/hotel-management/frontend/dist \
    /etc/nginx/sites-available/hotel-management

echo "Application backup completed: app_backup_$DATE.tar.gz"
```

## 🔍 Troubleshooting

### Common Issues

#### Backend Service Won't Start
```bash
# Check service status
sudo systemctl status hotel-backend

# Check logs
sudo journalctl -u hotel-backend -n 50

# Common fixes:
# 1. Check database connection
# 2. Verify environment variables
# 3. Check file permissions
```

#### Frontend Not Loading
```bash
# Check Nginx status
sudo systemctl status nginx

# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Test Nginx configuration
sudo nginx -t

# Common fixes:
# 1. Check file paths in Nginx config
# 2. Verify SSL certificate
# 3. Check firewall rules
```

#### Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-14-main.log

# Test connection
sudo -u postgres psql hotel_management

# Common fixes:
# 1. Check pg_hba.conf authentication
# 2. Verify database credentials
# 3. Check network connectivity
```

### Performance Issues

#### High CPU Usage
```bash
# Check running processes
top -p $(pgrep -d',' -f hotel)

# Check database queries
sudo -u postgres psql hotel_management -c "SELECT query, state, query_start FROM pg_stat_activity WHERE state = 'active';"
```

#### High Memory Usage
```bash
# Check memory usage
free -h

# Check application memory
ps aux | grep -E "(gunicorn|nginx|postgres)"

# Optimize if needed:
# 1. Reduce Gunicorn workers
# 2. Tune PostgreSQL memory settings
# 3. Enable swap if necessary
```

## 📈 Scaling Considerations

### Horizontal Scaling

#### Load Balancer Setup
```nginx
upstream backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    location /api/ {
        proxy_pass http://backend;
    }
}
```

#### Database Replication
```bash
# Set up PostgreSQL streaming replication
# Master server configuration in postgresql.conf:
wal_level = replica
max_wal_senders = 3
wal_keep_segments = 64

# Slave server setup
# Create replication user and configure recovery.conf
```

### Vertical Scaling

#### Resource Optimization
```bash
# Increase system limits
echo "hotelapp soft nofile 65536" >> /etc/security/limits.conf
echo "hotelapp hard nofile 65536" >> /etc/security/limits.conf

# Optimize PostgreSQL
# In postgresql.conf:
shared_buffers = 25% of RAM
effective_cache_size = 75% of RAM
work_mem = RAM / max_connections
```

## ✅ Deployment Checklist

### Pre-deployment
- [ ] Server meets minimum requirements
- [ ] SSL certificate obtained
- [ ] Domain DNS configured
- [ ] Firewall rules configured
- [ ] Backup strategy implemented

### Deployment
- [ ] PostgreSQL installed and configured
- [ ] Database schema imported
- [ ] Backend service running
- [ ] Frontend built and deployed
- [ ] Nginx configured and running
- [ ] SSL certificate installed

### Post-deployment
- [ ] Application accessible via HTTPS
- [ ] All modules functioning correctly
- [ ] Analytics data displaying
- [ ] Database backups working
- [ ] Monitoring scripts active
- [ ] Log rotation configured

### Security
- [ ] Default passwords changed
- [ ] Unnecessary services disabled
- [ ] Security headers configured
- [ ] Access logs enabled
- [ ] Intrusion detection considered

This deployment guide provides a comprehensive foundation for running the Hotel Management System in production. Regular maintenance, monitoring, and security updates are essential for optimal performance and security.

