# Vérification du déploiement sur VM Ubuntu

## Commandes de vérification

```bash
# 1. Voir les conteneurs en cours d'exécution
docker ps

# 2. Voir les logs du conteneur
docker logs flask-app

# 3. Tester l'application localement sur la VM
curl http://172.20.10.2:5000

# 4. Obtenir l'IP de votre VM
hostname -I
# ou
ip addr show
```

## Accéder à l'application

### Depuis la VM (SSH)
```bash
curl http://localhost:5000
```

### Depuis votre navigateur
Ouvrez : `http://172.20.10.2:5000`

## Si vous ne pouvez pas accéder depuis l'extérieur

### Ouvrir le port 5000 dans le firewall
```bash
# Pour UFW (Ubuntu Firewall)
sudo ufw allow 5000
sudo ufw status

# Vérifier que le port écoute
sudo netstat -tlnp | grep 5000
# ou
sudo ss -tlnp | grep 5000
```

### Vérifier les règles de sécurité cloud

Si votre VM est sur un cloud provider :
- **AWS** : Security Groups → Ajouter règle entrante TCP port 5000
- **Azure** : Network Security Groups → Ajouter règle entrante port 5000
- **GCP** : Firewall Rules → Ajouter règle TCP:5000

## Commandes utiles

```bash
# Arrêter le conteneur
docker stop flask-app

# Démarrer le conteneur
docker start flask-app

# Redémarrer le conteneur
docker restart flask-app

# Voir les logs en temps réel
docker logs -f flask-app

# Supprimer le conteneur
docker stop flask-app && docker rm flask-app

# Mettre à jour vers la dernière version
docker pull moustaphafal/flask-helloworld:latest
docker stop flask-app
docker rm flask-app
docker run -d --name flask-app -p 5000:5000 --restart unless-stopped moustaphafal/flask-helloworld:latest
```

## Vérifier que l'application fonctionne correctement

```bash
# Test simple
curl http://localhost:5000

# Test avec plus de détails
curl -v http://localhost:5000

# Test depuis l'extérieur (remplacez IP_VM par votre IP)
curl http://IP_VM:5000
```
