<script setup>
import { ref, onMounted, computed } from 'vue'
import { useApiCache } from '../composables/useApiCache'

const API_URL = 'http://127.0.0.1:8000'
const { fetchWithCache } = useApiCache()

const allProjects = ref([])
const allSkills = ref([])
const loading = ref(true)
const error = ref(null)

// Filtres
const searchQuery = ref('')
const selectedSkills = ref([])
const selectedYears = ref([])
const sortOrder = ref('desc') // 'desc' = plus récent d'abord, 'asc' = plus ancien d'abord
const filtersExpanded = ref(false) // État du volet déroulant

// Extraire les années uniques des projets
const availableYears = computed(() => {
  const years = new Set()
  allProjects.value.forEach(p => {
    if (p.date && p.date !== 'N/A') {
      const year = p.date.toString().substring(0, 4)
      if (year && !isNaN(year)) {
        years.add(year)
      }
    }
  })
  return Array.from(years).sort((a, b) => b - a) // Plus récent en premier
})

// Projets filtrés
const filteredProjects = computed(() => {
  let projects = allProjects.value

  // Filtre par recherche texte
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    projects = projects.filter(p => 
      p.title.toLowerCase().includes(query) || 
      (p.description && p.description.toLowerCase().includes(query))
    )
  }

  // Filtre par compétences sélectionnées
  if (selectedSkills.value.length > 0) {
    projects = projects.filter(p => 
      p.skills && selectedSkills.value.some(skill => p.skills.includes(skill))
    )
  }

  // Filtre par années sélectionnées
  if (selectedYears.value.length > 0) {
    projects = projects.filter(p => {
      if (!p.date || p.date === 'N/A') return false
      const projectYear = p.date.toString().substring(0, 4)
      return selectedYears.value.includes(projectYear)
    })
  }

  // Tri par date
  projects = [...projects].sort((a, b) => {
    const dateA = a.date === 'N/A' ? '' : a.date
    const dateB = b.date === 'N/A' ? '' : b.date
    
    if (sortOrder.value === 'desc') {
      return dateB.localeCompare(dateA)
    } else {
      return dateA.localeCompare(dateB)
    }
  })

  return projects
})

// Toggle skill filter
function toggleSkill(skill) {
  const index = selectedSkills.value.indexOf(skill)
  if (index === -1) {
    selectedSkills.value.push(skill)
  } else {
    selectedSkills.value.splice(index, 1)
  }
}

// Toggle year filter
function toggleYear(year) {
  const index = selectedYears.value.indexOf(year)
  if (index === -1) {
    selectedYears.value.push(year)
  } else {
    selectedYears.value.splice(index, 1)
  }
}

// Reset filters
function resetFilters() {
  searchQuery.value = ''
  selectedSkills.value = []
  selectedYears.value = []
  sortOrder.value = 'desc'
}

// Formater la date pour l'affichage compact
function formatDate(dateStr) {
  if (!dateStr || dateStr === 'N/A') return 'N/A'
  
  try {
    const date = new Date(dateStr)
    if (isNaN(date.getTime())) return dateStr
    
    const months = ['Jan.', 'Fév.', 'Mars', 'Avr.', 'Mai', 'Juin', 'Juil.', 'Août', 'Sept.', 'Oct.', 'Nov.', 'Déc.']
    const month = months[date.getMonth()]
    const year = date.getFullYear()
    
    return `${month} ${year}`
  } catch {
    return dateStr
  }
}

// Récupération des projets depuis l'API
onMounted(async () => {
  try {
    const [projectsData, skillsData] = await Promise.all([
      fetchWithCache(`${API_URL}/projects/search`),
      fetchWithCache(`${API_URL}/skills/top?k=20`)
    ])
    
    allProjects.value = projectsData.projects.map(p => ({
      id: p.id,
      title: p.titre,
      description: p.description,
      date: p.date_projet || 'N/A',
      github: p.github_url || '#',
      lien: p.lien_url,
      skills: p.skills || []
    }))

    allSkills.value = skillsData.skills.map(s => s.nom)
    
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
        github: '#',
        skills: []
      }
    ]
    loading.value = false
  }
})
</script>

