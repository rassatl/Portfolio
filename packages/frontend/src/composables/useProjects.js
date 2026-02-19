import { ref } from 'vue'
import { useApiCache } from './useApiCache'

const API_URL = 'http://127.0.0.1:8000'

/**
 * Composable pour gérer les projets
 */
export function useProjects() {
  const { fetchWithCache } = useApiCache()
  
  const allProjects = ref([])
  const loading = ref(true)
  const error = ref(null)

  /**
   * Récupère tous les projets depuis l'API
   */
  async function fetchProjects() {
    loading.value = true
    error.value = null
    
    try {
      const data = await fetchWithCache(`${API_URL}/projects/search`)
      
      allProjects.value = data.projects.map(p => ({
        id: p.id,
        title: p.titre,
        description: p.description,
        date: p.date_projet || 'N/A',
        github: p.github_url || '#',
        lien: p.lien_url,
        skills: p.skills || []
      }))
      
      loading.value = false
      return allProjects.value
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
      return allProjects.value
    }
  }

  /**
   * Récupère les projets mis en avant (pour la page d'accueil)
   */
  async function fetchFeaturedProjects(limit = 3) {
    try {
      const data = await fetchWithCache(`${API_URL}/projects/featured?limit=${limit}`)
      
      return data.projects.map(p => ({
        id: p.id,
        title: p.titre,
        description: p.description,
        date: p.date_projet || 'N/A',
        github: p.github_url || '#',
        lien: p.lien_url,
        skills: p.skills || []
      }))
    } catch (err) {
      console.error('Erreur lors du chargement des projets mis en avant:', err)
      return []
    }
  }

  return {
    allProjects,
    loading,
    error,
    fetchProjects,
    fetchFeaturedProjects
  }
}
