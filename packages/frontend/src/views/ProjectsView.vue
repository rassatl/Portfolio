<script setup>
import { ref, onMounted } from 'vue'

const API_URL = 'http://127.0.0.1:8000'

const allProjects = ref([])
const loading = ref(true)
const error = ref(null)

// Récupération des projets depuis l'API
onMounted(async () => {
  try {
    const response = await fetch(`${API_URL}/projects/search`)
    const data = await response.json()
    
    allProjects.value = data.projects.map(p => ({
      id: p.id,
      title: p.titre,
      description: p.description,
      date: p.date_projet || 'N/A',
      github: p.github_url || '#',
      lien: p.lien_url
    }))
    
    loading.value = false
  } catch (err) {
    console.error('Erreur lors du chargement des projets:', err)
    error.value = 'Erreur de chargement des projets'
    
    // Fallback sur données mock
    allProjects.value = [
      {
        id: 1,
        title: 'Portfolio Dynamique',
        description: 'Application portfolio complète',
        date: '2024',
        github: '#'
      }
    ]
    loading.value = false
  }
})
</script>

<template>
  <div class="projects-view bg-pastel-green min-h-screen py-16 px-6">
    <!-- Loader -->
    <div v-if="loading" class="min-h-screen flex items-center justify-center">
      <div class="text-center">
        <div class="animate-spin rounded-full h-16 w-16 border-b-4 border-green-600 mx-auto mb-4"></div>
        <p class="text-gray-700 text-lg">Chargement des projets...</p>
      </div>
    </div>

    <!-- Contenu -->
    <div v-else class="container mx-auto max-w-7xl">
      <!-- Message d'erreur si nécessaire -->
      <div v-if="error" class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4 rounded">
        <p>{{ error }} - Affichage des données par défaut</p>
      </div>

      <h1 class="text-5xl font-bold text-center text-gray-800 mb-4">
        Tous mes Projets
      </h1>
      <p class="text-center text-gray-600 mb-12 text-lg">
        Découvrez l'ensemble de mes réalisations techniques
      </p>
      
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div
          v-for="project in allProjects"
          :key="project.id"
          class="bg-white rounded-xl shadow-lg p-6 hover:shadow-2xl transition-all duration-300 hover:-translate-y-1 border-2 border-green-300"
        >
          <div class="flex justify-between items-start mb-3">
            <h2 class="text-2xl font-bold text-gray-800">{{ project.title }}</h2>
            <span class="text-sm text-gray-500 font-semibold">{{ project.date }}</span>
          </div>
          
          <p class="text-gray-600 mb-4 leading-relaxed">
            {{ project.description || 'Aucune description disponible' }}
          </p>
          
          <div class="flex gap-3">
            <a
              v-if="project.github && project.github !== '#'"
              :href="project.github"
              target="_blank"
              rel="noopener noreferrer"
              class="inline-flex items-center gap-2 text-green-600 hover:text-green-700 font-semibold transition-colors"
            >
              <span>🐙</span>
              <span>GitHub</span>
            </a>
            
            <a
              v-if="project.lien"
              :href="project.lien"
              target="_blank"
              rel="noopener noreferrer"
              class="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 font-semibold transition-colors"
            >
              <span>🔗</span>
              <span>Voir le projet</span>
            </a>
          </div>
        </div>
      </div>
      
      <div class="text-center mt-12">
        <RouterLink
          to="/"
          class="inline-block px-8 py-3 bg-green-600 text-white font-semibold rounded-lg shadow-md hover:bg-green-700 transition-colors"
        >
          ← Retour à l'accueil
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
