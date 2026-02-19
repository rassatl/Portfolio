# Documentation API Portfolio

## 📋 Table des matières
- [Introduction](#introduction)
- [Configuration serveur](#configuration-serveur)
- [Authentification](#authentification)
- [Endpoints](#endpoints)
  - [Expériences](#expériences)
  - [Projets](#projets)
  - [Compétences](#compétences)
  - [Contact](#contact)
- [Modèles de données](#modèles-de-données)
- [Codes de réponse](#codes-de-réponse)

---

## Introduction

L'API Portfolio est une API REST construite avec **FastAPI** pour gérer un portfolio professionnel. Elle permet de :
- Consulter les expériences professionnelles
- Gérer les projets (créer, voir, supprimer)
- Rechercher par compétences
- S'authentifier
- Soumettre des messages de contact

**Framework** : FastAPI
**Base de données** : PostgreSQL + MongoDB (optionnel)
**Authentification** : Bcrypt pour les mots de passe

---

## Configuration serveur

### URLs de base

| Environnement | URL |
|---------------|-----|
| Développement | `http://localhost:8000` |
| Production | `https://api.portfolio.com` |

### Middleware CORS

L'API accepte les requêtes des origines suivantes :
- `http://localhost:5173`
- `http://127.0.0.1:5173`

---

## Authentification

### Endpoint de connexion

```
POST /login
```

**Description** : Authentifie un utilisateur avec ses identifiants.

**Corps de la requête** (JSON) :
```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```

**Réponse 200 (Succès)** :
```json
{
  "success": true,
  "message": "Connexion réussie",
  "user_id": 42
}
```

**Réponse 401 (Échec)** :
```json
{
  "detail": "Identifiants invalides"
}
```

---

## Endpoints

### Expériences

#### GET / (Racine)

Récupère la liste complète de toutes les expériences.

```
GET /
```

**Réponse 200** :
```json
{
  "experience": [
    {
      "id": 1,
      "titre": "Développeur Full Stack",
      "entreprise": "TechCorp",
      "description": "...",
      "date_debut": "2020-01-15",
      "date_fin": null
    }
  ]
}
```

---

#### GET /experiences

Liste les expériences avec le nombre de projets associés.

```
GET /experiences?sort=-date_debut
```

**Paramètres** :
| Nom | Type | Par défaut | Description |
|-----|------|-----------|-------------|
| `sort` | string | `-date_debut` | Tri : `-date_debut` (DESC) ou `date_debut` (ASC) |

**Réponse 200** :
```json
{
  "experiences": [
    {
      "id": 1,
      "titre": "Développeur Full Stack",
      "entreprise": "TechCorp",
      "date_debut": "2020-01-15",
      "date_fin": null,
      "project_count": 5
    }
  ]
}
```

**Réponse 400** :
```json
{
  "detail": "Invalid sort field"
}
```

---

#### GET /experiences/{experience_id}/full

Récupère une expérience complète avec tous ses projets et compétences.

```
GET /experiences/1/full
```

**Paramètres** :
| Nom | Type | Description |
|-----|------|-------------|
| `experience_id` | integer | ID de l'expérience (path) |

**Réponse 200** :
```json
{
  "experience": {
    "id": 1,
    "titre": "Développeur Full Stack",
    "entreprise": "TechCorp",
    "description": "...",
    "date_debut": "2020-01-15",
    "date_fin": null
  },
  "projects": [
    {
      "id": 10,
      "titre": "Mon superbe projet",
      "description": "...",
      "github_url": "https://github.com/user/repo",
      "date_projet": "2024-01-15"
    }
  ],
  "skills": [
    {
      "id": 1,
      "nom": "Python"
    },
    {
      "id": 2,
      "nom": "FastAPI"
    }
  ]
}
```

**Réponse 404** :
```json
{
  "detail": "Experience not found"
}
```

---

### Projets

#### GET /projects/featured

Récupère les projets en vedette, optimisé pour la page d'accueil.

```
GET /projects/featured?limit=3
```

**Paramètres** :
| Nom | Type | Par défaut | Min | Max | Description |
|-----|------|-----------|-----|-----|-------------|
| `limit` | integer | `3` | 1 | 10 | Nombre de projets à retourner |

**Réponse 200** :
```json
{
  "projects": [
    {
      "id": 10,
      "titre": "Mon superbe projet",
      "description": "Une description détaillée",
      "github_url": "https://github.com/user/repo",
      "lien_url": "https://project.com",
      "date_projet": "2024-01-15",
      "experience_id": 1,
      "user_id": 42,
      "skills": ["Python", "FastAPI", "PostgreSQL"]
    }
  ]
}
```

**Réponse 400** :
```json
{
  "detail": "limit must be between 1 and 10"
}
```

---

#### GET /projects/search

Recherche des projets par texte ou par compétences.

```
GET /projects/search?query=React&skills=JavaScript,React
```

**Paramètres** :
| Nom | Type | Description |
|-----|------|-------------|
| `query` | string | Texte à rechercher dans titre et description (ILIKE) |
| `skills` | string | Compétences séparées par des virgules |

**Réponse 200** :
```json
{
  "projects": [
    {
      "id": 10,
      "titre": "Application React",
      "description": "Une application React moderne",
      "github_url": "https://github.com/user/repo",
      "lien_url": "https://app.com",
      "date_projet": "2024-01-15",
      "experience_id": null,
      "user_id": 42,
      "skills": ["JavaScript", "React", "Vite"]
    }
  ]
}
```

---

#### GET /projects/{project_id}/similar

Trouve les projets ayant des compétences en commun.

```
GET /projects/10/similar?k=5
```

**Paramètres** :
| Nom | Type | Par défaut | Description |
|-----|------|-----------|-------------|
| `project_id` | integer | - | ID du projet de référence (path) |
| `k` | integer | `5` | Nombre de projets similaires (doit être > 0) |

**Réponse 200** :
```json
{
  "projects": [
    {
      "id": 11,
      "titre": "Autre projet React",
      "description": "...",
      "skills": ["JavaScript", "React"],
      "shared_skills": 2
    }
  ]
}
```

**Réponse 400** :
```json
{
  "detail": "k must be positive"
}
```

---

#### POST /projects

Crée un nouveau projet avec ses compétences associées.

```
POST /projects
Content-Type: application/json

{
  "titre": "Mon superbe projet",
  "description": "Une description détaillée du projet",
  "github_url": "https://github.com/username/repo",
  "lien_url": "https://project.com",
  "date_projet": "2024-01-15",
  "experience_id": 1,
  "user_id": 42,
  "skills": ["Python", "FastAPI", "PostgreSQL"]
}
```

**Champs** :
| Nom | Type | Requis | Description |
|-----|------|--------|-------------|
| `titre` | string | ✅ | Titre du projet (min 1 caractère) |
| `description` | string | ✅ | Description (min 1 caractère) |
| `github_url` | string(uri) | ❌ | URL du repository GitHub |
| `lien_url` | string(uri) | ❌ | URL de déploiement |
| `date_projet` | string(date) | ❌ | Date du projet (format: YYYY-MM-DD) |
| `experience_id` | integer | ❌ | ID de l'expérience associée |
| `user_id` | integer | ❌ | ID de l'utilisateur créateur |
| `skills` | array[string] | ❌ | Liste des compétences (créées si inexistantes) |

**Réponse 200** :
```json
{
  "success": true,
  "message": "Projet créé avec succès",
  "project_id": 10
}
```

**Réponse 500** :
```json
{
  "detail": "Erreur lors de la création du projet"
}
```

---

#### DELETE /projects/{project_id}

Supprime un projet si l'utilisateur en est le propriétaire.

```
DELETE /projects/10
Content-Type: application/json

{
  "user_id": 42
}
```

**Paramètres** :
| Nom | Type | Description |
|-----|------|-------------|
| `project_id` | integer | ID du projet à supprimer (path) |

**Corps de la requête** :
| Nom | Type | Requis | Description |
|-----|------|--------|-------------|
| `user_id` | integer | ✅ | ID de l'utilisateur (doit être propriétaire) |

**Réponse 200** :
```json
{
  "success": true,
  "message": "Projet supprimé avec succès"
}
```

**Réponse 403** :
```json
{
  "detail": "Vous ne pouvez pas supprimer ce projet"
}
```

**Réponse 404** :
```json
{
  "detail": "Projet non trouvé"
}
```

**Réponse 500** :
```json
{
  "detail": "Erreur lors de la suppression du projet"
}
```

---

### Compétences

#### GET /skills/top

Retourne le top K des compétences par fréquence d'utilisation.

```
GET /skills/top?k=10
```

**Paramètres** :
| Nom | Type | Par défaut | Description |
|-----|------|-----------|-------------|
| `k` | integer | `10` | Nombre de compétences (doit être > 0) |

**Réponse 200** :
```json
{
  "skills": [
    {
      "id": 1,
      "nom": "Python",
      "usage_count": 15
    },
    {
      "id": 2,
      "nom": "JavaScript",
      "usage_count": 12
    },
    {
      "id": 3,
      "nom": "React",
      "usage_count": 10
    }
  ]
}
```

**Réponse 400** :
```json
{
  "detail": "k must be positive"
}
```

---

### Contact

#### POST /contact

Crée un message de contact. Sauvegarde en MongoDB en priorité, sinon en JSON local.

```
POST /contact
Content-Type: application/json

{
  "name": "Jean Dupont",
  "email": "jean@example.com",
  "message": "J'aimerais discuter d'une collaboration..."
}
```

**Champs** :
| Nom | Type | Requis | Description |
|-----|------|--------|-------------|
| `name` | string | ✅ | Nom du contact (min 1 caractère) |
| `email` | string(email) | ✅ | Email valide |
| `message` | string | ✅ | Message (min 1 caractère) |

**Réponse 200** :
```json
{
  "id": "507f1f77bcf86cd799439011",
  "message": "Contact saved successfully (MongoDB)"
}
```

Ou en fallback local :
```json
{
  "id": "local",
  "message": "Contact saved successfully (Local Fallback)"
}
```

**Réponse 422** :
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "invalid email format",
      "type": "value_error.email"
    }
  ]
}
```

**Réponse 500** :
```json
{
  "detail": "Failed to save contact"
}
```

---

## Modèles de données

### Experience

```json
{
  "id": 1,
  "titre": "Développeur Full Stack",
  "entreprise": "TechCorp",
  "description": "...",
  "date_debut": "2020-01-15",
  "date_fin": "2023-12-31"
}
```

### Project

```json
{
  "id": 10,
  "titre": "Mon superbe projet",
  "description": "Une description détaillée",
  "github_url": "https://github.com/user/repo",
  "lien_url": "https://project.com",
  "date_projet": "2024-01-15",
  "experience_id": 1,
  "user_id": 42,
  "skills": ["Python", "FastAPI", "PostgreSQL"]
}
```

### Skill

```json
{
  "id": 1,
  "nom": "Python"
}
```

### User

```json
{
  "id": 42,
  "username": "john_doe",
  "password_hash": "$2b$12$..."
}
```

### Contact

```json
{
  "name": "Jean Dupont",
  "email": "jean@example.com",
  "message": "...",
  "date": "2024-02-19T10:30:45.123456"
}
```

---

## Codes de réponse

| Code | Signification | Utilisation |
|------|---------------|-------------|
| **200** | OK | Requête réussie |
| **400** | Bad Request | Erreur de validation (paramètres invalides) |
| **401** | Unauthorized | Authentification échouée |
| **403** | Forbidden | Accès refusé (ex: ne pas être propriétaire) |
| **404** | Not Found | Ressource non trouvée |
| **422** | Unprocessable Entity | Erreur de validation du corps de requête |
| **500** | Internal Server Error | Erreur serveur |

---

## Notes de sécurité

⚠️ **Attention**

1. **Stockage des mots de passe** : Les mots de passe sont hashés avec bcrypt. Ne stockez jamais les mots de passe en clair.

2. **Suppression de projets** : Vérififiez toujours que l'utilisateur est le propriétaire du projet avant suppression.

3. **Email validation** : L'endpoint `/contact` utilise `email-validator` pour valider les emails.

4. **CORS** : Les origines autorisées sont limitées. Modifiez au besoin pour la production.

5. **Connexion MongoDB** : Optionnelle. L'API retombe sur le stockage JSON local si MongoDB n'est pas disponible.

**Dernière mise à jour** : 19 février 2026
