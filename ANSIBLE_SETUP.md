# Ansible Deployment Setup

## Configuration du déploiement automatique avec Ansible

Ce projet utilise Ansible pour déployer automatiquement l'application Flask sur votre VM Ubuntu via GitHub Actions.

## Prérequis

### 1. Sur votre VM Ubuntu

**Créer une clé SSH pour GitHub Actions :**

```bash
# Sur votre VM Ubuntu
ssh-keygen -t rsa -b 4096 -C "github-actions" -f ~/.ssh/github_actions_key -N ""

# Ajouter la clé publique aux clés autorisées
cat ~/.ssh/github_actions_key.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Afficher la clé privée (à copier pour GitHub)
cat ~/.ssh/github_actions_key
```

**Copier la clé privée** (tout le contenu, y compris `-----BEGIN` et `-----END`).

### 2. Configurer les secrets GitHub

Allez sur : https://github.com/moustaphafal/flask-helloworld/settings/secrets/actions

Créez ces 3 secrets :

| Nom du secret | Valeur | Description |
|---------------|---------|-------------|
| `VM_SSH_PRIVATE_KEY` | Contenu de la clé privée SSH | La clé complète copiée ci-dessus |
| `VM_HOST` | `172.20.10.2` | L'IP de votre VM Ubuntu |
| `VM_USER` | Votre nom d'utilisateur Ubuntu | Ex: `ubuntu`, `user`, etc. |

### 3. Tester la connexion SSH manuellement

Sur votre machine Windows (avec WSL ou Git Bash) :

```bash
ssh -i chemin/vers/cle your-username@172.20.10.2
```

Si ça fonctionne, le déploiement automatique fonctionnera aussi !

## Workflow de déploiement

Une fois configuré, à chaque `git push` sur `master` :

1. ✅ **Tests** : Pytest vérifie le code
2. 🐳 **Build** : Construction de l'image Docker
3. 📤 **Push** : Publication sur Docker Hub
4. 🚀 **Deploy** : Ansible déploie automatiquement sur la VM
   - Installe Docker si nécessaire
   - Pull la dernière image
   - Redémarre le conteneur
   - Vérifie que l'app fonctionne

## Structure des fichiers Ansible

```
ansible/
├── playbook.yml              # Script de déploiement
├── inventory.yml             # Configuration des serveurs
└── host_vars/
    └── vm-ubuntu.yml         # Variables spécifiques à la VM
```

## Déploiement manuel (optionnel)

Si vous voulez déployer manuellement depuis Windows :

```powershell
# Installer Ansible (avec WSL)
wsl sudo apt-get install ansible

# Mettre à jour l'inventaire avec vos vraies valeurs
# Éditer ansible/inventory.yml et ansible/host_vars/vm-ubuntu.yml

# Déployer
wsl ansible-playbook -i ansible/inventory.yml ansible/playbook.yml
```

## Vérification du déploiement

Après un push, vérifiez :

1. **GitHub Actions** : https://github.com/moustaphafal/flask-helloworld/actions
2. **Votre application** : http://172.20.10.2:5000

## Logs sur la VM

Pour voir les logs en cas de problème :

```bash
# Sur votre VM Ubuntu
docker logs flask-app
docker ps
```

## Désactiver le déploiement automatique

Si vous voulez seulement build sans déployer :

1. Supprimez le job `deploy` dans `.github/workflows/ci-cd-ansible.yml`
2. Ou déployez manuellement avec le script `deploy.sh`

## Avantages de cette solution

- ✅ **Zero-touch deployment** : Push → Déploiement automatique
- ✅ **Idempotent** : Peut être exécuté plusieurs fois sans problème
- ✅ **Rollback facile** : Revenez à une version précédente en re-déployant
- ✅ **Multi-serveurs** : Ajoutez facilement d'autres VMs dans l'inventory
- ✅ **Infrastructure as Code** : Toute la configuration est versionnée
