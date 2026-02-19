<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 py-12 px-4">
    <div class="max-w-3xl mx-auto">
      <!-- Header -->
      <div class="mb-8 text-center">
        <h1 class="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
          Création de projet
        </h1>
        <p class="text-gray-600 text-lg">Ajoutez un nouveau projet au portfolio</p>
      </div>

      <!-- Form Card -->
      <div class="bg-white rounded-2xl shadow-xl p-10">
        <!-- Titre -->
        <div class="mb-7">
          <label for="titre" class="block text-sm font-bold text-gray-800 mb-3">
            Titre du projet <span class="text-red-500">*</span>
          </label>
          <input
            id="titre"
            v-model="form.titre"
            type="text"
            placeholder="Ex: E-commerce Platform"
            class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200 transition"
          />
          <span v-if="errors.titre" class="text-red-500 text-sm mt-2 block">{{ errors.titre }}</span>
        </div>

        <!-- Description -->
        <div class="mb-7">
          <label for="description" class="block text-sm font-bold text-gray-800 mb-3">
            Description <span class="text-red-500">*</span>
          </label>
          <textarea
            id="description"
            v-model="form.description"
            placeholder="Décrivez votre projet en détail..."
            rows="6"
            class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200 transition resize-none"
          ></textarea>
          <span v-if="errors.description" class="text-red-500 text-sm mt-2 block">{{ errors.description }}</span>
        </div>

        <!-- Liens en deux colonnes -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-7 mb-7">
          <!-- Lien GitHub -->
          <div>
            <label for="github_url" class="block text-sm font-bold text-gray-800 mb-3">
              🐙 Lien GitHub
            </label>
            <input
              id="github_url"
              v-model="form.github_url"
              type="url"
              placeholder="https://github.com/..."
              class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200 transition"
            />
          </div>

          <!-- Lien Deployed -->
          <div>
            <label for="lien_url" class="block text-sm font-bold text-gray-800 mb-3">
              🌐 Lien du site deployed
            </label>
            <input
              id="lien_url"
              v-model="form.lien_url"
              type="url"
              placeholder="https://..."
              class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200 transition"
            />
          </div>
        </div>

        <!-- Date du projet -->
        <div class="mb-7">
          <label for="date_projet" class="block text-sm font-bold text-gray-800 mb-3">
            📅 Date du projet
          </label>
          <input
            id="date_projet"
            v-model="form.date_projet"
            type="date"
            class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200 transition"
          />
        </div>

        <!-- Compétences -->
        <div class="mb-8">
          <label class="block text-sm font-bold text-gray-800 mb-3">
            🛠️ Compétences utilisées
          </label>
          <div class="flex gap-2 mb-4">
            <input
              v-model="newSkill"
              type="text"
              placeholder="Ex: Vue.js, Python, PostgreSQL..."
              @keyup.enter="addSkill"
              class="flex-1 px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200 transition"
            />
            <button
              type="button"
              @click="addSkill"
              class="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition font-semibold"
            >
              Ajouter
            </button>
          </div>

          <!-- Tags des compétences -->
          <div v-if="form.skills.length > 0" class="flex flex-wrap gap-3">
            <div
              v-for="(skill, index) in form.skills"
              :key="index"
              class="px-4 py-2 bg-gradient-to-r from-blue-100 to-purple-100 text-gray-700 rounded-full text-sm font-semibold flex items-center gap-2 border border-blue-200"
            >
              ✓ {{ skill }}
              <button
                type="button"
                @click="removeSkill(index)"
                class="text-gray-500 hover:text-red-600 transition ml-1"
              >
                ✕
              </button>
            </div>
          </div>
        </div>

        <!-- Messages -->
        <div v-if="successMessage" class="mb-6 p-4 bg-green-100 text-green-700 rounded-lg border border-green-300 font-semibold">
          ✓ {{ successMessage }}
        </div>
        <div v-if="errorMessage" class="mb-6 p-4 bg-red-100 text-red-700 rounded-lg border border-red-300 font-semibold">
          ✗ {{ errorMessage }}
        </div>

        <!-- Buttons -->
        <div class="flex gap-3 pt-4">
          <button
            @click="submitForm"
            :disabled="loading"
            class="flex-1 px-6 py-4 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 transition font-bold text-lg disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
          >
            <span v-if="!loading">Créer le projet</span>
            <span v-else>⏳ En cours...</span>
          </button>
          <RouterLink
            to="/projets"
            class="flex-1 px-6 py-4 bg-gray-100 text-gray-800 rounded-lg hover:bg-gray-200 transition font-bold text-lg text-center"
          >
            Annuler
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { RouterLink } from 'vue-router'

const router = useRouter()

const form = ref({
  titre: '',
  description: '',
  github_url: '',
  lien_url: '',
  date_projet: '',
  experience_id: null,
  skills: []
})

const newSkill = ref('')
const loading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const errors = ref({})

const addSkill = () => {
  const skill = newSkill.value.trim()
  if (skill && !form.value.skills.includes(skill)) {
    form.value.skills.push(skill)
    newSkill.value = ''
  }
}

const removeSkill = (index) => {
  form.value.skills.splice(index, 1)
}

const validateForm = () => {
  errors.value = {}

  if (!form.value.titre.trim()) {
    errors.value.titre = 'Le titre est requis'
  }

  if (!form.value.description.trim()) {
    errors.value.description = 'La description est requise'
  }

  return Object.keys(errors.value).length === 0
}

const submitForm = async () => {
  if (!validateForm()) {
    return
  }

  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const formData = {
      ...form.value,
      user_id: parseInt(localStorage.getItem('user_id'))
    }
    
    const response = await fetch('http://127.0.0.1:8000/projects', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || 'Erreur lors de la création du projet')
    }

    successMessage.value = 'Projet créé avec succès !'

    // Rediriger vers la page projets après 1.5 secondes
    setTimeout(() => {
      router.push('/projets')
    }, 1500)
  } catch (error) {
    errorMessage.value = error.message || 'Une erreur est survenue'
    console.error('Erreur:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
input:focus,
textarea:focus {
  box-shadow: 0 0 0 3px rgba(135, 206, 235, 0.1);
}
</style>
