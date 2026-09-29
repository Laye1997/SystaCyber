# Déploiement — Systalink CyberSécurité

L'application est prête à être déployée sur un hébergeur Python (Render, Railway, un VPS…).
Elle utilise WhiteNoise pour les fichiers statiques et `DATABASE_URL` pour la base.

## 1. Variables d'environnement à définir sur l'hébergeur

| Variable | Valeur | Obligatoire |
|---|---|---|
| `SECRET_KEY` | une longue chaîne aléatoire (générée, voir plus bas) | **oui** |
| `DEBUG` | `false` | **oui** |
| `ALLOWED_HOSTS` | le domaine du site, ex. `secure.systalink.com` | **oui** |
| `CSRF_TRUSTED_ORIGINS` | `https://secure.systalink.com` | **oui** |
| `DATABASE_URL` | fournie par l'hébergeur (PostgreSQL) | recommandé |
| `CAMPAGNE_BASE_URL` | `https://secure.systalink.com` (liens de traçage) | pour les campagnes |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS` | compte d'envoi (SES/Brevo/SMTP) | pour l'envoi réel |

Générer une `SECRET_KEY` :
```
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

## 2. Commandes

- **Build** (installe, collecte les statiques, migre) : `./build.sh`
- **Démarrage** (dans le `Procfile`) : `gunicorn config.wsgi`
- Les migrations tournent aussi automatiquement au release (voir `Procfile`).

## 3. Déploiement sur Render (exemple)

1. Pousser le code sur un dépôt Git (GitHub).
2. Sur Render : *New > Web Service*, relier le dépôt.
3. **Build Command** : `./build.sh`
4. **Start Command** : `gunicorn config.wsgi`
5. Ajouter les variables d'environnement du tableau ci-dessus.
6. Créer une base **PostgreSQL** sur Render et coller son `DATABASE_URL`.
7. Déployer, puis créer le compte formateur :
   `python manage.py createsuperuser` (via le shell de l'hébergeur).
8. Charger le contenu : `python manage.py charger_programme` et `python manage.py charger_modeles`.

## 4. Points d'attention

- **Fichiers envoyés (vidéos)** : sur un hébergeur « éphémère » (Render/Railway free), le dossier
  `media/` est effacé à chaque redéploiement. Pour conserver les vidéos, utiliser un stockage
  externe (S3) ou un disque persistant. Les vidéos peuvent aussi rester en local pendant les
  formations en salle.
- **Envoi des campagnes** : sans les variables `EMAIL_*`, aucun email ne part (sécurité).
  Voir la stratégie domaine dédié + service d'envoi (SES/Brevo).
- **HTTPS** : le site force le HTTPS en production. Si l'hébergeur gère déjà la redirection,
  on peut mettre `SECURE_SSL_REDIRECT=false`.
