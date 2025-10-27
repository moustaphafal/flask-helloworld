# Configuration Self-Hosted Runner GitHub Actions

## Option 1 : Runner sur la VM Ubuntu (Recommandé)

### 1. Sur votre VM Ubuntu, téléchargez et configurez le runner

```bash
# Se connecter à votre VM
ssh votre-user@172.20.10.2

# Créer un dossier pour le runner
mkdir -p ~/actions-runner && cd ~/actions-runner

# Télécharger le runner (vérifiez la dernière version sur GitHub)
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz

# Extraire l'archive
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz
```

### 2. Obtenir le token de configuration

1. Allez sur : https://github.com/moustaphafal/flask-helloworld/settings/actions/runners/new
2. Sélectionnez **Linux** comme système d'exploitation
3. Copiez la commande `./config.sh` avec le token fourni

### 3. Configurer le runner

```bash
# Exécutez la commande copiée de GitHub (avec votre token)
./config.sh --url https://github.com/moustaphafal/flask-helloworld --token VOTRE_TOKEN_ICI

# Répondez aux questions :
# - Enter the name of the runner group: [Press Enter for default]
# - Enter the name of runner: ubuntu-vm (ou un autre nom)
# - Enter any additional labels: docker,ubuntu (optionnel)
# - Enter name of work folder: [Press Enter for _work]
```

### 4. Installer le runner comme service (pour qu'il démarre automatiquement)

```bash
# Installer le service
sudo ./svc.sh install

# Démarrer le service
sudo ./svc.sh start

# Vérifier le statut
sudo ./svc.sh status
```

### 5. Vérifier que le runner est actif

Allez sur : https://github.com/moustaphafal/flask-helloworld/settings/actions/runners

Vous devriez voir votre runner avec le statut **"Idle"** (vert) 🟢

## Option 2 : Runner sur votre machine Windows

### 1. Télécharger le runner

1. Allez sur : https://github.com/moustaphafal/flask-helloworld/settings/actions/runners/new
2. Sélectionnez **Windows**
3. Téléchargez l'archive

### 2. Configuration (PowerShell en tant qu'administrateur)

```powershell
# Créer un dossier
mkdir C:\actions-runner ; cd C:\actions-runner

# Extraire l'archive téléchargée
Expand-Archive -Path .\actions-runner-win-x64-2.311.0.zip -DestinationPath .

# Configurer (utilisez le token de GitHub)
.\config.cmd --url https://github.com/moustaphafal/flask-helloworld --token VOTRE_TOKEN_ICI

# Installer comme service Windows
.\svc.sh install

# Démarrer le service
.\svc.sh start
```

## Modification du workflow pour utiliser le Self-Hosted Runner

Modifiez `.github/workflows/ci-cd-ansible.yml` :

```yaml
deploy:
  runs-on: self-hosted  # ← Changez de ubuntu-latest à self-hosted
  needs: build-and-push
  if: github.ref == 'refs/heads/master' || github.ref == 'refs/heads/main'
  
  steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    # Plus besoin de Setup SSH car le runner est sur votre réseau local !
    - name: Deploy with Ansible
      run: |
        ansible-playbook -i ansible/inventory.yml ansible/playbook.yml
      env:
        ANSIBLE_HOST_KEY_CHECKING: 'False'
    
    - name: Verify deployment
      run: |
        echo "Deployment completed successfully!"
        curl http://172.20.10.2:5000
```

## Avantages du Self-Hosted Runner

✅ **Accès direct à votre VM locale** (172.20.10.2)
✅ **Pas besoin de secrets SSH** (déjà sur le même réseau)
✅ **Plus rapide** (pas de téléchargement depuis Internet)
✅ **Gratuit** (pas de limite de minutes)
✅ **Sécurisé** (tout reste dans votre réseau local)

## Commandes utiles

```bash
# Sur la VM Ubuntu
cd ~/actions-runner

# Vérifier le statut
sudo ./svc.sh status

# Redémarrer le service
sudo ./svc.sh restart

# Arrêter le service
sudo ./svc.sh stop

# Voir les logs
journalctl -u actions.runner.* -f
```

## Notes importantes

- Le runner doit être **toujours actif** pour que les workflows fonctionnent
- Si votre VM est éteinte, les workflows échoueront
- Vous pouvez avoir plusieurs runners (VM + Windows)
- Les runners self-hosted utilisent vos ressources, pas celles de GitHub

## Prochaine étape

Une fois le runner configuré et actif, je modifierai le workflow pour utiliser `runs-on: self-hosted`.

Voulez-vous que je vous aide à configurer le runner maintenant ?
