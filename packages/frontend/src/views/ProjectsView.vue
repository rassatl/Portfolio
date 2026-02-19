<script setup>
import { ref, computed, onMounted, onActivated } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useApiCache } from '../composables/useApiCache'
import { useProjects } from '../composables/useProjects'
import { useFilters } from '../composables/useFilters'
import ProjectCard from '../components/ProjectCard.vue'
import FilterPanel from '../components/FilterPanel.vue'
import SkeletonLoader from '../components/SkeletonLoader.vue'

const route = useRoute()
const API_URL = 'http://127.0.0.1:8000'
const { fetchWithCache } = useApiCache()

// Utilisation du composable useProjects
const { allProjects, loading, error, fetchProjects } = useProjects()

// Utilisation du composable useFilters
const {
  searchQuery,
  selectedSkills,
  selectedYears,
  selectedType,
  selectedExperienceId,
  sortOrder,
  filtersExpanded,
  availableYears,
  filteredProjects,
  activeFiltersCount,
  hasActiveFilters,
  toggleSkill,
  toggleYear,
  resetFilters
} = useFilters(allProjects)

const allSkills = ref([])
const experienceLabel = ref('')

// Applique les filtres depuis les query params
function applyQueryFilters() {
  const skill = route.query.skill
  const expId = route.query.experience_id

  if (skill && !selectedSkills.value.includes(skill)) {
    resetFilters()
    selectedSkills.value.push(skill)
    filtersExpanded.value = true
  } else if (expId) {
    const id = parseInt(expId)
    if (!isNaN(id) && selectedExperienceId.value !== id) {
      resetFilters()
      selectedExperienceId.value = id
      filtersExpanded.value = true
      // Charger le nom de l'expérience
      fetchWithCache(`${API_URL}/experiences/${id}/full`)
        .then(data => {
          experienceLabel.value = data.experience
            ? `${data.experience.poste || ''} — ${data.experience.structure || ''}`.replace(/ — $/, '')
            : `Expérience #${id}`
        })
        .catch(() => {
          experienceLabel.value = `Expérience #${id}`
        })
    }
  }
}

const username = ref(localStorage.getItem('username'))

const handleProjectDeleted = (projectId) => {
  // Supprimer le projet de la liste allProjects
  const index = allProjects.value.findIndex(p => p.id === projectId)
  if (index !== -1) {
    allProjects.value.splice(index, 1)
  }
}

// Récupération des projets et compétences depuis l'API
onMounted(async () => {
  try {
    const skillsData = await fetchWithCache(`${API_URL}/skills/top?k=20`)
    allSkills.value = skillsData.skills.map(s => s.nom)
    
    await fetchProjects()
    applyQueryFilters()
  } catch (err) {
    console.error('Erreur lors du chargement:', err)
  }
})

// Ré-appliquer le filtre quand on revient sur la page (keep-alive)
onActivated(() => {
  applyQueryFilters()
})

</script>

<template>
  <div class="projects-view bg-pastel-green min-h-screen py-16 px-6">
    <div class="container mx-auto max-w-7xl">
      <!-- Message d'erreur si nécessaire -->
      <div v-if="error" class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4 rounded">
        <p>{{ error }} - Affichage des données par défaut</p>
      </div>

      <!-- Titre -->
      <SkeletonLoader v-if="loading" type="title" class="mb-4" />
      <h1 v-else class="text-5xl font-bold text-center text-gray-800 mb-4">
        Tous mes Projets
      </h1>
      
      <!-- Sous-titre -->
      <SkeletonLoader v-if="loading" type="text" class="mb-12" />
      <p v-else class="text-center text-gray-600 mb-8 text-lg">
        Découvrez l'ensemble de mes réalisations techniques
      </p>
      
      <!-- Bouton créer nouveau projet si connecté -->
      <div v-if="username" class="flex justify-center mb-8">
        <RouterLink
          to="/projets/nouveau"
          class="px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors duration-200 font-medium"
        >
          ➕ Nouveau projet
        </RouterLink>
      </div>
      
      <!-- Panel de filtres -->
      <FilterPanel
        v-if="!loading"
        :search-query="searchQuery"
        :selected-skills="selectedSkills"
        :selected-years="selectedYears"
        :selected-type="selectedType"
        :sort-order="sortOrder"
        :filters-expanded="filtersExpanded"
        :all-skills="allSkills"
        :available-years="availableYears"
        :filtered-count="filteredProjects.length"
        :total-count="allProjects.length"
        :active-filters-count="activeFiltersCount"
        :has-active-filters="hasActiveFilters"
        :experience-label="experienceLabel"
        @update:search-query="searchQuery = $event"
        @update:sort-order="sortOrder = $event"
        @update:selected-type="selectedType = $event"
        @update:filters-expanded="filtersExpanded = $event"
        @toggle-skill="toggleSkill"
        @toggle-year="toggleYear"
        @reset-filters="resetFilters(); experienceLabel = ''"
      />
      
      <!-- Message si aucun résultat -->
      <div v-if="!loading && filteredProjects.length === 0" class="text-center py-12">
        <div class="text-6xl mb-4">🔍</div>
        <h3 class="text-2xl font-bold text-gray-700 mb-2">Aucun projet trouvé</h3>
        <p class="text-gray-600 mb-4">Essayez de modifier vos filtres ou votre recherche</p>
        <button
          @click="resetFilters(); experienceLabel = ''"
          class="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
        >
          Réinitialiser les filtres
        </button>
      </div>
      
      <!-- Grille de squelettes de chargement -->
      <div v-if="loading" class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <SkeletonLoader v-for="n in 6" :key="n" type="card" />
      </div>
      
      <!-- Grille de projets -->
      <div v-else-if="filteredProjects.length > 0" class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <ProjectCard
          v-for="project in filteredProjects"
          :key="project.id"
          :project="project"
          @project-deleted="handleProjectDeleted"
        />
      </div>
      
      <!-- Lien retour -->
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
