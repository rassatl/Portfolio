# Portfolio Frontend

Application Vue.js 3 pour portfolio personnel.

## Installation

```bash
cd packages/frontend
npm install
```

## Lancement en développement

```bash
npm run dev
```

L'application sera accessible sur `http://localhost:5173`

## Build pour production

```bash
npm run build
```

## Stack technique

- **Vue.js 3** (Composition API)
- **Vue Router** (navigation)
- **Tailwind CSS** (styling)
- **Vite** (build tool)

## Structure

- `/src/views/HomeView.vue` - Page d'accueil avec 4 sections
- `/src/views/ProjectsView.vue` - Page liste complète des projets
- `/src/components/Navigation.vue` - Header de navigation
- `/src/router/index.js` - Configuration des routes
