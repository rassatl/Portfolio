# Fonctionnalites techniques du site

## Frontend (Vue 3 + Vite)

- Cache API cote client pour eviter les rechargements complets lors du switch Accueil/Projets (useApiCache).
- Composables modulaires pour projets, filtres et formatage (useProjects, useFilters, useFormatters).
- Filtrage avance: recherche texte, competences, annees, tri asc/desc.
- Chargement progressif avec skeleton loaders pour une UI fluide.
- Composants reutilisables: cartes projets, tags de competences, panneau de filtres, section competences.
- Auth locale via localStorage (username, user_id) pour afficher les actions.

## Backend (FastAPI)

- Aggregation SQL des competences via array_agg.
- Validation Pydantic des payloads (login, contact, creation projet).
- Suppression securisee avec verification du proprietaire.
- Contact: MongoDB si dispo, sinon stockage JSON local.

## UX / UI

- Navigation rapide via vue-router.
- Feedback utilisateur: messages success/erreur, validation des champs requis.
- Boutons conditionnels selon connexion (creation/suppression).
