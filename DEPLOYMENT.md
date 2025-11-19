# Deployment Guide

## Production Deployment

### Option 1: Docker Compose (Recommended)

1. **Prepare Environment**
```bash
# Clone repository
git clone https://github.com/tekdela/company-ai-assistant.git
cd company-ai-assistant

# Create production environment file
cp backend/.env.example backend/.env

# Edit .env and set production values
nano backend/.env
```

2. **Configure Production Variables**
```env
GEMINI_API_KEY=your_production_gemini_key
CLOUDFLARE_API_TOKEN=your_cloudflare_token
CLOUDFLARE_ZONE_ID=your_zone_id
CLOUDFLARE_ACCOUNT_ID=your_account_id
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
CORS_ORIGINS=https://your-domain.com
REDIS_URL=redis://redis:6379
ENVIRONMENT=production
```

3. **Deploy with Docker Compose**
```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f backend

# Stop services
docker-compose -f docker-compose.prod.yml down
```

### Option 2: Cloudflare Pages + Workers

#### Deploy Frontend to Cloudflare Pages

1. **Install Wrangler**
```bash
npm install -g wrangler
```

2. **Login to Cloudflare**
```bash
wrangler login
```

3. **Build Frontend**
```bash
cd frontend
npm install
npm run build
```

4. **Deploy to Cloudflare Pages**
```bash
wrangler pages publish dist --project-name=company-ai-assistant
```

Or use GitHub Actions (automatic deployment):
- Push to `main` branch
- GitHub Actions will build and deploy automatically

#### Deploy Cloudflare Workers

```bash
# From root directory
wrangler publish workers/api-proxy.js --name company-ai-assistant-api
```

#### Configure Workers Environment Variables

```bash
# Set backend URL
wrangler secret put BACKEND_URL --env production
# Enter: https://your-backend-api.com

# Set other secrets as needed
```

### Option 3: Manual Deployment

#### Backend (VPS/Cloud Server)

1. **Setup Server**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install Docker (optional)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

2. **Deploy Backend**
```bash
# Clone repository
git clone https://github.com/tekdela/company-ai-assistant.git
cd company-ai-assistant/backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
nano .env  # Edit with production values

# Run with systemd
sudo nano /etc/systemd/system/ai-assistant.service
```

3. **Systemd Service File**
```ini
[Unit]
Description=Company AI Assistant Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/company-ai-assistant/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python -m app.main

[Install]
WantedBy=multi-user.target
```

4. **Start Service**
```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-assistant
sudo systemctl start ai-assistant
sudo systemctl status ai-assistant
```

#### Frontend (Static Hosting)

1. **Build Frontend**
```bash
cd frontend
npm install
npm run build
```

2. **Deploy to Server**
```bash
# Copy dist folder to web server
scp -r dist/* user@server:/var/www/ai-assistant/

# Or use rsync
rsync -avz dist/ user@server:/var/www/ai-assistant/
```

3. **Nginx Configuration**
```nginx
server {
    listen 80;
    server_name ai-assistant.yourdomain.com;
    
    root /var/www/ai-assistant;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Environment-Specific Configurations

### Development
```env
ENVIRONMENT=development
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Staging
```env
ENVIRONMENT=staging
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
CORS_ORIGINS=https://staging.yourdomain.com
```

### Production
```env
ENVIRONMENT=production
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
CORS_ORIGINS=https://yourdomain.com
```

## Monitoring & Logging

### Health Checks

```bash
# Backend health
curl http://localhost:8000/api/health

# Expected response
{
  "status": "healthy",
  "timestamp": "2024-11-19T06:39:05.471Z",
  "services": {
    "api": true,
    "gemini": true,
    "knowledge_base": true
  }
}
```

### Docker Logs

```bash
# View backend logs
docker-compose logs -f backend

# View all logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100
```

### Application Logs

Logs are written to stdout/stderr and can be viewed with:
```bash
# Systemd service
sudo journalctl -u ai-assistant -f

# Docker
docker logs -f <container_id>
```

## SSL/TLS Configuration

### Using Cloudflare (Automatic)
- Cloudflare provides automatic SSL/TLS
- No configuration needed
- Free SSL certificates

### Using Let's Encrypt (Manual)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d ai-assistant.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

## Backup & Recovery

### Database Backup (if using PostgreSQL/MySQL)

```bash
# PostgreSQL
pg_dump dbname > backup.sql

# MySQL
mysqldump dbname > backup.sql
```

### Redis Backup

```bash
# Save Redis data
docker-compose exec redis redis-cli SAVE

# Copy backup
docker cp <container_id>:/data/dump.rdb ./backup/
```

### Application Backup

```bash
# Backup configuration
tar -czf backup-config.tar.gz backend/.env

# Backup uploaded files (if any)
tar -czf backup-uploads.tar.gz backend/uploads/
```

## Scaling

### Horizontal Scaling

1. **Load Balancer Configuration**
```nginx
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

server {
    location /api/ {
        proxy_pass http://backend;
    }
}
```

2. **Docker Swarm**
```bash
docker stack deploy -c docker-compose.prod.yml ai-assistant
```

3. **Kubernetes**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-assistant-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-assistant
  template:
    spec:
      containers:
      - name: backend
        image: company-ai-assistant-backend:latest
        ports:
        - containerPort: 8000
```

### Vertical Scaling

Increase resources in `docker-compose.prod.yml`:
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

## Troubleshooting

### Backend Issues

```bash
# Check if backend is running
curl http://localhost:8000/api/health

# Check Docker container
docker ps | grep backend

# View logs
docker logs <container_id>

# Restart service
docker-compose restart backend
```

### Frontend Issues

```bash
# Check build errors
cd frontend
npm run build

# Clear cache
rm -rf node_modules package-lock.json
npm install
```

### Cloudflare Issues

```bash
# Check Workers status
wrangler tail

# View deployment logs
wrangler pages deployment list

# Check DNS
dig ai-assistant.yourdomain.com
```

## Security Checklist

- [ ] GEMINI_API_KEY properly secured
- [ ] CORS origins restricted to production domains
- [ ] SSL/TLS enabled
- [ ] DDoS protection active (Cloudflare)
- [ ] Rate limiting configured
- [ ] Security headers enabled
- [ ] Firewall rules configured
- [ ] Regular security updates
- [ ] Backup strategy in place
- [ ] Monitoring and alerting configured

## Performance Optimization

1. **Enable Cloudflare CDN**
   - Cache static assets
   - Enable Brotli compression
   - Use Cloudflare Auto Minify

2. **Backend Optimization**
   - Enable Redis caching
   - Use connection pooling
   - Optimize database queries

3. **Frontend Optimization**
   - Code splitting
   - Lazy loading
   - Image optimization
   - Service workers

## Support

For deployment issues:
- Check logs first
- Review documentation
- Open GitHub issue
- Contact: support@yourcompany.com
