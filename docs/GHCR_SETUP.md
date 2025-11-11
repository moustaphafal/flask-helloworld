# GitHub Container Registry (GHCR) Setup

## Configuration automatique

Ce projet est configuré pour publier automatiquement les images Docker sur GitHub Container Registry (GHCR).

## Workflow automatique

Le workflow `.github/workflows/docker-publish.yml` :
- Lance les tests avec pytest
- Build l'image Docker
- Publie sur `ghcr.io/moustaphafal/flask-helloworld`
- Tags automatiques : `latest`, `sha-xxxxx`, branches, et versions

## Utiliser l'image depuis GHCR

### 1. Se connecter à GHCR

```bash
# Créer un Personal Access Token sur GitHub avec permission packages:read
echo YOUR_TOKEN | docker login ghcr.io -u moustaphafal --password-stdin
```

### 2. Télécharger l'image

```bash
docker pull ghcr.io/moustaphafal/flask-helloworld:latest
```

### 3. Lancer le conteneur

```bash
docker run -d -p 5000:5000 ghcr.io/moustaphafal/flask-helloworld:latest
```

## Publier manuellement

```bash
# Builder
docker build -t ghcr.io/moustaphafal/flask-helloworld:latest .

# Pusher
docker push ghcr.io/moustaphafal/flask-helloworld:latest
```

## Rendre l'image publique

1. Allez sur https://github.com/moustaphafal?tab=packages
2. Cliquez sur votre package
3. Package settings → Change visibility → Public

## Tags disponibles

- `latest` : Dernière version de la branche principale
- `sha-xxxxxx` : Commit spécifique
- `v1.0.0` : Version sémantique (si vous créez des tags git)
