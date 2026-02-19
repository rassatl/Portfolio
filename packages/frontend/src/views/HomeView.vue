<script setup>
import { ref, onMounted } from 'vue'
import { useApiCache } from '../composables/useApiCache'
import { useProjects } from '../composables/useProjects'
import { formatDateRange, getExperienceIcon } from '../composables/useFormatters'
import ProjectCard from '../components/ProjectCard.vue'
import SkillTag from '../components/SkillTag.vue'
import SkeletonLoader from '../components/SkeletonLoader.vue'
import SkillsSection from '../components/SkillsSection.vue'

const API_URL = 'http://127.0.0.1:8000'
const { fetchWithCache } = useApiCache()
const { fetchFeaturedProjects } = useProjects()

// Profil statique
const profile = ref({
  firstName: 'Jean',
  lastName: 'Dupont',
  about: 'Passionné par le développement web et les nouvelles technologies. Je cherche constamment à apprendre et à créer des solutions innovantes.',
  skills: []
})

const experiences = ref([])
const mainProjects = ref([])
const loading = ref(true)
const loadingProjects = ref(true)
const error = ref(null)

const contact = ref({
  email: 'lou.rassat2003@gmail.com',
  github: 'https://github.com/rassatl',
  linkedin: 'https://linkedin.com/in/lou-rassat'
})


const contactForm = ref({
  name: '',
  email: '',
  message: ''
})
const submitStatus = ref(null) // 'success', 'error', 'loading', 'invalid_input'
const errors = ref({
  name: false,
  email: false,
  message: false
})

const validateEmail = (email) => {
  return String(email)
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    )
}

const submitContact = async () => {
  // Reset errors
  errors.value = {
    name: !contactForm.value.name.trim(),
    email: !validateEmail(contactForm.value.email),
    message: !contactForm.value.message.trim()
  }

  if (errors.value.name || errors.value.email || errors.value.message) {
    submitStatus.value = 'invalid_input'
    return
  }

  submitStatus.value = 'loading'
  try {
    const response = await fetch(`${API_URL}/contact`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(contactForm.value)
    })
    
    if (!response.ok) throw new Error('Erreur réseau')
    
    submitStatus.value = 'success'
    contactForm.value = { name: '', email: '', message: '' }
    setTimeout(() => submitStatus.value = null, 3000)
  } catch (e) {
    console.error(e)
    submitStatus.value = 'error'
  }
}

// Récupération des données depuis l'API
onMounted(async () => {
  try {
    // Charger en priorité : expériences + compétences (contenu critique)
    const [expData, skillsData] = await Promise.all([
      fetchWithCache(`${API_URL}/experiences?sort=-date_debut`),
      fetchWithCache(`${API_URL}/skills/top?k=10`)
    ])
    
    // Mapper les expériences pour la timeline
    experiences.value = expData.experiences.map(exp => ({
      id: exp.id,
      title: exp.poste || exp.structure || 'Expérience',
      year: formatDateRange(exp.date_debut, exp.date_fin),
      icon: getExperienceIcon(exp.poste)
    }))

    // Mapper les compétences
    profile.value.skills = skillsData.skills.map(s => s.nom)
    
    loading.value = false

    // Charger les projets principaux en différé (non-bloquant)
    fetchFeaturedProjects(3)
      .then(projects => {
        mainProjects.value = projects
        loadingProjects.value = false
      })
      .catch(err => {
        console.error('Erreur chargement projets principaux:', err)
        mainProjects.value = []
        loadingProjects.value = false
      })
    
  } catch (err) {
    console.error('Erreur lors du chargement des données:', err)
    error.value = 'Erreur de chargement des données'
    
    // Fallback sur des données mock en cas d'erreur
    experiences.value = [
      { id: 1, title: 'Prépa', year: '2020-2022', icon: '📚' },
      { id: 2, title: 'ESIGELEC', year: '2022-2025', icon: '🎓' },
      { id: 3, title: 'Futur', year: '2025+', icon: '🚀' }
    ]
    profile.value.skills = ['Vue.js', 'Python', 'FastAPI', 'PostgreSQL', 'Tailwind CSS']
    mainProjects.value = [
      { id: 1, title: 'Portfolio', description: 'Application portfolio complète', date: '2024', github: '#', lien: null, skills: [] }
    ]
    loading.value = false
    loadingProjects.value = false
  }
})
</script>

