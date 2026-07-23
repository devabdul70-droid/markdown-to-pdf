# Production Deployment Guide

This guide covers deploying the Markdown to PDF Converter to production environments.

## Pre-Deployment Checklist

- [ ] All tests passing (`pytest tests/ -v`)
- [ ] Code formatted (`black app tests`)
- [ ] No type errors (`mypy app`)
- [ ] No linting issues (`flake8 app`)
- [ ] Dependencies pinned in `requirements.txt`
- [ ] Environment variables documented in `.env.example`
- [ ] Security review completed
- [ ] Performance testing done

## Environment Setup

### Required Environment Variables

```bash
# Security
DEBUG=False
SECRET_KEY=your-secret-key-here

# Limits
MAX_FILE_SIZE=5242880        # 5MB
MAX_MARKDOWN_LENGTH=500000

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Page Defaults
DEFAULT_PAGE_SIZE=A4
DEFAULT_MARGIN=2cm
DEFAULT_FONT_SIZE=12

# Temp Directory
TEMP_DIR=/var/tmp/markdown-to-pdf
```

### Create Non-Root User

```bash
# Create dedicated app user
useradd -m -u 1000 -s /bin/bash appuser

# Create directories
mkdir -p /opt/markdown-to-pdf
mkdir -p /var/log/markdown-to-pdf
mkdir -p /var/tmp/markdown-to-pdf

# Set permissions
chown -R appuser:appuser /opt/markdown-to-pdf
chown -R appuser:appuser /var/log/markdown-to-pdf
chown -R appuser:appuser /var/tmp/markdown-to-pdf
chmod 755 /var/log/markdown-to-pdf
chmod 755 /var/tmp/markdown-to-pdf
```

## Docker Deployment

### Build Production Image

```bash
# Build image
docker build -t markdown-to-pdf:v1.0.0 .

# Tag for registry
docker tag markdown-to-pdf:v1.0.0 your-registry/markdown-to-pdf:v1.0.0
docker tag markdown-to-pdf:v1.0.0 your-registry/markdown-to-pdf:latest

# Push to registry
docker push your-registry/markdown-to-pdf:v1.0.0
docker push your-registry/markdown-to-pdf:latest
```

### Run Container

```bash
docker run \
  --name markdown-to-pdf \
  --restart unless-stopped \
  --detach \
  --publish 8000:8000 \
  --env-file .env.prod \
  --volume /var/log/markdown-to-pdf:/app/logs \
  --volume /var/tmp/markdown-to-pdf:/tmp \
  --memory 2g \
  --cpus 1.5 \
  your-registry/markdown-to-pdf:v1.0.0
```

### Docker Compose Production

```yaml
version: '3.8'

services:
  markdown-to-pdf:
    image: your-registry/markdown-to-pdf:v1.0.0
    restart: unless-stopped
    env_file: .env.prod
    ports:
      - "127.0.0.1:8000:8000"  # Only expose to localhost
    volumes:
      - /var/log/markdown-to-pdf:/app/logs
      - /var/tmp/markdown-to-pdf:/tmp
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    deploy:
      resources:
        limits:
          cpus: '1.5'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

## Kubernetes Deployment

### Create ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: markdown-to-pdf-config
  namespace: default
data:
  DEBUG: "False"
  MAX_FILE_SIZE: "5242880"
  MAX_MARKDOWN_LENGTH: "500000"
  ALLOWED_ORIGINS: "https://yourdomain.com"
```

### Create Secret

```bash
kubectl create secret generic markdown-to-pdf-secret \
  --from-literal=secret_key=$(openssl rand -hex 32) \
  -n default
```

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: markdown-to-pdf
  namespace: default
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: markdown-to-pdf
  template:
    metadata:
      labels:
        app: markdown-to-pdf
    spec:
      containers:
      - name: app
        image: your-registry/markdown-to-pdf:v1.0.0
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8000
          name: http
        envFrom:
        - configMapRef:
            name: markdown-to-pdf-config
        - secretRef:
            name: markdown-to-pdf-secret
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 30
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          readOnlyRootFilesystem: false
          allowPrivilegeEscalation: false
          capabilities:
            drop:
              - ALL
```

### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: markdown-to-pdf
  namespace: default
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
  selector:
    app: markdown-to-pdf
```

### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: markdown-to-pdf
  namespace: default
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - markdown-to-pdf.yourdomain.com
    secretName: markdown-to-pdf-tls
  rules:
  - host: markdown-to-pdf.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: markdown-to-pdf
            port:
              number: 80
