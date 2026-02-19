<script setup>
import { RouterLink, useRoute } from 'vue-router'
import { ref, onMounted, watch, computed } from 'vue'

const route = useRoute()
const usernameFromStorage = ref(null)

const username = computed(() => {
  return localStorage.getItem('username')
})

// Surveiller les changements de route
watch(() => route.path, () => {
  usernameFromStorage.value = localStorage.getItem('username')
})

onMounted(() => {
  // Récupérer le username du localStorage au chargement
  usernameFromStorage.value = localStorage.getItem('username')
})

const isActive = (name) => route.name === name

function logout() {
  // Supprimer les données de la session
  localStorage.removeItem('user_id')
  localStorage.removeItem('username')
  // Rediriger vers login
  window.location.href = '/login'
}
</script>

<template>
  <nav class="bg-white shadow-md sticky top-0 z-50">
    <div class="container mx-auto px-6 py-4">
      <div class="flex justify-between items-center">
        <div class="flex items-center gap-4">
          <div class="text-xl font-bold text-gray-800">
            Mon Portfolio
          </div>
          <div v-if="username" class="text-sm text-gray-600">
            Bonjour <span class="font-semibold text-blue-600">{{ username }}</span> 👋 
          </div>
        </div>
        <div class="flex gap-6 items-center">
          <RouterLink
            to="/"
            class="px-4 py-2 rounded-lg transition-colors duration-200"
            :class="isActive('home') 
              ? 'bg-blue-500 text-white' 
              : 'text-gray-700 hover:bg-gray-100'"
          >
            Accueil
          </RouterLink>
          <RouterLink
            to="/projets"
            class="px-4 py-2 rounded-lg transition-colors duration-200"
            :class="isActive('projets') 
              ? 'bg-blue-500 text-white' 
              : 'text-gray-700 hover:bg-gray-100'"
          >
            Projets
          </RouterLink>
          
          <!-- Bouton de déconnexion si connecté -->
          <button
            v-if="username"
            @click="logout"
            class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors duration-200 text-sm font-medium"
          >
            Déconnexion
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped>
</style>