<template>
  <div class="projects-view bg-pastel-green min-h-screen py-16 px-6">
    <div class="container mx-auto max-w-7xl">
      <!-- Message d'erreur si nécessaire -->
      <div v-if="error" class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4 rounded">
        <p>{{ error }} - Affichage des données par défaut</p>
      </div>

      <h1 v-if="loading" class="h-14 w-96 bg-gray-300 rounded-lg animate-pulse mx-auto mb-4"></h1>
      <h1 v-else class="text-5xl font-bold text-center text-gray-800 mb-4">
        Tous mes Projets
      </h1>
      
      <p v-if="loading" class="h-6 w-80 bg-gray-300 rounded animate-pulse mx-auto mb-12"></p>
      <p v-else class="text-center text-gray-600 mb-8 text-lg">
        Découvrez l'ensemble de mes réalisations techniques
      </p>
      
      <!-- Section Filtres -->
      <div v-if="!loading" class="bg-white rounded-xl shadow-md mb-8 border-2 border-green-300 overflow-hidden">
        <!-- Header cliquable -->
        <button
          @click="filtersExpanded = !filtersExpanded"
          class="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
        >
          <div class="flex items-center gap-3">
            <span class="text-2xl">🎯</span>
            <h3 class="text-xl font-bold text-gray-800">Filtres et recherche</h3>
            <span v-if="selectedSkills.length > 0 || selectedYears.length > 0 || searchQuery" class="px-2 py-1 bg-green-600 text-white text-xs rounded-full font-semibold">
              {{ (selectedSkills.length + selectedYears.length + (searchQuery ? 1 : 0)) }}
            </span>
          </div>
          <svg
            :class="['w-6 h-6 text-gray-600 transform transition-transform duration-300', filtersExpanded ? 'rotate-180' : '']"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>

        <!-- Contenu des filtres avec transition -->
        <transition
          enter-active-class="transition-all duration-300 ease-out"
          leave-active-class="transition-all duration-300 ease-in"
          enter-from-class="opacity-0 max-h-0"
          enter-to-class="opacity-100 max-h-screen"
          leave-from-class="opacity-100 max-h-screen"
          leave-to-class="opacity-0 max-h-0"
        >
          <div v-show="filtersExpanded" class="px-6 pb-6">
            <!-- Barre de recherche -->
            <div class="mb-6 pt-2">
          <label class="block text-sm font-semibold text-gray-700 mb-2">
            🔍 Rechercher un projet
          </label>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Titre ou description..."
            class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none transition-colors"
          />
        </div>

        <!-- Filtres par compétences -->
        <div class="mb-6">
          <label class="block text-sm font-semibold text-gray-700 mb-3">
            🏷️ Filtrer par compétences
          </label>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="skill in allSkills"
              :key="skill"
              @click="toggleSkill(skill)"
              :class="[
                'px-4 py-2 rounded-full text-sm font-medium transition-all duration-200',
                selectedSkills.includes(skill)
                  ? 'bg-green-600 text-white shadow-md scale-105'
                  : 'bg-gray-100 text-gray-700 hover:bg-green-100 hover:text-green-700'
              ]"
            >
              {{ skill }}
              <span v-if="selectedSkills.includes(skill)" class="ml-1">✓</span>
            </button>
          </div>
        </div>

        <!-- Filtres par année -->
        <div class="mb-6" v-if="availableYears.length > 0">
          <label class="block text-sm font-semibold text-gray-700 mb-3">
            📅 Filtrer par année
          </label>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="year in availableYears"
              :key="year"
              @click="toggleYear(year)"
              :class="[
                'px-4 py-2 rounded-full text-sm font-medium transition-all duration-200',
                selectedYears.includes(year)
                  ? 'bg-blue-600 text-white shadow-md scale-105'
                  : 'bg-gray-100 text-gray-700 hover:bg-blue-100 hover:text-blue-700'
              ]"
            >
              {{ year }}
              <span v-if="selectedYears.includes(year)" class="ml-1">✓</span>
            </button>
          </div>
        </div>

        <!-- Tri par date -->
        <div class="mb-6">
          <label class="block text-sm font-semibold text-gray-700 mb-3">
            ⏰ Trier par date
          </label>
          <div class="flex gap-2">
            <button
              @click="sortOrder = 'desc'"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 flex items-center gap-2',
                sortOrder === 'desc'
                  ? 'bg-green-600 text-white shadow-md'
                  : 'bg-gray-100 text-gray-700 hover:bg-green-100 hover:text-green-700'
              ]"
            >
              <span>📉</span>
              <span>Plus récent d'abord</span>
            </button>
            <button
              @click="sortOrder = 'asc'"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 flex items-center gap-2',
                sortOrder === 'asc'
                  ? 'bg-green-600 text-white shadow-md'
                  : 'bg-gray-100 text-gray-700 hover:bg-green-100 hover:text-green-700'
              ]"
            >
              <span>📈</span>
              <span>Plus ancien d'abord</span>
            </button>
          </div>
        </div>

        <!-- Bouton de réinitialisation et compteur -->
        <div class="flex items-center justify-between pt-4 border-t-2 border-gray-200">
          <div class="text-sm text-gray-600">
            <span class="font-semibold text-lg">{{ filteredProjects.length }}</span>
            projet{{ filteredProjects.length > 1 ? 's' : '' }} trouvé{{ filteredProjects.length > 1 ? 's' : '' }}
            <span v-if="selectedSkills.length > 0 || selectedYears.length > 0 || searchQuery" class="text-green-700">
              ({{ allProjects.length }} au total)
            </span>
          </div>
          <button
            v-if="selectedSkills.length > 0 || selectedYears.length > 0 || searchQuery || sortOrder === 'asc'"
            @click="resetFilters"
            class="px-4 py-2 bg-red-500 text-white rounded-lg text-sm font-medium hover:bg-red-600 transition-colors shadow-md"
          >
            🔄 Réinitialiser tous les filtres
          </button>
        </div>
          </div>
        </transition>
      </div>
      
      <!-- Message si aucun résultat -->
      <div v-if="!loading && filteredProjects.length === 0" class="text-center py-12">
        <div class="text-6xl mb-4">🔍</div>
        <h3 class="text-2xl font-bold text-gray-700 mb-2">Aucun projet trouvé</h3>
        <p class="text-gray-600 mb-4">Essayez de modifier vos filtres ou votre recherche</p>
        <button
          @click="resetFilters"
          class="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
        >
          Réinitialiser les filtres
        </button>
      </div>
      
      <div v-if="loading" class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="n in 6" :key="n" class="bg-white rounded-xl shadow-lg p-6 border-2 border-green-300">
          <div class="flex justify-between items-start mb-3">
            <div class="h-8 w-2/3 bg-gray-300 rounded animate-pulse"></div>
            <div class="h-6 w-16 bg-gray-300 rounded animate-pulse"></div>
          </div>
          <div class="space-y-2 mb-4">
            <div class="h-4 bg-gray-300 rounded animate-pulse"></div>
            <div class="h-4 bg-gray-300 rounded animate-pulse"></div>
            <div class="h-4 bg-gray-300 rounded animate-pulse w-5/6"></div>
          </div>
          <div class="h-6 w-24 bg-gray-300 rounded animate-pulse"></div>
        </div>
      </div>
      <div v-else-if="filteredProjects.length > 0" class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div
          v-for="project in filteredProjects"
          :key="project.id"
          class="bg-white rounded-xl shadow-lg p-6 hover:shadow-2xl transition-all duration-300 hover:-translate-y-1 border-2 border-green-300"
        >
          <div class="flex justify-between items-start mb-3">
            <h2 class="text-2xl font-bold text-gray-800">{{ project.title }}</h2>
            <span class="text-sm text-gray-500 font-semibold whitespace-nowrap ml-2">{{ formatDate(project.date) }}</span>
          </div>
          
          <p class="text-gray-600 mb-4 leading-relaxed">
            {{ project.description || 'Aucune description disponible' }}
          </p>
          
          <!-- Tags de compétences -->
          <div v-if="project.skills && project.skills.length > 0" class="mb-4">
            <div class="flex flex-wrap gap-2">
              <span
                v-for="skill in project.skills"
                :key="skill"
                class="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium"
              >
                {{ skill }}
              </span>
            </div>
          </div>
          
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