```

## Reverse Proxy Setup

### Nginx Configuration

```nginx
upstream markdown_to_pdf {
    server 127.0.0.1:8000 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name markdown-to-pdf.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name markdown-to-pdf.yourdomain.com;
    
    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/markdown-to-pdf.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/markdown-to-pdf.yourdomain.com/privkey.pem;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    # Request size limit
    client_max_body_size 10M;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;
    
    # Proxy settings
    location / {
        proxy_pass http://markdown_to_pdf;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
        
        # Disable buffering for streaming responses
        proxy_buffering off;
        proxy_request_buffering off;
    }
    
    # Gzip compression
    gzip on;
    gzip_types application/json text/plain;
    gzip_min_length 1000;
}
```

### Apache Configuration

```apache
<VirtualHost *:443>
    ServerName markdown-to-pdf.yourdomain.com
    
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/markdown-to-pdf.yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/markdown-to-pdf.yourdomain.com/privkey.pem
    
    # Security headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set X-Content-Type-Options "nosniff"
    
    # Enable proxy modules
    ProxyRequests Off
    ProxyPreserveHost On
    
    # Rate limiting
    <Location />
        SetEnvIf Request_URI "^" RATE_LIMIT
        ModSecDefaultAction "phase:2,pass,log"
    </Location>
    
    # Proxy settings
    ProxyPass / http://127.0.0.1:8000/ timeout=300
    ProxyPassReverse / http://127.0.0.1:8000/
    
    # Gzip compression
    AddOutputFilterByType DEFLATE application/json text/plain
    SetEnvIfNoCase Request_URI "\.pdf$" no-gzip
</VirtualHost>

<VirtualHost *:80>
    ServerName markdown-to-pdf.yourdomain.com
    Redirect / https://markdown-to-pdf.yourdomain.com/
</VirtualHost>
```

## Systemd Service (For Linux)

### Create Service File

```bash
sudo nano /etc/systemd/system/markdown-to-pdf.service
```

```ini
[Unit]
Description=Markdown to PDF Converter
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
User=appuser
WorkingDirectory=/opt/markdown-to-pdf
Environment="PATH=/opt/markdown-to-pdf/venv/bin"
ExecStart=/opt/markdown-to-pdf/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

# Process management
KillMode=process
KillSignal=SIGTERM

# Resource limits
MemoryMax=2G
CPUQuota=150%

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=markdown-to-pdf

[Install]
WantedBy=multi-user.target
```

### Enable and Start

```bash
sudo systemctl daemon-reload
sudo systemctl enable markdown-to-pdf
sudo systemctl start markdown-to-pdf
sudo systemctl status markdown-to-pdf

# View logs
sudo journalctl -u markdown-to-pdf -f
```

## Monitoring and Logging

### Application Logging

```bash
# View logs from Docker
docker logs -f markdown-to-pdf

# View logs from systemd
journalctl -u markdown-to-pdf -f

# Persistent log file
./logs/app.log
```

### Metrics to Monitor

- **Response time**: Target <2s for typical conversions
- **PDF generation failures**: Target 0 failures
- **CPU usage**: Should stay <70%
- **Memory usage**: Should stay <1.5G
- **Disk I/O**: Monitor temp directory usage

### Health Checks

```bash
# Check application health
curl https://markdown-to-pdf.yourdomain.com/health

# Expected response
{"status": "healthy", "app": "Markdown to PDF Converter", "version": "1.0.0"}
```

## Backup and Recovery

### Backup Application
```bash
# Backup configuration
tar czf backup-config.tar.gz app/themes app/templates .env

# Store securely
aws s3 cp backup-config.tar.gz s3://backups/markdown-to-pdf/
```

### Recovery
```bash
# Restore from backup
aws s3 cp s3://backups/markdown-to-pdf/backup-config.tar.gz .
tar xzf backup-config.tar.gz

# Restart application
docker-compose restart
```

## Scaling Considerations

### Horizontal Scaling
- Run multiple instances behind load balancer
- Use shared logging and metrics
- Stateless design allows easy scaling

### Vertical Scaling
- Increase memory/CPU limits
- Increase uvicorn workers
- Consider async queue for large conversions

### Performance Optimization
- Enable gzip compression
- Cache theme CSS files
- Use CDN for static docs
- Monitor and optimize PDF generation time

## Security Hardening

### Network Security
```bash
# Allow only necessary ports
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### SSL/TLS
```bash
# Generate self-signed certificate (development only)
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Use Let's Encrypt for production
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d markdown-to-pdf.yourdomain.com
```

### Application Security
- Always set `DEBUG=False` in production
- Use strong `ALLOWED_ORIGINS` settings
- Implement rate limiting
- Add authentication if needed
- Regular dependency updates

## Troubleshooting

### Container won't start
```bash
# Check logs
docker logs markdown-to-pdf

# Check resource limits
docker stats markdown-to-pdf

# Verify environment variables
docker exec markdown-to-pdf env | grep -E "^(DEBUG|MAX_)"
```

### High memory usage
```bash
# Increase memory limit
docker update --memory 3g markdown-to-pdf

# Check for memory leaks in logs
```

### SSL certificate issues
```bash
# Check certificate expiration
sudo certbot certificates

# Renew certificate
sudo certbot renew --dry-run
```

## Maintenance

### Regular Tasks
- Update dependencies monthly
- Review logs weekly
- Monitor performance weekly
- Backup configuration daily
- Test disaster recovery quarterly

### Dependency Updates
```bash
# Check for outdated packages
pip list --outdated

# Update safely
pip install --upgrade package-name
pip freeze > requirements.txt
# Test thoroughly
pytest tests/ -v
```

---

For questions or issues, check:
- Application logs
- Health check endpoint
- README and API documentation
- Contributing guide for development setup
