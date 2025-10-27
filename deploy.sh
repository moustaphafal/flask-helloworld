#!/bin/bash
set -e

echo "🚀 Deploying Flask App from Docker Hub..."

# Pull latest image
echo "📥 Pulling latest image..."
docker pull moustaphafal/flask-helloworld:latest

# Stop and remove old container if exists
echo "🛑 Stopping old container..."
docker stop flask-app 2>/dev/null || true
docker rm flask-app 2>/dev/null || true

# Run new container
echo "▶️  Starting new container..."
docker run -d \
  --name flask-app \
  -p 5000:5000 \
  --restart unless-stopped \
  moustaphafal/flask-helloworld:latest

echo "✅ Deployment complete!"
echo "🌐 Access your app at http://192.168.1.20:5000"

# Show logs
echo ""
echo "📋 Container logs:"
docker logs flask-app
