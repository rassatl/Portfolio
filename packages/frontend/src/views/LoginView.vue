<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const API_URL = 'http://127.0.0.1:8000'

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref(null)
const showPassword = ref(false)

async function handleLogin() {
  error.value = null
  
  // Validation
  if (!username.value || !password.value) {
    error.value = 'Veuillez remplir tous les champs'
    return
  }

  loading.value = true

  try {
    const response = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value
      })
    })

    const data = await response.json()

    if (!response.ok) {
      error.value = data.detail || 'Identifiants invalides'
      loading.value = false
      return
    }

    // Connexion réussie
    if (data.success) {
      // Stocker l'ID utilisateur en localStorage
      localStorage.setItem('user_id', data.user_id)
      localStorage.setItem('username', username.value)
      
      // Rediriger vers la page d'accueil
      router.push('/')
    }
  } catch (err) {
    console.error('Erreur lors de la connexion:', err)
    error.value = 'Erreur de connexion au serveur'
  } finally {
    loading.value = false
  }
}

function handleKeypress(event) {
  if (event.key === 'Enter') {
    handleLogin()
  }
}
</script>

<template>
  <div class="login-page bg-gradient-to-br from-blue-500 to-purple-600 min-h-screen flex items-center justify-center px-6 py-12">
    <div class="w-full max-w-md">
      <!-- Card de connexion -->
      <div class="bg-white rounded-2xl shadow-2xl p-8">
        <!-- En-tête -->
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold text-gray-800 mb-2">Connexion</h1>
          <p class="text-gray-600">Accédez à votre portfolio</p>
        </div>

        <!-- Message d'erreur -->
        <div v-if="error" class="mb-6 p-4 bg-red-100 border-l-4 border-red-500 text-red-700 rounded-lg">
          <p class="font-medium">{{ error }}</p>
        </div>

        <!-- Formulaire -->
        <form @submit.prevent="handleLogin" class="space-y-5">
          <!-- Champ Username -->
          <div>
            <label for="username" class="block text-sm font-semibold text-gray-700 mb-2">
              Identifiant
            </label>
            <input
              id="username"
              v-model="username"
              type="text"
              placeholder="Entrez votre identifiant"
              @keypress="handleKeypress"
              class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none transition-colors"
              :disabled="loading"
            />
          </div>

          <!-- Champ Password -->
          <div>
            <label for="password" class="block text-sm font-semibold text-gray-700 mb-2">
              Mot de passe
            </label>
            <div class="relative">
              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Entrez votre mot de passe"
                @keypress="handleKeypress"
                class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none transition-colors"
                :disabled="loading"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-600 hover:text-gray-800"
                :disabled="loading"
              >
                <span v-if="showPassword">👁️</span>
                <span v-else>👁️‍🗨️</span>
              </button>
            </div>
          </div>

          <!-- Bouton de connexion -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-lg hover:shadow-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <span v-if="loading" class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            <span>{{ loading ? 'Connexion...' : 'Se connecter' }}</span>
          </button>
        </form>

        <!-- Lien retour -->
        <div class="mt-6 text-center">
          <RouterLink
            to="/"
            class="text-blue-600 hover:text-blue-700 font-medium underline transition-colors"
          >
            ← Retour à l'accueil
          </RouterLink>
        </div>
      </div>

      <!-- Info démo -->
      <div class="mt-8 text-center text-white text-sm">
        <p class="opacity-80">Compte de test: <span class="font-bold">admin</span> / <span class="font-bold">test123</span></p>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>