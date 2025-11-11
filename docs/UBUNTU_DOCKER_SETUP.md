# Configuration Docker sur VM Ubuntu

## 1. Installation de Docker

Connectez-vous à votre VM Ubuntu via SSH et exécutez ces commandes :

```bash
# Mettre à jour les paquets
sudo apt-get update
sudo apt-get upgrade -y

# Installer les dépendances
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# Ajouter la clé GPG officielle de Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Configurer le dépôt Docker
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Installer Docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Vérifier l'installation
sudo docker --version
sudo docker run hello-world
```

## 2. Configuration de l'utilisateur (optionnel mais recommandé)

Pour utiliser Docker sans `sudo` :

```bash
# Ajouter votre utilisateur au groupe docker
sudo usermod -aG docker $USER

# Appliquer les changements (ou reconnectez-vous)
newgrp docker

# Tester sans sudo
docker --version
docker ps
```

## 3. Se connecter à GitHub Container Registry

```bash
# Remplacez YOUR_TOKEN par votre token GitHub
echo YOUR_TOKEN | docker login ghcr.io -u moustaphafal --password-stdin
```

## 4. Déployer l'application Flask depuis GHCR

```bash
# Télécharger l'image
docker pull ghcr.io/moustaphafal/flask-helloworld:latest

# Lancer le conteneur
docker run -d \
  --name flask-app \
  -p 5000:5000 \
  --restart unless-stopped \
  ghcr.io/moustaphafal/flask-helloworld:latest

# Vérifier que le conteneur tourne
docker ps

# Voir les logs
docker logs flask-app

# Tester l'application
curl http://localhost:5000
```

## 5. Accéder à l'application

- **Depuis la VM** : http://localhost:5000
- **Depuis votre navigateur** : http://IP_DE_VOTRE_VM:5000

⚠️ **Important** : Si vous ne pouvez pas accéder depuis l'extérieur, vérifiez :
- Le firewall de la VM : `sudo ufw allow 5000`
- Les règles de sécurité de votre cloud provider (AWS, Azure, etc.)

## 6. Commandes utiles

```bash
# Voir les conteneurs en cours
docker ps

# Voir tous les conteneurs (y compris arrêtés)
docker ps -a

# Arrêter le conteneur
docker stop flask-app

# Démarrer le conteneur
docker start flask-app

# Redémarrer le conteneur
docker restart flask-app

# Supprimer le conteneur
docker rm flask-app

# Voir les logs en temps réel
docker logs -f flask-app

# Mettre à jour l'application (après un nouveau push)
docker pull ghcr.io/moustaphafal/flask-helloworld:latest
docker stop flask-app
docker rm flask-app
docker run -d --name flask-app -p 5000:5000 --restart unless-stopped ghcr.io/moustaphafal/flask-helloworld:latest
```

## 7. Script de déploiement automatique (optionnel)

Créez un fichier `deploy.sh` :

```bash
#!/bin/bash
set -e

echo "🚀 Deploying Flask App from GHCR..."

# Pull latest image
echo "📥 Pulling latest image..."
docker pull ghcr.io/moustaphafal/flask-helloworld:latest

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
  ghcr.io/moustaphafal/flask-helloworld:latest

echo "✅ Deployment complete!"
echo "🌐 Access your app at http://$(hostname -I | awk '{print $1}'):5000"

# Show logs
docker logs flask-app
```

Rendez-le exécutable et lancez-le :

```bash
chmod +x deploy.sh
./deploy.sh
```

## 8. Déploiement continu (CD)

Pour automatiser le déploiement à chaque push, vous pouvez :
- Utiliser un webhook GitHub
- Configurer GitHub Actions avec SSH
- Utiliser un runner GitHub Actions auto-hébergé sur votre VM

Voulez-vous que je configure le déploiement automatique ?
