# Docker Hub Setup

## Configuration du projet

Ce projet publie automatiquement les images Docker sur Docker Hub.

## Configuration GitHub Actions

### 1. Ajouter votre Docker Hub Token comme secret GitHub

1. Allez sur votre repo : https://github.com/moustaphafal/flask-helloworld
2. Cliquez sur **Settings** → **Secrets and variables** → **Actions**
3. Cliquez sur **New repository secret**
4. Créez un secret :
   - **Name** : `DOCKER_TOKEN`
   - **Value** : Votre Docker Hub Access Token
5. Cliquez sur **Add secret**

### 2. Le workflow s'exécutera automatiquement

À chaque push sur `master`, le workflow :
- Lance les tests avec pytest
- Build l'image Docker
- Publie sur Docker Hub : `moustaphafal/flask-helloworld`
- Tags : `latest`, `sha-xxxxx`, versions

## Utiliser l'image depuis Docker Hub

### Sur votre VM Ubuntu

```bash
# Se connecter à Docker Hub (optionnel pour les images publiques)
docker login -u moustaphafal

# Télécharger l'image
docker pull moustaphafal/flask-helloworld:latest

# Lancer le conteneur
docker run -d -p 5000:5000 --name flask-app --restart unless-stopped moustaphafal/flask-helloworld:latest

# Vérifier
docker ps
curl http://localhost:5000
```

### Script de déploiement

Utilisez `deploy.sh` sur votre VM Ubuntu :

```bash
#!/bin/bash
set -e

echo "🚀 Deploying Flask App from Docker Hub..."

docker pull moustaphafal/flask-helloworld:latest
docker stop flask-app 2>/dev/null || true
docker rm flask-app 2>/dev/null || true
docker run -d --name flask-app -p 5000:5000 --restart unless-stopped moustaphafal/flask-helloworld:latest

echo "✅ Deployment complete!"
docker logs flask-app
```

## Push manuel

```bash
# Se connecter
docker login -u moustaphafal

# Builder
docker build -t moustaphafal/flask-helloworld:latest .

# Pusher
docker push moustaphafal/flask-helloworld:latest
```

## Lien vers l'image

- Docker Hub : https://hub.docker.com/r/moustaphafal/flask-helloworld