<template>
  <div class="home-view">
    <!-- Message d'erreur si nécessaire -->
    <div v-if="error" class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4">
      <p>{{ error }} - Affichage des données par défaut</p>
    </div>

    <!-- Section 1: Présentation (Bleu Clair) -->
    <section class="bg-pastel-blue min-h-screen flex items-center justify-center px-6 py-16">
      <div class="container mx-auto max-w-5xl">
        <div class="flex flex-col md:flex-row items-center gap-12">
          <!-- Photo placeholder -->
          <div class="flex-shrink-0">
            <div v-if="loading" class="w-48 h-48 md:w-64 md:h-64 rounded-full bg-blue-200 animate-pulse shadow-lg"></div>
            <div v-else class="w-48 h-48 md:w-64 md:h-64 rounded-full bg-blue-300 flex items-center justify-center text-6xl shadow-lg">
              👤
            </div>
          </div>
          
          <!-- Infos -->
          <div class="flex-1 text-center md:text-left">
            <h1 v-if="loading" class="h-16 bg-gray-300 rounded-lg animate-pulse mb-4"></h1>
            <h1 v-else class="text-5xl md:text-6xl font-bold text-gray-800 mb-4">
              {{ profile.firstName }} {{ profile.lastName }}
            </h1>
            
            <div class="my-8">
              <h2 v-if="loading" class="h-8 w-48 bg-gray-300 rounded animate-pulse mb-3"></h2>
              <h2 v-else class="text-2xl font-semibold text-gray-700 mb-3">À propos de moi</h2>
              
              <div v-if="loading" class="space-y-2">
                <div class="h-6 bg-gray-300 rounded animate-pulse"></div>
                <div class="h-6 bg-gray-300 rounded animate-pulse w-5/6"></div>
                <div class="h-6 bg-gray-300 rounded animate-pulse w-4/6"></div>
              </div>
              <p v-else class="text-lg text-gray-600 leading-relaxed">
                {{ profile.about }}
              </p>
            </div>
            
            <div>
              <SkillsSection :skills="profile.skills" :loading="loading" />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 2: Timeline Expériences (Blanc) -->
    <section class="bg-white py-20 px-6">
      <div class="container mx-auto max-w-6xl">
        <h2 v-if="loading" class="h-12 w-64 bg-gray-300 rounded-lg animate-pulse mx-auto mb-16"></h2>
        <h2 v-else class="text-4xl font-bold text-center text-gray-800 mb-16">Mon Parcours</h2>
        
        <!-- Timeline avec skeleton -->
        <div v-if="loading" class="relative">
          <!-- Ligne centrale skeleton -->
          <div class="hidden md:block absolute left-1/2 transform -translate-x-1/2 w-1 h-full bg-gray-200"></div>
          
          <div class="space-y-12 md:space-y-24">
            <div v-for="n in 3" :key="n" class="relative">
              <div class="flex flex-col md:flex-row items-center justify-center gap-8">
                <div class="md:w-5/12 order-2 md:order-1">
                  <div class="bg-gray-100 rounded-xl p-6 shadow-md">
                    <div class="h-6 bg-gray-300 rounded animate-pulse mb-2"></div>
                    <div class="h-4 bg-gray-300 rounded animate-pulse w-32"></div>
                  </div>
                </div>
                <div class="order-1 md:order-2 relative z-10">
                  <div class="w-16 h-16 rounded-full bg-gray-300 animate-pulse shadow-xl"></div>
                </div>
                <div class="md:w-5/12 order-3"></div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Timeline réelle -->
        <div v-else class="relative">
          <!-- Ligne centrale (desktop only) -->
          <div class="hidden md:block absolute left-1/2 transform -translate-x-1/2 w-1 h-full bg-gradient-to-b from-blue-400 via-blue-500 to-blue-600"></div>
          
          <!-- Mobile: ligne verticale à gauche -->
          <div class="md:hidden absolute left-8 top-0 w-1 h-full bg-gradient-to-b from-blue-400 via-blue-500 to-blue-600"></div>
          
          <div class="space-y-12 md:space-y-24">
            <div
              v-for="(exp, index) in experiences"
              :key="exp.id"
              class="relative"
            >
              <!-- Desktop: alternance gauche/droite -->
              <div class="flex flex-col md:flex-row items-center md:items-stretch justify-center gap-8">
                <!-- Carte à gauche (desktop) ou toujours à droite (mobile) -->
                <div 
                  :class="[
                    'md:w-5/12',
                    index % 2 === 0 ? 'order-2 md:order-1 md:text-right' : 'order-2 md:order-3 md:text-left'
                  ]"
                >
                  <div 
                    class="bg-white rounded-xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border-2 border-blue-200 ml-12 md:ml-0"
                    :class="index % 2 === 0 ? '' : 'md:ml-0'"
                  >
                    <div class="flex items-center gap-3 mb-2" :class="index % 2 === 0 ? 'md:flex-row-reverse md:justify-start' : ''">
                      <span class="text-4xl">{{ exp.icon }}</span>
                      <h3 class="text-2xl font-bold text-gray-800">{{ exp.title }}</h3>
                    </div>
                    <p class="text-blue-600 font-semibold text-sm">{{ exp.year }}</p>
                  </div>
                </div>
                
                <!-- Point central -->
                <div class="order-1 md:order-2 absolute left-8 md:relative md:left-0 z-10 flex items-center">
                  <div class="w-16 h-16 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center shadow-xl border-4 border-white">
                    <div class="w-3 h-3 rounded-full bg-white"></div>
                  </div>
                </div>
                
                <!-- Espace vide de l'autre côté -->
                <div 
                  :class="[
                    'md:w-5/12',
                    index % 2 === 0 ? 'order-3' : 'order-1'
                  ]"
                  class="hidden md:block"
                ></div>
              </div>
            </div>
          </div>
          
          <!-- Point final de la timeline -->
          <div class="relative mt-12 flex items-center justify-center md:justify-center">
            <div class="absolute left-8 md:relative md:left-0">
              <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-xl border-4 border-white">
                <span class="text-xl">🚀</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Section 3: Projets Principaux (Jaune Clair) -->
    <section class="bg-pastel-yellow py-20 px-6">
      <div class="container mx-auto max-w-6xl">
        <h2 v-if="loadingProjects" class="h-12 w-80 bg-gray-300 rounded-lg animate-pulse mx-auto mb-12"></h2>
        <h2 v-else class="text-4xl font-bold text-center text-gray-800 mb-12">Projets Principaux</h2>
        
        <div v-if="loadingProjects" class="grid md:grid-cols-3 gap-8">
          <SkeletonLoader v-for="n in 3" :key="n" type="card" />
        </div>
        <div v-else class="grid md:grid-cols-3 gap-8">
          <ProjectCard
            v-for="project in mainProjects"
            :key="project.id"
            :project="project"
            class="border-yellow-300"
          />
        </div>
        
        <div class="text-center mt-12">
          <RouterLink
            to="/projets"
            class="inline-block px-8 py-3 bg-yellow-500 text-white font-semibold rounded-lg shadow-md hover:bg-yellow-600 transition-colors"
          >
            Voir tous les projets →
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Section 4: Contact (Rouge/Rose Clair) -->
    <section class="bg-pastel-red py-20 px-6">
      <div class="container mx-auto max-w-4xl text-center">
        <h2 class="text-4xl font-bold text-gray-800 mb-12">Contact</h2>
        
        <div class="flex flex-col md:flex-row items-center justify-center gap-6">
          <a
            :href="`mailto:${contact.email}`"
            class="flex items-center gap-3 px-8 py-4 bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 text-gray-800 font-semibold min-w-[250px]"
          >
            <span class="text-3xl">✉️</span>
            <span>Email</span>
          </a>
          
          <a
            :href="contact.github"
            target="_blank"
            rel="noopener noreferrer"
            class="flex items-center gap-3 px-8 py-4 bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 text-gray-800 font-semibold min-w-[250px]"
          >
            <span class="text-3xl">🐙</span>
            <span>GitHub</span>
          </a>
          
          <a
            :href="contact.linkedin"
            target="_blank"
            rel="noopener noreferrer"
            class="flex items-center gap-3 px-8 py-4 bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 text-gray-800 font-semibold min-w-[250px]"
          >
            <span class="text-3xl">💼</span>
            <span>LinkedIn</span>
          </a>
        </div>

        <!-- Formulaire de Contact -->
        <div class="mt-12 max-w-lg mx-auto bg-white rounded-xl shadow-lg p-8">
          <h3 class="text-2xl font-bold text-gray-800 mb-6 font-handwriting">Envoyez-moi un message</h3>
          
          <form @submit.prevent="submitContact" class="space-y-4" novalidate>
            <div>
              <label for="name" class="block text-left text-gray-700 font-medium mb-1">Nom</label>
              <input 
                v-model="contactForm.name"
                type="text" 
                id="name" 
                @input="errors.name = false"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-300 focus:border-red-300 outline-none transition-all"
                :class="{'border-red-500 focus:border-red-500 focus:ring-red-200': errors.name}"
                placeholder="Votre nom"
              >
              <div v-if="errors.name" class="text-red-500 text-sm mt-1 flex items-center gap-1 animate-pulse">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
                <span>Ce champ est requis</span>
              </div>
            </div>
            
            <div>
              <label for="email" class="block text-left text-gray-700 font-medium mb-1">Email</label>
              <input 
                v-model="contactForm.email"
                type="email" 
                id="email" 
                @input="errors.email = false"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-300 focus:border-red-300 outline-none transition-all"
                :class="{'border-red-500 focus:border-red-500 focus:ring-red-200': errors.email}"
                placeholder="votre@email.com"
              >
              <div v-if="errors.email" class="flex items-center gap-2 mt-2 text-red-500 text-sm font-medium animate-pulse">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
                <span>{{ contactForm.email ? 'Adresse email invalide' : 'Ce champ est requis' }}</span>
              </div>
            </div>
            
            <div>
              <label for="message" class="block text-left text-gray-700 font-medium mb-1">Message</label>
              <textarea 
                v-model="contactForm.message"
                id="message" 
                rows="4" 
                @input="errors.message = false"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-300 focus:border-red-300 outline-none transition-all resize-none"
                :class="{'border-red-500 focus:border-red-500 focus:ring-red-200': errors.message}"
                placeholder="Votre message..."
              ></textarea>
              <div v-if="errors.message" class="text-red-500 text-sm mt-1 flex items-center gap-1 animate-pulse">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
                <span>Ce champ est requis</span>
              </div>
            </div>
            
            <button 
              type="submit" 
              :disabled="submitStatus === 'loading'"
              class="w-full bg-red-400 hover:bg-red-500 text-white font-bold py-3 px-6 rounded-lg shadow-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="submitStatus === 'loading'">Envoi en cours...</span>
              <span v-else>Envoyer</span>
            </button>
            
            <p v-if="submitStatus === 'success'" class="text-green-600 font-medium mt-2">Message envoyé avec succès !</p>
            <p v-if="submitStatus === 'error'" class="text-red-600 font-medium mt-2">Une erreur est survenue.</p>
            <div v-if="submitStatus === 'invalid_email'" class="flex items-center gap-2 mt-2 text-red-500 text-sm font-medium animate-pulse">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
              <span>Adresse email invalide</span>
            </div>
          </form>
        </div>
      </div>
    </section>
    </div>
</template>

<style scoped>
</style>
