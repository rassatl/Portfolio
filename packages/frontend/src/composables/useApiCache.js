import { ref } from 'vue'

const cache = new Map()
const CACHE_DURATION = 5 * 60 * 1000 // 5 minutes

export function useApiCache() {
  async function fetchWithCache(url, options = {}) {
    const cacheKey = url
    const now = Date.now()

    // Vérifier si on a des données en cache valides
    if (cache.has(cacheKey)) {
      const { data, timestamp } = cache.get(cacheKey)
      if (now - timestamp < CACHE_DURATION) {
        return data
      }
    }

    // Sinon, fetch et mettre en cache
    const response = await fetch(url, options)
    const data = await response.json()
    
    cache.set(cacheKey, {
      data,
      timestamp: now
    })

    return data
  }

  function clearCache() {
    cache.clear()
  }

  return {
    fetchWithCache,
    clearCache
  }
}
