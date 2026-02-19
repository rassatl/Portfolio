import { ref, computed } from 'vue'

/**
 * Composable pour gérer les filtres de projets
 */
export function useFilters(projects) {
  const searchQuery = ref('')
  const selectedSkills = ref([])
  const selectedYears = ref([])
  const sortOrder = ref('desc') // 'desc' = plus récent d'abord, 'asc' = plus ancien d'abord
  const filtersExpanded = ref(false)

  /**
   * Extrait les années uniques des projets
   */
  const availableYears = computed(() => {
    const years = new Set()
    projects.value.forEach(p => {
      if (p.date && p.date !== 'N/A') {
        const year = p.date.toString().substring(0, 4)
        if (year && !isNaN(year)) {
          years.add(year)
        }
      }
    })
    return Array.from(years).sort((a, b) => b - a) // Plus récent en premier
  })

  /**
   * Filtre et trie les projets selon les critères sélectionnés
   */
  const filteredProjects = computed(() => {
    let result = projects.value

    // Filtre par recherche texte
    if (searchQuery.value.trim()) {
      const query = searchQuery.value.toLowerCase()
      result = result.filter(p => 
        p.title.toLowerCase().includes(query) || 
        (p.description && p.description.toLowerCase().includes(query))
      )
    }

    // Filtre par compétences sélectionnées
    if (selectedSkills.value.length > 0) {
      result = result.filter(p => 
        p.skills && selectedSkills.value.some(skill => p.skills.includes(skill))
      )
    }

    // Filtre par années sélectionnées
    if (selectedYears.value.length > 0) {
      result = result.filter(p => {
        if (!p.date || p.date === 'N/A') return false
        const projectYear = p.date.toString().substring(0, 4)
        return selectedYears.value.includes(projectYear)
      })
    }

    // Tri par date
    result = [...result].sort((a, b) => {
      const dateA = a.date === 'N/A' ? '' : a.date
      const dateB = b.date === 'N/A' ? '' : b.date
      
      if (sortOrder.value === 'desc') {
        return dateB.localeCompare(dateA)
      } else {
        return dateA.localeCompare(dateB)
      }
    })

    return result
  })

  /**
   * Compte le nombre de filtres actifs
   */
  const activeFiltersCount = computed(() => {
    return selectedSkills.value.length + 
           selectedYears.value.length + 
           (searchQuery.value ? 1 : 0)
  })

  /**
   * Vérifie si des filtres sont actifs
   */
  const hasActiveFilters = computed(() => {
    return selectedSkills.value.length > 0 || 
           selectedYears.value.length > 0 || 
           searchQuery.value.trim() !== '' ||
           sortOrder.value === 'asc'
  })

  /**
   * Toggle une compétence dans les filtres
   */
  function toggleSkill(skill) {
    const index = selectedSkills.value.indexOf(skill)
    if (index === -1) {
      selectedSkills.value.push(skill)
    } else {
      selectedSkills.value.splice(index, 1)
    }
  }

  /**
   * Toggle une année dans les filtres
   */
  function toggleYear(year) {
    const index = selectedYears.value.indexOf(year)
    if (index === -1) {
      selectedYears.value.push(year)
    } else {
      selectedYears.value.splice(index, 1)
    }
  }

  /**
   * Réinitialise tous les filtres
   */
  function resetFilters() {
    searchQuery.value = ''
    selectedSkills.value = []
    selectedYears.value = []
    sortOrder.value = 'desc'
  }

  return {
    // État
    searchQuery,
    selectedSkills,
    selectedYears,
    sortOrder,
    filtersExpanded,
    
    // Computed
    availableYears,
    filteredProjects,
    activeFiltersCount,
    hasActiveFilters,
    
    // Méthodes
    toggleSkill,
    toggleYear,
    resetFilters
  }
}
